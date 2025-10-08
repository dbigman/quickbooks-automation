"""Business logic and service layer for QuickBooks Auto Reporter."""

from .qbxml_generator import (
    build_report_qbxml,
    build_salesorder_query,
    validate_xml_structure,
    generate_xml_with_version_fallback,
    test_xml_generation,
)

from .report_parser import (
    parse_report_rows,
    parse_salesorders_to_rows,
    handle_missing_columns,
    handle_empty_values,
    validate_parsed_data,
    parse_and_validate_response,
)

from .export_service import (
    render_csv,
    export_to_csv,
    export_to_excel,
    handle_change_detection,
    export_report_with_change_detection,
)

from .report_service import (
    export_report,
    export_all_reports,
    validate_report_parameters,
)

from .diagnostics_service import (
    check_quickbooks_installation,
    check_sdk_installation,
    test_com_object_creation,
    test_quickbooks_connection,
    diagnose_quickbooks_connection,
    create_diagnostic_excel_report,
    print_diagnostics_summary,
)

from .scheduler import (
    SchedulerThread,
    SchedulerManager,
)

__all__ = [
    # qbXML generation
    "build_report_qbxml",
    "build_salesorder_query",
    "validate_xml_structure",
    "generate_xml_with_version_fallback",
    "test_xml_generation",
    
    # Report parsing
    "parse_report_rows",
    "parse_salesorders_to_rows",
    "handle_missing_columns",
    "handle_empty_values",
    "validate_parsed_data",
    "parse_and_validate_response",
    
    # Export service
    "render_csv",
    "export_to_csv",
    "export_to_excel",
    "handle_change_detection",
    "export_report_with_change_detection",
    
    # Report service
    "export_report",
    "export_all_reports",
    "validate_report_parameters",
    
    # Diagnostics service
    "check_quickbooks_installation",
    "check_sdk_installation",
    "test_com_object_creation",
    "test_quickbooks_connection",
    "diagnose_quickbooks_connection",
    "create_diagnostic_excel_report",
    "print_diagnostics_summary",
    
    # Scheduler
    "SchedulerThread",
    "SchedulerManager",
]