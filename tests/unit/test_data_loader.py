"""
Unit tests for dashboard data loader module.

Tests FileScanner and ExcelLoader classes with various scenarios
including empty directories, valid/invalid files, and data validation.
"""

import sys
import tempfile
import time
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

# Mock pythoncom and win32com before importing from quickbooks_autoreport
# This allows testing dashboard modules without QuickBooks dependencies
sys.modules['pythoncom'] = MagicMock()
sys.modules['win32com'] = MagicMock()
sys.modules['win32com.client'] = MagicMock()
sys.modules['pywintypes'] = MagicMock()

# Add src directory to path
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Now we can safely import dashboard modules
from quickbooks_autoreport.dashboard.data_loader import (  # noqa: E402
    ExcelLoader,
    FileScanner,
)


class TestFileScanner(unittest.TestCase):
    """Test suite for FileScanner class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        self.scanner = FileScanner(directory=self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir_obj.cleanup()

    def test_init_with_default_directory(self):
        """Test FileScanner initialization with default directory."""
        scanner = FileScanner()
        self.assertEqual(scanner.directory, Path("output"))

    def test_init_with_custom_directory(self):
        """Test FileScanner initialization with custom directory."""
        scanner = FileScanner(directory=self.temp_dir)
        self.assertEqual(scanner.directory, self.temp_dir)

    def test_list_excel_files_empty_directory(self):
        """Test listing files in empty directory returns empty list."""
        files = self.scanner.list_excel_files()
        self.assertEqual(files, [])
        self.assertIsInstance(files, list)

    def test_list_excel_files_single_file(self):
        """Test listing files with single Excel file."""
        # Create a single Excel file
        test_file = self.temp_dir / "test_sales.xlsx"
        df = pd.DataFrame({"A": [1, 2, 3]})
        df.to_excel(test_file, index=False)

        files = self.scanner.list_excel_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "test_sales.xlsx")
        self.assertTrue(files[0].exists())

    def test_list_excel_files_multiple_files(self):
        """Test listing files with multiple Excel files."""
        # Create multiple Excel files
        file_names = ["sales_1.xlsx", "sales_2.xlsx", "sales_3.xlsx"]
        for name in file_names:
            test_file = self.temp_dir / name
            df = pd.DataFrame({"A": [1, 2, 3]})
            df.to_excel(test_file, index=False)

        files = self.scanner.list_excel_files()
        self.assertEqual(len(files), 3)
        self.assertTrue(all(f.suffix == ".xlsx" for f in files))
        self.assertEqual(set(f.name for f in files), set(file_names))

    def test_list_excel_files_sorted_by_modification_time(self):
        """Test files sorted by modification time (newest first)."""
        # Create files with different modification times
        file1 = self.temp_dir / "old_file.xlsx"
        df = pd.DataFrame({"A": [1]})
        df.to_excel(file1, index=False)

        time.sleep(0.1)  # Ensure different timestamps

        file2 = self.temp_dir / "new_file.xlsx"
        df.to_excel(file2, index=False)

        files = self.scanner.list_excel_files()
        self.assertEqual(len(files), 2)
        # Newest file should be first
        self.assertEqual(files[0].name, "new_file.xlsx")
        self.assertEqual(files[1].name, "old_file.xlsx")

    def test_list_excel_files_filters_temp_files(self):
        """Test temporary Excel files (starting with ~$) filtered."""
        # Create regular and temporary files
        regular_file = self.temp_dir / "sales.xlsx"
        temp_file = self.temp_dir / "~$sales.xlsx"

        df = pd.DataFrame({"A": [1]})
        df.to_excel(regular_file, index=False)
        df.to_excel(temp_file, index=False)

        files = self.scanner.list_excel_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "sales.xlsx")

    def test_list_excel_files_ignores_non_excel_files(self):
        """Test that non-Excel files are ignored."""
        # Create Excel and non-Excel files
        excel_file = self.temp_dir / "sales.xlsx"
        csv_file = self.temp_dir / "data.csv"
        txt_file = self.temp_dir / "readme.txt"

        df = pd.DataFrame({"A": [1]})
        df.to_excel(excel_file, index=False)
        df.to_csv(csv_file, index=False)
        txt_file.write_text("test")

        files = self.scanner.list_excel_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "sales.xlsx")

    def test_list_excel_files_nonexistent_directory(self):
        """Test that FileNotFoundError is raised for nonexistent directory."""
        nonexistent_dir = Path("/nonexistent/directory/path")
        scanner = FileScanner(directory=nonexistent_dir)

        with self.assertRaises(FileNotFoundError) as context:
            scanner.list_excel_files()
        self.assertIn("Directory not found", str(context.exception))

    def test_list_excel_files_path_is_file_not_directory(self):
        """Test NotADirectoryError raised when path is a file."""
        # Create a file instead of directory
        file_path = self.temp_dir / "not_a_directory.txt"
        file_path.write_text("test")

        scanner = FileScanner(directory=file_path)

        with self.assertRaises(NotADirectoryError) as context:
            scanner.list_excel_files()
        self.assertIn("Path is not a directory", str(context.exception))

    def test_get_file_modified_time(self):
        """Test getting file modification time."""
        test_file = self.temp_dir / "test.xlsx"
        df = pd.DataFrame({"A": [1]})
        df.to_excel(test_file, index=False)

        modified_time = self.scanner.get_file_modified_time(test_file)

        self.assertIsInstance(modified_time, datetime)
        # Check that time is recent (within last minute)
        time_diff = datetime.now() - modified_time
        self.assertLess(time_diff.total_seconds(), 60)

    def test_get_file_modified_time_nonexistent_file(self):
        """Test FileNotFoundError raised for nonexistent file."""
        nonexistent_file = self.temp_dir / "nonexistent.xlsx"

        with self.assertRaises(FileNotFoundError) as context:
            self.scanner.get_file_modified_time(nonexistent_file)
        self.assertIn("File not found", str(context.exception))

    def test_file_exists_returns_true_for_existing_file(self):
        """Test file_exists returns True for existing file."""
        test_file = self.temp_dir / "test.xlsx"
        df = pd.DataFrame({"A": [1]})
        df.to_excel(test_file, index=False)

        self.assertTrue(self.scanner.file_exists(test_file))

    def test_file_exists_returns_false_for_nonexistent_file(self):
        """Test file_exists returns False for nonexistent file."""
        nonexistent_file = self.temp_dir / "nonexistent.xlsx"
        self.assertFalse(self.scanner.file_exists(nonexistent_file))

    def test_file_exists_returns_false_for_directory(self):
        """Test file_exists returns False for directory path."""
        subdir = self.temp_dir / "subdir"
        subdir.mkdir()

        self.assertFalse(self.scanner.file_exists(subdir))


class TestExcelLoader(unittest.TestCase):
    """Test suite for ExcelLoader class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        self.loader = ExcelLoader()
        self.sample_valid_data = pd.DataFrame({
            'Transaction_Total': [100.0, 200.0, 150.0],
            'Sales_Amount': [90.0, 180.0, 135.0],
            'Sales_Qty': [10, 20, 15],
            'Product': ['Product A', 'Product B', 'Product C'],
            'Date': ['2025-10-06', '2025-10-07', '2025-10-08']
        })

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir_obj.cleanup()

    def test_init_with_default_columns(self):
        """Test ExcelLoader initialization with default columns."""
        loader = ExcelLoader()
        self.assertIn('Transaction_Total', loader.required_columns)
        self.assertIn('Sales_Amount', loader.required_columns)
        self.assertIn('Sales_Qty', loader.required_columns)

    def test_init_with_custom_columns(self):
        """Test ExcelLoader initialization with custom columns."""
        custom_columns = ['Column1', 'Column2']
        loader = ExcelLoader(required_columns=custom_columns)
        self.assertEqual(loader.required_columns, custom_columns)

    def test_load_file_valid_data(self):
        """Test loading valid Excel file."""
        test_file = self.temp_dir / "valid_sales.xlsx"
        self.sample_valid_data.to_excel(test_file, index=False)

        df = self.loader.load_file(test_file)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertEqual(list(df.columns), list(self.sample_valid_data.columns))

    def test_load_file_nonexistent_file(self):
        """Test FileNotFoundError raised for nonexistent file."""
        nonexistent_file = self.temp_dir / "nonexistent.xlsx"

        with self.assertRaises(FileNotFoundError) as context:
            self.loader.load_file(nonexistent_file)
        self.assertIn("File not found", str(context.exception))

    def test_load_file_empty_excel(self):
        """Test ValueError raised for empty Excel file."""
        empty_file = self.temp_dir / "empty.xlsx"
        empty_df = pd.DataFrame()
        empty_df.to_excel(empty_file, index=False)

        with self.assertRaises(ValueError) as context:
            self.loader.load_file(empty_file)
        self.assertIn("empty", str(context.exception).lower())

    def test_load_file_corrupted_file(self):
        """Test ValueError raised for corrupted Excel file."""
        corrupted_file = self.temp_dir / "corrupted.xlsx"
        # Create a text file with .xlsx extension
        corrupted_file.write_text("This is not a valid Excel file")

        with self.assertRaises(ValueError) as context:
            self.loader.load_file(corrupted_file)
        self.assertIn("Failed to read Excel file", str(context.exception))

    def test_validate_columns_all_present(self):
        """Test validation when all required columns are present."""
        is_valid, missing = self.loader.validate_columns(self.sample_valid_data)

        self.assertTrue(is_valid)
        self.assertEqual(missing, [])

    def test_validate_columns_missing_one_column(self):
        """Test validation when one required column is missing."""
        df = pd.DataFrame({
            'Transaction_Total': [100.0],
            'Sales_Amount': [90.0],
            # Missing 'Sales_Qty'
        })

        is_valid, missing = self.loader.validate_columns(df)

        self.assertFalse(is_valid)
        self.assertIn('Sales_Qty', missing)
        self.assertEqual(len(missing), 1)

    def test_validate_columns_missing_multiple_columns(self):
        """Test validation when multiple columns are missing."""
        df = pd.DataFrame({
            'Transaction_Total': [100.0],
            # Missing 'Sales_Amount' and 'Sales_Qty'
        })

        is_valid, missing = self.loader.validate_columns(df)

        self.assertFalse(is_valid)
        self.assertIn('Sales_Amount', missing)
        self.assertIn('Sales_Qty', missing)
        self.assertEqual(len(missing), 2)

    def test_validate_columns_extra_columns_allowed(self):
        """Test that extra columns don't affect validation."""
        df = pd.DataFrame({
            'Transaction_Total': [100.0],
            'Sales_Amount': [90.0],
            'Sales_Qty': [10],
            'Extra_Column_1': ['data'],
            'Extra_Column_2': [123],
        })

        is_valid, missing = self.loader.validate_columns(df)

        self.assertTrue(is_valid)
        self.assertEqual(missing, [])

    def test_add_weekday_column_valid_dates(self):
        """Test adding weekday column with valid date data."""
        df = self.loader.add_weekday_column(
            self.sample_valid_data.copy(),
            date_column='Date'
        )

        self.assertIn('Weekday', df.columns)
        self.assertEqual(len(df), 3)
        # Verify weekday names are valid
        valid_weekdays = [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday'
        ]
        self.assertTrue(all(day in valid_weekdays for day in df['Weekday']))

    def test_add_weekday_column_custom_column_name(self):
        """Test adding weekday column with custom column name."""
        df = self.loader.add_weekday_column(
            self.sample_valid_data.copy(),
            date_column='Date',
            weekday_column='DayOfWeek'
        )

        self.assertIn('DayOfWeek', df.columns)
        self.assertNotIn('Weekday', df.columns)

    def test_add_weekday_column_datetime_format(self):
        """Test weekday extraction with datetime objects."""
        df = pd.DataFrame({
            'Date': pd.to_datetime([
                '2025-10-06',
                '2025-10-07',
                '2025-10-08'
            ])
        })

        result_df = self.loader.add_weekday_column(df, date_column='Date')

        self.assertIn('Weekday', result_df.columns)
        self.assertEqual(len(result_df), 3)

    def test_add_weekday_column_string_dates(self):
        """Test weekday extraction with string date formats."""
        df = pd.DataFrame({
            'Date': ['2025-10-06', '2025-10-07', '2025-10-08']
        })

        result_df = self.loader.add_weekday_column(df, date_column='Date')

        self.assertIn('Weekday', result_df.columns)
        # Verify conversion worked
        self.assertEqual(result_df['Weekday'].iloc[0], 'Monday')

    def test_add_weekday_column_various_date_formats(self):
        """Test weekday extraction with various date formats."""
        test_cases = [
            ['2025-10-06', '2025-10-07'],  # ISO format
            ['10/06/2025', '10/07/2025'],  # US format
            ['06-10-2025', '07-10-2025'],  # European format
        ]

        for dates in test_cases:
            df = pd.DataFrame({'Date': dates})
            result_df = self.loader.add_weekday_column(
                df,
                date_column='Date'
            )
            self.assertIn('Weekday', result_df.columns)
            self.assertEqual(len(result_df), 2)

    def test_add_weekday_column_missing_date_column(self):
        """Test ValueError raised when date column doesn't exist."""
        df = pd.DataFrame({'Other_Column': [1, 2, 3]})

        with self.assertRaises(ValueError) as context:
            self.loader.add_weekday_column(df, date_column='Date')
        self.assertIn("not found in DataFrame", str(context.exception))

    def test_add_weekday_column_invalid_date_data(self):
        """Test ValueError raised for invalid date data."""
        df = pd.DataFrame({
            'Date': ['not a date', 'invalid', 'bad data']
        })

        with self.assertRaises(ValueError) as context:
            self.loader.add_weekday_column(df, date_column='Date')
        self.assertIn("Failed to extract weekday", str(context.exception))

    def test_add_weekday_column_mixed_valid_invalid_dates(self):
        """Test mixed valid/invalid dates raises ValueError."""
        df = pd.DataFrame({
            'Date': ['2025-10-06', 'invalid', '2025-10-08']
        })

        # pandas will raise ValueError for mixed valid/invalid dates
        # This is expected behavior - data should be cleaned before processing
        with self.assertRaises(ValueError) as context:
            self.loader.add_weekday_column(df, date_column='Date')
        self.assertIn("Failed to extract weekday", str(context.exception))

    def test_add_weekday_column_preserves_original_data(self):
        """Test that adding weekday column preserves original data."""
        original_columns = list(self.sample_valid_data.columns)
        original_len = len(self.sample_valid_data)

        result_df = self.loader.add_weekday_column(
            self.sample_valid_data.copy(),
            date_column='Date'
        )

        # All original columns should still exist
        for col in original_columns:
            self.assertIn(col, result_df.columns)

        # Row count should be unchanged
        self.assertEqual(len(result_df), original_len)

        # Original data should be unchanged
        self.assertEqual(
            result_df['Product'].tolist(),
            ['Product A', 'Product B', 'Product C']
        )


if __name__ == '__main__':
    unittest.main()
