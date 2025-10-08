"""End-to-end report flow integration tests.

Validates the complete pipeline for a report type using mock QuickBooks responses.
"""

import sys
from pathlib import Path
from unittest.mock import Mock

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402
from quickbooks_autoreport.adapters.logger_adapter import LoggerAdapter  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_builder import XMLBuilder  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_parser import XMLParser  # noqa: E402
from quickbooks_autoreport.domain.report_config import ReportConfig  # noqa: E402
from quickbooks_autoreport.domain.report_result import ReportResult  # noqa: E402
from quickbooks_autoreport.services.report_generator import ReportGenerator  # noqa: E402


def test_end_to_end_report_flow(tmp_path):
    """Test full report generation pipeline with mocked QuickBooks."""
    logger_adapter = LoggerAdapter()
    logger = logger_adapter.setup_logger("test")
    file_adapter = FileAdapter(logger)
    xml_builder = XMLBuilder()
    xml_parser = XMLParser()

    # Setup mock responses
    mock_response = """<?xml version="1.0"?>
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
    xml_parser.extract_error_info.return_value = None
    xml_parser.parse_report_response.return_value = (
        ["TxnID", "RefNumber"],
        [["123", "SO001"]],
    )

    # Configure report
    config = ReportConfig(
        key="open_sales_orders",
        name="Open Sales Orders by Item",
        qbxml_type="OpenSalesOrderByItem",
        query_type="GeneralDetail",
        csv_filename="Open_Sales_Orders_By_Item.csv",
        excel_filename="Open_Sales_Orders_By_Item.xlsx",
        hash_filename="Open_Sales_Orders_By_Item.hash",
        request_log="open_so_request.xml",
        response_log="open_so_response.xml",
        uses_date_range=False,
    )

    generator = ReportGenerator(file_adapter, logger_adapter, xml_builder, xml_parser, logger)
    result = generator.generate_report(config, str(tmp_path))

    # Validate result
    assert isinstance(result, ReportResult)
    assert result.success is True
    assert result.rows == 1
    assert result.changed is True
    assert result.excel_created is True

    # Verify files were written
    assert (tmp_path / "Open_Sales_Orders_By_Item.csv").exists()
    assert (tmp_path / "open_so_request.xml").exists()
    assert (tmp_path / "open_so_response.xml").exists()