#!/usr/bin/env python3
"""
Debug script for QuickBooks Auto Reporter
Tests individual reports and provides detailed error information
"""

import os
import sys
import traceback

from quickbooks_autoreport import (
    DEFAULT_OUT_DIR,
    REPORT_CONFIGS,
    export_report,
    load_settings,
    log,
)


def test_single_report(report_key: str, out_dir: str = None):
    """Test a single report with detailed error reporting"""
    if out_dir is None:
        out_dir = DEFAULT_OUT_DIR
    
    config = REPORT_CONFIGS[report_key]
    print(f"\n{'='*60}")
    print(f"Testing: {config['name']} (key: {report_key})")
    print(f"qbXML Type: {config['qbxml_type']}")
    print(f"Uses Date Range: {config.get('uses_date_range', False)}")
    print(f"{'='*60}")
    
    try:
        # Load settings for date range
        settings = load_settings()
        date_from = settings.get("report_date_from")
        date_to = settings.get("report_date_to")
        
        print(f"Date range: {date_from} to {date_to}")
        
        # Attempt the export
        result = export_report(report_key, out_dir, date_from, date_to)
        
        print(f"✅ SUCCESS!")
        print(f"   Rows: {result['rows']}")
        print(f"   Excel Created: {'Yes' if result['excel_created'] else 'No'}")
        print(f"   Changed: {'Yes' if result['changed'] else 'No'}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        return False

def test_all_reports():
    """Test all reports individually"""
    print("QuickBooks Auto Reporter - Debug Mode")
    print("Testing all reports individually...\n")
    
    # Ensure output directory exists
    os.makedirs(DEFAULT_OUT_DIR, exist_ok=True)
    
    results = {}
    
    for report_key in REPORT_CONFIGS.keys():
        success = test_single_report(report_key)
        results[report_key] = success
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    successful = [k for k, v in results.items() if v]
    failed = [k for k, v in results.items() if not v]
    
    print(f"Successful ({len(successful)}):")
    for key in successful:
        print(f"  ✅ {REPORT_CONFIGS[key]['name']}")
    
    print(f"\nFailed ({len(failed)}):")
    for key in failed:
        print(f"  ❌ {REPORT_CONFIGS[key]['name']}")
    
    print(f"\nOverall: {len(successful)}/{len(results)} reports successful")
    
    # Check log file
    log_file = os.path.join(DEFAULT_OUT_DIR, "QuickBooks_Auto_Reports.log")
    if os.path.exists(log_file):
        print(f"\nDetailed logs available at: {log_file}")

def test_quickbooks_connection():
    """Test basic QuickBooks connection"""
    print("Testing QuickBooks connection...")
    
    try:
        from quickbooks_autoreport import build_report_qbxml, qb_request
        
        # Try a simple request
        xml = build_report_qbxml("16.0", "OpenSalesOrderByItem", report_key="open_sales_orders")
        print(f"Built XML request: {len(xml)} characters")
        
        resp, info = qb_request(xml, DEFAULT_OUT_DIR, "open_sales_orders")
        print(f"✅ Connection successful!")
        print(f"Response length: {len(resp)} characters")
        print(f"Company info: {info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--connection":
            test_quickbooks_connection()
        elif sys.argv[1] in REPORT_CONFIGS:
            test_single_report(sys.argv[1])
        else:
            print(f"Unknown report key: {sys.argv[1]}")
            print(f"Available keys: {', '.join(REPORT_CONFIGS.keys())}")
    else:
        test_all_reports()