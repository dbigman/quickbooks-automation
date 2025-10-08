"""qbXML response parser adapter for QuickBooks Auto Reporter.

Wraps report_parser to provide a clean interface for parsing XML responses.
"""

from typing import List, Tuple, Optional

from quickbooks_autoreport.services.report_parser import (
    extract_error_info as extract_error_info_base,
    parse_report_rows as parse_report_rows_base,
)


class XMLParser:
    """Parses qbXML responses."""

    @staticmethod
    def parse_report_response(xml: str) -> Tuple[List[str], List[List[str]]]:
        """Parse report response into headers and rows.

        Args:
            xml: XML response string

        Returns:
            Tuple of (headers list, rows list of lists)
        """
        return parse_report_rows_base(xml)

    @staticmethod
    def extract_error_info(xml: str) -> Optional[dict]:
        """Extract error information from response.

        Args:
            xml: XML response string

        Returns:
            Dictionary with error details, or None if not an error
        """
        return extract_error_info_base(xml)