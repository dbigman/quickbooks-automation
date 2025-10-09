"""Domain models for sales dashboard data."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple

import pandas as pd

if TYPE_CHECKING:
    from quickbooks_autoreport.dashboard.data_loader import (
        ExcelLoader,
        FileScanner,
    )


@dataclass
class SalesData:
    """Container for validated sales data.

    Attributes:
        df: DataFrame containing sales data
        filepath: Path to the source Excel file
        loaded_at: Timestamp when data was loaded
        row_count: Number of rows in the dataset
    """
    df: pd.DataFrame
    filepath: Path
    loaded_at: datetime
    row_count: int

    @classmethod
    def from_file(
        cls,
        filepath: Path,
        loader: 'ExcelLoader',
        file_mtime: Optional[float] = None
    ) -> 'SalesData':
        """Factory method to load and validate data from file.

        Args:
            filepath: Path to Excel file to load
            loader: ExcelLoader instance for loading data
            file_mtime: File modification time for cache key (optional)

        Returns:
            SalesData instance with loaded and validated data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns are missing or data is invalid
        """
        # Get file modification time if not provided
        if file_mtime is None:
            file_mtime = filepath.stat().st_mtime

        # Load the file (with caching based on mtime)
        df = loader.load_file(filepath, file_mtime)

        # Validate columns
        is_valid, missing_columns = loader.validate_columns(df)
        if not is_valid:
            raise ValueError(
                f"Required columns missing: {', '.join(missing_columns)}"
            )

        # Create instance
        return cls(
            df=df,
            filepath=filepath,
            loaded_at=datetime.now(),
            row_count=len(df)
        )

    def get_date_range(self) -> Tuple[datetime, datetime]:
        """Return min and max dates in dataset.

        Returns:
            Tuple of (min_date, max_date)

        Raises:
            ValueError: If no date column found or dates cannot be parsed
        """
        # Look for common date column names
        date_columns = ['Date', 'date', 'Transaction_Date', 'transaction_date']
        date_col = None

        for col in date_columns:
            if col in self.df.columns:
                date_col = col
                break

        if date_col is None:
            raise ValueError("No date column found in dataset")

        # Convert to datetime if not already
        dates = pd.to_datetime(self.df[date_col], errors='coerce')

        # Remove NaT values
        dates = dates.dropna()

        if len(dates) == 0:
            raise ValueError("No valid dates found in dataset")

        return dates.min().to_pydatetime(), dates.max().to_pydatetime()


@dataclass
class DashboardState:
    """Streamlit session state container.

    Attributes:
        current_file: Currently selected file path
        sales_data: Loaded sales data instance
        last_update: Timestamp of last data update
        last_file_mtime: Last known file modification time
        error_message: Current error message if any
        last_poll_check: Timestamp of last polling check
    """
    current_file: Optional[Path] = None
    sales_data: Optional[SalesData] = None
    last_update: Optional[datetime] = None
    last_file_mtime: Optional[float] = None
    error_message: Optional[str] = None
    last_poll_check: Optional[datetime] = None

    def should_reload(
        self,
        file_scanner: 'FileScanner',
        debounce_seconds: int = 5
    ) -> bool:
        """Check if file has been modified since last load.

        This method implements optimized polling with debouncing to
        avoid excessive file system checks and rapid reloads.

        Args:
            file_scanner: FileScanner instance to check file modification time
            debounce_seconds: Minimum seconds between reload checks
                (default: 5)

        Returns:
            True if file should be reloaded, False otherwise

        Requirements:
            - 6.1: Check modification time before reloading
            - 10.3: Avoid blocking UI during polling
            - Debounce rapid file changes
        """
        # No file selected or no previous load
        if self.current_file is None or self.last_file_mtime is None:
            return False

        # Debounce: Don't check too frequently
        now = datetime.now()
        if self.last_poll_check is not None:
            time_since_last_check = (
                (now - self.last_poll_check).total_seconds()
            )
            if time_since_last_check < debounce_seconds:
                return False

        # Update last poll check time
        self.last_poll_check = now

        # Check if file still exists (fast check)
        if not file_scanner.file_exists(self.current_file):
            return False

        # Get current modification time
        try:
            current_mtime = file_scanner.get_file_modified_time(
                self.current_file
            ).timestamp()

            # Compare with last known modification time
            # Only reload if file is actually newer
            if current_mtime > self.last_file_mtime:
                # Additional debounce: ensure file is stable
                # (not being actively written)
                time_since_modification = now.timestamp() - current_mtime
                if time_since_modification >= 2:  # 2 second stability check
                    return True

            return False
        except Exception:
            # If we can't get modification time, don't reload
            return False
