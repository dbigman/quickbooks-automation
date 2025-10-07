"""QuickBooks Open Sales Orders processing and reporting.

This package contains modules for:
- CSV parsing and normalization
- Optional Odoo enrichment
- DataFrame utilities
- Excel/JSON export
- CLI orchestration
"""

from .csv_reader import extract_sales_orders_from_csv
from .excel_export import generate_quickbooks_excel_report

__all__ = [
    "extract_sales_orders_from_csv",
    "generate_quickbooks_excel_report",
]
