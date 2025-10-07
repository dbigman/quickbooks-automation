import os
import requests
import pandas as pd
from typing import List, Optional
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class OdooConnector:
    """Connector for Odoo 18 via JSON-RPC with enhanced API features."""

    def __init__(self, logger):
        self.logger = logger
        self.url = os.getenv("ODOO_URL")
        self.database = os.getenv("ODOO_DATABASE")
        self.username = os.getenv("ODOO_USERNAME")
        self.password = os.getenv("ODOO_PASSWORD")
        self.uid: Optional[int] = None

        # HTTP session with retry strategy for resilience
        self.session = requests.Session()
        retry_total = int(os.getenv("REQUEST_MAX_RETRIES", "3"))
        backoff = float(os.getenv("REQUEST_BACKOFF_FACTOR", "0.5"))
        status_forcelist = (502, 503, 504)
        retry = Retry(
            total=retry_total,
            backoff_factor=backoff,
            status_forcelist=status_forcelist,
            allowed_methods=("POST",),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        missing = [
            v
            for v in (
                "ODOO_URL",
                "ODOO_DATABASE",
                "ODOO_USERNAME",
                "ODOO_PASSWORD",
            )
            if not os.getenv(v)
        ]
        if missing:
            raise ValueError(f"Missing Odoo configuration: {missing}")
        self.logger.info(f"Initializing Odoo connector for {self.url}")

    def authenticate(self) -> int:
        if self.uid:
            return self.uid
        self.logger.info("Authenticating with Odoo...")
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [self.database, self.username, self.password, {}],
            },
            "id": 1,
        }
        try:
            resp = self.session.post(
                f"{self.url}/jsonrpc", json=payload, timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            if "error" in data:
                raise RuntimeError(f"Odoo auth error: {data['error']}")
            self.uid = data["result"]
            if not self.uid:
                raise RuntimeError("Odoo authentication returned no UID")
            self.logger.info(f"✅ Authenticated. UID={self.uid}")
            return self.uid
        except requests.exceptions.Timeout:
            self.logger.error(
                "Connection to Odoo timed out during authentication"
            )
            raise RuntimeError(
                f"Unable to connect to Odoo at {self.url} (timeout). "
                "Check network connectivity, Odoo server status, and ODOO_URL."
            )
        except requests.exceptions.ConnectionError:
            self.logger.error(
                "Connection error while contacting Odoo for authentication"
            )
            raise RuntimeError(
                f"Unable to connect to Odoo at {self.url} (connection error). "
                "Verify the server is reachable and credentials are correct."
            )
        except requests.exceptions.RequestException as e:
            self.logger.error(f"HTTP error during Odoo authentication: {e}")
            raise RuntimeError(f"HTTP error during Odoo authentication: {e}")
        except ValueError as e:
            self.logger.error(
                f"Invalid JSON from Odoo during authentication: {e}"
            )
            raise RuntimeError(
                f"Invalid JSON from Odoo during authentication: {e}"
            )

    def execute_kw(
        self, model: str, method: str, args: List, kwargs: dict = None
    ):
        """Execute Odoo API call with improved error handling."""
        if not self.uid:
            self.authenticate()

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.database,
                    self.uid,
                    self.password,
                    model,
                    method,
                    args,
                    kwargs or {},
                ],
            },
            "id": 1,
        }

        try:
            resp = self.session.post(
                f"{self.url}/jsonrpc", json=payload, timeout=60
            )
            resp.raise_for_status()
            result = resp.json()

            if "error" in result:
                error_msg = result["error"]
                self.logger.error(
                    f"Odoo API error for {model}.{method}: {error_msg}"
                )
                raise RuntimeError(f"Odoo API error: {error_msg}")

            return result.get("result", [])

        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout error calling {model}.{method}")
            raise RuntimeError(
                f"Unable to reach Odoo at {self.url} (timeout) while calling {model}.{method}. "
                "Check server availability and try again."
            )
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error calling {model}.{method}")
            raise RuntimeError(
                f"Connection error to Odoo server at {self.url} while calling {model}.{method}. "
                "Verify network, DNS, and that Odoo is running."
            )
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error calling {model}.{method}: {e}")
            raise RuntimeError(f"Request error: {e}")
        except ValueError as e:
            self.logger.error(f"JSON parsing error for {model}.{method}: {e}")
            raise RuntimeError(f"Invalid JSON response from Odoo: {e}")

    def get_sales_orders(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> pd.DataFrame:
        self.logger.info("Fetching sales orders from Odoo...")
        domain = [["state", "in", ["sale", "done"]]]
        if date_from:
            domain.append(["date_order", ">=", date_from.strftime("%Y-%m-%d")])
        if date_to:
            domain.append(["date_order", "<=", date_to.strftime("%Y-%m-%d")])
        # Fetch all matching ids then page reads to avoid large payloads
        ids = self.execute_kw("sale.order", "search", [domain])
        if not ids:
            return pd.DataFrame()
        fields = [
            "id",
            "name",
            "partner_id",
            "date_order",
            "commitment_date",
            "state",
            "order_line",
            "amount_total",
            "invoice_status",
            "delivery_count",
            "picking_ids",
            "client_order_ref",
            "note",
            "user_id",
        ]
        batch_size = int(os.getenv("BATCH_SIZE", "100"))
        orders = []
        for i in range(0, len(ids), batch_size):
            chunk = ids[i : i + batch_size]
            orders.extend(
                self.execute_kw(
                    "sale.order", "read", [chunk], {"fields": fields}
                )
            )
        line_ids = [l for o in orders for l in o.get("order_line", [])]
        lines = []
        if line_ids:
            line_fields = [
                "order_id",
                "product_id",
                "product_uom_qty",
                "price_unit",
                "qty_delivered",
                "qty_invoiced",
            ]
            # Page large line reads as well
            lines = []
            for i in range(0, len(line_ids), batch_size):
                chunk = line_ids[i : i + batch_size]
                lines.extend(
                    self.execute_kw(
                        "sale.order.line",
                        "read",
                        [chunk],
                        {"fields": line_fields},
                    )
                )
        # Get unique product IDs to fetch product details
        product_ids = list(
            set(l["product_id"][0] for l in lines if l["product_id"])
        )

        # Fetch product details including category
        product_details = {}
        if product_ids:
            product_fields = ["id", "name", "categ_id"]
            products = self.execute_kw(
                "product.product",
                "read",
                [product_ids],
                {"fields": product_fields},
            )
            for p in products:
                product_details[p["id"]] = {
                    "product_category": (
                        p["categ_id"][1] if p.get("categ_id") else "Unknown"
                    )
                }

        data = []
        for o in orders:
            for l in lines:
                if l["order_id"][0] == o["id"]:
                    product_id = l["product_id"][0] if l["product_id"] else None
                    product_info = product_details.get(
                        product_id, {"product_category": "Unknown"}
                    )

                    data.append(
                        {
                            "order_id": o["name"],
                            "customer_id": (
                                o["partner_id"][0] if o["partner_id"] else None
                            ),
                            "customer_name": (
                                o["partner_id"][1] if o["partner_id"] else None
                            ),
                            "product_id": product_id,
                            "product_name": (
                                l["product_id"][1] if l["product_id"] else None
                            ),
                            "product_category": product_info[
                                "product_category"
                            ],
                            "quantity": l["product_uom_qty"],
                            "delivered": l.get("qty_delivered", 0),
                            "invoiced": l.get("qty_invoiced", 0),
                            "pending": l["product_uom_qty"]
                            - l.get("qty_delivered", 0),
                            "unit_price": l["price_unit"],
                            "order_date": o["date_order"],
                            "delivery_date": o.get("commitment_date")
                            or o["date_order"],
                            "status": o["state"],
                            "invoice_status": o.get("invoice_status", "no"),
                            "order_total": o["amount_total"],
                            "delivery_count": o.get("delivery_count", 0),
                            "client_order_ref": o.get("client_order_ref", ""),
                            "order_note": o.get("note", ""),
                            "salesperson_id": (
                                o.get("user_id", [None, ""])[0]
                                if o.get("user_id")
                                else None
                            ),
                            "salesperson_name": (
                                o.get("user_id", [None, ""])[1]
                                if o.get("user_id")
                                else ""
                            ),
                        }
                    )
        df = pd.DataFrame(data).dropna(subset=["product_id"])

        # Optimize memory usage by converting to appropriate dtypes
        if not df.empty:
            # Convert numeric columns to more efficient types
            numeric_cols = [
                "quantity",
                "delivered",
                "invoiced",
                "pending",
                "unit_price",
                "order_total",
            ]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

            # Convert date columns
            date_cols = ["order_date", "delivery_date"]
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors="coerce")

        self.logger.info(f"✅ Retrieved {len(df)} sales order lines")
        return df

    def get_inventory_levels_old_method(self) -> pd.DataFrame:
        """
        Get inventory levels using the OLD METHOD (with quantity > 0 filter).
        This method is kept for comparison purposes during physical inventory audits.
        ⚠️  WARNING: This method has a known bug - it excludes negative quantities!
        """
        self.logger.info(
            "Fetching inventory levels using OLD METHOD (for comparison only)..."
        )

        # Define the specific warehouse locations
        target_locations = [
            "WH1/Stock",
            "WH1/Stock/A1A",
            "WH1/Stock/A1B",
            "WH1/Stock/A1C",
            "WH1/Stock/A2A",
            "WH1/Stock/A2B",
            "WH1/Stock/A2C",
            "WH1/Stock/Pasillo 1 - Piso",
            "WH1/Stock/Pasillo 2 - Piso",
            "WH2/Stock",
        ]

        # Get the location IDs for all target locations
        wh_locations = []
        location_mapping = {}  # Map location_id to location name

        try:
            # Build search domain for all target locations
            if len(target_locations) == 1:
                location_domain = [["complete_name", "=", target_locations[0]]]
                location_ids = self.execute_kw(
                    "stock.location", "search", [location_domain]
                )
            else:
                # Attempt fast domain search with "in" operator
                try:
                    location_domain = [["complete_name", "in", target_locations]]
                    location_ids = self.execute_kw(
                        "stock.location", "search", [location_domain]
                    )
                except Exception as e:
                    # Fall back to individual name_search calls
                    self.logger.debug(
                        "Domain 'in' search failed for locations; "
                        f"falling back to name_search: {e}"
                    )
                    location_ids = []
                    for loc_name in target_locations:
                        try:
                            result = self.execute_kw(
                                "stock.location",
                                "name_search",
                                [loc_name],
                                {"operator": "=", "limit": 1},
                            )
                        except Exception:
                            result = []
                        if result:
                            location_ids.append(result[0][0])

            if location_ids:
                location_fields = ["id", "name", "complete_name", "usage"]
                locations = self.execute_kw(
                    "stock.location",
                    "read",
                    [location_ids],
                    {"fields": location_fields},
                )

                # Create mapping and collect location IDs
                for loc in locations:
                    wh_locations.append(loc["id"])
                    location_mapping[loc["id"]] = loc["complete_name"]

        except Exception as e:
            self.logger.error(
                f"Error fetching warehouse locations (old method): {e}"
            )
            return pd.DataFrame()

        # Search for stock quants with OLD METHOD filter (quantity > 0)
        domain = [
            ["quantity", ">", 0],  # ⚠️  BUG: This excludes negative quantities!
            ["location_id", "in", wh_locations],
        ]
        quant_ids = self.execute_kw("stock.quant", "search", [domain])
        if not quant_ids:
            return pd.DataFrame()

        # Fetch quant data with location information
        fields = ["product_id", "quantity", "reserved_quantity", "location_id"]
        quants = []
        batch_size = int(os.getenv("BATCH_SIZE", "100"))
        for i in range(0, len(quant_ids), batch_size):
            chunk = quant_ids[i : i + batch_size]
            quants.extend(
                self.execute_kw(
                    "stock.quant", "read", [chunk], {"fields": fields}
                )
            )

        # Get unique product IDs to fetch product details
        product_ids = list(
            set(q["product_id"][0] for q in quants if q["product_id"])
        )

        # Process quant data - create separate columns for each location
        inventory_data = (
            {}
        )  # product_id -> {location: {available_qty, total_qty}}

        for q in quants:
            product_id = q["product_id"][0] if q["product_id"] else None
            if not product_id:
                continue

            location_id = q["location_id"][0] if q["location_id"] else None
            location_name = location_mapping.get(location_id, "Unknown")

            if product_id not in inventory_data:
                inventory_data[product_id] = {}

            if location_name not in inventory_data[product_id]:
                inventory_data[product_id][location_name] = {
                    "available_qty": 0,
                    "total_qty": 0,
                }

            inventory_data[product_id][location_name]["available_qty"] += (
                q["quantity"] - q["reserved_quantity"]
            )
            inventory_data[product_id][location_name]["total_qty"] += q[
                "quantity"
            ]

        # Build the final DataFrame with separate columns for each location
        records = []
        for product_id, location_data in inventory_data.items():
            # Start with basic product information
            record = {"product_id": product_id}

            # Add columns for each target location
            total_available = 0
            total_qty = 0

            for location in target_locations:
                if location in location_data:
                    # Available quantity for this location
                    available = location_data[location]["available_qty"]
                    total = location_data[location]["total_qty"]
                    record[f"{location}_available"] = available
                    record[f"{location}_total"] = total
                    total_available += available
                    total_qty += total
                else:
                    # No inventory in this location
                    record[f"{location}_available"] = 0
                    record[f"{location}_total"] = 0

            # Add summary columns
            record["total_available_qty"] = total_available
            record["total_qty"] = total_qty

            records.append(record)

        # Create DataFrame
        df = pd.DataFrame(records)
        if df.empty:
            return pd.DataFrame()

        # Optimize memory usage for numeric columns
        numeric_cols = [
            col
            for col in df.columns
            if col.endswith("_available")
            or col.endswith("_total")
            or col in ["total_available_qty", "total_qty"]
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        self.logger.info(
            f"✅ Retrieved OLD METHOD inventory for {len(df)} products"
        )
        return df

    def get_inventory_levels(self) -> pd.DataFrame:
        self.logger.info(
            "Fetching inventory levels from Odoo (WH1 and WH2 with separate location columns)..."
        )

        # Define the specific warehouse locations
        target_locations = [
            "WH1/Stock",
            "WH1/Stock/A1A",
            "WH1/Stock/A1B",
            "WH1/Stock/A1C",
            "WH1/Stock/A2A",
            "WH1/Stock/A2B",
            "WH1/Stock/A2C",
            "WH1/Stock/Pasillo 1 - Piso",
            "WH1/Stock/Pasillo 2 - Piso",
            "WH2/Stock",
        ]

        self.logger.info(
            f"Filtering inventory for specific locations: {len(target_locations)} locations"
        )

        # Get the location IDs for all target locations
        wh_locations = []
        location_mapping = {}  # Map location_id to location name

        try:
            # Build search domain for all target locations
            if len(target_locations) == 1:
                location_domain = [["complete_name", "=", target_locations[0]]]
                location_ids = self.execute_kw(
                    "stock.location", "search", [location_domain]
                )
            else:
                # Attempt fast domain search with "in" operator
                try:
                    location_domain = [["complete_name", "in", target_locations]]
                    location_ids = self.execute_kw(
                        "stock.location", "search", [location_domain]
                    )
                except Exception as e:
                    # Fall back to individual name_search calls
                    self.logger.debug(
                        "Domain 'in' search failed for locations; "
                        f"falling back to name_search: {e}"
                    )
                    location_ids = []
                    for loc_name in target_locations:
                        try:
                            result = self.execute_kw(
                                "stock.location",
                                "name_search",
                                [loc_name],
                                {"operator": "=", "limit": 1},
                            )
                        except Exception:
                            result = []
                        if result:
                            location_ids.append(result[0][0])

            if location_ids:
                location_fields = ["id", "name", "complete_name", "usage"]
                locations = self.execute_kw(
                    "stock.location",
                    "read",
                    [location_ids],
                    {"fields": location_fields},
                )

                # Create mapping and collect location IDs
                for loc in locations:
                    wh_locations.append(loc["id"])
                    location_mapping[loc["id"]] = loc["complete_name"]

                found_locations = [loc["complete_name"] for loc in locations]
                self.logger.info(
                    f"Found {len(found_locations)} warehouse locations: {found_locations}"
                )

                # Check for missing locations
                missing_locations = set(target_locations) - set(found_locations)
                if missing_locations:
                    self.logger.warning(
                        f"Missing locations: {list(missing_locations)}"
                    )
            else:
                self.logger.warning(
                    "No target warehouse locations found in Odoo"
                )
                return pd.DataFrame()

        except Exception as e:
            self.logger.error(f"Error fetching warehouse locations: {e}")
            return pd.DataFrame()

        # Search for stock quants only in target warehouse locations
        # Note: Include ALL quantities (positive and negative) for accurate inventory calculation
        domain = [["location_id", "in", wh_locations]]
        quant_ids = self.execute_kw("stock.quant", "search", [domain])
        if not quant_ids:
            self.logger.info("No inventory found in target warehouse locations")
            return pd.DataFrame()

        # Fetch quant data with location information
        fields = ["product_id", "quantity", "reserved_quantity", "location_id"]
        quants = []
        batch_size = int(os.getenv("BATCH_SIZE", "100"))
        for i in range(0, len(quant_ids), batch_size):
            chunk = quant_ids[i : i + batch_size]
            quants.extend(
                self.execute_kw(
                    "stock.quant", "read", [chunk], {"fields": fields}
                )
            )

        # Get unique product IDs to fetch product details
        product_ids = list(
            set(q["product_id"][0] for q in quants if q["product_id"])
        )

        # Fetch product details
        product_details = {}
        if product_ids:
            product_fields = [
                "id",
                "name",
                "type",
                "categ_id",
                "responsible_id",
            ]
            products = self.execute_kw(
                "product.product",
                "read",
                [product_ids],
                {"fields": product_fields},
            )
            for p in products:
                product_details[p["id"]] = {
                    "product_name": p.get("name", "Unknown"),
                    "type": p.get("type", "Unknown"),
                    "product_category": (
                        p["categ_id"][1] if p.get("categ_id") else "Unknown"
                    ),
                    "production_location": (
                        p["responsible_id"][1]
                        if p.get("responsible_id")
                        else "Unknown"
                    ),
                }

        # Process quant data - create separate columns for each location
        inventory_data = (
            {}
        )  # product_id -> {location: {available_qty, total_qty}}

        for q in quants:
            product_id = q["product_id"][0] if q["product_id"] else None
            if not product_id:
                continue

            location_id = q["location_id"][0] if q["location_id"] else None
            location_name = location_mapping.get(location_id, "Unknown")

            if product_id not in inventory_data:
                inventory_data[product_id] = {}

            if location_name not in inventory_data[product_id]:
                inventory_data[product_id][location_name] = {
                    "available_qty": 0,
                    "total_qty": 0,
                }

            inventory_data[product_id][location_name]["available_qty"] += (
                q["quantity"] - q["reserved_quantity"]
            )
            inventory_data[product_id][location_name]["total_qty"] += q[
                "quantity"
            ]

        # Build the final DataFrame with separate columns for each location
        records = []
        for product_id, location_data in inventory_data.items():
            product_info = product_details.get(
                product_id,
                {
                    "product_name": "Unknown",
                    "type": "Unknown",
                    "product_category": "Unknown",
                    "production_location": "Unknown",
                },
            )

            # Start with basic product information
            record = {
                "product_id": product_id,
                "product_name": product_info["product_name"],
                "type": product_info["type"],
                "product_category": product_info["product_category"],
                "production_location": product_info["production_location"],
            }

            # Add columns for each target location
            total_available = 0
            total_qty = 0

            for location in target_locations:
                if location in location_data:
                    # Available quantity for this location
                    available = location_data[location]["available_qty"]
                    total = location_data[location]["total_qty"]
                    record[f"{location}_available"] = available
                    record[f"{location}_total"] = total
                    total_available += available
                    total_qty += total
                else:
                    # No inventory in this location
                    record[f"{location}_available"] = 0
                    record[f"{location}_total"] = 0

            # Add summary columns
            record["total_available_qty"] = total_available
            record["total_qty"] = total_qty

            records.append(record)

        # Create DataFrame
        df = pd.DataFrame(records)
        if df.empty:
            return pd.DataFrame()

        # Optimize memory usage for numeric columns
        numeric_cols = [
            col
            for col in df.columns
            if col.endswith("_available")
            or col.endswith("_total")
            or col in ["total_available_qty", "total_qty"]
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        self.logger.info(
            f"✅ Retrieved inventory for {len(df)} products with separate location columns"
        )
        return df

    def get_bom_data(
        self, product_ids: Optional[List[int]] = None
    ) -> pd.DataFrame:
        """Fetch Bill of Materials data, handling missing many2one fields gracefully."""
        self.logger.info("Fetching BOM data from Odoo...")
        domain = []
        if product_ids:
            domain.append(
                ["product_tmpl_id.product_variant_ids", "in", product_ids]
            )
        bom_ids = self.execute_kw(
            "mrp.bom", "search", [domain], {"limit": 1000}
        )
        if not bom_ids:
            return pd.DataFrame()

        # Read both product_id and template for fallback
        fields = [
            "id",
            "product_tmpl_id",
            "product_id",
            "bom_line_ids",
            "product_qty",
        ]
        boms = self.execute_kw("mrp.bom", "read", [bom_ids], {"fields": fields})

        # Read BOM lines
        line_ids = [li for b in boms for li in b.get("bom_line_ids", [])]
        bom_lines = []
        if line_ids:
            bom_lines = self.execute_kw(
                "mrp.bom.line",
                "read",
                [line_ids],
                {"fields": ["bom_id", "product_id", "product_qty"]},
            )

        records = []
        for b in boms:
            # Use product_id if set, else fallback to template
            parent = b.get("product_id") or b.get("product_tmpl_id")
            if not parent:
                continue
            parent_id, parent_name = parent

            # Iterate matching BOM lines
            for line in bom_lines:
                if line["bom_id"][0] != b["id"]:
                    continue
                comp = line.get("product_id") or (None, "Unknown")
                comp_id, comp_name = comp
                records.append(
                    {
                        "parent_product_id": parent_id,
                        "parent_product_name": parent_name,
                        "component_id": comp_id,
                        "component_name": comp_name,
                        "quantity_needed": line["product_qty"],
                    }
                )

        df = pd.DataFrame(records)
        self.logger.info(f"✅ Retrieved {len(df)} BOM components")
        return df
