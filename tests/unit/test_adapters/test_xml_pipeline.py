import sys
from pathlib import Path

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.quickbooks.xml_builder import XMLBuilder  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_parser import XMLParser  # noqa: E402
from quickbooks_autoreport.domain.report_config import ReportConfig


def test_xml_builder_generates_valid_xml():
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
    xml = XMLBuilder.build_report_request(config, version="16.0")
    assert "<?xml" in xml
    assert "OpenSalesOrderByItem" in xml


def test_xml_parser_extracts_headers_and_rows():
    sample = """<?xml version="1.0"?>
    <QBXML>
    <QBXMLMsgsRs>
    <SalesOrderQueryRs>
    <SalesOrderRet>
    <TxnID>123</TxnID>
    <RefNumber>SO001</RefNumber>
    </SalesOrderRet>
    <SalesOrderRet>
    <TxnID>124</TxnID>
    <RefNumber>SO002</RefNumber>
    </SalesOrderRet>
    </SalesOrderQueryRs>
    </QBXMLMsgsRs>
    </QBXML>"""
    headers, rows = XMLParser.parse_report_response(sample)
    assert isinstance(headers, list)
    assert isinstance(rows, list)
    assert len(rows) == 2
    assert rows[0][0] == "123"
    assert rows[1][0] == "124"


def test_xml_parser_error_extraction():
    error_xml = """<?xml version="1.0"?>
    <QBXML>
    <QBXMLMsgsRs>
    <SalesOrderQueryRs statusCode="500">
    <ErrorMessage>Test error</ErrorMessage>
    </SalesOrderQueryRs>
    </QBXMLMsgsRs>
    </QBXML>"""
    error = XMLParser.extract_error_info(error_xml)
    assert error is not None
    assert "500" in str(error)