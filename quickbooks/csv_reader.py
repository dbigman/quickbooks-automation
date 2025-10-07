from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd


def extract_sales_orders_from_csv(file_path: str) -> pd.DataFrame:
    """Parse QuickBooks CSV into a normalized orders DataFrame.
    
    Supports two formats:
    1. Sales Orders by Customer: customer_name in col A, order details in subsequent rows
    2. Sales Orders by Item: product_name in col A, order details in subsequent rows
       with order_number in col E, customer_name in col F

    Returns columns: customer_name, order_type, order_date, order_number,
    memo, amount, open_balance, order_status, delivery_date, entry_date,
    is_revised, is_exchange.
    """
    encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
    df: Optional[pd.DataFrame] = None
    for encoding in encodings:
        try:
            # First try to read with flexible column handling
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            
            # Find the maximum number of columns in any row
            max_cols = 0
            for line in lines:
                cols = len(line.split(','))
                max_cols = max(max_cols, cols)
            
            # Read CSV with the maximum number of columns expected
            column_names = None
            if lines:
                header_cols = lines[0].strip().split(',')
                # Extend header with generic names if needed
                while len(header_cols) < max_cols:
                    header_cols.append(f'Col_{len(header_cols)}')
                column_names = header_cols
            
            df = pd.read_csv(file_path, header=0, encoding=encoding, names=column_names, skiprows=1)
            break
        except UnicodeDecodeError:
            continue
        except Exception:
            # Fallback to simple read with error handling
            try:
                df = pd.read_csv(file_path, header=0, encoding=encoding, on_bad_lines='skip', engine='python')
                break
            except Exception:
                continue
    if df is None:
        raise ValueError("Could not read CSV file with any supported encoding")

    sales_orders: List[Dict[str, Any]] = []
    current_customer: Optional[str] = None
    current_product: Optional[str] = None
    
    # Detect CSV format by checking the first few rows
    csv_format = _detect_csv_format(df)
    
    for _, row in df.iterrows():
        if row.isna().all():
            continue
            
        # Handle "Sales Orders by Item" format
        if csv_format == "by_item":
            # Check if this is a product/item header row
            if pd.notna(row.iloc[0]) and not str(row.iloc[0]).startswith(","):
                item_name = str(row.iloc[0]).strip()
                if (
                    not item_name.startswith("Total ")
                    and item_name != "TOTAL"
                    and item_name != "Subtotal"
                    and item_name != "Parts"
                    and "(" in item_name  # Product names typically have part numbers in parentheses
                ):
                    current_product = item_name
                continue
                
            # Check if this is a sales order line (has "Sales Order" in column B)
            if (
                pd.notna(row.iloc[1])
                and str(row.iloc[1]).strip() == "Sales Order"
                and current_product is not None
            ):
                # For "by item" format: order_number is in column E (index 4), customer in column F (index 5)
                order_data: Dict[str, Any] = {
                    "product_name": current_product,
                    "customer_name": (
                        str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else "Unknown"
                    ),
                    "order_type": str(row.iloc[1]).strip(),
                    "order_date": (
                        _parse_date(str(row.iloc[2]))
                        if pd.notna(row.iloc[2])
                        else None
                    ),
                    "delivery_date": (
                        _parse_date(str(row.iloc[3]))
                        if pd.notna(row.iloc[3])
                        else None
                    ),
                    "order_number": (
                        str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else None
                    ),
                    "quantity": (
                        _parse_amount(row.iloc[6]) if pd.notna(row.iloc[6]) else 0.0
                    ),
                    "invoiced_qty": (
                        _parse_amount(row.iloc[7]) if pd.notna(row.iloc[7]) else 0.0
                    ),
                    "pending_qty": (
                        _parse_amount(row.iloc[8]) if pd.notna(row.iloc[8]) else 0.0
                    ),
                    "amount": (
                        _parse_amount(row.iloc[9]) if pd.notna(row.iloc[9]) else 0.0
                    ),
                    "open_balance": (
                        _parse_amount(row.iloc[10]) if pd.notna(row.iloc[10]) else 0.0
                    ),
                    "memo": "",  # No memo field in by_item format
                }
                # Add basic status info
                order_data.update({
                    "order_status": "OPEN" if order_data["open_balance"] > 0 else "CLOSED",
                    "is_revised": False,
                    "is_exchange": False,
                    "entry_date": None,
                })
                sales_orders.append(order_data)
                
        # Handle "Sales Orders by Customer" format (original logic)
        else:
            if pd.notna(row.iloc[0]) and not str(row.iloc[0]).startswith(","):
                customer_name = str(row.iloc[0]).strip()
                if (
                    not customer_name.startswith("Total ")
                    and customer_name != "TOTAL"
                ):
                    current_customer = customer_name
                continue
            if (
                pd.notna(row.iloc[1])
                and str(row.iloc[1]).strip() == "Sales Order"
                and current_customer is not None
            ):
                order_data: Dict[str, Any] = {
                    "customer_name": current_customer,
                    "order_type": str(row.iloc[1]).strip(),
                    "order_date": (
                        _parse_date(str(row.iloc[2]))
                        if pd.notna(row.iloc[2])
                        else None
                    ),
                    "order_number": (
                        str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else None
                    ),
                    "memo": (
                        str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ""
                    ),
                    "amount": (
                        _parse_amount(row.iloc[5]) if pd.notna(row.iloc[5]) else 0.0
                    ),
                    "open_balance": (
                        _parse_amount(row.iloc[6]) if pd.notna(row.iloc[6]) else 0.0
                    ),
                }
                order_data.update(_extract_memo_info(order_data["memo"]))
                sales_orders.append(order_data)

    if not sales_orders:
        raise ValueError("No sales orders found in the CSV file")

    result_df = pd.DataFrame(sales_orders)
    
    # Add computed fields based on available data
    if "amount" in result_df.columns and "open_balance" in result_df.columns:
        result_df["invoiced_amount"] = (
            result_df["amount"] - result_df["open_balance"]
        )
        result_df["is_fully_paid"] = result_df["open_balance"] == 0
    else:
        result_df["invoiced_amount"] = 0.0
        result_df["is_fully_paid"] = False
        
    if "order_status" in result_df.columns:
        result_df["is_partial"] = result_df["order_status"].str.contains(
            "PARTIAL", na=False
        )
    else:
        result_df["is_partial"] = False
    
    # Sort by customer name and order date (if available)
    sort_columns = []
    if "customer_name" in result_df.columns:
        sort_columns.append("customer_name")
    if "order_date" in result_df.columns:
        sort_columns.append("order_date")
        
    if sort_columns:
        result_df = result_df.sort_values(sort_columns, na_position="last").reset_index(drop=True)
    
    return result_df


def _detect_csv_format(df: pd.DataFrame) -> str:
    """Detect whether this is a 'by_customer' or 'by_item' CSV format.
    
    Returns:
        'by_item' if this appears to be a Sales Orders by Item report
        'by_customer' if this appears to be a Sales Orders by Customer report
    """
    # Look at the first 20 rows to detect the format
    sample_rows = df.head(20)
    
    # Check for indicators of "by_item" format
    by_item_indicators = 0
    by_customer_indicators = 0
    
    for _, row in sample_rows.iterrows():
        if pd.notna(row.iloc[0]):
            cell_value = str(row.iloc[0]).strip()
            
            # "by_item" indicators: product names with part numbers in parentheses
            if "(" in cell_value and ")" in cell_value and not cell_value.startswith("Total"):
                by_item_indicators += 1
                
            # "by_customer" indicators: company/customer names (no parentheses, not product codes)
            elif (
                not "(" in cell_value 
                and not cell_value.startswith("Total")
                and not cell_value == "TOTAL"
                and not cell_value == "Parts"
                and not cell_value == "Subtotal"
                and len(cell_value) > 5  # Customer names are typically longer
            ):
                by_customer_indicators += 1
    
    # Also check column headers or structure
    if len(df.columns) >= 11:  # "by_item" format typically has more columns
        by_item_indicators += 2
    elif len(df.columns) <= 7:  # "by_customer" format typically has fewer columns  
        by_customer_indicators += 2
        
    return "by_item" if by_item_indicators > by_customer_indicators else "by_customer"


def _parse_date(date_str: str) -> Optional[datetime]:
    if not date_str or date_str.strip() == "":
        return None
    try:
        return datetime.strptime(date_str.strip(), "%m/%d/%Y")
    except ValueError:
        try:
            return datetime.strptime(date_str.strip(), "%m/%d/%y")
        except ValueError:
            return None


def _parse_amount(amount_value: Any) -> float:
    if pd.isna(amount_value):
        return 0.0
    try:
        amount_str = str(amount_value).replace(",", "").replace("$", "").strip()
        if amount_str == "" or amount_str == "nan":
            return 0.0
        return float(amount_str)
    except (ValueError, TypeError):
        return 0.0


def _extract_memo_info(memo: str) -> dict:
    info = {
        "order_status": "UNKNOWN",
        "delivery_date": None,
        "entry_date": None,
        "is_revised": False,
        "is_exchange": False,
    }
    if not memo or memo.strip() == "":
        return info
    import re

    memo_upper = memo.upper()
    for pattern in [
        "PARTIAL",
        "ENTERED",
        "DELIVER",
        "REVISED",
        "EXCHANGE",
        "SCHEDULED",
    ]:
        if pattern in memo_upper:
            info["order_status"] = pattern
            break
    info["is_revised"] = "REVISED" in memo_upper
    info["is_exchange"] = "EXCHANGE" in memo_upper
    deliver_match = re.search(r"DELIVER\s+(\d{2}-\d{2}-\d{2})", memo_upper)
    if deliver_match:
        try:
            info["delivery_date"] = datetime.strptime(
                deliver_match.group(1), "%m-%d-%y"
            )
        except ValueError:
            pass
    entered_match = re.search(r"ENTERED\s+(\d{2}-\d{2}-\d{2})", memo_upper)
    if entered_match:
        try:
            info["entry_date"] = datetime.strptime(
                entered_match.group(1), "%m-%d-%y"
            )
        except ValueError:
            pass
    return info
