"""
Utility functions for the sales dashboard.

This module provides formatting utilities for currency, numbers, dates,
error messages, and logging setup with emoji indicators.
"""

import logging
from datetime import datetime
from typing import Optional

from .config import (
    CURRENCY_SYMBOL,
    DATE_FORMAT,
    LOG_EMOJI_ERROR,
    LOG_EMOJI_LOADING,
    LOG_EMOJI_PROCESSING,
    LOG_EMOJI_SUCCESS,
    LOG_EMOJI_WARNING,
)


# ============================================================================
# Currency and Number Formatting
# ============================================================================


def format_currency(value: float, symbol: str = CURRENCY_SYMBOL) -> str:
    """
    Format a numeric value as currency with symbol and thousand separators.

    Args:
        value: The numeric value to format
        symbol: Currency symbol to use (default: $)

    Returns:
        Formatted currency string (e.g., "$1,234.56")

    Examples:
        >>> format_currency(1234.56)
        '$1,234.56'
        >>> format_currency(1000000)
        '$1,000,000.00'
    """
    return f"{symbol}{value:,.2f}"


def format_number(value: float, decimals: int = 0) -> str:
    """
    Format a numeric value with thousand separators.

    Args:
        value: The numeric value to format
        decimals: Number of decimal places (default: 0)

    Returns:
        Formatted number string (e.g., "1,234" or "1,234.56")

    Examples:
        >>> format_number(1234)
        '1,234'
        >>> format_number(1234.567, decimals=2)
        '1,234.57'
    """
    if decimals == 0:
        return f"{int(value):,}"
    return f"{value:,.{decimals}f}"


def format_units(value: float) -> str:
    """
    Format units sold as whole numbers with thousand separators.

    Args:
        value: The numeric value representing units

    Returns:
        Formatted units string (e.g., "1,234")

    Examples:
        >>> format_units(1234.5)
        '1,234'
        >>> format_units(1000000)
        '1,000,000'
    """
    return format_number(value, decimals=0)


# ============================================================================
# Date and Time Formatting
# ============================================================================


def format_datetime(dt: datetime, fmt: str = DATE_FORMAT) -> str:
    """
    Format a datetime object as a string.

    Args:
        dt: The datetime object to format
        fmt: Format string (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        Formatted datetime string

    Examples:
        >>> dt = datetime(2025, 10, 8, 17, 0, 4)
        >>> format_datetime(dt)
        '2025-10-08 17:00:04'
    """
    return dt.strftime(fmt)


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """
    Format a timestamp for display. Uses current time if not provided.

    Args:
        timestamp: Optional datetime object (default: current time)

    Returns:
        Formatted timestamp string

    Examples:
        >>> format_timestamp()  # doctest: +SKIP
        '2025-10-08 17:00:04'
    """
    if timestamp is None:
        timestamp = datetime.now()
    return format_datetime(timestamp)


def format_date_range(start_date: datetime, end_date: datetime) -> str:
    """
    Format a date range for display.

    Args:
        start_date: Start date of the range
        end_date: End date of the range

    Returns:
        Formatted date range string

    Examples:
        >>> start = datetime(2025, 10, 1)
        >>> end = datetime(2025, 10, 7)
        >>> format_date_range(start, end)
        '2025-10-01 to 2025-10-07'
    """
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    return f"{start_str} to {end_str}"


# ============================================================================
# Error Message Formatting
# ============================================================================


def format_error_message(error: Exception, context: str = "") -> str:
    """
    Format an error message with optional context.

    Args:
        error: The exception object
        context: Optional context string (e.g., filename, operation)

    Returns:
        Formatted error message

    Examples:
        >>> err = ValueError("Invalid data")
        >>> format_error_message(err, "loading file.xlsx")
        'Error loading file.xlsx: Invalid data'
    """
    error_type = type(error).__name__
    error_msg = str(error)

    if context:
        return f"Error {context}: {error_msg}"
    return f"{error_type}: {error_msg}"


def format_missing_columns_message(missing_columns: list[str]) -> str:
    """
    Format a message for missing required columns.

    Args:
        missing_columns: List of missing column names

    Returns:
        Formatted error message

    Examples:
        >>> format_missing_columns_message(['Sales_Qty', 'Transaction_Total'])
        'Required columns missing: Sales_Qty, Transaction_Total'
    """
    columns_str = ", ".join(missing_columns)
    return f"Required columns missing: {columns_str}"


def format_file_not_found_message(filepath: str) -> str:
    """
    Format a message for file not found errors.

    Args:
        filepath: Path to the file that was not found

    Returns:
        Formatted error message

    Examples:
        >>> format_file_not_found_message('output/sales.xlsx')
        'File not found: output/sales.xlsx'
    """
    return f"File not found: {filepath}"


def format_empty_directory_message(directory: str) -> str:
    """
    Format a message for empty directory scenarios.

    Args:
        directory: Path to the empty directory

    Returns:
        Formatted message with instructions

    Examples:
        >>> format_empty_directory_message('output')
        "No Excel files found in 'output' folder. ..."
    """
    return (
        f"No Excel files found in '{directory}' folder. "
        "Please add .xlsx files to analyze."
    )


# ============================================================================
# Logging Setup
# ============================================================================


def setup_logger(
    name: str,
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with emoji indicators and consistent formatting.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: INFO)
        format_string: Optional custom format string

    Returns:
        Configured logger instance

    Examples:
        >>> logger = setup_logger(__name__)
        >>> logger.info(f"{LOG_EMOJI_LOADING} ...")  # doctest: +SKIP
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers if logger already configured
    if logger.handlers:
        return logger

    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(level)

    # Create formatter
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


def log_loading(logger: logging.Logger, message: str) -> None:
    """
    Log a loading message with emoji indicator.

    Args:
        logger: Logger instance
        message: Message to log

    Examples:
        >>> logger = setup_logger(__name__)
        >>> log_loading(logger, "Loading file")  # doctest: +SKIP
    """
    logger.info(f"{LOG_EMOJI_LOADING} {message}")


def log_processing(logger: logging.Logger, message: str) -> None:
    """
    Log a processing message with emoji indicator.

    Args:
        logger: Logger instance
        message: Message to log

    Examples:
        >>> logger = setup_logger(__name__)
        >>> log_processing(logger, "Calculating metrics...")  # doctest: +SKIP
    """
    logger.info(f"{LOG_EMOJI_PROCESSING} {message}")


def log_success(logger: logging.Logger, message: str) -> None:
    """
    Log a success message with emoji indicator.

    Args:
        logger: Logger instance
        message: Message to log

    Examples:
        >>> logger = setup_logger(__name__)
        >>> log_success(logger, "Dashboard updated")  # doctest: +SKIP
    """
    logger.info(f"{LOG_EMOJI_SUCCESS} {message}")


def log_error(logger: logging.Logger, message: str) -> None:
    """
    Log an error message with emoji indicator.

    Args:
        logger: Logger instance
        message: Message to log

    Examples:
        >>> logger = setup_logger(__name__)
        >>> log_error(logger, "Failed to load file")  # doctest: +SKIP
    """
    logger.error(f"{LOG_EMOJI_ERROR} {message}")


def log_warning(logger: logging.Logger, message: str) -> None:
    """
    Log a warning message with emoji indicator.

    Args:
        logger: Logger instance
        message: Message to log

    Examples:
        >>> logger = setup_logger(__name__)
        >>> log_warning(logger, "File modification detected")  # doctest: +SKIP
    """
    logger.warning(f"{LOG_EMOJI_WARNING} {message}")
