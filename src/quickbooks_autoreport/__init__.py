"""QuickBooks Auto Reporter - Core Package.

A comprehensive QuickBooks reporting solution with continuous polling,
change detection, and professional export capabilities.
"""

__version__ = "2.0.0"

# Core configuration
from .config import (
    APP_NAME,
    QBXML_VERSION_PRIMARY,
    QBXML_VERSION_FALLBACK,
    COMPANY_FILE,
    DEFAULT_OUT_DIR,
    INTERVAL_OPTIONS,
    DEFAULT_INTERVAL,
    SETTINGS_FILE,
    REPORT_CONFIGS,
    load_settings,
    save_settings,
    get_file_paths,
)

# Core services
from .services import (
    export_report,
    export_all_reports,
    diagnose_quickbooks_connection,
    test_xml_generation,
)

# Utilities
from .utils import (
    log,
    log_info,
    log_success,
    log_error,
    log_warning,
    log_progress,
    log_data,
    log_separator,
)

__all__ = [
    # Version
    "__version__",
    
    # Configuration
    "APP_NAME",
    "QBXML_VERSION_PRIMARY", 
    "QBXML_VERSION_FALLBACK",
    "COMPANY_FILE",
    "DEFAULT_OUT_DIR",
    "INTERVAL_OPTIONS",
    "DEFAULT_INTERVAL",
    "SETTINGS_FILE",
    "REPORT_CONFIGS",
    "load_settings",
    "save_settings",
    "get_file_paths",
    
    # Core services
    "export_report",
    "export_all_reports",
    "diagnose_quickbooks_connection",
    "test_xml_generation",
    
    # Utilities
    "log",
    "log_info",
    "log_success",
    "log_error",
    "log_warning",
    "log_progress",
    "log_data",
    "log_separator",
]