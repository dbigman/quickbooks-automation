"""QuickBooks request handling for QuickBooks Auto Reporter."""

import os
from typing import Tuple, Dict, Any

from .connection import initialize_com, open_connection, try_begin_session, cleanup_com
from .error_handler import handle_com_error
from ...config import get_file_paths
from ...utils.logging_utils import log_info, log_error, log_receive


def qb_request(xml: str, out_dir: str = None, report_key: str = "open_sales_orders") -> Tuple[str, Dict[str, Any]]:
    """Execute qbXML request with enhanced error handling and user-friendly messages.
    
    Args:
        xml: qbXML request string
        out_dir: Output directory for logging (uses default if None)
        report_key: Report configuration key for logging
        
    Returns:
        Tuple of (response_xml, session_info)
        
    Raises:
        RuntimeError: If request fails
    """
    if out_dir is None:
        out_dir = get_file_paths("", report_key)["log_file"].replace("QuickBooks_Auto_Reports.log", "")
    
    # Normalize qbXML to avoid parser errors
    xml = xml.lstrip("\ufeff \t\r\n")
    xml = xml.replace("\r\n", "\n")

    file_paths = get_file_paths(out_dir, report_key)
    rp = None
    
    try:
        # Initialize COM and create RequestProcessor
        try:
            rp = initialize_com()
        except Exception as com_error:
            raise handle_com_error(com_error, out_dir)
        
        # Open connection
        try:
            open_connection(rp)
        except Exception as conn_error:
            raise handle_com_error(conn_error, out_dir)
        
        # Begin session
        try:
            ticket, info = try_begin_session(rp)
        except Exception as session_error:
            raise handle_com_error(session_error, out_dir)
        
        try:
            # Log request
            os.makedirs(out_dir, exist_ok=True)
            with open(file_paths["req_log"], "w", encoding="utf-8") as f:
                f.write(xml)
            
            # Process request
            resp = rp.ProcessRequest(ticket, xml)
            
            # Log response
            with open(file_paths["resp_log"], "w", encoding="utf-8") as f:
                f.write(resp)
            
            log_receive(f"Received response for {report_key}: {len(resp)} characters", out_dir)
            return resp, info
            
        finally:
            # End session
            try:
                rp.EndSession(ticket)
            except Exception:
                pass
                
    finally:
        # Cleanup COM objects
        cleanup_com(rp)


def validate_xml_response(resp_xml: str) -> None:
    """Validate XML response for errors.
    
    Args:
        resp_xml: XML response string
        
    Raises:
        RuntimeError: If response contains errors
    """
    import xml.etree.ElementTree as ET
    
    try:
        root = ET.fromstring(resp_xml)
        
        # Look for any report query response
        rs = None
        for el in root.iter():
            if el.tag.endswith("ReportQueryRs"):
                rs = el
                break
        
        if rs is None:
            raise RuntimeError("No ReportQueryRs found in response")
        
        # Check for errors
        status_code = rs.get("statusCode")
        if status_code not in (None, "0"):
            status_msg = rs.get("statusMessage", "Unknown error")
            raise RuntimeError(f"ReportQuery failed: status={status_code}, message={status_msg}")
            
    except ET.ParseError as pe:
        raise RuntimeError(f"XML parsing error: {pe}")


def normalize_xml_request(xml: str) -> str:
    """Normalize XML request to avoid parsing errors.
    
    Args:
        xml: Raw XML string
        
    Returns:
        Normalized XML string
    """
    # Remove BOM and leading whitespace
    xml = xml.lstrip("\ufeff \t\r\n")
    # Normalize line endings
    xml = xml.replace("\r\n", "\n")
    return xml