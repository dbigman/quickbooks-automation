"""CSV creation service for QuickBooks Auto Reporter."""

import csv
import logging
from typing import List

from quickbooks_autoreport.adapters.file_adapter import FileAdapter


class CSVCreator:
    """Creates CSV files with proper formatting."""

    def __init__(self, file_adapter: FileAdapter, logger: logging.Logger) -> None:
        """Initialize with injected dependencies."""
        self._file = file_adapter
        self._logger = logger

    def create_csv(
        self,
        path: str,
        headers: List[str],
        rows: List[List[str]],
    ) -> None:
        """Write CSV file with headers and rows.

        Args:
            path: Output file path
            headers: Column headers
            rows: Data rows
        """
        self._logger.debug(f"Creating CSV: {path}")
        output = []
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        content = "\n".join(output)
        self._file.write_file(path, content)