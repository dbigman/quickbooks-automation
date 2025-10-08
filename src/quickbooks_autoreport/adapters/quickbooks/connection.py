"""QuickBooks connection management for QuickBooks Auto Reporter."""

import pythoncom  # type: ignore
from win32com.client import gencache  # type: ignore

from ...config import APP_NAME, COMPANY_FILE
from ...utils.logging_utils import log_error, log_info


def open_connection(rp):
    """Open connection to QuickBooks with multiple fallback strategies.
    
    Args:
        rp: RequestProcessor COM object
    """
    for local_enum in (1, 0, 2):
        try:
            rp.OpenConnection2("", APP_NAME, local_enum)
            return
        except Exception:
            pass
    rp.OpenConnection("", APP_NAME)


def host_info(rp, ticket):
    """Get QuickBooks host information.
    
    Args:
        rp: RequestProcessor COM object
        ticket: Session ticket
        
    Returns:
        Tuple of (company_filename, file_mode, is_automatic_login)
    """
    import xml.etree.ElementTree as ET
    
    host_req = """<?xml version="1.0"?>
<?qbxml version="16.0"?>
<QBXML><QBXMLMsgsRq onError="stopOnError"><HostQueryRq/></QBXMLMsgsRq></QBXML>"""
    resp = rp.ProcessRequest(ticket, host_req)
    root = ET.fromstring(resp)
    h = root.find(".//HostRet")
    fn = (h.findtext("CompanyFileName") or "") if h is not None else ""
    mode = (h.findtext("QBFileMode") or "") if h is not None else ""
    ai = (h.findtext("IsAutomaticLogin") or "") if h is not None else ""
    return fn, mode, ai


def try_begin_session(rp):
    """Begin QuickBooks session with multiple path/mode combinations.
    
    Args:
        rp: RequestProcessor COM object
        
    Returns:
        Tuple of (ticket, session_info)
        
    Raises:
        RuntimeError: If all session attempts fail
    """
    attempts = [("", 0), ("", 2), ("", 1), (COMPANY_FILE, 2), (COMPANY_FILE, 1)]
    last = None
    
    for path, mode in attempts:
        try:
            t = rp.BeginSession(path, mode)
            fn, fm, ai = host_info(rp, t)
            return t, {
                "CompanyFileName": fn,
                "QBFileMode": fm,
                "IsAutomaticLogin": ai,
                "PathUsed": path,
                "ModeUsed": mode,
            }
        except Exception as e:
            last = e
    
    raise RuntimeError(
        f"BeginSession attempts failed. Last error: {last}\nTried: {attempts}\nCOMPANY_FILE={COMPANY_FILE}"
    )


def initialize_com():
    """Initialize COM for QuickBooks communication.
    
    Returns:
        RequestProcessor COM object
        
    Raises:
        RuntimeError: If COM object creation fails
    """
    try:
        pythoncom.CoInitialize()
        return gencache.EnsureDispatch("QBXMLRP2.RequestProcessor")
    except Exception as e:
        raise RuntimeError(f"Failed to create QuickBooks COM object: {e}")


def cleanup_com(rp):
    """Clean up COM objects and connections.
    
    Args:
        rp: RequestProcessor COM object
    """
    try:
        if rp:
            rp.CloseConnection()
    except Exception:
        pass
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass