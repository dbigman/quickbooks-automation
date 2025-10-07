from __future__ import annotations

from typing import Any, Dict, List
import os

import pandas as pd
from datetime import datetime, timedelta

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # dotenv not available, environment variables should be set externally

try:
    from connector import OdooConnector  # type: ignore
except Exception:  # pragma: no cover
    OdooConnector = None  # type: ignore


def calculate_eta_date_from_order_date(order_date: str | None) -> str | None:
    """Calculate ETA Date as 10 weekdays from Order Date.
    
    Args:
        order_date: String-like order date (e.g., 'YYYY-MM-DD HH:MM:SS', 'YYYY-MM-DD', or ISO 8601)
        
    Returns:
        Date string in 'YYYY-MM-DD' format (10 weekdays later) or None if invalid
    """
    if not order_date:
        return None
        
    try:
        # Parse the order date (handle Odoo format: YYYY-MM-DD HH:MM:SS)
        if isinstance(order_date, str):
            # Handle various date formats from Odoo
            if order_date.endswith('Z'):
                dt = datetime.fromisoformat(order_date.replace('Z', '+00:00'))
            elif '+' in order_date and 'T' in order_date:
                dt = datetime.fromisoformat(order_date)
            elif ' ' in order_date:  # Odoo format: "YYYY-MM-DD HH:MM:SS"
                dt = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')
            elif 'T' in order_date:  # ISO format without timezone
                dt = datetime.fromisoformat(order_date)
            else:
                # Handle simple date format: "YYYY-MM-DD"
                dt = datetime.strptime(order_date, '%Y-%m-%d')
        else:
            return None
            
        # Calculate 10 weekdays (business days) from order date
        current_date = dt.date()
        weekdays_added = 0
        
        while weekdays_added < 10:
            current_date += timedelta(days=1)
            # Monday=0, Sunday=6; weekdays are 0-4
            if current_date.weekday() < 5:  # Monday to Friday
                weekdays_added += 1
        
        # Return normalized date string (YYYY-MM-DD)
        return current_date.isoformat()
        
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Warning: Could not calculate ETA date from '{order_date}': {e}")
        return None


def format_odoo_date_to_iso8601(date_str: str | None) -> str | None:
    """Normalize an Odoo date string to an Excel-compatible timestamp string.
    
    Args:
        date_str: Date string from Odoo (e.g., 'YYYY-MM-DD HH:MM:SS', 'YYYY-MM-DD', or ISO 8601)
        
    Returns:
        Normalized timestamp string 'YYYY-MM-DD HH:MM:SS' when parseable, otherwise None.
        Note: Returns timezone-naive format for Excel compatibility.
    """
    if not date_str:
        return None
        
    try:
        # Odoo typically returns dates in 'YYYY-MM-DD HH:MM:SS' format
        # Parse and convert to a normalized '...Z' timestamp for consistency
        if isinstance(date_str, str):
            # Handle various Odoo date formats
            formats_to_try = [
                "%Y-%m-%d %H:%M:%S",  # Standard Odoo datetime
                "%Y-%m-%d",           # Date only
                "%Y-%m-%dT%H:%M:%S",  # Already ISO-ish
                "%Y-%m-%dT%H:%M:%SZ", # Already ISO 8601
            ]
            
            for fmt in formats_to_try:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    # Return in Excel-compatible format WITHOUT timezone
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
                    
        return None  # Could not parse
        
    except Exception:
        return None


def get_formula_info_from_bom(
    item_codes: List[str], logger
) -> Dict[str, Dict[str, str]]:
    """Fetch formula metadata from BOM for given item codes.

    Returns mapping: item_code -> {"formula_name": str, "reference": str}
    """
    if not item_codes:
        logger.info(
            "No item codes provided for BOM lookup; skipping formula enrichment"
        )
        return {}
    if OdooConnector is None:
        logger.info(
            "Odoo connector not available - cannot fetch formula information"
        )
        return {}
    try:
        odoo_connector = OdooConnector(logger)
        try:
            odoo_connector.authenticate()
        except Exception as auth_error:
            if "Missing Odoo configuration" in str(auth_error):
                logger.info(
                    "Odoo configuration not found - skipping formula enhancement"
                )
                return {}
            raise

        # Find products by default_code in provided codes
        product_domain = [["default_code", "in", item_codes]]
        product_ids = odoo_connector.execute_kw(
            "product.product", "search", [product_domain], {"limit": 1000}
        )
        if not product_ids:
            logger.warning("No products found for the given item codes")
            return {}

        products = odoo_connector.execute_kw(
            "product.product",
            "read",
            [product_ids],
            {"fields": ["id", "default_code", "name", "product_tmpl_id"]},
        )
        product_id_to_code: Dict[int, str] = {
            p["id"]: p.get("default_code")
            for p in products
            if p.get("default_code")
        }
        product_id_to_template: Dict[int, int | None] = {
            p["id"]: (
                p["product_tmpl_id"][0] if p.get("product_tmpl_id") else None
            )
            for p in products
        }
        template_to_products: Dict[int, List[int]] = {}
        for pid, tmpl in product_id_to_template.items():
            if tmpl:
                template_to_products.setdefault(tmpl, []).append(pid)

        # BOMs by product_id - Fixed domain construction
        bom_by_product_domain = [["product_id", "in", product_ids]]
        bom_ids_product = odoo_connector.execute_kw(
            "mrp.bom", "search", [bom_by_product_domain], {"limit": 1000}
        )

        # BOMs by template variants - Fixed domain construction
        bom_by_template_domain = [
            ["product_tmpl_id.product_variant_ids", "in", product_ids]
        ]
        bom_ids_template = odoo_connector.execute_kw(
            "mrp.bom", "search", [bom_by_template_domain], {"limit": 1000}
        )

        all_bom_ids = list(set(bom_ids_product + bom_ids_template))
        if not all_bom_ids:
            logger.info("No BOMs found for the given products")
            return {}

        boms = odoo_connector.execute_kw(
            "mrp.bom",
            "read",
            [all_bom_ids],
            {
                "fields": [
                    "id",
                    "product_id",
                    "product_tmpl_id",
                    "bom_line_ids",
                    "code",
                ]
            },
        )
        all_line_ids: List[int] = []
        for bom in boms:
            all_line_ids.extend(bom.get("bom_line_ids", []))

        formula_info: Dict[str, Dict[str, str]] = {}
        if all_line_ids:
            bom_lines = odoo_connector.execute_kw(
                "mrp.bom.line",
                "read",
                [all_line_ids],
                {"fields": ["id", "bom_id", "product_id"]},
            )
            component_ids = [
                line["product_id"][0]
                for line in bom_lines
                if line.get("product_id")
            ]
            component_products = (
                odoo_connector.execute_kw(
                    "product.product",
                    "read",
                    [component_ids],
                    {"fields": ["id", "default_code", "name"]},
                )
                if component_ids
                else []
            )
            component_info = {p["id"]: p for p in component_products}

            for bom in boms:
                applicable_ids: List[int] = []
                if bom.get("product_id"):
                    applicable_ids = [bom["product_id"][0]]
                elif bom.get("product_tmpl_id"):
                    tmpl_id = bom["product_tmpl_id"][0]
                    applicable_ids = template_to_products.get(tmpl_id, [])
                for pid in applicable_ids:
                    item_code = product_id_to_code.get(pid)
                    if not item_code or item_code in formula_info:
                        continue
                    bom_reference = bom.get("code", "") or ""
                    formula_name = "Odoo info missing"
                    for line in bom_lines:
                        if line["bom_id"][0] == bom["id"]:
                            comp_id = line.get("product_id", [None])[0]
                            comp = component_info.get(comp_id)
                            if not comp:
                                continue
                            code = comp.get("default_code") or ""
                            name = comp.get("name") or ""
                            if code.startswith("F-") or name.startswith("F-"):
                                formula_name = (
                                    name if name.startswith("F-") else code
                                )
                                break
                    formula_info[item_code] = {
                        "formula_name": formula_name,
                        "reference": bom_reference or "Odoo info missing",
                    }
        return formula_info
    except Exception as e:  # pragma: no cover (network/dependency)
        logger.warning(
            f"Skipping BOM formula enrichment due to Odoo error: {e}"
        )
        return {}


def get_odoo_sales_order_line_items(
    orders_df: pd.DataFrame, logger
) -> pd.DataFrame:
    """Fetch actual Odoo sales order line items matching QuickBooks orders.

    Uses proper batching (50 records at a time) to avoid server overload.
    Falls back to placeholder items if Odoo is unavailable or errors occur.
    """
    logger.info(
        f"Starting Odoo enrichment for {len(orders_df)} QuickBooks orders"
    )

    if OdooConnector is None:
        logger.info(
            "Odoo connector not available - using QuickBooks placeholder data only"
        )
        return create_placeholder_line_items(orders_df)
    try:
        logger.info("Initializing Odoo connector...")
        odoo_connector = OdooConnector(logger)
        odoo_connector.authenticate()
        logger.info("Successfully authenticated with Odoo")

        # Load product categorization (try CWD, then docs/)
        try:
            categorization_df = pd.read_excel("product_categorization.xlsx")
            logger.info(
                f"Loaded product categorization data: {len(categorization_df)} products"
            )
        except FileNotFoundError:
            docs_path = os.path.join("docs", "product_categorization.xlsx")
            if os.path.exists(docs_path):
                categorization_df = pd.read_excel(docs_path)
                logger.info(
                    f"Loaded product categorization data from {docs_path}: {len(categorization_df)} products"
                )
            else:
                logger.warning(
                    "product_categorization.xlsx not found (also not in docs/) - production lines will be 'Unknown'"
                )
                categorization_df = pd.DataFrame()

        mapping: Dict[str, str] = {}
        if (
            not categorization_df.empty
            and "production_line" in categorization_df.columns
        ):
            for _, row in categorization_df.iterrows():
                name = str(row.get("Name", "")).strip().lower()
                code = str(row.get("Internal Reference", "")).strip()
                production_line = str(
                    row.get("production_line", "Unknown")
                ).strip()
                if name and production_line != "Unknown":
                    mapping[name] = production_line
                if code and production_line != "Unknown":
                    mapping[code] = production_line

        # Get all open sales orders from Odoo first, then match with QuickBooks
        logger.info("Fetching all open sales orders from Odoo...")

        # Search for open sales orders (confirmed but not fully delivered/invoiced)
        so_domain = [
            ["state", "=", "sale"],  # Confirmed orders only
            "|",
            ["invoice_status", "=", "to invoice"],  # Not fully invoiced
            ["invoice_status", "=", "no"],  # No invoice needed
        ]

        # Get total count first
        total_orders = odoo_connector.execute_kw(
            "sale.order", "search_count", [so_domain]
        )
        logger.info(f"Found {total_orders} open sales orders in Odoo")

        if total_orders == 0:
            logger.warning("No open sales orders found in Odoo")
            return create_placeholder_line_items(orders_df)

        all_line_items: List[Dict[str, Any]] = []
        batch_size = 50  # Process 50 orders at a time to avoid server overload
        processed_orders = 0

        # Process sales orders in batches to avoid server overload
        for offset in range(0, total_orders, batch_size):
            current_batch_size = min(batch_size, total_orders - offset)
            logger.info(
                f"Processing batch {offset//batch_size + 1}: orders {offset + 1}-{offset + current_batch_size} of {total_orders}"
            )

            # Fetch batch of sales orders with line items
            sales_orders = odoo_connector.execute_kw(
                "sale.order",
                "search_read",
                [so_domain],
                {
                    "fields": [
                        "id",
                        "name",
                        "client_order_ref",
                        "partner_id",
                                        "date_order",
                "commitment_date", 
                "eta_date",
                        "note",
                        "order_line",
                    ],
                    "limit": batch_size,
                    "offset": offset,
                },
            )

            if not sales_orders:
                logger.warning(
                    f"No sales orders returned for batch at offset {offset}"
                )
                continue

            # Get all line item IDs from this batch
            all_line_ids = []
            order_line_mapping = {}  # Maps line_id to order info

            for order in sales_orders:
                line_ids = order.get("order_line", [])
                all_line_ids.extend(line_ids)

                # Store order info for each line
                for line_id in line_ids:
                    # Get ETA date from Odoo or calculate fallback
                    odoo_eta_date = order.get("eta_date")
                    calculated_eta_date = None
                    
                    if not odoo_eta_date:
                        # Calculate ETA as 10 weekdays from order date
                        calculated_eta_date = calculate_eta_date_from_order_date(order.get("date_order"))
                    
                    order_line_mapping[line_id] = {
                        "order_id": order["id"],
                        "order_name": order["name"],
                        "customer_name": (
                            order["partner_id"][1]
                            if order.get("partner_id")
                            else "Unknown Customer"
                        ),
                        "order_date": order.get("date_order"),
                        "delivery_date": order.get("commitment_date") or None,
                        "eta_date": format_odoo_date_to_iso8601(odoo_eta_date) if odoo_eta_date else calculated_eta_date,
                        "memo": order.get("note", ""),
                        "client_order_ref": order.get("client_order_ref", ""),
                    }

            if not all_line_ids:
                logger.info(
                    f"No line items found in batch {offset//batch_size + 1}"
                )
                continue

            logger.info(
                f"Fetching {len(all_line_ids)} line items for batch {offset//batch_size + 1}"
            )

            # Fetch all line items for this batch in one call
            line_items = odoo_connector.execute_kw(
                "sale.order.line",
                "read",
                [all_line_ids],
                {
                    "fields": [
                        "id",
                        "order_id",
                        "product_id",
                        "name",
                        "product_uom_qty",
                        "qty_delivered",
                        "qty_invoiced",
                        "price_unit",
                        "price_subtotal",
                        "price_total",
                    ]
                },
            )

            # Get unique product IDs to fetch product details
            product_ids = list(
                set(
                    line["product_id"][0]
                    for line in line_items
                    if line.get("product_id")
                )
            )

            # Fetch product details in batch
            product_details = {}
            if product_ids:
                logger.info(f"Fetching details for {len(product_ids)} products")
                products = odoo_connector.execute_kw(
                    "product.product",
                    "read",
                    [product_ids],
                    {"fields": ["id", "name", "default_code", "categ_id"]},
                )

                for product in products:
                    product_details[product["id"]] = {
                        "name": product.get("name", "Unknown Product"),
                        "default_code": product.get("default_code", "") or "",
                        "category": (
                            product["categ_id"][1]
                            if product.get("categ_id")
                            else "Unknown"
                        ),
                    }

            # Process line items
            for line in line_items:
                order_info = order_line_mapping.get(line["id"], {})
                product_id = (
                    line["product_id"][0] if line.get("product_id") else None
                )
                product_info = product_details.get(
                    product_id,
                    {
                        "name": "Unknown Product",
                        "default_code": "",
                        "category": "Unknown",
                    },
                )

                # Get production line from mapping (prioritize Internal Reference)
                production_line = "Unknown"
                product_name_lower = product_info["name"].lower()
                product_code = product_info["default_code"]

                # First try to match by Internal Reference (product_code)
                if product_code and product_code in mapping:
                    production_line = mapping[product_code]
                # Fallback to product name matching
                elif product_name_lower in mapping:
                    production_line = mapping[product_name_lower]

                # Calculate quantities
                ordered_qty = line.get("product_uom_qty", 0) or 0
                delivered_qty = line.get("qty_delivered", 0) or 0
                invoiced_qty = line.get("qty_invoiced", 0) or 0
                open_qty = max(0, ordered_qty - delivered_qty)
                unit_price = line.get("price_unit", 0) or 0
                line_total = line.get("price_subtotal", 0) or 0
                open_amount = open_qty * unit_price

                # Include all line items (not just those with open quantities)
                # This ensures complete data visibility in reports
                all_line_items.append(
                    {
                        "Order Date": format_odoo_date_to_iso8601(order_info.get("order_date")),
                        "Number": order_info.get("order_name", ""),
                        "Customer": order_info.get("customer_name", ""),
                        "Due_Date": format_odoo_date_to_iso8601(order_info.get("delivery_date")),
                        "ETA_Date": order_info.get("eta_date"),
                        "Internal_Reference": product_code,
                        "Item_Code": product_code,
                        "Item": product_info["name"],
                        "Item_Name": product_info["name"],
                        "Item_Description": line.get(
                            "name", product_info["name"]
                        ),
                        "Category": product_info["category"],
                        "Production_Line": production_line,
                        "Formula_Name": "Odoo info missing",  # Will be enriched later if BOM data available
                        "Memo": order_info.get("memo", ""),
                        "Qty": ordered_qty,
                        "Delivered_Qty": delivered_qty,
                        "Invoiced_Qty": invoiced_qty,
                        "Open_Qty": open_qty,
                        "Unit_Price": unit_price,
                        "Line_Total": line_total,
                        "Open_Balance": open_amount,
                        "Odoo_SO_ID": order_info.get("order_id", ""),
                        "Odoo_SO_Name": order_info.get("order_name", ""),
                        "Data_Source": "Odoo",
                    }
                )

            processed_orders += len(sales_orders)
            logger.info(
                f"Processed {processed_orders}/{total_orders} orders, found {len(all_line_items)} open line items so far"
            )
        logger.info(
            f"Odoo enrichment completed: processed {processed_orders} orders, found {len(all_line_items)} open line items"
        )

        if all_line_items:
            logger.info("Creating DataFrame from Odoo line items")
            odoo_df = pd.DataFrame(all_line_items)
            logger.info(
                f"Successfully created DataFrame with {len(odoo_df)} line items from Odoo"
            )
            return odoo_df
        else:
            logger.warning("No open line items found in Odoo")
            # Return empty DataFrame with correct structure instead of placeholders
            return pd.DataFrame(
                columns=[
                    "Order Date",
                    "Number",
                    "Customer",
                    "Due_Date",
                    "ETA_Date",
                    "Internal_Reference",
                    "Item_Code",
                    "Item",
                    "Item_Name",
                    "Item_Description",
                    "Category",
                    "Production_Line",
                    "Formula_Name",
                    "Memo",
                    "Qty",
                    "Delivered_Qty",
                    "Invoiced_Qty",
                    "Open_Qty",
                    "Unit_Price",
                    "Line_Total",
                    "Open_Balance",
                    "Odoo_SO_ID",
                    "Odoo_SO_Name",
                    "Data_Source",
                ]
            )
    except Exception as e:  # pragma: no cover
        logger.error(
            f"Odoo enrichment failed. Error: {e}"
        )
        
        # Prompt user whether to continue without Odoo data
        print(f"\n❌ ODOO CONNECTION FAILED")
        print(f"Error: {e}")
        print(f"\nWithout Odoo data, the following columns will show 'Odoo info missing':")
        print(f"  - Item_Description")
        print(f"  - Category") 
        print(f"  - Production_Line")
        print(f"  - Formula_Name")
        print(f"  - Internal_Reference")
        
        while True:
            try:
                choice = input(f"\nDo you want to continue without Odoo data? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    logger.info("User chose to continue without Odoo data")
                    return create_placeholder_line_items(orders_df)
                elif choice in ['n', 'no']:
                    logger.info("User chose to abort due to Odoo connection failure")
                    print("Aborting operation due to Odoo connection failure.")
                    raise SystemExit(1)
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
            except (EOFError, KeyboardInterrupt):
                print("\nOperation cancelled by user.")
                raise SystemExit(1)


def create_placeholder_line_items(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Create placeholder line items for orders not resolved in Odoo."""
    if orders_df.empty:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(
            columns=[
                "Order Date",
                "Number",
                "Customer",
                "Due_Date",
                "ETA_Date",
                "Internal_Reference",
                "Item_Code",
                "Item",
                "Item_Name",
                "Item_Description",
                "Category",
                "Production_Line", 
                "Formula_Name",
                "Memo",
                "Qty",
                "Delivered_Qty",
                "Invoiced_Qty",
                "Open_Qty",
                "Unit_Price",
                "Line_Total",
                "Open_Balance",
                "Odoo_SO_ID",
                "Odoo_SO_Name",
                "Data_Source",
            ]
        )

    df = orders_df.copy()

    # Map QuickBooks columns to expected output columns
    column_mapping = {
        "order_date": "Order Date",  # Renamed from "Date" to "Order Date"
        "order_number": "Number",
        "customer_name": "Customer",
        "delivery_date": "Due_Date",
        "eta_date": "ETA_Date",  # New field for ETA Date
        "memo": "Memo",
        "open_balance": "Open_Balance",
    }

    # Rename columns that exist
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})

    # Add missing columns with default values
    df["Internal_Reference"] = "Odoo info missing"
    df["Item_Code"] = ""
    df["Item"] = "N/A - QB CSV Only"
    df["Item_Name"] = "N/A - No Odoo Match"
    df["Item_Description"] = "Odoo info missing"
    df["Category"] = "Odoo info missing"
    df["Production_Line"] = "Unknown"  # Use "Unknown" instead of "Odoo info missing" for PL sheet creation
    df["Formula_Name"] = "Odoo info missing"
    df["Qty"] = 1
    df["Delivered_Qty"] = 0
    df["Invoiced_Qty"] = 0
    df["Open_Qty"] = 1
    df["Unit_Price"] = df.get("amount", 0)
    df["Line_Total"] = df.get("amount", 0)

    # Calculate ETA_Date if not present (10 weekdays from Order Date)
    if "ETA_Date" not in df.columns:
        if "Order Date" in df.columns:
            df["ETA_Date"] = df["Order Date"].apply(calculate_eta_date_from_order_date)
        else:
            df["ETA_Date"] = None

    # Ensure Open_Balance exists
    if "Open_Balance" not in df.columns:
        df["Open_Balance"] = df.get("amount", 0)

    df["Odoo_SO_ID"] = ""
    df["Odoo_SO_Name"] = ""
    df["Data_Source"] = "QuickBooks CSV Only"

    return df
