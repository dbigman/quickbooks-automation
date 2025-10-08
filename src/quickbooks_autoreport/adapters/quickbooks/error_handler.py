"""Error handling and user-friendly messaging for QuickBooks Auto Reporter."""

from typing import Dict, Any

from ...utils.logging_utils import log_error, log_info


def get_user_friendly_error(error) -> Dict[str, Any]:
    """Convert technical errors to user-friendly messages with solutions.
    
    Args:
        error: Exception object
        
    Returns:
        Dictionary containing error information with title, message, solutions, etc.
    """
    error_str = str(error)
    
    # COM Error -2147221005: Invalid class string
    if "-2147221005" in error_str or "Invalid class string" in error_str:
        return {
            "title": "QuickBooks Connection Problem",
            "message": "Cannot connect to QuickBooks Desktop. This usually means QuickBooks SDK is not installed or not properly registered.",
            "solutions": [
                "1. Install QuickBooks Desktop if not already installed",
                "2. Download and install the QuickBooks SDK from Intuit Developer website",
                "3. Run the application as Administrator",
                "4. Restart your computer after SDK installation",
                "5. Make sure QuickBooks Desktop is closed before running reports"
            ],
            "technical_details": error_str,
            "error_type": "SDK_NOT_INSTALLED"
        }
    
    # COM Error -2147221164: Class not registered
    elif "-2147221164" in error_str or "Class not registered" in error_str:
        return {
            "title": "QuickBooks SDK Not Registered",
            "message": "The QuickBooks SDK components are not properly registered on this system.",
            "solutions": [
                "1. Reinstall the QuickBooks SDK",
                "2. Run 'regsvr32 qbxmlrp2.dll' as Administrator",
                "3. Restart your computer",
                "4. Contact your IT administrator for help with COM registration"
            ],
            "technical_details": error_str,
            "error_type": "SDK_NOT_REGISTERED"
        }
    
    # Access denied errors
    elif "Access" in error_str and "denied" in error_str:
        return {
            "title": "Permission Problem",
            "message": "The application doesn't have permission to access QuickBooks.",
            "solutions": [
                "1. Run the application as Administrator",
                "2. Check QuickBooks company file permissions",
                "3. Make sure QuickBooks is not in multi-user mode",
                "4. Close QuickBooks Desktop and try again"
            ],
            "technical_details": error_str,
            "error_type": "ACCESS_DENIED"
        }
    
    # File not found or path errors
    elif any(term in error_str.lower() for term in ["file not found", "path", "cannot find"]):
        return {
            "title": "QuickBooks File Problem",
            "message": "Cannot find or access the QuickBooks company file.",
            "solutions": [
                "1. Make sure QuickBooks Desktop is installed and working",
                "2. Open QuickBooks and verify the company file opens correctly",
                "3. Check the QB_COMPANY_FILE environment variable path",
                "4. Make sure the company file is not on a network drive that's disconnected"
            ],
            "technical_details": error_str,
            "error_type": "FILE_NOT_FOUND"
        }
    
    # Network or connection errors
    elif any(term in error_str.lower() for term in ["network", "connection", "timeout"]):
        return {
            "title": "Connection Problem",
            "message": "Cannot establish a connection to QuickBooks.",
            "solutions": [
                "1. Make sure QuickBooks Desktop is running",
                "2. Check if QuickBooks is in single-user mode",
                "3. Restart QuickBooks Desktop",
                "4. Check network connectivity if using a network installation"
            ],
            "technical_details": error_str,
            "error_type": "CONNECTION_ERROR"
        }
    
    # Generic error
    else:
        return {
            "title": "QuickBooks Error",
            "message": "An unexpected error occurred while connecting to QuickBooks.",
            "solutions": [
                "1. Make sure QuickBooks Desktop is installed and running",
                "2. Try restarting QuickBooks Desktop",
                "3. Run this application as Administrator",
                "4. Check the log file for more details",
                "5. Contact support with the technical details below"
            ],
            "technical_details": error_str,
            "error_type": "UNKNOWN_ERROR"
        }


def log_error_details(error_info: Dict[str, Any], out_dir: str = None) -> None:
    """Log detailed error information for debugging.
    
    Args:
        error_info: Error information dictionary from get_user_friendly_error
        out_dir: Output directory for logging
    """
    log_error(f"{error_info['title']}: {error_info['message']}", out_dir)
    
    # Log technical details for debugging
    log_error(f"Technical details: {error_info['technical_details']}", out_dir)
    
    # Log solutions
    log_info("Possible solutions:", out_dir)
    for solution in error_info['solutions']:
        log_info(f"   {solution}", out_dir)


def handle_com_error(error, out_dir: str = None) -> RuntimeError:
    """Handle COM error and convert to user-friendly RuntimeError.
    
    Args:
        error: Original exception
        out_dir: Output directory for logging
        
    Returns:
        RuntimeError with user-friendly message
    """
    error_info = get_user_friendly_error(error)
    log_error_details(error_info, out_dir)
    
    # Re-raise with user-friendly message
    return RuntimeError(f"{error_info['title']}: {error_info['message']}")