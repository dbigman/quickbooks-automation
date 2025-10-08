"""qbXML request generation service for QuickBooks Auto Reporter."""

import datetime as dt
from typing import Optional

from ..config import REPORT_CONFIGS, QBXML_VERSION_PRIMARY, QBXML_VERSION_FALLBACK
from ..utils.logging_utils import log_info, log_error


def build_report_qbxml(
    version: str,
    report_type: str,
    date_from: str = None,
    date_to: str = None,
    report_key: str = None,
) -> str:
    """Build qbXML for the appropriate report query with optional date range.
    
    Args:
        version: qbXML version to use
        report_type: QuickBooks report type
        date_from: Start date for reports with date ranges (YYYY-MM-DD)
        date_to: End date for reports with date ranges (YYYY-MM-DD)
        report_key: Report configuration key
        
    Returns:
        Complete qbXML request string
    """
    config = REPORT_CONFIGS.get(report_key, {}) if report_key else {}
    query = config.get("query", "GeneralDetail")
    uses_date_range = config.get("uses_date_range", False)

    # Build XML based on the working examples
    if query == "GeneralSummary":
        open_tag = "GeneralSummaryReportQueryRq"
        type_tag = "GeneralSummaryReportType"
    elif query == "Aging":
        open_tag = "AgingReportQueryRq"
        type_tag = "AgingReportType"
    else:
        open_tag = "GeneralDetailReportQueryRq"
        type_tag = "GeneralDetailReportType"

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<?qbxml version="{version}"?>',
        "<QBXML>",
        '  <QBXMLMsgsRq onError="continueOnError">',
        f'    <{open_tag} requestID="1">',
        f"      <{type_tag}>{report_type}</{type_tag}>",
    ]

    # Handle different date structures based on working examples
    if query == "Aging":
        # Aging reports use ReportPeriod with ToReportDate and ReportAgingAsOf
        as_of_date = date_to if date_to else dt.date.today().strftime("%Y-%m-%d")
        xml_parts.extend(
            [
                "      <ReportPeriod>",
                f"        <ToReportDate>{as_of_date}</ToReportDate>",
                "      </ReportPeriod>",
                "      <ReportAgingAsOf>ReportEndDate</ReportAgingAsOf>",
                "      <DisplayReport>true</DisplayReport>",
            ]
        )
    elif uses_date_range and date_from and date_to:
        # Validate dates
        try:
            dt.datetime.strptime(date_from, "%Y-%m-%d")
            dt.datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            today = dt.date.today()
            first_day = today.replace(day=1)
            date_from = first_day.strftime("%Y-%m-%d")
            date_to = today.strftime("%Y-%m-%d")

        # Different reports use different date structures
        if report_key == "purchase_by_vendor_detail":
            # Purchase reports have dates directly under the query element
            xml_parts.extend(
                [
                    f"      <FromReportDate>{date_from}</FromReportDate>",
                    f"      <ToReportDate>{date_to}</ToReportDate>",
                    "      <DisplayReport>true</DisplayReport>",
                ]
            )
        else:
            # Most reports use ReportPeriod wrapper
            xml_parts.extend(
                [
                    "      <DisplayReport>true</DisplayReport>",
                    "      <ReportPeriod>",
                    f"        <FromReportDate>{date_from}</FromReportDate>",
                    f"        <ToReportDate>{date_to}</ToReportDate>",
                    "      </ReportPeriod>",
                ]
            )
    else:
        # Reports without date ranges (like Open Sales Orders)
        xml_parts.append("      <DisplayReport>true</DisplayReport>")

    xml_parts.extend(
        [
            f"    </{open_tag}>",
            "  </QBXMLMsgsRq>",
            "</QBXML>",
        ]
    )

    return "\n".join(xml_parts)


def build_salesorder_query(version: str) -> str:
    """Build qbXML for Sales Order query (fallback for Open Sales Orders).
    
    Args:
        version: qbXML version to use
        
    Returns:
        Complete qbXML request string
    """
    return f"""<?xml version="1.0"?>
<?qbxml version="{version}"?>
<QBXML><QBXMLMsgsRq onError="stopOnError">
  <SalesOrderQueryRq iterator="Start">
    <MaxReturned>200</MaxReturned>
    <IncludeRetElement>RefNumber</IncludeRetElement>
    <IncludeRetElement>TxnDate</IncludeRetElement>
    <IncludeRetElement>CustomerRef</IncludeRetElement>
    <IncludeRetElement>IsFullyInvoiced</IncludeRetElement>
    <IncludeRetElement>IsManuallyClosed</IncludeRetElement>
  </SalesOrderQueryRq>
</QBXMLMsgsRq></QBXML>"""


def validate_xml_structure(xml: str) -> bool:
    """Validate XML structure for common issues.
    
    Args:
        xml: XML string to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        import xml.etree.ElementTree as ET
        ET.fromstring(xml)
        return True
    except ET.ParseError:
        return False


def generate_xml_with_version_fallback(
    report_type: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    report_key: Optional[str] = None,
) -> tuple[str, str]:
    """Generate XML with version fallback logic.
    
    Args:
        report_type: QuickBooks report type
        date_from: Start date for reports with date ranges
        date_to: End date for reports with date ranges
        report_key: Report configuration key
        
    Returns:
        Tuple of (xml_string, version_used)
    """
    # Try primary version first
    xml = build_report_qbxml(QBXML_VERSION_PRIMARY, report_type, date_from, date_to, report_key)
    
    if validate_xml_structure(xml):
        return xml, QBXML_VERSION_PRIMARY
    
    # Fallback to secondary version
    xml = build_report_qbxml(QBXML_VERSION_FALLBACK, report_type, date_from, date_to, report_key)
    return xml, QBXML_VERSION_FALLBACK


def test_xml_generation() -> None:
    """Test XML generation for all report types."""
    print("🧪 Testing XML generation for all report types...")

    test_date_from = "2025-08-01"
    test_date_to = "2025-08-15"

    for report_key, config in REPORT_CONFIGS.items():
        try:
            print(f"\n📋 Testing {config['name']} ({report_key})...")

            # Generate XML
            xml, version = generate_xml_with_version_fallback(
                config["qbxml_type"], test_date_from, test_date_to, report_key
            )

            print(f"✅ Generated XML with version {version} ({len(xml)} chars)")
            print("📄 XML Preview:")
            print(xml[:200] + "..." if len(xml) > 200 else xml)

            # Validate structure
            if validate_xml_structure(xml):
                print("✅ XML structure is valid")
            else:
                print("❌ XML structure is invalid")

        except Exception as e:
            print(f"❌ Error testing {report_key}: {e}")

    print("\n🏁 XML generation test completed!")