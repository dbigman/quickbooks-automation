"""Domain models for QuickBooks Auto Reporter.

This package contains all domain models (dataclasses) and custom exceptions
that define the core business entities and error types.
"""

from .diagnostics import DiagnosticResult
from .exceptions import (
    QuickBooksError,
    QuickBooksConnectionError,
    ReportGenerationError,
    FileOperationError,
    SettingsError,
)
from .report_config import ReportConfig
from .report_result import ReportResult
from .sales_data import DashboardState, SalesData
from .settings import Settings, DEFAULT_OUT_DIR, DEFAULT_INTERVAL, VALID_INTERVALS

__all__ = [
    # Exceptions
    "QuickBooksError",
    "QuickBooksConnectionError",
    "ReportGenerationError",
    "FileOperationError",
    "SettingsError",
    # Models
    "ReportConfig",
    "ReportResult",
    "Settings",
    "DiagnosticResult",
    "SalesData",
    "DashboardState",
    # Constants
    "DEFAULT_OUT_DIR",
    "DEFAULT_INTERVAL",
    "VALID_INTERVALS",
]
