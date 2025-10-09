"""
Integration tests for error handling and user feedback.

Tests comprehensive error handling across the dashboard application
to verify all requirements from task 10 are met.
"""

import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from quickbooks_autoreport.dashboard.data_loader import (
    ExcelLoader,
    FileScanner,
)
from quickbooks_autoreport.dashboard.utils import (
    format_empty_directory_message,
    format_error_message,
    format_file_not_found_message,
    format_missing_columns_message,
    log_error,
    setup_logger,
)
from quickbooks_autoreport.domain.sales_data import SalesData


class TestFileOperationErrorHandling:
    """Test error handling for file operations (Requirement 9.1)."""

    def test_file_not_found_error_handling(self):
        """Test handling of file not found errors."""
        loader = ExcelLoader()
        nonexistent_file = Path("/nonexistent/file.xlsx")

        with pytest.raises(FileNotFoundError):
            loader.load_file(nonexistent_file)

    def test_corrupted_file_error_handling(self, tmp_path):
        """Test handling of corrupted file errors."""
        loader = ExcelLoader()
        corrupted_file = tmp_path / "corrupted.xlsx"

        # Create a text file with .xlsx extension
        with open(corrupted_file, "w") as f:
            f.write("This is not a valid Excel file")

        with pytest.raises(ValueError, match="Failed to read Excel file"):
            loader.load_file(corrupted_file)

    def test_empty_file_error_handling(self, tmp_path):
        """Test handling of empty file errors."""
        loader = ExcelLoader()
        empty_file = tmp_path / "empty.xlsx"

        # Create empty Excel file
        empty_df = pd.DataFrame()
        empty_df.to_excel(empty_file, index=False)

        with pytest.raises(ValueError, match="empty"):
            loader.load_file(empty_file)


class TestColumnValidationErrorHandling:
    """Test error handling for column validation (Requirement 9.2)."""

    def test_missing_columns_error_message(self):
        """Test that missing columns are listed in error message."""
        missing = ["Sales_Qty", "Transaction_Total", "Sales_Amount"]
        message = format_missing_columns_message(missing)

        assert "Sales_Qty" in message
        assert "Transaction_Total" in message
        assert "Sales_Amount" in message
        assert "Required columns missing" in message

    def test_missing_columns_validation(self):
        """Test validation fails with missing columns."""
        loader = ExcelLoader()
        df = pd.DataFrame({"Other_Column": [1, 2, 3]})

        is_valid, missing = loader.validate_columns(df)

        assert not is_valid
        assert len(missing) > 0
        assert "Transaction_Total" in missing

    def test_sales_data_from_file_missing_columns(self):
        """Test SalesData.from_file raises error with missing columns."""
        loader = MagicMock()
        loader.load_file.return_value = pd.DataFrame({"Other": [1, 2]})
        loader.validate_columns.return_value = (
            False,
            ["Transaction_Total", "Sales_Qty"],
        )

        filepath = Path("test.xlsx")

        with pytest.raises(ValueError, match="Required columns missing"):
            SalesData.from_file(filepath, loader)


class TestLoadingIndicators:
    """Test loading indicators during data processing (Requirement 9.3)."""

    def test_loading_indicator_logged(self, caplog):
        """Test that loading operations are logged."""
        logger = setup_logger("test_loading")
        
        with caplog.at_level(logging.INFO):
            logger.info("📥 Loading file: test.xlsx")

        # Verify logging was called
        assert "Loading file: test.xlsx" in caplog.text
        assert logger.level == logging.INFO

    def test_log_loading_function(self, caplog):
        """Test log_loading utility function."""
        from quickbooks_autoreport.dashboard.utils import log_loading

        logger = setup_logger("test_loading")

        with caplog.at_level(logging.INFO):
            log_loading(logger, "Loading test file")

        assert "Loading test file" in caplog.text
        assert "📥" in caplog.text


class TestEmptyDirectoryHandling:
    """Test empty directory case handling (Requirement 9.4)."""

    def test_empty_directory_message_format(self):
        """Test empty directory message provides instructions."""
        message = format_empty_directory_message("output")

        assert "No Excel files found" in message
        assert "output" in message
        assert "add" in message.lower() or "please" in message.lower()

    def test_file_scanner_empty_directory(self, tmp_path):
        """Test FileScanner with empty directory."""
        scanner = FileScanner(directory=tmp_path)
        files = scanner.list_excel_files()

        assert len(files) == 0


class TestErrorLogging:
    """Test error logging for debugging (Requirement 9.5)."""

    def test_log_error_function(self, caplog):
        """Test log_error utility function."""
        logger = setup_logger("test_error")

        with caplog.at_level(logging.ERROR):
            log_error(logger, "Test error message")

        assert "Test error message" in caplog.text
        assert "❌" in caplog.text

    def test_error_message_formatting(self):
        """Test error message formatting utility."""
        error = ValueError("Invalid data format")
        message = format_error_message(error, "processing data")

        assert "Invalid data format" in message
        assert "processing data" in message

    def test_file_not_found_message_formatting(self):
        """Test file not found message formatting."""
        message = format_file_not_found_message("output/sales.xlsx")

        assert "File not found" in message
        assert "output/sales.xlsx" in message


class TestUserFriendlyErrorMessages:
    """Test user-friendly error messages with st.error."""

    def test_error_message_includes_context(self):
        """Test error messages include helpful context."""
        error = FileNotFoundError("test.xlsx")
        message = format_error_message(error, "loading file")

        # Should include both the error and context
        assert "loading file" in message
        assert "test.xlsx" in message

    def test_error_message_without_technical_jargon(self):
        """Test error messages are user-friendly."""
        missing_cols = ["Sales_Qty", "Transaction_Total"]
        message = format_missing_columns_message(missing_cols)

        # Should be clear and direct
        assert "Required columns missing" in message
        # Should list the specific columns
        assert "Sales_Qty" in message
        assert "Transaction_Total" in message


class TestTryCatchBlocks:
    """Test try-catch blocks around file operations."""

    def test_file_scanner_handles_exceptions(self):
        """Test FileScanner handles exceptions gracefully."""
        scanner = FileScanner(directory=Path("/nonexistent"))

        with pytest.raises(FileNotFoundError):
            scanner.list_excel_files()

    def test_excel_loader_handles_exceptions(self):
        """Test ExcelLoader handles exceptions gracefully."""
        loader = ExcelLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_file(Path("/nonexistent/file.xlsx"))

    def test_weekday_column_handles_exceptions(self):
        """Test add_weekday_column handles exceptions."""
        loader = ExcelLoader()
        df = pd.DataFrame({"Other": [1, 2, 3]})

        with pytest.raises(ValueError, match="not found"):
            loader.add_weekday_column(df, date_column="Date")


class TestErrorRecovery:
    """Test that errors don't crash the application."""

    def test_polling_error_doesnt_crash(self):
        """Test that polling errors are handled gracefully."""
        from quickbooks_autoreport.domain.sales_data import DashboardState

        state = DashboardState()
        file_scanner = MagicMock()
        file_scanner.get_file_modified_time.side_effect = Exception(
            "Test error"
        )

        # Should return False instead of crashing
        result = state.should_reload(file_scanner)
        assert result is False

    def test_missing_file_during_reload(self):
        """Test handling of missing file during reload."""
        from quickbooks_autoreport.domain.sales_data import DashboardState

        state = DashboardState(current_file=Path("test.xlsx"))
        file_scanner = MagicMock()
        file_scanner.file_exists.return_value = False

        # Should return False instead of crashing
        result = state.should_reload(file_scanner)
        assert result is False


class TestComprehensiveErrorScenarios:
    """Test comprehensive error scenarios end-to-end."""

    def test_complete_error_flow_missing_columns(self, tmp_path):
        """Test complete error flow for missing columns."""
        # Create file with wrong columns
        test_file = tmp_path / "test.xlsx"
        df = pd.DataFrame({"Wrong_Column": [1, 2, 3]})
        df.to_excel(test_file, index=False)

        loader = ExcelLoader()

        # Load file (should succeed)
        loaded_df = loader.load_file(test_file)
        assert loaded_df is not None

        # Validate columns (should fail)
        is_valid, missing = loader.validate_columns(loaded_df)
        assert not is_valid
        assert len(missing) > 0

        # Format error message
        error_msg = format_missing_columns_message(missing)
        assert "Required columns missing" in error_msg

    def test_complete_error_flow_file_not_found(self):
        """Test complete error flow for file not found."""
        nonexistent = Path("/nonexistent/file.xlsx")
        loader = ExcelLoader()

        # Should raise FileNotFoundError
        with pytest.raises(FileNotFoundError):
            loader.load_file(nonexistent)

        # Format error message
        error_msg = format_file_not_found_message(str(nonexistent))
        assert "File not found" in error_msg
        assert str(nonexistent) in error_msg
