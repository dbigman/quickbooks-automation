import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402
from quickbooks_autoreport.adapters.logger_adapter import LoggerAdapter  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_builder import XMLBuilder  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_parser import XMLParser  # noqa: E402
from quickbooks_autoreport.domain.report_config import ReportConfig  # noqa: E402
from quickbooks_autoreport.domain.report_result import ReportResult  # noqa: E402
from quickbooks_autoreport.services.report_generator import ReportGenerator  # noqa: E402


def test_report_generator_success(tmp_path):
    logger = Mock()
    file_adapter = Mock(spec=FileAdapter)
    logger_adapter = Mock(spec=LoggerAdapter)
    xml_builder = Mock(spec=XMLBuilder)
    xml_parser = Mock(spec=XMLParser)

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

    xml_builder.build_report_request.return_value = "<request/>"
    xml_parser.extract_error_info.return_value = None
    xml_parser.parse_report_response.return_value = (["TxnID", "RefNumber"], [["123", "SO001"]])
    file_adapter.read_hash.return_value = None

    gen = ReportGenerator(file_adapter, logger_adapter, xml_builder, xml_parser, logger)
    result = gen.generate_report(config, str(tmp_path))

    assert isinstance(result, ReportResult)
    assert result.report_key == config.key
    assert result.rows == 1
    assert result.changed is True


def test_report_generator_handles_error(tmp_path):
    logger = Mock()
    file_adapter = Mock(spec=FileAdapter)
    logger_adapter = Mock(spec=LoggerAdapter)
    xml_builder = Mock(spec=XMLBuilder)
    xml_parser = Mock(spec=XMLParser)

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

    xml_builder.build_report_request.return_value = "<request/>"
    xml_parser.extract_error_info.return_value = {"statusCode": "500", "message": "Test error"}
    xml_parser.parse_report_response.return_value = ([], [])

    gen = ReportGenerator(file_adapter, logger_adapter, xml_builder, xml_parser, logger)
    result = gen.generate_report(config, str(tmp_path))

    assert result.success is False
    assert "QuickBooks error" in result.error