"""
Unit tests for sidebar UI component.

Tests the sidebar rendering functions including file selection,
status display, and metadata rendering.
"""

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quickbooks_autoreport.dashboard.sidebar import (
    _render_file_selector,
    _render_status_section,
    render_file_metadata,
)


class TestRenderFileSelector:
    """Tests for _render_file_selector function."""

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_no_files_available(self, mock_st):
        """Test file selector with empty file list."""
        # Arrange
        available_files = []
        current_file = None

        # Act
        result = _render_file_selector(available_files, current_file)

        # Assert
        assert result is None
        mock_st.warning.assert_called_once()
        mock_st.info.assert_called_once()

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_single_file_available(self, mock_st):
        """Test file selector with one file."""
        # Arrange
        file1 = Path("output/sales_data.xlsx")
        available_files = [file1]
        current_file = None

        mock_st.selectbox.return_value = "sales_data.xlsx"

        # Act
        result = _render_file_selector(available_files, current_file)

        # Assert
        assert result == file1
        mock_st.selectbox.assert_called_once()
        call_args = mock_st.selectbox.call_args
        assert call_args[1]['options'] == ["sales_data.xlsx"]
        assert call_args[1]['index'] == 0

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_multiple_files_with_current_selection(self, mock_st):
        """Test file selector with multiple files and current selection."""
        # Arrange
        file1 = Path("output/sales_jan.xlsx")
        file2 = Path("output/sales_feb.xlsx")
        file3 = Path("output/sales_mar.xlsx")
        available_files = [file1, file2, file3]
        current_file = file2

        mock_st.selectbox.return_value = "sales_feb.xlsx"

        # Act
        result = _render_file_selector(available_files, current_file)

        # Assert
        assert result == file2
        call_args = mock_st.selectbox.call_args
        assert call_args[1]['index'] == 1  # file2 is at index 1

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_file_selection_change(self, mock_st):
        """Test changing file selection."""
        # Arrange
        file1 = Path("output/sales_jan.xlsx")
        file2 = Path("output/sales_feb.xlsx")
        available_files = [file1, file2]
        current_file = file1

        # User selects file2
        mock_st.selectbox.return_value = "sales_feb.xlsx"

        # Act
        result = _render_file_selector(available_files, current_file)

        # Assert
        assert result == file2


class TestRenderStatusSection:
    """Tests for _render_status_section function."""

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_with_update_and_file(self, mock_st):
        """Test status section with update timestamp and file."""
        # Arrange
        current_file = Path("output/sales_data.xlsx")
        last_update = datetime(2025, 10, 8, 17, 0, 4)

        # Act
        _render_status_section(current_file, last_update)

        # Assert
        mock_st.metric.assert_called_once()
        call_args = mock_st.metric.call_args
        assert call_args[1]['label'] == "Latest Update"
        assert "2025-10-08 17:00:04" in call_args[1]['value']

        # Check file display
        assert mock_st.text.call_count == 1
        mock_st.code.assert_called()

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_without_update(self, mock_st):
        """Test status section without update timestamp."""
        # Arrange
        current_file = Path("output/sales_data.xlsx")
        last_update = None

        # Act
        _render_status_section(current_file, last_update)

        # Assert
        mock_st.info.assert_called_once_with("No data loaded yet")

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_without_file(self, mock_st):
        """Test status section without selected file."""
        # Arrange
        current_file = None
        last_update = datetime(2025, 10, 8, 17, 0, 4)

        # Act
        _render_status_section(current_file, last_update)

        # Assert
        # Should show "None selected" in code block
        code_calls = [call[0][0] for call in mock_st.code.call_args_list]
        assert "None selected" in code_calls


class TestRenderFileMetadata:
    """Tests for render_file_metadata function."""

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_file_not_found(self, mock_st):
        """Test metadata rendering for non-existent file."""
        # Arrange
        filepath = Path("output/nonexistent.xlsx")

        # Act
        render_file_metadata(filepath)

        # Assert
        mock_st.warning.assert_called_once()

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_file_metadata_display(self, mock_st, tmp_path):
        """Test metadata rendering for existing file."""
        # Arrange
        test_file = tmp_path / "test_sales.xlsx"
        test_file.write_text("test data")

        # Act
        render_file_metadata(test_file)

        # Assert
        mock_st.subheader.assert_called_once_with("📄 File Information")
        assert mock_st.metric.call_count == 2  # Size and modified time

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_file_size_formatting_kb(self, mock_st, tmp_path):
        """Test file size formatting for small files (KB)."""
        # Arrange
        test_file = tmp_path / "small_file.xlsx"
        test_file.write_bytes(b"x" * 512)  # 512 bytes

        # Act
        render_file_metadata(test_file)

        # Assert
        size_call = [
            call for call in mock_st.metric.call_args_list
            if call[1]['label'] == "File Size"
        ][0]
        assert "KB" in size_call[1]['value']

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_file_size_formatting_mb(self, mock_st, tmp_path):
        """Test file size formatting for large files (MB)."""
        # Arrange
        test_file = tmp_path / "large_file.xlsx"
        test_file.write_bytes(b"x" * (2 * 1024 * 1024))  # 2 MB

        # Act
        render_file_metadata(test_file)

        # Assert
        size_call = [
            call for call in mock_st.metric.call_args_list
            if call[1]['label'] == "File Size"
        ][0]
        assert "MB" in size_call[1]['value']

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_show_size_only(self, mock_st, tmp_path):
        """Test showing only file size."""
        # Arrange
        test_file = tmp_path / "test_file.xlsx"
        test_file.write_text("test")

        # Act
        render_file_metadata(test_file, show_size=True, show_modified=False)

        # Assert
        assert mock_st.metric.call_count == 1
        call_args = mock_st.metric.call_args
        assert call_args[1]['label'] == "File Size"

    @patch('quickbooks_autoreport.dashboard.sidebar.st')
    def test_show_modified_only(self, mock_st, tmp_path):
        """Test showing only last modified time."""
        # Arrange
        test_file = tmp_path / "test_file.xlsx"
        test_file.write_text("test")

        # Act
        render_file_metadata(test_file, show_size=False, show_modified=True)

        # Assert
        assert mock_st.metric.call_count == 1
        call_args = mock_st.metric.call_args
        assert call_args[1]['label'] == "Last Modified"
