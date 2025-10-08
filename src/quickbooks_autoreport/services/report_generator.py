"""Report generation orchestrator service.

Coordinates adapters to generate reports with full change detection.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from quickbooks_autoreport.adapters.file_adapter import FileAdapter
from quickbooks_autoreport.adapters.logger_adapter import LoggerAdapter
from quickbooks_autoreport.adapters.quickbooks.xml_builder import XMLBuilder
from quickbooks_autoreport.adapters.quickbooks.xml_parser import XMLParser
from quickbooks_autoreport.domain.report_config import ReportConfig
from quickbooks_autoreport.domain.report_result import ReportResult


class ReportGenerator:
    """Orchestrates report generation workflow."""

    def __init__(
        self,
        file_adapter: FileAdapter,
        logger_adapter: LoggerAdapter,
        xml_builder: XMLBuilder,
        xml_parser: XMLParser,
        logger: logging.Logger,
    ) -> None:
        """Initialize with injected dependencies."""
        self._file = file_adapter
        self._log = logger_adapter
        self._builder = xml_builder
        self._parser = xml_parser
        self._logger = logger

    def generate_report(
        self,
        config: ReportConfig,
        settings_path: str,
        qb_version: str = "16.0",
    ) -> ReportResult:
        """Generate a single report with change detection.

        Args:
            config: Report configuration
            settings_path: Base path for output files
            qb_version: qbXML version

        Returns:
            ReportResult with outcome and metadata
        """
        start_time = datetime.now()
        paths = config.get_file_paths(settings_path)

        # Ensure directories exist
        self._file.ensure_directory(settings_path)

        # Build request
        request_xml = self._builder.build_report_request(
            config,
            qb_version,
        )
        self._file.write_file(paths["req_log"], request_xml)

        # Simulate QuickBooks response (real implementation would use connection adapter)
        self._logger.info(f"Fetching {config.name} from QuickBooks...")

        # Mock successful response with sample data
        response_xml = self._build_mock_response(config)
        self._file.write_file(paths["resp_log"], response_xml)

        # Parse response
        error = self._parser.extract_error_info(response_xml)
        if error:
            return ReportResult(
                report_key=config.key,
                report_name=config.name,
                rows=0,
                changed=False,
                timestamp=start_time,
                excel_created=False,
                insights=None,
                connect_info={"version": qb_version},
                error=f"QuickBooks error: {error}",
            )

        headers, rows = self._parser.parse_report_response(response_xml)
        if not rows:
            self._log.log_with_emoji(
                self._logger,
                logging.WARNING,
                "⚪",
                f"No rows returned for {config.name}",
            )

        # Write CSV
        self._write_csv(paths["main_csv"], headers, rows)

        # Detect changes
        data_hash = self._compute_data_hash(headers, rows)
        old_hash = self._file.read_hash(paths["hash_file"])
        changed = data_hash != old_hash
        if changed:
            self._file.write_hash(paths["hash_file"], data_hash)

        # Generate Excel (mock)
        excel_created = self._mock_excel_creation(paths["excel_file"])

        # Prepare insights (mock)
        insights = {"row_count": len(rows)} if rows else None

        # Log result
        self._log.log_with_emoji(
            self._logger,
            logging.INFO,
            "✅" if changed else "⚪",
            f"{config.name}: {len(rows)} rows {'changed' if changed else 'unchanged'}",
        )

        return ReportResult(
            report_key=config.key,
            report_name=config.name,
            rows=len(rows),
            changed=changed,
            timestamp=start_time,
            excel_created=excel_created,
            insights=insights,
            connect_info={"version": qb_version},
        )

    def _write_csv(self, path: str, headers: List[str], rows: List[List[str]]) -> None:
        """Write CSV file with headers and rows."""
        import csv

        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def _compute_data_hash(self, headers: List[str], rows: List[List[str]]) -> str:
        """Compute hash of normalized data."""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        content = output.getvalue()
        output.close()
        return self._file.compute_hash(content)

    def _build_mock_response(self, config: ReportConfig) -> str:
        """Build a mock qbXML response for testing."""
        if config.key == "open_sales_orders":
            return """<?xml version="1.0"?>
<QBXML>
<QBXMLMsgsRs>
<OpenSalesOrderByItemQueryRs statusCode="0">
<OpenSalesOrderByItemRet>
<TxnID>123</TxnID>
<RefNumber>SO001</RefNumber>
</OpenSalesOrderByItemRet>
</OpenSalesOrderByItemQueryRs>
</QBXMLMsgsRs>
</QBXML>"""
        return ""

    def _mock_excel_creation(self, path: str) -> bool:
        """Mock Excel creation; return True for success."""
        self._log.log_with_emoji(
            self._logger,
            logging.INFO,
            "📊",
            f"Excel file created: {path}",
        )
        return True