"""Configuration module for QuickBooks Auto Reporter.

This module contains all configuration constants, report configurations,
and settings management functions.
"""

import datetime as dt
import json
import os
from typing import Dict, Any

# Application constants
APP_NAME = "Gasco Auto Reporter"
QBXML_VERSION_PRIMARY = "16.0"
QBXML_VERSION_FALLBACK = "13.0"
ALLOW_SALESORDER_FALLBACK = True

# Company file configuration
COMPANY_FILE = os.environ.get(
    "QB_COMPANY_FILE",
    r"C:\Users\Public\Documents\Intuit\QuickBooks\Company Files"
    r"\Gasco Industrial 2019\Gasco Industrial -  2019.QBW",
)

# Default output directory (can be changed by user)
DEFAULT_OUT_DIR = r"C:\Reports"

# Interval options in seconds
INTERVAL_OPTIONS = {
    "5 minutes": 5 * 60,
    "15 minutes": 15 * 60,
    "30 minutes": 30 * 60,
    "60 minutes": 60 * 60,
}
DEFAULT_INTERVAL = "15 minutes"

# Settings file for persistence
SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".qb_auto_reporter_settings.json")

# Report configurations for all 9 report types
REPORT_CONFIGS = {
    "open_sales_orders": {
        "name": "Open Sales Orders by Item",
        "qbxml_type": "OpenSalesOrderByItem",
        "query": "GeneralDetail",
        "csv_filename": "Open_Sales_Orders_By_Item.csv",
        "excel_filename": "Open_Sales_Orders_By_Item.xlsx",
        "hash_filename": "Open_Sales_Orders_By_Item.hash",
        "request_log": "open_so_request.xml",
        "response_log": "open_so_response.xml",
        "uses_date_range": False,
    },
    "profit_loss": {
        "name": "Profit & Loss",
        "qbxml_type": "ProfitAndLossStandard",
        "query": "GeneralSummary",
        "csv_filename": "Profit_And_Loss.csv",
        "excel_filename": "Profit_And_Loss.xlsx",
        "hash_filename": "Profit_And_Loss.hash",
        "request_log": "pl_request.xml",
        "response_log": "pl_response.xml",
        "uses_date_range": True,
    },
    "profit_loss_detail": {
        "name": "Profit & Loss Detail",
        "qbxml_type": "ProfitAndLossDetail",
        "query": "GeneralDetail",
        "csv_filename": "Profit_And_Loss_Detail.csv",
        "excel_filename": "Profit_And_Loss_Detail.xlsx",
        "hash_filename": "Profit_And_Loss_Detail.hash",
        "request_log": "pl_detail_request.xml",
        "response_log": "pl_detail_response.xml",
        "uses_date_range": True,
    },
    "sales_by_item": {
        "name": "Sales by Item",
        "qbxml_type": "SalesByItemSummary",
        "query": "GeneralSummary",
        "csv_filename": "Sales_By_Item.csv",
        "excel_filename": "Sales_By_Item.xlsx",
        "hash_filename": "Sales_By_Item.hash",
        "request_log": "sales_item_request.xml",
        "response_log": "sales_item_response.xml",
        "uses_date_range": True,
    },
    "sales_by_item_detail": {
        "name": "Sales by Item Detail",
        "qbxml_type": "SalesByItemDetail",
        "query": "GeneralDetail",
        "csv_filename": "Sales_By_Item_Detail.csv",
        "excel_filename": "Sales_By_Item_Detail.xlsx",
        "hash_filename": "Sales_By_Item_Detail.hash",
        "request_log": "sales_item_detail_request.xml",
        "response_log": "sales_item_detail_response.xml",
        "uses_date_range": True,
    },
    "sales_by_rep_detail": {
        "name": "Sales by Rep Detail",
        "qbxml_type": "SalesByRepDetail",
        "query": "GeneralDetail",
        "csv_filename": "Sales_By_Rep_Detail.csv",
        "excel_filename": "Sales_By_Rep_Detail.xlsx",
        "hash_filename": "Sales_By_Rep_Detail.hash",
        "request_log": "sales_rep_detail_request.xml",
        "response_log": "sales_rep_detail_response.xml",
        "uses_date_range": True,
    },
    "purchase_by_vendor_detail": {
        "name": "Purchase by Vendor Detail",
        "qbxml_type": "PurchasesByVendorDetail",
        "query": "GeneralDetail",
        "csv_filename": "Purchase_By_Vendor_Detail.csv",
        "excel_filename": "Purchase_By_Vendor_Detail.xlsx",
        "hash_filename": "Purchase_By_Vendor_Detail.hash",
        "request_log": "purchase_vendor_detail_request.xml",
        "response_log": "purchase_vendor_detail_response.xml",
        "uses_date_range": True,
    },
    "ap_aging_detail": {
        "name": "AP Aging Detail",
        "qbxml_type": "APAgingDetail",
        "query": "Aging",
        "csv_filename": "AP_Aging_Detail.csv",
        "excel_filename": "AP_Aging_Detail.xlsx",
        "hash_filename": "AP_Aging_Detail.hash",
        "request_log": "ap_aging_detail_request.xml",
        "response_log": "ap_aging_detail_response.xml",
        "uses_date_range": False,  # Aging reports use AsOfReportDate
    },
    "ar_aging_detail": {
        "name": "AR Aging Detail",
        "qbxml_type": "ARAgingDetail",
        "query": "Aging",
        "csv_filename": "AR_Aging_Detail.csv",
        "excel_filename": "AR_Aging_Detail.xlsx",
        "hash_filename": "AR_Aging_Detail.hash",
        "request_log": "ar_aging_detail_request.xml",
        "response_log": "ar_aging_detail_response.xml",
        "uses_date_range": False,  # Aging reports use AsOfReportDate
    },
}


def load_settings() -> Dict[str, Any]:
    """Load user settings from file.
    
    Returns:
        Dictionary containing user settings with defaults applied.
    """
    # Default to current month date range
    today = dt.date.today()
    first_day = today.replace(day=1)
    default_settings = {
        "output_dir": DEFAULT_OUT_DIR,
        "interval": DEFAULT_INTERVAL,
        "report_date_from": first_day.strftime("%Y-%m-%d"),
        "report_date_to": today.strftime("%Y-%m-%d"),
    }
    
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
                if settings.get("interval") not in INTERVAL_OPTIONS:
                    settings["interval"] = DEFAULT_INTERVAL
                # Ensure date settings exist
                if "report_date_from" not in settings:
                    settings["report_date_from"] = default_settings["report_date_from"]
                if "report_date_to" not in settings:
                    settings["report_date_to"] = default_settings["report_date_to"]
                return settings
    except Exception:
        pass
    
    return default_settings


def save_settings(settings: Dict[str, Any]) -> None:
    """Save user settings to file.
    
    Args:
        settings: Dictionary of settings to save
    """
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception:
        pass


def get_file_paths(out_dir: str, report_key: str) -> Dict[str, str]:
    """Get all file paths based on output directory and report type.
    
    Args:
        out_dir: Output directory path
        report_key: Report configuration key
        
    Returns:
        Dictionary containing all file paths for the report
    """
    config = REPORT_CONFIGS[report_key]
    return {
        "main_csv": os.path.join(out_dir, config["csv_filename"]),
        "excel_file": os.path.join(out_dir, config["excel_filename"]),
        "hash_file": os.path.join(out_dir, config["hash_filename"]),
        "log_file": os.path.join(out_dir, "QuickBooks_Auto_Reports.log"),
        "req_log": os.path.join(out_dir, config["request_log"]),
        "resp_log": os.path.join(out_dir, config["response_log"]),
    }