"""qbXML request builder adapter for QuickBooks Auto Reporter.

Wraps qbxml_generator to provide a clean interface for XML requests.
"""

from typing import Optional

from quickbooks_autoreport.domain.report_config import ReportConfig
from quickbooks_autoreport.services.qbxml_generator import (
    build_report_qbxml as build_report_qbxml_base,
    normalize_xml as normalize_xml_base,
)


class XMLBuilder:
    """Builds qbXML requests."""

    @staticmethod
    def build_report_request(
        config: ReportConfig,
        version: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> str:
        """Build qbXML request for a report.

        Args:
            config: Report configuration
            version: qbXML version
            date_from: Optional start date
            date_to: Optional end date

        Returns:
            qbXML request string
        """
        xml = build_report_qbxml_base(
            version=version,
            report_type=config.qbxml_type,
            report_key=config.key,
            date_from=date_from,
            date_to=date_to,
        )
        return normalize_xml_base(xml)

    @staticmethod
    def normalize_xml(xml: str) -> str:
        """Normalize XML to avoid parser errors.

        Args:
            xml: XML string

        Returns:
            Normalized XML string
        """
        return normalize_xml_base(xml)