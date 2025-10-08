"""Tests for configuration module."""

import unittest
import tempfile
import os
import json
from datetime import date

from src.quickbooks_autoreport.config import (
    load_settings,
    save_settings,
    get_file_paths,
    REPORT_CONFIGS,
    DEFAULT_OUT_DIR,
    SETTINGS_FILE,
)


class TestConfig(unittest.TestCase):
    """Test configuration functions."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        self.original_settings_file = SETTINGS_FILE
        # Override settings file for testing
        import src.quickbooks_autoreport.config as config_module
        config_module.SETTINGS_FILE = os.path.join(self.test_dir, "test_settings.json")
    
    def tearDown(self):
        """Clean up test environment."""
        # Restore original settings file
        import src.quickbooks_autoreport.config as config_module
        config_module.SETTINGS_FILE = self.original_settings_file
        
        # Clean up test directory
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_load_settings_default(self):
        """Test loading default settings when no file exists."""
        settings = load_settings()
        
        self.assertIn("output_dir", settings)
        self.assertIn("interval", settings)
        self.assertIn("report_date_from", settings)
        self.assertIn("report_date_to", settings)
        
        self.assertEqual(settings["output_dir"], DEFAULT_OUT_DIR)
        self.assertEqual(settings["interval"], "15 minutes")
    
    def test_save_and_load_settings(self):
        """Test saving and loading settings."""
        test_settings = {
            "output_dir": "C:\\Test\\Reports",
            "interval": "30 minutes",
            "report_date_from": "2025-01-01",
            "report_date_to": "2025-01-31",
        }
        
        save_settings(test_settings)
        loaded_settings = load_settings()
        
        self.assertEqual(loaded_settings["output_dir"], "C:\\Test\\Reports")
        self.assertEqual(loaded_settings["interval"], "30 minutes")
        self.assertEqual(loaded_settings["report_date_from"], "2025-01-01")
        self.assertEqual(loaded_settings["report_date_to"], "2025-01-31")
    
    def test_load_settings_invalid_interval(self):
        """Test loading settings with invalid interval falls back to default."""
        test_settings = {
            "output_dir": "C:\\Test\\Reports",
            "interval": "invalid_interval",
            "report_date_from": "2025-01-01",
            "report_date_to": "2025-01-31",
        }
        
        save_settings(test_settings)
        loaded_settings = load_settings()
        
        # Should fall back to default interval
        self.assertEqual(loaded_settings["interval"], "15 minutes")
    
    def test_get_file_paths(self):
        """Test getting file paths for a report."""
        paths = get_file_paths("C:\\Test\\Reports", "profit_loss")
        
        self.assertIn("main_csv", paths)
        self.assertIn("excel_file", paths)
        self.assertIn("hash_file", paths)
        self.assertIn("log_file", paths)
        self.assertIn("req_log", paths)
        self.assertIn("resp_log", paths)
        
        # Check that paths are correctly constructed
        self.assertTrue(paths["main_csv"].endswith("Profit_And_Loss.csv"))
        self.assertTrue(paths["excel_file"].endswith("Profit_And_Loss.xlsx"))
        self.assertTrue(paths["hash_file"].endswith("Profit_And_Loss.hash"))
    
    def test_report_configs_structure(self):
        """Test that REPORT_CONFIGS has the expected structure."""
        self.assertIn("profit_loss", REPORT_CONFIGS)
        self.assertIn("open_sales_orders", REPORT_CONFIGS)
        
        # Check a specific report configuration
        pl_config = REPORT_CONFIGS["profit_loss"]
        required_keys = ["name", "qbxml_type", "query", "csv_filename", "excel_filename", "hash_filename", "uses_date_range"]
        
        for key in required_keys:
            self.assertIn(key, pl_config)
        
        self.assertEqual(pl_config["name"], "Profit & Loss")
        self.assertEqual(pl_config["qbxml_type"], "ProfitAndLossStandard")
        self.assertEqual(pl_config["query"], "GeneralSummary")
        self.assertTrue(pl_config["uses_date_range"])


if __name__ == "__main__":
    unittest.main()