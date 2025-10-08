"""Excel creation service for QuickBooks Auto Reporter.

Provides mock Excel creation with placeholder for future openpyxl integration.
"""

import logging
from typing import List

from quickbooks_autoreport.adapters.file_adapter import FileAdapter


class ExcelCreator:
    """Creates Excel files with professional formatting."""

    def __init__(self, file_adapter: FileAdapter, logger: logging.Logger) -> None:
        """Initialize with injected dependencies."""
        self._file = file_adapter
        self._logger = logger

    def create_excel(
        self,
        path: str,
        headers: List[str],
        rows: List[List[str]],
    ) -> bool:
        """Create Excel file (mock implementation).

        Args:
            path: Output file path
            headers: Column headers
            rows: Data rows

        Returns:
            True on success
        """
        self._logger.info(f"Creating Excel (mock): {path}")
        # Mock Excel file creation – in real implementation, use openpyxl here
        mock_content = f"Mock Excel with {len(headers)} columns, {len(rows)} rows"
        self._file.write_file(path, mock_content)
        return True