"""QuickBooks adapter for QuickBooks Auto Reporter."""

from .connection import (
    open_connection,
    host_info,
    try_begin_session,
    initialize_com,
    cleanup_com,
)

from .error_handler import (
    get_user_friendly_error,
    log_error_details,
    handle_com_error,
)

from .request_handler import (
    qb_request,
    validate_xml_response,
    normalize_xml_request,
)

__all__ = [
    # Connection management
    "open_connection",
    "host_info",
    "try_begin_session",
    "initialize_com",
    "cleanup_com",
    
    # Error handling
    "get_user_friendly_error",
    "log_error_details",
    "handle_com_error",
    
    # Request handling
    "qb_request",
    "validate_xml_response",
    "normalize_xml_request",
]