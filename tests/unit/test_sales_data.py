"""Unit tests for sales data domain models."""

from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
import pytest

from quickbooks_autoreport.domain.sales_data import DashboardState, SalesData


class TestSalesData:
    """Tests for SalesData dataclass."""

    def test_sales_data_creation(self):
        """Test creating SalesData instance."""
        df = pd.DataFrame({
            'Transaction_Total': [100, 200],
            'Sales_Amount': [50, 100],
            'Sales_Qty': [1, 2]
        })
        filepath = Path('test.xlsx')
        loaded_at = datetime.now()

        sales_data = SalesData(
            df=df,
            filepath=filepath,
            loaded_at=loaded_at,
            row_count=2
        )

        assert sales_data.df.equals(df)
        assert sales_data.filepath == filepath
        assert sales_data.loaded_at == loaded_at
        assert sales_data.row_count == 2

    def test_from_file_success(self):
        """Test loading data from file successfully."""
        df = pd.DataFrame({
            'Transaction_Total': [100, 200],
            'Sales_Amount': [50, 100],
            'Sales_Qty': [1, 2]
        })
        filepath = Path('test.xlsx')

        # Mock loader
        loader = Mock()
        loader.load_file.return_value = df
        loader.validate_columns.return_value = (True, [])

        sales_data = SalesData.from_file(filepath, loader)

        assert sales_data.filepath == filepath
        assert sales_data.row_count == 2
        assert sales_data.df.equals(df)
        loader.load_file.assert_called_once_with(filepath)
        loader.validate_columns.assert_called_once()

    def test_from_file_missing_columns(self):
        """Test loading data with missing columns raises error."""
        df = pd.DataFrame({'Other_Column': [1, 2]})
        filepath = Path('test.xlsx')

        # Mock loader
        loader = Mock()
        loader.load_file.return_value = df
        loader.validate_columns.return_value = (False, ['Transaction_Total'])

        with pytest.raises(ValueError, match="Required columns missing"):
            SalesData.from_file(filepath, loader)

    def test_get_date_range_success(self):
        """Test getting date range from dataset."""
        df = pd.DataFrame({
            'Date': pd.to_datetime(['2025-01-01', '2025-01-05', '2025-01-03']),
            'Transaction_Total': [100, 200, 150]
        })

        sales_data = SalesData(
            df=df,
            filepath=Path('test.xlsx'),
            loaded_at=datetime.now(),
            row_count=3
        )

        min_date, max_date = sales_data.get_date_range()

        assert min_date == datetime(2025, 1, 1)
        assert max_date == datetime(2025, 1, 5)

    def test_get_date_range_no_date_column(self):
        """Test getting date range with no date column raises error."""
        df = pd.DataFrame({
            'Transaction_Total': [100, 200]
        })

        sales_data = SalesData(
            df=df,
            filepath=Path('test.xlsx'),
            loaded_at=datetime.now(),
            row_count=2
        )

        with pytest.raises(ValueError, match="No date column found"):
            sales_data.get_date_range()


class TestDashboardState:
    """Tests for DashboardState dataclass."""

    def test_dashboard_state_creation(self):
        """Test creating DashboardState instance."""
        state = DashboardState()

        assert state.current_file is None
        assert state.sales_data is None
        assert state.last_update is None
        assert state.last_file_mtime is None
        assert state.error_message is None

    def test_should_reload_no_file(self):
        """Test should_reload returns False when no file selected."""
        state = DashboardState()
        file_scanner = Mock()

        assert state.should_reload(file_scanner) is False

    def test_should_reload_file_modified(self):
        """Test should_reload returns True when file modified."""
        filepath = Path('test.xlsx')
        state = DashboardState(
            current_file=filepath,
            last_file_mtime=1000.0
        )

        file_scanner = Mock()
        file_scanner.file_exists.return_value = True
        file_scanner.get_file_modified_time.return_value = datetime.fromtimestamp(2000.0)

        assert state.should_reload(file_scanner) is True

    def test_should_reload_file_not_modified(self):
        """Test should_reload returns False when file not modified."""
        filepath = Path('test.xlsx')
        state = DashboardState(
            current_file=filepath,
            last_file_mtime=2000.0
        )

        file_scanner = Mock()
        file_scanner.file_exists.return_value = True
        file_scanner.get_file_modified_time.return_value = datetime.fromtimestamp(1000.0)

        assert state.should_reload(file_scanner) is False

    def test_should_reload_file_not_exists(self):
        """Test should_reload returns False when file doesn't exist."""
        filepath = Path('test.xlsx')
        state = DashboardState(
            current_file=filepath,
            last_file_mtime=1000.0
        )

        file_scanner = Mock()
        file_scanner.file_exists.return_value = False

        assert state.should_reload(file_scanner) is False

    def test_should_reload_error_handling(self):
        """Test should_reload handles errors gracefully."""
        filepath = Path('test.xlsx')
        state = DashboardState(
            current_file=filepath,
            last_file_mtime=1000.0
        )

        file_scanner = Mock()
        file_scanner.file_exists.return_value = True
        file_scanner.get_file_modified_time.side_effect = Exception("Error")

        assert state.should_reload(file_scanner) is False
