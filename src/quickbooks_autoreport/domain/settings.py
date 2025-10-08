"""Application settings domain model.

This module defines the Settings dataclass that replaces dict-based
settings with a strongly-typed model.
"""

import datetime as dt
import os
from dataclasses import dataclass, field
from typing import Optional


# Default output directory
DEFAULT_OUT_DIR = r"C:\Reports"

# Default interval
DEFAULT_INTERVAL = "15 minutes"

# Valid interval options
VALID_INTERVALS = {
    "5 minutes",
    "15 minutes",
    "30 minutes",
    "60 minutes",
}


@dataclass
class Settings:
    """Application settings.
    
    This dataclass defines all user-configurable settings for the application.
    It replaces dict-based settings with a strongly-typed, validated model.
    
    Attributes:
        output_dir: Directory for report output files
        interval: Report generation interval
        report_date_from: Start date for date-range reports (YYYY-MM-DD)
        report_date_to: End date for date-range reports (YYYY-MM-DD)
        company_file: Optional QuickBooks company file path
    """

    output_dir: str = DEFAULT_OUT_DIR
    interval: str = DEFAULT_INTERVAL
    report_date_from: str = field(
        default_factory=lambda: dt.date.today().replace(day=1).isoformat()
    )
    report_date_to: str = field(default_factory=lambda: dt.date.today().isoformat())
    company_file: Optional[str] = None

    def validate(self) -> None:
        """Validate settings values.
        
        Raises:
            ValueError: If any setting is invalid
        """
        # Validate output directory
        if not self.output_dir:
            raise ValueError("Output directory cannot be empty")
        
        # Validate interval
        if self.interval not in VALID_INTERVALS:
            raise ValueError(
                f"Invalid interval: {self.interval}. "
                f"Must be one of: {', '.join(sorted(VALID_INTERVALS))}"
            )
        
        # Validate date format and range
        try:
            date_from = dt.date.fromisoformat(self.report_date_from)
            date_to = dt.date.fromisoformat(self.report_date_to)
            
            if date_from > date_to:
                raise ValueError(
                    f"Start date ({self.report_date_from}) cannot be after "
                    f"end date ({self.report_date_to})"
                )
        except ValueError as e:
            if "Invalid isoformat string" in str(e):
                raise ValueError(
                    "Dates must be in YYYY-MM-DD format. "
                    f"Got: from={self.report_date_from}, to={self.report_date_to}"
                )
            raise
        
        # Validate company file if provided
        if self.company_file and not os.path.exists(self.company_file):
            raise ValueError(f"Company file does not exist: {self.company_file}")

    def get_interval_seconds(self) -> int:
        """Get interval in seconds.
        
        Returns:
            Interval duration in seconds
            
        Raises:
            ValueError: If interval is invalid
        """
        interval_map = {
            "5 minutes": 5 * 60,
            "15 minutes": 15 * 60,
            "30 minutes": 30 * 60,
            "60 minutes": 60 * 60,
        }
        
        if self.interval not in interval_map:
            raise ValueError(f"Invalid interval: {self.interval}")
        
        return interval_map[self.interval]

    def ensure_output_directory(self) -> None:
        """Ensure output directory exists.
        
        Creates the output directory if it doesn't exist.
        
        Raises:
            OSError: If directory cannot be created
        """
        os.makedirs(self.output_dir, exist_ok=True)
