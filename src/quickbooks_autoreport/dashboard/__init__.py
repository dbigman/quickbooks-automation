"""
Dashboard module for sales analytics.

This module provides data loading, metrics calculation, chart generation,
and UI components for the Streamlit sales dashboard.
"""

from .charts import ChartGenerator
from .data_loader import ExcelLoader, FileScanner
from .metrics import MetricsCalculator
from .sidebar import (
    render_sidebar,
    render_file_metadata,
    render_loading_indicator,
    render_success_indicator,
    render_error_indicator,
    render_warning_indicator,
)

__version__ = "0.1.0"

__all__ = [
    "ChartGenerator",
    "ExcelLoader",
    "FileScanner",
    "MetricsCalculator",
    "render_sidebar",
    "render_file_metadata",
    "render_loading_indicator",
    "render_success_indicator",
    "render_error_indicator",
    "render_warning_indicator",
]
