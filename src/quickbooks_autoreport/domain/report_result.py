"""Report result domain model.

This module defines the ReportResult dataclass for structured return values
from report generation operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class ReportResult:
    """Result of a report execution.
    
    This dataclass encapsulates all information about a report generation
    attempt, including success/failure status, metadata, and any errors.
    
    Attributes:
        report_key: Unique identifier of the report
        report_name: Human-readable report name
        rows: Number of data rows in the report
        changed: Whether report data changed since last run
        timestamp: When the report was generated
        excel_created: Whether Excel file was successfully created
        insights: Optional business insights dictionary
        connect_info: Connection metadata (version, company, etc.)
        error: Optional error message if generation failed
    """

    report_key: str
    report_name: str
    rows: int
    changed: bool
    timestamp: datetime
    excel_created: bool
    insights: Optional[Dict[str, Any]]
    connect_info: Dict[str, Any]
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """Whether the report executed successfully.
        
        Returns:
            True if no error occurred, False otherwise
        """
        return self.error is None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.
        
        Returns:
            Dictionary representation of the report result
        """
        return {
            "report_key": self.report_key,
            "report_name": self.report_name,
            "rows": self.rows,
            "changed": self.changed,
            "timestamp": self.timestamp.isoformat(),
            "excel_created": self.excel_created,
            "insights": self.insights,
            "connect_info": self.connect_info,
            "error": self.error,
            "success": self.success,
        }

    def get_summary(self) -> str:
        """Get a human-readable summary of the result.
        
        Returns:
            Summary string describing the report result
        """
        if not self.success:
            return f"❌ {self.report_name}: {self.error}"
        
        status = "✅ Changed" if self.changed else "⚪ Unchanged"
        excel_status = "📊 Excel created" if self.excel_created else ""
        
        parts = [
            f"{status} {self.report_name}",
            f"({self.rows} rows)",
        ]
        
        if excel_status:
            parts.append(excel_status)
        
        return " ".join(parts)
