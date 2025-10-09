"""
Data loading and file scanning utilities for the sales dashboard.

This module provides classes for discovering Excel files and loading
sales data with validation.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
import streamlit as st

from .config import (
    OUTPUT_DIR,
    REQUIRED_COLUMNS,
    SHEET_NAME,
    LOG_EMOJI_LOADING,
    LOG_EMOJI_ERROR,
)

logger = logging.getLogger(__name__)


class FileScanner:
    """
    Scans and monitors Excel files in the output directory.

    This class provides methods to discover .xlsx files, check
    modification times, and validate file existence.
    """

    def __init__(self, directory: Path = OUTPUT_DIR):
        """
        Initialize FileScanner with target directory.

        Args:
            directory: Path to directory containing Excel files
        """
        self.directory = directory
        logger.info(
            f"{LOG_EMOJI_LOADING} FileScanner initialized for "
            f"directory: {directory}"
        )

    def list_excel_files(self) -> List[Path]:
        """
        Scan directory for Excel files (.xlsx).

        Returns:
            List of Path objects for .xlsx files found in directory,
            sorted by modification time (newest first)

        Raises:
            FileNotFoundError: If directory does not exist
        """
        if not self.directory.exists():
            error_msg = f"Directory not found: {self.directory}"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise FileNotFoundError(error_msg)

        if not self.directory.is_dir():
            error_msg = f"Path is not a directory: {self.directory}"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise NotADirectoryError(error_msg)

        # Find all .xlsx files
        excel_files = list(self.directory.glob("*.xlsx"))

        # Filter out temporary Excel files (starting with ~$)
        excel_files = [
            f for f in excel_files if not f.name.startswith("~$")
        ]

        # Sort by modification time, newest first
        excel_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        logger.info(
            f"{LOG_EMOJI_LOADING} Found {len(excel_files)} Excel "
            f"files in {self.directory}"
        )
        return excel_files

    def get_file_modified_time(self, filepath: Path) -> datetime:
        """
        Get last modification timestamp of file.

        Args:
            filepath: Path to file

        Returns:
            datetime object representing last modification time

        Raises:
            FileNotFoundError: If file does not exist
        """
        if not filepath.exists():
            error_msg = f"File not found: {filepath}"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise FileNotFoundError(error_msg)

        mtime = filepath.stat().st_mtime
        modified_time = datetime.fromtimestamp(mtime)

        logger.debug(
            f"File {filepath.name} last modified: {modified_time}"
        )
        return modified_time

    def file_exists(self, filepath: Path) -> bool:
        """
        Check if file exists.

        Args:
            filepath: Path to file

        Returns:
            True if file exists and is a file, False otherwise
        """
        exists = filepath.exists() and filepath.is_file()
        logger.debug(f"File exists check for {filepath.name}: {exists}")
        return exists


class ExcelLoader:
    """
    Loads and validates Excel data for the sales dashboard.

    This class handles reading Excel files, validating required columns,
    and adding derived columns like weekday names.
    """

    def __init__(
        self, required_columns: Optional[List[str]] = None
    ):
        """
        Initialize ExcelLoader with required columns.

        Args:
            required_columns: List of column names that must exist in
                loaded data. Defaults to REQUIRED_COLUMNS from config.
        """
        self.required_columns = required_columns or REQUIRED_COLUMNS
        logger.info(
            f"{LOG_EMOJI_LOADING} ExcelLoader initialized with "
            f"required columns: {self.required_columns}"
        )

    @st.cache_data(ttl=300, show_spinner=False)
    def load_file(_self, filepath: Path, file_mtime: float) -> pd.DataFrame:
        """
        Load Excel file and return DataFrame with caching.

        This method uses Streamlit's caching mechanism to avoid
        reloading the same file multiple times. Cache is based on
        filepath and modification time, ensuring fresh data when
        files are updated.

        Optimizations:
        - Converts numeric columns early for better performance
        - Uses efficient pandas operations

        Args:
            filepath: Path to Excel file
            file_mtime: File modification time (used for cache key)

        Returns:
            pandas DataFrame containing the Excel data with optimized
            data types

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file cannot be read or is empty

        Requirements:
            - 10.1: Load files under 10MB within 3 seconds
            - 10.2: Cache based on filepath and modification time
            - 10.3: Optimize data processing
            - 10.5: Use efficient pandas operations
        """
        if not filepath.exists():
            error_msg = f"File not found: {filepath}"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise FileNotFoundError(error_msg)

        try:
            logger.info(
                f"{LOG_EMOJI_LOADING} Loading Excel file: "
                f"{filepath.name} (mtime: {file_mtime})"
            )

            # Read Excel file from specific sheet
            df = pd.read_excel(filepath, sheet_name=SHEET_NAME)

            # Check if DataFrame is empty
            if df.empty:
                error_msg = f"Excel file sheet '{SHEET_NAME}' is empty: {filepath.name}"
                logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
                raise ValueError(error_msg)

            # Optimize data types early for better performance
            # Convert numeric columns to appropriate types
            numeric_columns = [
                'Sales_Amount',
                'Sales_Qty',
                'Net_Amount',
                'Net_Qty'
            ]

            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(
                        df[col],
                        errors='coerce',
                        downcast='float'
                    )
                    logger.debug(
                        f"Converted column '{col}' to numeric type"
                    )

            logger.info(
                f"{LOG_EMOJI_LOADING} Loaded and optimized {len(df)} "
                f"rows from {filepath.name}"
            )
            return df

        except pd.errors.EmptyDataError as e:
            error_msg = f"Excel file contains no data: {filepath.name}"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg) from e

        except Exception as e:
            error_msg = (
                f"Failed to read Excel file {filepath.name}: {str(e)}"
            )
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg) from e

    def validate_columns(
        self, df: pd.DataFrame
    ) -> Tuple[bool, List[str]]:
        """
        Validate that required columns exist in DataFrame.

        Args:
            df: pandas DataFrame to validate

        Returns:
            Tuple of (is_valid, missing_columns) where:
                - is_valid: True if all required columns exist
                - missing_columns: List of column names that are missing
        """
        df_columns = set(df.columns)
        required_set = set(self.required_columns)

        missing_columns = list(required_set - df_columns)
        is_valid = len(missing_columns) == 0

        if not is_valid:
            logger.warning(
                f"⚠️ Missing required columns: {missing_columns}"
            )
        else:
            logger.info(
                f"{LOG_EMOJI_LOADING} All required columns present"
            )

        return is_valid, missing_columns

    def add_weekday_column(
        self,
        df: pd.DataFrame,
        date_column: str,
        weekday_column: str = "Weekday"
    ) -> pd.DataFrame:
        """
        Add weekday name column from date column.

        Args:
            df: pandas DataFrame containing date data
            date_column: Name of column containing date values
            weekday_column: Name for new weekday column
                (default: "Weekday")

        Returns:
            DataFrame with added weekday column

        Raises:
            ValueError: If date_column does not exist in DataFrame
        """
        if date_column not in df.columns:
            error_msg = (
                f"Date column '{date_column}' not found in DataFrame"
            )
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg)

        try:
            # Convert to datetime if not already
            df[date_column] = pd.to_datetime(df[date_column])

            # Extract weekday name
            df[weekday_column] = df[date_column].dt.day_name()

            logger.info(
                f"{LOG_EMOJI_LOADING} Added weekday column "
                f"'{weekday_column}' from '{date_column}'"
            )
            return df

        except Exception as e:
            error_msg = (
                f"Failed to extract weekday from column "
                f"'{date_column}': {str(e)}"
            )
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg) from e
