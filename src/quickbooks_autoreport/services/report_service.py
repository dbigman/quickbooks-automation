"""Main report service for QuickBooks Auto Reporter.

Orchestrates the entire report generation process from XML generation
to export with change detection.
"""

import datetime as dt
from typing import Dict, Any, Optional, Tuple

from ..adapters.quickbooks.request_handler import qb_request
from ..config import REPORT_CONFIGS, ALLOW_SALESORDER_FALLBACK
from ..services.qbxml_generator import build_report_qbxml, build_salesorder_query, generate_xml_with_version_fallback
from ..services.report_parser import parse_and_validate_response
from ..services.export_service import export_report_with_change_detection
from ..utils.logging_utils import log_progress, log_info, log_error, log_data, log_separator


def export_report(
    report_key: str,
    out_dir: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    status_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """Execute single report export with dynamic output directory and date range.
    
    Args:
        report_key: Report configuration key
        out_dir: Output directory (uses default if None)
        date_from: Start date for reports with date ranges (YYYY-MM-DD)
        date_to: End date for reports with date ranges (YYYY-MM-DD)
        status_callback: Optional callback for status updates
        
    Returns:
        Dictionary with export results
        
    Raises:
        RuntimeError: If export fails
    """
    if out_dir is None:
        from ..config import DEFAULT_OUT_DIR
        out_dir = DEFAULT_OUT_DIR

    import os
    os.makedirs(out_dir, exist_ok=True)
    config = REPORT_CONFIGS[report_key]

    log_progress(f"Starting export for {config['name']} (key: {report_key})", out_dir)
    
    if status_callback:
        status_callback(report_key, "Running", "Generating XML...")

    try_versions = []
    if report_key == "open_sales_orders" and ALLOW_SALESORDER_FALLBACK:
        # For Open Sales Orders, try the sales order query as fallback
        try_versions.extend([
            ("report", "16.0"),
            ("report", "13.0"),
            ("salesorder", "13.0")
        ])
    else:
        # For other reports, try version fallback
        try_versions.extend([
            ("report", "16.0"),
            ("report", "13.0")
        ])

    last_exc = None

    for ver_idx, (request_type, version) in enumerate(try_versions):
        try:
            log_progress(
                f"Attempting {config['name']} with {request_type} query, qbXML version {version} "
                f"(attempt {ver_idx + 1}/{len(try_versions)})",
                out_dir
            )

            if status_callback:
                status_callback(report_key, "Running", f"Trying version {version}...")

            # Build the XML request
            if request_type == "salesorder":
                req = build_salesorder_query(version)
                resp, info = qb_request(req, out_dir, report_key)
                headers, rows = parse_and_validate_response(resp, "salesorder")
            else:
                xml, actual_version = generate_xml_with_version_fallback(
                    config["qbxml_type"], date_from, date_to, report_key
                )
                log_data(f"Built XML request for {config['name']}: {len(xml)} characters", out_dir)
                
                if status_callback:
                    status_callback(report_key, "Running", "Connecting to QuickBooks...")

                # Execute the request
                resp, info = qb_request(xml, out_dir, report_key)
                log_data(f"Received response for {config['name']}: {len(resp)} characters", out_dir)

                if status_callback:
                    status_callback(report_key, "Running", "Parsing response...")

                # Parse the response
                headers, rows = parse_and_validate_response(resp, "standard")

            log_data(f"Parsed {config['name']}: {len(headers)} columns, {len(rows)} rows", out_dir)

            if status_callback:
                status_callback(report_key, "Running", "Exporting files...")

            # Export with change detection
            result = export_report_with_change_detection(headers, rows, out_dir, report_key)
            
            # Add connection info to result
            result["connect_info"] = info
            result["version_used"] = version
            result["request_type"] = request_type
            
            if status_callback:
                status_callback(
                    report_key,
                    "Success" if result["excel_created"] else "Partial",
                    str(result["rows"])
                )

            return result

        except Exception as e:
            last_exc = e
            log_error(f"{config['name']} {request_type} v{version} failed: {e}", out_dir)
            if "parsing the provided XML text stream" in str(e):
                continue
            else:
                break

    # If we get here, all attempts failed
    raise last_exc if last_exc else RuntimeError(f"Unknown failure for {config['name']}")


def export_all_reports(
    out_dir: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    status_callback: Optional[callable] = None
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Export all configured reports with enhanced error handling.
    
    Args:
        out_dir: Output directory (uses default if None)
        date_from: Start date for reports with date ranges (YYYY-MM-DD)
        date_to: End date for reports with date ranges (YYYY-MM-DD)
        status_callback: Optional callback for status updates
        
    Returns:
        Tuple of (results_dict, errors_dict)
    """
    if out_dir is None:
        from ..config import DEFAULT_OUT_DIR
        out_dir = DEFAULT_OUT_DIR

    results = {}
    errors = {}
    connection_tested = False
    connection_working = False

    log_info(f"Starting export of all reports to: {out_dir}", out_dir)
    if date_from and date_to:
        log_info(f"Date range: {date_from} to {date_to}", out_dir)

    # Process reports in order of complexity (simplest first)
    report_order = [
        "open_sales_orders",  # Usually works
        "profit_loss",
        "sales_by_item",
        "profit_loss_detail",
        "sales_by_item_detail",
        "sales_by_rep_detail",
        "purchase_by_vendor_detail",
        "ap_aging_detail",
        "ar_aging_detail",
    ]

    for report_key in report_order:
        if report_key not in REPORT_CONFIGS:
            continue

        config = REPORT_CONFIGS[report_key]
        try:
            log_progress(f"Starting export for {config['name']} (key: {report_key})", out_dir)
            result = export_report(report_key, out_dir, date_from, date_to, status_callback)
            results[report_key] = result
            connection_working = True
            log_info(
                f"{config['name']} completed successfully - {result['rows']} rows, "
                f"Excel: {'Yes' if result['excel_created'] else 'No'}",
                out_dir
            )

        except Exception as e:
            # Enhanced error handling with user-friendly messages
            if not connection_tested:
                connection_tested = True
                # Check if this is a connection issue that affects all reports
                error_str = str(e)
                if any(code in error_str for code in ["-2147221005", "-2147221164", "Invalid class string", "Class not registered"]):
                    log_error("Detected QuickBooks connection issue. Running diagnostics...", out_dir)
                    
                    # Run diagnostics
                    from ..services.diagnostics_service import diagnose_quickbooks_connection
                    diagnostics = diagnose_quickbooks_connection(out_dir)
                    
                    # Log user-friendly error message
                    log_separator(out_dir)
                    log_error("QUICKBOOKS CONNECTION PROBLEM DETECTED", out_dir)
                    log_info("The application cannot connect to QuickBooks Desktop.", out_dir)
                    log_info("This is usually because the QuickBooks SDK is not installed or not working properly.", out_dir)
                    log_separator(out_dir)
                    log_info("IMMEDIATE STEPS TO FIX:", out_dir)
                    log_info("1. Make sure QuickBooks Desktop is installed on this computer", out_dir)
                    log_info("2. Download and install the QuickBooks SDK from the Intuit Developer website", out_dir)
                    log_info("3. Restart your computer after installing the SDK", out_dir)
                    log_info("4. Run this application as Administrator", out_dir)
                    log_separator(out_dir)
                    log_info(f"A detailed diagnostic report has been saved to: {out_dir}", out_dir)
                    log_info("Check 'QuickBooks_Diagnostic_Report.xlsx' for more information.", out_dir)
                    
                    # Since this is a fundamental connection issue, all reports will fail
                    # Add the same error to all remaining reports
                    for remaining_key in report_order:
                        if remaining_key not in results and remaining_key not in errors:
                            errors[remaining_key] = "Cannot connect to QuickBooks Desktop - SDK not installed or not working"
                    break
            
            # Log individual report error
            user_friendly_msg = "Cannot connect to QuickBooks Desktop - check diagnostic report for solutions"
            errors[report_key] = user_friendly_msg
            log_error(f"{config['name']}: {user_friendly_msg}", out_dir)
            
            if status_callback:
                status_callback(report_key, "Error", user_friendly_msg)

    # Enhanced summary with user guidance
    total_reports = len(report_order)
    successful_reports = len(results)
    failed_reports = len(errors)

    log_separator(out_dir)
    log_info(f"EXPORT SUMMARY: {successful_reports}/{total_reports} successful, {failed_reports} failed", out_dir)
    log_separator(out_dir)

    if successful_reports > 0:
        log_info(f"Successful reports: {', '.join([REPORT_CONFIGS[k]['name'] for k in results.keys()])}", out_dir)

    if failed_reports > 0:
        if not connection_working:
            log_error("ALL REPORTS FAILED - QuickBooks connection problem", out_dir)
            log_separator(out_dir)
            log_info("NEXT STEPS:", out_dir)
            log_info("1. Check the diagnostic report in the output folder", out_dir)
            log_info("2. Install QuickBooks SDK if not already installed", out_dir)
            log_info("3. Run as Administrator", out_dir)
            log_info("4. Make sure QuickBooks Desktop is properly installed", out_dir)
        else:
            log_error(f"Failed reports: {', '.join([REPORT_CONFIGS[k]['name'] for k in errors.keys()])}", out_dir)

    return results, errors


def validate_report_parameters(report_key: str, date_from: Optional[str], date_to: Optional[str]) -> None:
    """Validate report parameters before processing.
    
    Args:
        report_key: Report configuration key
        date_from: Start date for reports with date ranges
        date_to: End date for reports with date ranges
        
    Raises:
        ValueError: If parameters are invalid
    """
    if report_key not in REPORT_CONFIGS:
        raise ValueError(f"Unknown report key: {report_key}")
    
    config = REPORT_CONFIGS[report_key]
    
    if config.get("uses_date_range", False):
        if not date_from or not date_to:
            raise ValueError(f"Report {report_key} requires date range parameters")
        
        try:
            dt.datetime.strptime(date_from, "%Y-%m-%d")
            dt.datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")