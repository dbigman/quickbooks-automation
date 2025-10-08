"""Custom exception classes for QuickBooks Auto Reporter.

This module defines domain-specific exceptions for better error handling
and user-friendly error messages.
"""

from typing import List


class QuickBooksError(Exception):
    """Base exception for QuickBooks-related errors."""

    pass


class QuickBooksConnectionError(QuickBooksError):
    """QuickBooks connection failed.
    
    Attributes:
        message: Human-readable error message
        error_type: Classification of the error (e.g., SDK_NOT_INSTALLED)
        solutions: List of potential solutions to resolve the error
    """

    def __init__(self, message: str, error_type: str, solutions: List[str]) -> None:
        """Initialize QuickBooksConnectionError.
        
        Args:
            message: Human-readable error message
            error_type: Classification of the error
            solutions: List of potential solutions
        """
        self.error_type = error_type
        self.solutions = solutions
        super().__init__(message)


class ReportGenerationError(QuickBooksError):
    """Report generation failed.
    
    Raised when a report cannot be generated due to QuickBooks errors,
    data issues, or other problems during report execution.
    """

    pass


class FileOperationError(Exception):
    """File operation failed.
    
    Raised when file read, write, or other file system operations fail.
    """

    pass


class SettingsError(Exception):
    """Settings validation or loading failed.
    
    Raised when settings cannot be loaded, saved, or validated properly.
    """

    pass
