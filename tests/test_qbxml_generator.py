"""Tests for qbXML generation service."""

import unittest
import xml.etree.ElementTree as ET
from datetime import date

from src.quickbooks_autoreport.services.qbxml_generator import (
    build_report_qbxml,
    validate_xml_structure,
    generate_xml_with_version_fallback,
)


class TestQBXMLGenerator(unittest.TestCase):
    """Test qbXML generation functions."""
    
    def test_build_report_qbxml_profit_loss(self):
        """Test building qbXML for Profit & Loss report."""
        xml = build_report_qbxml(
            version="16.0",
            report_type="ProfitAndLossStandard",
            date_from="2025-01-01",
            date_to="2025-01-31",
            report_key="profit_loss"
        )
        
        # Check that XML is well-formed
        self.assertTrue(validate_xml_structure(xml))
        
        # Check for expected elements
        root = ET.fromstring(xml)
        self.assertEqual(root.find(".//GeneralSummaryReportType").text, "ProfitAndLossStandard")
        self.assertEqual(root.find(".//FromReportDate").text, "2025-01-01")
        self.assertEqual(root.find(".//ToReportDate").text, "2025-01-31")
    
    def test_build_report_qbxml_open_sales_orders(self):
        """Test building qbXML for Open Sales Orders report."""
        xml = build_report_qbxml(
            version="16.0",
            report_type="OpenSalesOrderByItem",
            report_key="open_sales_orders"
        )
        
        # Check that XML is well-formed
        self.assertTrue(validate_xml_structure(xml))
        
        # Check for expected elements
        root = ET.fromstring(xml)
        self.assertEqual(root.find(".//GeneralDetailReportType").text, "OpenSalesOrderByItem")
        # Should not have date elements for reports that don't use date ranges
        self.assertIsNone(root.find(".//FromReportDate"))
        self.assertIsNone(root.find(".//ToReportDate"))
    
    def test_build_report_qbxml_aging_report(self):
        """Test building qbXML for Aging report."""
        xml = build_report_qbxml(
            version="16.0",
            report_type="APAgingDetail",
            date_to="2025-01-31",
            report_key="ap_aging_detail"
        )
        
        # Check that XML is well-formed
        self.assertTrue(validate_xml_structure(xml))
        
        # Check for expected elements
        root = ET.fromstring(xml)
        self.assertEqual(root.find(".//AgingReportType").text, "APAgingDetail")
        self.assertEqual(root.find(".//ToReportDate").text, "2025-01-31")
        self.assertEqual(root.find(".//ReportAgingAsOf").text, "ReportEndDate")
    
    def test_build_report_qbxml_with_invalid_dates(self):
        """Test building qbXML with invalid dates falls back to current month."""
        xml = build_report_qbxml(
            version="16.0",
            report_type="ProfitAndLossStandard",
            date_from="invalid-date",
            date_to="also-invalid",
            report_key="profit_loss"
        )
        
        # Should still generate valid XML
        self.assertTrue(validate_xml_structure(xml))
        
        # Should have valid dates (current month)
        root = ET.fromstring(xml)
        from_date = root.find(".//FromReportDate").text
        to_date = root.find(".//ToReportDate").text
        
        # Should be valid date format
        try:
            date.fromisoformat(from_date)
            date.fromisoformat(to_date)
        except ValueError:
            self.fail("Generated dates should be valid ISO format")
    
    def test_validate_xml_structure_valid(self):
        """Test validating valid XML structure."""
        valid_xml = """<?xml version="1.0" encoding="UTF-8"?>
<?qbxml version="16.0"?>
<QBXML>
  <QBXMLMsgsRq onError="continueOnError">
    <GeneralSummaryReportQueryRq requestID="1">
      <GeneralSummaryReportType>ProfitAndLossStandard</GeneralSummaryReportType>
      <DisplayReport>true</DisplayReport>
    </GeneralSummaryReportQueryRq>
  </QBXMLMsgsRq>
</QBXML>"""
        
        self.assertTrue(validate_xml_structure(valid_xml))
    
    def test_validate_xml_structure_invalid(self):
        """Test validating invalid XML structure."""
        invalid_xml = """<?xml version="1.0" encoding="UTF-8"?>
<QBXML>
  <UnclosedTag>
</QBXML>"""
        
        self.assertFalse(validate_xml_structure(invalid_xml))
    
    def test_generate_xml_with_version_fallback(self):
        """Test XML generation with version fallback."""
        xml, version = generate_xml_with_version_fallback(
            report_type="ProfitAndLossStandard",
            date_from="2025-01-01",
            date_to="2025-01-31",
            report_key="profit_loss"
        )
        
        # Should return valid XML
        self.assertTrue(validate_xml_structure(xml))
        self.assertIn(version, ["16.0", "13.0"])
        
        # Check that XML contains the report type
        root = ET.fromstring(xml)
        self.assertEqual(root.find(".//GeneralSummaryReportType").text, "ProfitAndLossStandard")
    
    def test_build_report_qbxml_purchase_by_vendor_detail(self):
        """Test building qbXML for Purchase by Vendor Detail report (special date handling)."""
        xml = build_report_qbxml(
            version="16.0",
            report_type="PurchasesByVendorDetail",
            date_from="2025-01-01",
            date_to="2025-01-31",
            report_key="purchase_by_vendor_detail"
        )
        
        # Check that XML is well-formed
        self.assertTrue(validate_xml_structure(xml))
        
        # Check for expected elements (purchase reports have dates directly under query)
        root = ET.fromstring(xml)
        self.assertEqual(root.find(".//GeneralDetailReportType").text, "PurchasesByVendorDetail")
        self.assertEqual(root.find(".//FromReportDate").text, "2025-01-01")
        self.assertEqual(root.find(".//ToReportDate").text, "2025-01-31")
    
    def test_all_report_configs_generate_valid_xml(self):
        """Test that all report configurations can generate valid XML."""
        from src.quickbooks_autoreport.config import REPORT_CONFIGS
        
        for report_key, config in REPORT_CONFIGS.items():
            with self.subTest(report_key=report_key):
                if config.get("uses_date_range"):
                    xml = build_report_qbxml(
                        version="16.0",
                        report_type=config["qbxml_type"],
                        date_from="2025-01-01",
                        date_to="2025-01-31",
                        report_key=report_key
                    )
                else:
                    xml = build_report_qbxml(
                        version="16.0",
                        report_type=config["qbxml_type"],
                        report_key=report_key
                    )
                
                # All should generate valid XML
                self.assertTrue(validate_xml_structure(xml), 
                              f"XML validation failed for {report_key}")
                
                # Check that the correct report type is included
                root = ET.fromstring(xml)
                if config["query"] == "GeneralSummary":
                    report_type_elem = root.find(".//GeneralSummaryReportType")
                elif config["query"] == "Aging":
                    report_type_elem = root.find(".//AgingReportType")
                else:
                    report_type_elem = root.find(".//GeneralDetailReportType")
                
                self.assertIsNotNone(report_type_elem, 
                                   f"Report type element not found for {report_key}")
                self.assertEqual(report_type_elem.text, config["qbxml_type"])


if __name__ == "__main__":
    unittest.main()