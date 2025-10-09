"""
Unit tests for dashboard utility functions.

Tests formatting utilities for currency, numbers, dates, error messages,
and logging setup.
"""

import logging
from datetime import datetime

from src.quickbooks_autoreport.dashboard.utils import (
    format_currency,
    format_date_range,
    format_datetime,
    format_empty_directory_message,
    format_error_message,
    format_file_not_found_message,
    format_missing_columns_message,
    format_number,
    format_timestamp,
    format_units,
    log_error,
    log_loading,
    log_processing,
    log_success,
    log_warning,
    setup_logger,
)


# ============================================================================
# Currency and Number Formatting Tests
# ============================================================================


class TestCurrencyFormatting:
    """Tests for currency formatting functions."""

    def test_format_currency_basic(self):
        """Test basic currency formatting."""
        assert format_currency(1234.56) == "$1,234.56"

    def test_format_currency_large_value(self):
        """Test currency formatting with large values."""
        assert format_currency(1000000) == "$1,000,000.00"

    def test_format_currency_small_value(self):
        """Test currency formatting with small values."""
        assert format_currency(0.99) == "$0.99"

    def test_format_currency_zero(self):
        """Test currency formatting with zero."""
        assert format_currency(0) == "$0.00"

    def test_format_currency_negative(self):
        """Test currency formatting with negative values."""
        assert format_currency(-1234.56) == "$-1,234.56"

    def test_format_currency_custom_symbol(self):
        """Test currency formatting with custom symbol."""
        assert format_currency(1234.56, symbol="€") == "€1,234.56"


class TestNumberFormatting:
    """Tests for number formatting functions."""

    def test_format_number_integer(self):
        """Test number formatting with integers."""
        assert format_number(1234) == "1,234"

    def test_format_number_with_decimals(self):
        """Test number formatting with decimal places."""
        assert format_number(1234.567, decimals=2) == "1,234.57"

    def test_format_number_large_value(self):
        """Test number formatting with large values."""
        assert format_number(1000000) == "1,000,000"

    def test_format_number_zero(self):
        """Test number formatting with zero."""
        assert format_number(0) == "0"

    def test_format_number_rounding(self):
        """Test number formatting rounds correctly."""
        assert format_number(1234.999, decimals=2) == "1,235.00"

    def test_format_units(self):
        """Test units formatting."""
        assert format_units(1234.5) == "1,234"
        assert format_units(1000000) == "1,000,000"


# ============================================================================
# Date and Time Formatting Tests
# ============================================================================


class TestDateTimeFormatting:
    """Tests for date and time formatting functions."""

    def test_format_datetime_default(self):
        """Test datetime formatting with default format."""
        dt = datetime(2025, 10, 8, 17, 0, 4)
        assert format_datetime(dt) == "2025-10-08 17:00:04"

    def test_format_datetime_custom_format(self):
        """Test datetime formatting with custom format."""
        dt = datetime(2025, 10, 8, 17, 0, 4)
        assert format_datetime(dt, fmt="%Y-%m-%d") == "2025-10-08"

    def test_format_timestamp_with_datetime(self):
        """Test timestamp formatting with provided datetime."""
        dt = datetime(2025, 10, 8, 17, 0, 4)
        assert format_timestamp(dt) == "2025-10-08 17:00:04"

    def test_format_timestamp_current_time(self):
        """Test timestamp formatting with current time."""
        result = format_timestamp()
        # Just verify it returns a string in the expected format
        assert len(result) == 19  # "YYYY-MM-DD HH:MM:SS"
        assert result[4] == "-"
        assert result[7] == "-"
        assert result[10] == " "
        assert result[13] == ":"
        assert result[16] == ":"

    def test_format_date_range(self):
        """Test date range formatting."""
        start = datetime(2025, 10, 1)
        end = datetime(2025, 10, 7)
        assert format_date_range(start, end) == "2025-10-01 to 2025-10-07"

    def test_format_date_range_same_day(self):
        """Test date range formatting with same start and end."""
        dt = datetime(2025, 10, 8)
        assert format_date_range(dt, dt) == "2025-10-08 to 2025-10-08"


# ============================================================================
# Error Message Formatting Tests
# ============================================================================


class TestErrorMessageFormatting:
    """Tests for error message formatting functions."""

    def test_format_error_message_with_context(self):
        """Test error message formatting with context."""
        error = ValueError("Invalid data")
        result = format_error_message(error, "loading file.xlsx")
        assert result == "Error loading file.xlsx: Invalid data"

    def test_format_error_message_without_context(self):
        """Test error message formatting without context."""
        error = ValueError("Invalid data")
        result = format_error_message(error)
        assert result == "ValueError: Invalid data"

    def test_format_error_message_different_exception_types(self):
        """Test error message formatting with different exception types."""
        error = FileNotFoundError("File not found")
        result = format_error_message(error)
        assert result == "FileNotFoundError: File not found"

    def test_format_missing_columns_message_single(self):
        """Test missing columns message with single column."""
        result = format_missing_columns_message(["Sales_Qty"])
        assert result == "Required columns missing: Sales_Qty"

    def test_format_missing_columns_message_multiple(self):
        """Test missing columns message with multiple columns."""
        result = format_missing_columns_message(["Sales_Qty", "Transaction_Total"])
        assert result == "Required columns missing: Sales_Qty, Transaction_Total"

    def test_format_file_not_found_message(self):
        """Test file not found message formatting."""
        result = format_file_not_found_message("output/sales.xlsx")
        assert result == "File not found: output/sales.xlsx"

    def test_format_empty_directory_message(self):
        """Test empty directory message formatting."""
        result = format_empty_directory_message("output")
        assert "No Excel files found in 'output' folder" in result
        assert "Please add .xlsx files to analyze" in result


# ============================================================================
# Logging Setup Tests
# ============================================================================


class TestLoggingSetup:
    """Tests for logging setup and helper functions."""

    def test_setup_logger_basic(self):
        """Test basic logger setup."""
        logger = setup_logger("test_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0

    def test_setup_logger_custom_level(self):
        """Test logger setup with custom level."""
        logger = setup_logger("test_logger_debug", level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_setup_logger_idempotent(self):
        """Test that calling setup_logger multiple times doesn't add handlers."""
        logger_name = "test_logger_idempotent"
        logger1 = setup_logger(logger_name)
        handler_count = len(logger1.handlers)

        logger2 = setup_logger(logger_name)
        assert len(logger2.handlers) == handler_count

    def test_log_loading(self, caplog):
        """Test loading log message."""
        logger = setup_logger("test_loading")
        with caplog.at_level(logging.INFO):
            log_loading(logger, "Loading file: sales.xlsx")

        assert "📥" in caplog.text
        assert "Loading file: sales.xlsx" in caplog.text

    def test_log_processing(self, caplog):
        """Test processing log message."""
        logger = setup_logger("test_processing")
        with caplog.at_level(logging.INFO):
            log_processing(logger, "Calculating metrics...")

        assert "📊" in caplog.text
        assert "Calculating metrics..." in caplog.text

    def test_log_success(self, caplog):
        """Test success log message."""
        logger = setup_logger("test_success")
        with caplog.at_level(logging.INFO):
            log_success(logger, "Dashboard updated successfully")

        assert "✅" in caplog.text
        assert "Dashboard updated successfully" in caplog.text

    def test_log_error(self, caplog):
        """Test error log message."""
        logger = setup_logger("test_error")
        with caplog.at_level(logging.ERROR):
            log_error(logger, "Failed to load file")

        assert "❌" in caplog.text
        assert "Failed to load file" in caplog.text

    def test_log_warning(self, caplog):
        """Test warning log message."""
        logger = setup_logger("test_warning")
        with caplog.at_level(logging.WARNING):
            log_warning(logger, "File modification detected")

        assert "⚠️" in caplog.text
        assert "File modification detected" in caplog.text


# ============================================================================
# Integration Tests
# ============================================================================


class TestUtilsIntegration:
    """Integration tests for utility functions."""

    def test_format_error_with_missing_columns(self):
        """Test formatting error message for missing columns scenario."""
        missing = ["Sales_Qty", "Transaction_Total"]
        error_msg = format_missing_columns_message(missing)

        assert "Sales_Qty" in error_msg
        assert "Transaction_Total" in error_msg
        assert "Required columns missing" in error_msg

    def test_logging_workflow(self, caplog):
        """Test complete logging workflow."""
        logger = setup_logger("test_workflow")

        with caplog.at_level(logging.INFO):
            log_loading(logger, "Starting data load")
            log_processing(logger, "Processing data")
            log_success(logger, "Completed successfully")

        assert "📥" in caplog.text
        assert "📊" in caplog.text
        assert "✅" in caplog.text

    def test_currency_and_units_formatting_together(self):
        """Test using currency and units formatting together."""
        revenue = 12345.67
        units = 1234.5

        revenue_str = format_currency(revenue)
        units_str = format_units(units)

        assert revenue_str == "$12,345.67"
        assert units_str == "1,234"
