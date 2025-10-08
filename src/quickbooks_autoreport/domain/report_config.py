"""Report configuration domain model.

This module defines the ReportConfig dataclass that replaces dict-based
report configurations with a strongly-typed, immutable model.
"""

import os
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReportConfig:
    """Configuration for a QuickBooks report.
    
    This immutable dataclass defines all metadata and file paths for a
    specific report type. It replaces the dict-based REPORT_CONFIGS.
    
    Attributes:
        key: Unique identifier for the report (e.g., "open_sales_orders")
        name: Human-readable report name
        qbxml_type: QuickBooks XML report type
        query_type: Query classification ("GeneralDetail", "GeneralSummary", "Aging")
        csv_filename: Output CSV filename
        excel_filename: Output Excel filename
        hash_filename: Hash file for change detection
        request_log: XML request log filename
        response_log: XML response log filename
        uses_date_range: Whether report uses date range parameters
    """

    key: str
    name: str
    qbxml_type: str
    query_type: str
    csv_filename: str
    excel_filename: str
    hash_filename: str
    request_log: str
    response_log: str
    uses_date_range: bool

    def get_file_paths(self, output_dir: str) -> Dict[str, str]:
        """Get all file paths for this report.
        
        Args:
            output_dir: Base output directory path
            
        Returns:
            Dictionary containing all file paths:
                - main_csv: Path to CSV output file
                - excel_file: Path to Excel output file
                - hash_file: Path to hash file for change detection
                - log_file: Path to main application log
                - req_log: Path to XML request log
                - resp_log: Path to XML response log
        """
        return {
            "main_csv": os.path.join(output_dir, self.csv_filename),
            "excel_file": os.path.join(output_dir, self.excel_filename),
            "hash_file": os.path.join(output_dir, self.hash_filename),
            "log_file": os.path.join(output_dir, "QuickBooks_Auto_Reports.log"),
            "req_log": os.path.join(output_dir, self.request_log),
            "resp_log": os.path.join(output_dir, self.response_log),
        }

    def validate(self) -> None:
        """Validate report configuration.
        
        Raises:
            ValueError: If any required field is empty or invalid
        """
        if not self.key:
            raise ValueError("Report key cannot be empty")
        if not self.name:
            raise ValueError("Report name cannot be empty")
        if not self.qbxml_type:
            raise ValueError("qbXML type cannot be empty")
        if self.query_type not in ("GeneralDetail", "GeneralSummary", "Aging"):
            raise ValueError(
                f"Invalid query_type: {self.query_type}. "
                "Must be GeneralDetail, GeneralSummary, or Aging"
            )
        if not self.csv_filename:
            raise ValueError("CSV filename cannot be empty")
        if not self.excel_filename:
            raise ValueError("Excel filename cannot be empty")
