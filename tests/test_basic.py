#!/usr/bin/env python3
"""
Basic tests for QuickBooks Order Exporter
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from quickbooks import cli, csv_reader, odoo_enrichment, excel_export, dataframe_utils
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_logger():
    """Test logger setup."""
    try:
        from logger import setup_logging
        logger = setup_logging()
        logger.info("Test log message")
        print("✅ Logger setup successful")
        return True
    except Exception as e:
        print(f"❌ Logger test failed: {e}")
        return False

def test_connector():
    """Test Odoo connector (without actual connection)."""
    try:
        import os
        os.environ['ODOO_URL'] = 'http://test'
        os.environ['ODOO_DATABASE'] = 'test'
        os.environ['ODOO_USERNAME'] = 'test'
        os.environ['ODOO_PASSWORD'] = 'test'
        
        from connector import OdooConnector
        from logger import setup_logging
        logger = setup_logging()
        
        # Just test instantiation, not actual connection
        connector = OdooConnector(logger)
        print("✅ Connector instantiation successful")
        return True
    except Exception as e:
        print(f"❌ Connector test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running QuickBooks Order Exporter Tests")
    print("=" * 70)
    
    tests = [
        ("Module Imports", test_imports),
        ("Logger Setup", test_logger),
        ("Connector Instantiation", test_connector),
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
