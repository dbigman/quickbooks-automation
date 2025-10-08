"""Report parsing service for QuickBooks Auto Reporter."""

import xml.etree.ElementTree as ET
from typing import List, Tuple

from ..utils.logging_utils import log_data, log_error


def parse_report_rows(resp_xml: str) -> Tuple[List[str], List[List[str]]]:
    """Parse QuickBooks report response XML with enhanced error handling.
    
    Args:
        resp_xml: XML response string from QuickBooks
        
    Returns:
        Tuple of (headers_list, rows_list)
        
    Raises:
        RuntimeError: If parsing fails
    """
    try:
        root = ET.fromstring(resp_xml)

        # Look for the response element
        rs = root.find(".//GeneralDetailReportQueryRs")
        if rs is None:
            # Try to find any report query response
            for el in root.iter():
                if el.tag.endswith("ReportQueryRs"):
                    rs = el
                    break

        # Check for errors in the response
        if rs is None:
            raise RuntimeError("No ReportQueryRs found in response")

        status_code = rs.get("statusCode")
        if status_code not in (None, "0"):
            status_msg = rs.get("statusMessage", "Unknown error")
            raise RuntimeError(
                f"ReportQuery failed: status={status_code}, message={status_msg}"
            )

        # Find the report data
        rep = rs.find(".//ReportRet")
        if rep is None:
            raise RuntimeError("No ReportRet found in response")

        # Extract column headers
        headers = []
        col_descs = rep.findall(".//ColDesc")
        for c in col_descs:
            title = (c.findtext("ColTitle") or "").strip()
            if title:
                headers.append(title)

        # If no headers found, create default ones
        if not headers:
            headers = [f"Column_{i}" for i in range(1, 16)]

        rows = []

        def add_text_row(text: str) -> None:
            """Add a text row (like subtotals) to the results."""
            row = [""] * len(headers)
            if text.strip():
                row[0] = text.strip()
                rows.append(row)

        def walk(node) -> None:
            """Recursively walk through the XML structure."""
            for child in list(node):
                tag = child.tag

                if tag.endswith("TextRow"):
                    # Handle text rows (headers, subtotals, etc.)
                    vals = [cd.get("value", "") for cd in child.findall(".//ColData")]
                    text = (vals[0] if vals else child.get("value", "")).strip()
                    if text:
                        add_text_row(text)
                    walk(child)

                elif tag.endswith("DataRow"):
                    # Handle data rows
                    row = [""] * len(headers)
                    col_data_elements = child.findall("ColData")

                    for cd in col_data_elements:
                        val = cd.get("value", "")
                        col_id = cd.get("colID")

                        # Try to place value in correct column
                        if col_id and col_id.isdigit():
                            idx = int(col_id) - 1
                            if 0 <= idx < len(headers):
                                row[idx] = val
                        else:
                            # Find first empty column
                            for i in range(len(headers)):
                                if row[i] == "":
                                    row[i] = val
                                    break

                    # Only add non-empty rows
                    if any(cell.strip() for cell in row):
                        rows.append(row)
                    walk(child)

                elif tag.endswith("SubtotalRow"):
                    add_text_row("Subtotal")
                    walk(child)
                else:
                    walk(child)

        # Start walking from ReportData
        data = rep.find(".//ReportData")
        if data is not None:
            walk(data)
        else:
            # If no ReportData, try walking from the report root
            walk(rep)

        return headers, rows

    except ET.ParseError as pe:
        raise RuntimeError(f"XML parsing error: {pe}")
    except Exception as e:
        raise RuntimeError(f"Error parsing report response: {e}")


def parse_salesorders_to_rows(resp_xml: str) -> Tuple[List[str], List[List[str]]]:
    """Parse Sales Order query response (fallback for Open Sales Orders).
    
    Args:
        resp_xml: XML response string from QuickBooks
        
    Returns:
        Tuple of (headers_list, rows_list)
        
    Raises:
        RuntimeError: If parsing fails
    """
    root = ET.fromstring(resp_xml)
    rs = root.find(".//SalesOrderQueryRs")
    if rs is None or rs.get("statusCode") not in (None, "0"):
        raise RuntimeError("SalesOrderQuery failed")
    
    headers = [
        "RefNumber",
        "TxnDate",
        "Customer",
        "IsFullyInvoiced",
        "IsManuallyClosed",
    ]
    rows = []
    for so in rs.findall("SalesOrderRet"):
        fully = (so.findtext("IsFullyInvoiced") or "").strip().lower() == "true"
        closed = (so.findtext("IsManuallyClosed") or "").strip().lower() == "true"
        if fully or closed:
            continue
        rows.append(
            [
                so.findtext("RefNumber") or "",
                so.findtext("TxnDate") or "",
                so.findtext("CustomerRef/FullName") or "",
                str(fully).lower(),
                str(closed).lower(),
            ]
        )
    return headers, rows


def handle_missing_columns(headers: List[str], rows: List[List[str]]) -> Tuple[List[str], List[List[str]]]:
    """Handle missing columns gracefully with default values.
    
    Args:
        headers: List of column headers
        rows: List of data rows
        
    Returns:
        Tuple of (normalized_headers, normalized_rows)
    """
    if not headers:
        headers = [f"Column_{i}" for i in range(1, 16)]
    
    # Ensure all rows have the same number of columns
    max_cols = len(headers)
    normalized_rows = []
    
    for row in rows:
        if len(row) < max_cols:
            # Pad with empty values
            normalized_row = row + [""] * (max_cols - len(row))
        elif len(row) > max_cols:
            # Truncate extra columns
            normalized_row = row[:max_cols]
        else:
            normalized_row = row
        
        normalized_rows.append(normalized_row)
    
    return headers, normalized_rows


def handle_empty_values(rows: List[List[str]]) -> List[List[str]]:
    """Handle empty values in data rows.
    
    Args:
        rows: List of data rows
        
    Returns:
        List of rows with empty values handled
    """
    cleaned_rows = []
    
    for row in rows:
        cleaned_row = []
        for cell in row:
            # Convert None to empty string and strip whitespace
            cleaned_cell = "" if cell is None else str(cell).strip()
            cleaned_row.append(cleaned_cell)
        cleaned_rows.append(cleaned_row)
    
    return cleaned_rows


def validate_parsed_data(headers: List[str], rows: List[List[str]]) -> bool:
    """Validate parsed data for consistency.
    
    Args:
        headers: List of column headers
        rows: List of data rows
        
    Returns:
        True if data is valid, False otherwise
    """
    if not headers:
        return False
    
    # Check if all rows have the same number of columns
    for row in rows:
        if len(row) != len(headers):
            return False
    
    return True


def parse_and_validate_response(resp_xml: str, report_type: str = "standard") -> Tuple[List[str], List[List[str]]]:
    """Parse and validate XML response with comprehensive error handling.
    
    Args:
        resp_xml: XML response string from QuickBooks
        report_type: Type of report ("standard" or "salesorder")
        
    Returns:
        Tuple of (headers_list, rows_list)
        
    Raises:
        RuntimeError: If parsing or validation fails
    """
    try:
        if report_type == "salesorder":
            headers, rows = parse_salesorders_to_rows(resp_xml)
        else:
            headers, rows = parse_report_rows(resp_xml)
        
        # Handle missing columns
        headers, rows = handle_missing_columns(headers, rows)
        
        # Handle empty values
        rows = handle_empty_values(rows)
        
        # Validate data consistency
        if not validate_parsed_data(headers, rows):
            log_error("Parsed data validation failed")
        
        log_data(f"Parsed {len(headers)} columns, {len(rows)} rows")
        
        return headers, rows
        
    except Exception as e:
        log_error(f"Failed to parse response: {e}")
        raise