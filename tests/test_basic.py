#!/usr/bin/env python3
"""
Basic tests for QuickBooks Auto Reporter
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that main module can be imported."""
    try:
        import quickbooks_autoreport

        print("✅ Main module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_report_configs():
    """Test that report configurations are valid."""
    try:
        import quickbooks_autoreport

        configs = quickbooks_autoreport.REPORT_CONFIGS
        assert len(configs) > 0, "No report configurations found"

        required_keys = [
            "name",
            "qbxml_type",
            "query",
            "csv_filename",
            "excel_filename",
            "hash_filename",
            "request_log",
            "response_log",
            "uses_date_range",
        ]

        for report_key, config in configs.items():
            for key in required_keys:
                assert key in config, f"Missing key '{key}' in {report_key}"

        print(f"✅ All {len(configs)} report configurations are valid")
        return True
    except Exception as e:
        print(f"❌ Report config test failed: {e}")
        return False


def test_xml_generation():
    """Test qbXML generation for different report types."""
    try:
        import quickbooks_autoreport

        # Test GeneralDetail report (no date range)
        xml = quickbooks_autoreport.build_report_qbxml(
            version="16.0",
            report_type="OpenSalesOrderByItem",
            report_key="open_sales_orders",
        )
        assert '<?xml version="1.0"' in xml
        assert "OpenSalesOrderByItem" in xml
        assert "GeneralDetailReportQueryRq" in xml

        # Test GeneralSummary report (with date range)
        xml = quickbooks_autoreport.build_report_qbxml(
            version="16.0",
            report_type="ProfitAndLossStandard",
            date_from="2025-01-01",
            date_to="2025-01-31",
            report_key="profit_loss",
        )
        assert "ProfitAndLossStandard" in xml
        assert "GeneralSummaryReportQueryRq" in xml
        assert "ReportPeriod" in xml

        # Test Aging report
        xml = quickbooks_autoreport.build_report_qbxml(
            version="16.0",
            report_type="APAgingDetail",
            date_to="2025-01-31",
            report_key="ap_aging_detail",
        )
        assert "APAgingDetail" in xml
        assert "AgingReportQueryRq" in xml
        assert "ReportAgingAsOf" in xml

        print("✅ XML generation tests passed")
        return True
    except Exception as e:
        print(f"❌ XML generation test failed: {e}")
        return False


def test_settings_functions():
    """Test settings load/save functions."""
    try:
        import os
        import tempfile

        import quickbooks_autoreport

        # Override settings file for testing
        test_settings_file = os.path.join(
            tempfile.gettempdir(), "test_qb_settings.json"
        )
        original_settings_file = quickbooks_autoreport.SETTINGS_FILE
        quickbooks_autoreport.SETTINGS_FILE = test_settings_file

        try:
            # Test save
            test_settings = {
                "output_dir": "C:\\TestReports",
                "interval": "15 minutes",
                "report_date_from": "2025-01-01",
                "report_date_to": "2025-01-31",
            }
            quickbooks_autoreport.save_settings(test_settings)

            # Test load
            loaded_settings = quickbooks_autoreport.load_settings()
            assert loaded_settings["output_dir"] == test_settings["output_dir"]
            assert loaded_settings["interval"] == test_settings["interval"]

            # Cleanup
            if os.path.exists(test_settings_file):
                os.remove(test_settings_file)

            print("✅ Settings functions test passed")
            return True
        finally:
            quickbooks_autoreport.SETTINGS_FILE = original_settings_file

    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False


def test_file_paths():
    """Test file path generation."""
    try:
        import quickbooks_autoreport

        out_dir = "C:\\TestReports"
        report_key = "open_sales_orders"

        paths = quickbooks_autoreport.get_file_paths(out_dir, report_key)

        required_paths = [
            "main_csv",
            "excel_file",
            "hash_file",
            "log_file",
            "req_log",
            "resp_log",
        ]

        for path_key in required_paths:
            assert path_key in paths, f"Missing path key: {path_key}"
            assert out_dir in paths[path_key], f"Output dir not in {path_key}"

        print("✅ File path generation test passed")
        return True
    except Exception as e:
        print(f"❌ File path test failed: {e}")
        return False


def test_error_handling():
    """Test user-friendly error message generation."""
    try:
        import quickbooks_autoreport

        # Test COM error
        test_error = Exception("COM error -2147221005: Invalid class string")
        error_info = quickbooks_autoreport.get_user_friendly_error(test_error)

        assert "title" in error_info
        assert "message" in error_info
        assert "solutions" in error_info
        assert len(error_info["solutions"]) > 0
        assert error_info["error_type"] == "SDK_NOT_INSTALLED"

        # Test generic error
        test_error = Exception("Unknown error occurred")
        error_info = quickbooks_autoreport.get_user_friendly_error(test_error)
        assert error_info["error_type"] == "UNKNOWN_ERROR"

        print("✅ Error handling test passed")
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Running QuickBooks Auto Reporter Tests")
    print("=" * 70)

    tests = [
        ("Module Imports", test_imports),
        ("Report Configurations", test_report_configs),
        ("XML Generation", test_xml_generation),
        ("Settings Functions", test_settings_functions),
        ("File Path Generation", test_file_paths),
        ("Error Handling", test_error_handling),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        results.append(test_func())

    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
