"""
Integration tests for Sales Dashboard end-to-end flows.

Tests the complete dashboard workflow including:
- File selection and data loading
- Manual refresh functionality
- Automatic polling detection
- Error scenarios (missing files, bad data)

Requirements: 5.3, 6.4, 9.1, 10.1, 10.2, 10.5, 1.4, 2.4, 3.5, 4.5, 9.2
"""

import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# Mock Windows-specific modules before importing dashboard modules
sys.modules['pythoncom'] = MagicMock()
sys.modules['win32com'] = MagicMock()
sys.modules['win32com.client'] = MagicMock()

from quickbooks_autoreport.dashboard.data_loader import ExcelLoader, FileScanner
from quickbooks_autoreport.dashboard.metrics import MetricsCalculator
from quickbooks_autoreport.domain.sales_data import DashboardState, SalesData


class TestEndToEndFlow:
    """Test complete end-to-end dashboard workflows."""

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory with test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            yield output_dir

    @pytest.fixture
    def valid_sales_file(self, temp_output_dir):
        """Create a valid sales Excel file."""
        filepath = temp_output_dir / "sales_test.xlsx"
        
        # Create sample data with all required columns
        data = {
            'Transaction_Total': [100.0, 200.0, 150.0, 300.0, 250.0],
            'Sales_Amount': [90.0, 180.0, 135.0, 270.0, 225.0],
            'Sales_Qty': [10, 20, 15, 30, 25],
            'Product': ['Product A', 'Product B', 'Product C', 'Product A', 'Product B'],
            'Date': pd.date_range('2025-01-06', periods=5, freq='D')  # Monday-Friday
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        return filepath

    @pytest.fixture
    def missing_columns_file(self, temp_output_dir):
        """Create Excel file with missing required columns."""
        filepath = temp_output_dir / "sales_missing_cols.xlsx"
        
        data = {
            'Transaction_Total': [100.0, 200.0],
            'Product': ['Product A', 'Product B'],
            # Missing Sales_Amount and Sales_Qty
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        return filepath

    @pytest.fixture
    def empty_file(self, temp_output_dir):
        """Create empty Excel file."""
        filepath = temp_output_dir / "sales_empty.xlsx"
        df = pd.DataFrame()
        df.to_excel(filepath, index=False)
        return filepath

    def test_file_selection_to_metrics_display(self, valid_sales_file, temp_output_dir):
        """
        Test complete flow: file selection → data load → metrics display.
        
        Requirements: 5.3, 6.4, 9.1
        """
        # Step 1: File selection - scan directory
        scanner = FileScanner(temp_output_dir)  # Pass Path object, not string
        available_files = scanner.list_excel_files()
        
        assert len(available_files) > 0
        assert valid_sales_file in available_files
        
        # Step 2: Data loading
        loader = ExcelLoader()
        file_mtime = valid_sales_file.stat().st_mtime
        df = loader.load_file(valid_sales_file, file_mtime)
        
        # Validate columns
        is_valid, missing = loader.validate_columns(df)
        assert is_valid
        assert len(missing) == 0
        
        # Add weekday column
        df = loader.add_weekday_column(df, 'Date')
        assert 'Weekday' in df.columns
        
        # Step 3: Create SalesData instance
        sales_data = SalesData.from_file(valid_sales_file, loader)
        
        assert sales_data.filepath == valid_sales_file
        assert sales_data.row_count == 5
        assert sales_data.loaded_at is not None
        
        # Add weekday column for aggregation tests
        sales_data.df = loader.add_weekday_column(sales_data.df, 'Date')
        
        # Step 4: Calculate metrics
        calculator = MetricsCalculator(sales_data.df)
        
        total_revenue = calculator.calculate_total_revenue()
        total_units = calculator.calculate_total_units()
        
        assert total_revenue == 1000.0  # Sum of Transaction_Total
        assert total_units == 100  # Sum of Sales_Qty
        
        # Step 5: Get top products
        top_revenue = calculator.get_top_products_by_revenue(top_n=5)
        top_units = calculator.get_top_products_by_units(top_n=5)
        
        assert len(top_revenue) > 0
        assert len(top_units) > 0
        
        # Step 6: Get weekday aggregations
        revenue_by_weekday = calculator.aggregate_by_weekday('Sales_Amount')
        units_by_weekday = calculator.aggregate_by_weekday('Sales_Qty')
        
        assert len(revenue_by_weekday) == 5  # Monday-Friday
        assert len(units_by_weekday) == 5

    def test_manual_refresh_functionality(self, valid_sales_file, temp_output_dir):
        """
        Test manual refresh updates data and metrics.
        
        Requirements: 6.4
        """
        # Initial load
        loader = ExcelLoader()
        state = DashboardState()
        
        # First load
        sales_data_1 = SalesData.from_file(valid_sales_file, loader)
        state.sales_data = sales_data_1
        state.current_file = valid_sales_file
        state.last_update = datetime.now()
        first_update = state.last_update
        
        assert state.sales_data is not None
        
        # Simulate manual refresh - reload the same file
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp difference
        
        sales_data_2 = SalesData.from_file(valid_sales_file, loader)
        state.sales_data = sales_data_2
        state.last_update = datetime.now()
        second_update = state.last_update
        
        # Verify refresh updated timestamp
        assert second_update > first_update
        assert state.sales_data.loaded_at > sales_data_1.loaded_at
        
        # Verify data is still valid
        calculator = MetricsCalculator(state.sales_data.df)
        assert calculator.calculate_total_revenue() == 1000.0

    def test_automatic_polling_detection(self, valid_sales_file, temp_output_dir):
        """
        Test automatic polling detects file modifications.
        
        Requirements: 6.4
        """
        scanner = FileScanner(temp_output_dir)
        loader = ExcelLoader()
        state = DashboardState()
        
        # Initial load
        sales_data = SalesData.from_file(valid_sales_file, loader)
        state.sales_data = sales_data
        state.current_file = valid_sales_file
        state.last_file_mtime = scanner.get_file_modified_time(valid_sales_file).timestamp()
        
        # Check if reload needed (should be False initially)
        assert not state.should_reload(scanner, debounce_seconds=0)
        
        # Simulate file modification
        import time
        time.sleep(3)  # Wait for stability check (2 seconds) + buffer
        valid_sales_file.touch()  # Update modification time
        time.sleep(3)  # Wait for file to be stable
        
        # Check if reload needed (should be True now)
        assert state.should_reload(scanner, debounce_seconds=0)
        
        # Perform reload
        new_sales_data = SalesData.from_file(valid_sales_file, loader)
        state.sales_data = new_sales_data
        state.last_file_mtime = scanner.get_file_modified_time(valid_sales_file).timestamp()
        
        # Should not need reload anymore
        assert not state.should_reload(scanner, debounce_seconds=0)

    def test_error_missing_file(self, temp_output_dir):
        """
        Test error handling when file doesn't exist.
        
        Requirements: 9.1
        """
        loader = ExcelLoader()
        non_existent_file = temp_output_dir / "does_not_exist.xlsx"
        
        with pytest.raises(FileNotFoundError):
            loader.load_file(non_existent_file, 0.0)

    def test_error_missing_columns(self, missing_columns_file):
        """
        Test error handling when required columns are missing.
        
        Requirements: 9.1, 9.2
        """
        loader = ExcelLoader()
        file_mtime = missing_columns_file.stat().st_mtime
        df = loader.load_file(missing_columns_file, file_mtime)
        
        is_valid, missing = loader.validate_columns(df)
        
        assert not is_valid
        assert 'Sales_Amount' in missing
        assert 'Sales_Qty' in missing

    def test_error_empty_file(self, empty_file):
        """
        Test error handling with empty Excel file.
        
        Requirements: 9.1, 1.4, 2.4
        """
        loader = ExcelLoader()
        file_mtime = empty_file.stat().st_mtime
        
        # Empty file should raise ValueError
        with pytest.raises(ValueError, match="empty"):
            loader.load_file(empty_file, file_mtime)

    def test_error_bad_data_types(self, temp_output_dir):
        """
        Test error handling with invalid data types.
        
        Requirements: 9.2
        """
        filepath = temp_output_dir / "sales_bad_types.xlsx"
        
        # Create file with non-numeric values in numeric columns
        data = {
            'Transaction_Total': ['invalid', 'data', 'here'],
            'Sales_Amount': ['not', 'numbers', 'either'],
            'Sales_Qty': ['bad', 'qty', 'values'],
            'Product': ['Product A', 'Product B', 'Product C'],
            'Date': pd.date_range('2025-01-06', periods=3, freq='D')
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        loader = ExcelLoader()
        file_mtime = filepath.stat().st_mtime
        df_loaded = loader.load_file(filepath, file_mtime)
        
        # Data loads but numeric conversion will produce NaN
        calculator = MetricsCalculator(df_loaded)
        
        # Should handle NaN gracefully
        total_revenue = calculator.calculate_total_revenue()
        total_units = calculator.calculate_total_units()
        
        # NaN values should result in 0 or NaN
        assert pd.isna(total_revenue) or total_revenue == 0
        assert pd.isna(total_units) or total_units == 0


class TestRealDataScenarios:
    """Test dashboard with real-world data scenarios."""

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_multiweek_data(self, temp_output_dir):
        """
        Test with data spanning multiple weeks.
        
        Requirements: 3.5, 4.5
        """
        filepath = temp_output_dir / "sales_multiweek.xlsx"
        
        # Create 3 weeks of data
        dates = []
        for week in range(3):
            week_start = pd.Timestamp('2025-01-06') + pd.Timedelta(weeks=week)
            dates.extend(pd.date_range(week_start, periods=7, freq='D'))
        
        data = {
            'Transaction_Total': [100.0] * len(dates),
            'Sales_Amount': [90.0] * len(dates),
            'Sales_Qty': [10] * len(dates),
            'Product': ['Product A'] * len(dates),
            'Date': dates
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        # Load and process
        loader = ExcelLoader()
        sales_data = SalesData.from_file(filepath, loader)
        
        # Add weekday column
        sales_data.df = loader.add_weekday_column(sales_data.df, 'Date')
        
        calculator = MetricsCalculator(sales_data.df)
        
        # Aggregate by weekday (should combine all weeks)
        revenue_by_weekday = calculator.aggregate_by_weekday('Sales_Amount')
        
        # Should have 7 weekdays
        assert len(revenue_by_weekday) == 7
        
        # Each weekday should have 3 occurrences (3 weeks)
        # So each weekday total should be 90.0 * 3 = 270.0
        for weekday_revenue in revenue_by_weekday['Sales_Amount']:
            assert weekday_revenue == 270.0

    def test_single_day_data(self, temp_output_dir):
        """
        Test with single day of data.
        
        Requirements: 3.5, 4.5
        """
        filepath = temp_output_dir / "sales_single_day.xlsx"
        
        data = {
            'Transaction_Total': [100.0, 200.0, 150.0],
            'Sales_Amount': [90.0, 180.0, 135.0],
            'Sales_Qty': [10, 20, 15],
            'Product': ['Product A', 'Product B', 'Product C'],
            'Date': ['2025-01-06'] * 3  # All same day (Monday)
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        # Load and process
        loader = ExcelLoader()
        sales_data = SalesData.from_file(filepath, loader)
        
        # Add weekday column
        sales_data.df = loader.add_weekday_column(sales_data.df, 'Date')
        
        calculator = MetricsCalculator(sales_data.df)
        
        # Aggregate by weekday
        revenue_by_weekday = calculator.aggregate_by_weekday('Sales_Amount')
        
        # Should have only 1 weekday (Monday)
        assert len(revenue_by_weekday) == 1
        assert revenue_by_weekday['Weekday'].iloc[0] == 'Monday'
        assert revenue_by_weekday['Sales_Amount'].iloc[0] == 405.0  # Sum of all

    def test_large_file_performance(self, temp_output_dir):
        """
        Test performance with large dataset.
        
        Requirements: 10.1, 10.2, 10.5
        """
        filepath = temp_output_dir / "sales_large.xlsx"
        
        # Create large dataset (1000 rows)
        num_rows = 1000
        data = {
            'Transaction_Total': [100.0] * num_rows,
            'Sales_Amount': [90.0] * num_rows,
            'Sales_Qty': [10] * num_rows,
            'Product': [f'Product {i % 50}' for i in range(num_rows)],
            'Date': pd.date_range('2025-01-01', periods=num_rows, freq='H')
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        # Measure load time
        import time
        loader = ExcelLoader()
        
        start_time = time.time()
        sales_data = SalesData.from_file(filepath, loader)
        load_time = time.time() - start_time
        
        # Should load within 3 seconds (Requirement 10.1)
        assert load_time < 3.0
        assert sales_data.row_count == num_rows
        
        # Measure metrics calculation time
        start_time = time.time()
        calculator = MetricsCalculator(sales_data.df)
        total_revenue = calculator.calculate_total_revenue()
        top_products = calculator.get_top_products_by_revenue(top_n=5)
        calc_time = time.time() - start_time
        
        # Calculations should be fast (< 2 seconds for Requirement 10.2)
        assert calc_time < 2.0
        assert total_revenue == 100000.0  # 100 * 1000
        assert len(top_products) <= 5


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_zero_values(self, temp_output_dir):
        """Test handling of zero values in metrics."""
        filepath = temp_output_dir / "sales_zeros.xlsx"
        
        data = {
            'Transaction_Total': [0.0, 0.0, 0.0],
            'Sales_Amount': [0.0, 0.0, 0.0],
            'Sales_Qty': [0, 0, 0],
            'Product': ['Product A', 'Product B', 'Product C'],
            'Date': pd.date_range('2025-01-06', periods=3, freq='D')
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        loader = ExcelLoader()
        sales_data = SalesData.from_file(filepath, loader)
        calculator = MetricsCalculator(sales_data.df)
        
        assert calculator.calculate_total_revenue() == 0.0
        assert calculator.calculate_total_units() == 0

    def test_negative_values(self, temp_output_dir):
        """Test handling of negative values (returns/refunds)."""
        filepath = temp_output_dir / "sales_negative.xlsx"
        
        data = {
            'Transaction_Total': [100.0, -50.0, 200.0],
            'Sales_Amount': [90.0, -45.0, 180.0],
            'Sales_Qty': [10, -5, 20],
            'Product': ['Product A', 'Product B', 'Product C'],
            'Date': pd.date_range('2025-01-06', periods=3, freq='D')
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        loader = ExcelLoader()
        sales_data = SalesData.from_file(filepath, loader)
        calculator = MetricsCalculator(sales_data.df)
        
        # Should handle negative values correctly
        assert calculator.calculate_total_revenue() == 250.0  # 100 - 50 + 200
        assert calculator.calculate_total_units() == 25  # 10 - 5 + 20

    def test_duplicate_products(self, temp_output_dir):
        """Test aggregation with duplicate product names."""
        filepath = temp_output_dir / "sales_duplicates.xlsx"
        
        data = {
            'Transaction_Total': [100.0, 200.0, 150.0, 300.0],
            'Sales_Amount': [90.0, 180.0, 135.0, 270.0],
            'Sales_Qty': [10, 20, 15, 30],
            'Product': ['Product A', 'Product A', 'Product B', 'Product B'],
            'Date': pd.date_range('2025-01-06', periods=4, freq='D')
        }
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        
        loader = ExcelLoader()
        sales_data = SalesData.from_file(filepath, loader)
        calculator = MetricsCalculator(sales_data.df)
        
        top_revenue = calculator.get_top_products_by_revenue(top_n=5)
        
        # Should aggregate duplicates
        assert len(top_revenue) == 2  # Only 2 unique products
        
        # Product B should be first (270 + 135 = 405)
        # Product A should be second (90 + 180 = 270)
        assert top_revenue.iloc[0]['Product'] == 'Product B'
        assert top_revenue.iloc[0]['Sales_Amount'] == 405.0
