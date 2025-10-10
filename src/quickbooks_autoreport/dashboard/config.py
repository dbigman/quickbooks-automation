"""
Configuration constants for the sales dashboard.

This module defines all configuration constants including file paths,
polling intervals, required columns, and display settings.
"""

from pathlib import Path
from typing import List

# Directory Configuration
OUTPUT_DIR: Path = Path("output")
REPORTS_DIR: Path = Path("reports")

# Polling Configuration
POLL_INTERVAL_SECONDS: int = 3600  # 1 hour

# Data Configuration
SHEET_NAME: str = "Transactions"  # Sheet to read from Excel file
REQUIRED_COLUMNS: List[str] = [
    'Date',
    'Product_Name',
    'Sales_Amount',
    'Sales_Qty'
]

# Display Configuration
TOP_N_PRODUCTS: int = 5
DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
CURRENCY_SYMBOL: str = "$"

# Weekday Configuration
WEEKDAY_ORDER: List[str] = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

# Performance Configuration
MAX_FILE_SIZE_MB: int = 10
CACHE_TTL_SECONDS: int = 300  # 5 minutes

# Logging Configuration
LOG_EMOJI_LOADING: str = "📥"
LOG_EMOJI_PROCESSING: str = "📊"
LOG_EMOJI_SUCCESS: str = "✅"
LOG_EMOJI_ERROR: str = "❌"
LOG_EMOJI_WARNING: str = "⚠️"
