"""File system adapter for QuickBooks Auto Reporter.

Wraps file_utils to provide a clean interface for file operations.
"""

import hashlib
import logging
import os
from typing import Optional

from quickbooks_autoreport.utils.file_utils import (
    ensure_directory as ensure_dir,
    read_file as read_file_content,
    write_file as write_file_content,
)


class FileAdapter:
    """Handles file system operations with dependency injection."""

    def __init__(self, logger: logging.Logger) -> None:
        """Initialize with injected logger."""
        self._logger = logger

    def write_file(self, path: str, content: str) -> None:
        """Write content to file."""
        self._logger.debug(f"Writing file: {path}")
        write_file_content(path, content)

    def read_file(self, path: str) -> str:
        """Read content from file."""
        self._logger.debug(f"Reading file: {path}")
        return read_file_content(path)

    def file_exists(self, path: str) -> bool:
        """Check if file exists."""
        return os.path.exists(path)

    def ensure_directory(self, path: str) -> None:
        """Ensure directory exists."""
        self._logger.debug(f"Ensuring directory: {path}")
        ensure_dir(path)

    def compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def read_hash(self, path: str) -> Optional[str]:
        """Read hash from file."""
        if not self.file_exists(path):
            return None
        return self.read_file(path).strip()

    def write_hash(self, path: str, hash_value: str) -> None:
        """Write hash to file."""
        self.write_file(path, hash_value)