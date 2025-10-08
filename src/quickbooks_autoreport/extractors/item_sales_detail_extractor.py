"""
Extract and organize QuickBooks Item Sales Detail report data.

This module parses the Item Sales Detail CSV export from QuickBooks and
organizes it into structured pandas DataFrames for analysis.

Convention: Memo field contains Product Name (Gasco-specific).
"""

import logging
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class ItemSalesDetailExtractor:
    """Extract and organize Item Sales Detail report data."""

    def __init__(self, csv_path: Path):
        """
        Initialize extractor with CSV file path.

        Args:
            csv_path: Path to QuickBooks Item Sales Detail CSV export
        """
        self.csv_path = csv_path
        self._raw_df: Optional[pd.DataFrame] = None
        self._transactions_df: Optional[pd.DataFrame] = None
        self._product_summary_df: Optional[pd.DataFrame] = None
        self._customer_product_df: Optional[pd.DataFrame] = None

    def load_raw_data(self) -> pd.DataFrame:
        """
        Load raw CSV data.

        Returns:
            Raw DataFrame with all rows from CSV
        """
        logger.info(f"📥 Loading raw data from {self.csv_path}")
        self._raw_df = pd.read_csv(self.csv_path, encoding="latin-1")

        logger.info(f"✅ Loaded {len(self._raw_df)} rows")
        return self._raw_df

    def extract_transactions(self) -> pd.DataFrame:
        """
        Extract transaction-level data (invoices, credit memos, etc.).

        Filters out header rows, totals, and product category rows.

        Returns:
            DataFrame with transaction lines only
        """
        if self._raw_df is None:
            self.load_raw_data()

        logger.info("🎯 Extracting transaction lines")

        # Extract product codes from Type column
        # Pattern: "A00403 (BELCA Vinagre...)" -> extract "A00403"
        product_code_pattern = r'^([A-Z0-9\-]+)\s*\('
        self._raw_df["Product_Code"] = self._raw_df["Type"].str.extract(
            product_code_pattern, expand=False
        )

        # Identify section breaks (Parts, Service, Other Charges, etc.)
        section_markers = [
            "Parts", "Service", "Other Charges", "TOTAL"
        ]
        self._raw_df["Is_Section_Break"] = self._raw_df[
            "Type"
        ].isin(section_markers)

        # Create section groups - reset at each section break
        self._raw_df["Section"] = self._raw_df[
            "Is_Section_Break"
        ].cumsum()

        # Forward fill product codes only within each section
        self._raw_df["Product_Code"] = self._raw_df.groupby("Section")[
            "Product_Code"
        ].ffill()

        # Filter to actual transaction rows
        valid_types = [
            "Invoice",
            "Credit Memo",
            "Sales Receipt",
            "Refund Receipt",
            "Statement Charge",
        ]
        transactions = self._raw_df[
            self._raw_df["Type"].isin(valid_types)
        ].copy()

        # Map product codes to transaction rows
        transactions["Product_Code"] = transactions.index.map(
            self._raw_df["Product_Code"]
        )

        # Convert data types
        transactions["Date"] = pd.to_datetime(
            transactions["Date"], format="%m/%d/%Y", errors="coerce"
        )
        transactions["Qty"] = pd.to_numeric(
            transactions["Qty"], errors="coerce"
        )
        transactions["Sales Price"] = pd.to_numeric(
            transactions["Sales Price"], errors="coerce"
        )
        transactions["Amount"] = pd.to_numeric(
            transactions["Amount"], errors="coerce"
        )
        transactions["Balance"] = pd.to_numeric(
            transactions["Balance"], errors="coerce"
        )

        # Clean up Memo field (Product Name)
        transactions["Product_Name"] = transactions["Memo"].str.strip()

        # Add derived fields
        transactions["Is_Return"] = transactions["Type"].isin(
            ["Credit Memo", "Refund Receipt"]
        )
        transactions["Realized_Unit_Price"] = np.where(
            transactions["Qty"] != 0,
            transactions["Amount"] / transactions["Qty"],
            np.nan
        )

        # Split customer and job
        split_result = transactions["Name"].str.split(":", n=1, expand=True)
        transactions["Customer"] = split_result[0]

        # Drop unnecessary columns
        columns_to_drop = ["Job", "Is_Section_Break", "Section"]
        transactions = transactions.drop(
            columns=[
                col for col in columns_to_drop if col in transactions.columns
            ],
            errors="ignore"
        )

        self._transactions_df = transactions
        logger.info(f"✅ Extracted {len(transactions)} transaction lines")

        return self._transactions_df

    def create_product_summary(self) -> pd.DataFrame:
        """
        Create product-level summary with sales and returns.

        Returns:
            DataFrame with product sales summary
        """
        if self._transactions_df is None:
            self.extract_transactions()

        logger.info("📊 Creating product summary")

        # Separate sales and returns
        sales = self._transactions_df[
            ~self._transactions_df["Is_Return"]
        ].copy()
        returns = self._transactions_df[
            self._transactions_df["Is_Return"]
        ].copy()

        # Aggregate sales
        sales_agg = sales.groupby("Product_Name").agg({
            "Qty": "sum",
            "Amount": "sum",
            "Num": "count",  # Transaction count
            "Product_Code": lambda x: (
                x.dropna().iloc[0] if len(x.dropna()) > 0 else ""
            )
        }).rename(columns={
            "Qty": "Sales_Qty",
            "Amount": "Sales_Amount",
            "Num": "Sales_Transactions"
        })

        # Aggregate returns (convert to positive for clarity)
        returns_agg = returns.groupby("Product_Name").agg({
            "Qty": lambda x: abs(x.sum()),
            "Amount": lambda x: abs(x.sum()),
            "Num": "count"
        }).rename(columns={
            "Qty": "Return_Qty",
            "Amount": "Return_Amount",
            "Num": "Return_Transactions"
        })

        # Combine
        summary = sales_agg.join(returns_agg, how="outer").fillna(0)

        # Calculate net values
        summary["Net_Qty"] = (
            summary["Sales_Qty"] - summary["Return_Qty"]
        )
        summary["Net_Amount"] = (
            summary["Sales_Amount"] - summary["Return_Amount"]
        )

        # Calculate total quantity (absolute sum of all transactions)
        summary["Total_Qty"] = summary["Sales_Qty"] + summary["Return_Qty"]

        # Calculate average unit price
        summary["Avg_Unit_Price"] = np.where(
            summary["Net_Qty"] != 0,
            summary["Net_Amount"] / summary["Net_Qty"],
            np.nan
        )

        # Filter out products with no activity (all quantities are 0)
        summary = summary[
            ~((summary["Sales_Qty"] == 0) & 
              (summary["Return_Qty"] == 0) & 
              (summary["Net_Qty"] == 0))
        ]

        # Sort by net amount descending
        summary = summary.sort_values("Net_Amount", ascending=False)

        self._product_summary_df = summary.reset_index()
        logger.info(f"✅ Created summary for {len(summary)} products")

        return self._product_summary_df

    def create_customer_product_matrix(self) -> pd.DataFrame:
        """
        Create customer-product matrix for key account analysis.

        Returns:
            DataFrame with customer × product sales
        """
        if self._transactions_df is None:
            self.extract_transactions()

        logger.info("📊 Creating customer-product matrix")

        # Aggregate by customer and product
        matrix = self._transactions_df.groupby(
            ["Customer", "Product_Name"]
        ).agg({
            "Qty": "sum",
            "Amount": "sum",
            "Num": "count",
            "Product_Code": lambda x: (
                x.dropna().iloc[0] if len(x.dropna()) > 0 else ""
            )
        }).rename(columns={
            "Qty": "Total_Qty",
            "Amount": "Total_Amount",
            "Num": "Transaction_Count"
        })

        # Calculate average transaction size
        matrix["Avg_Transaction_Amount"] = (
            matrix["Total_Amount"] / matrix["Transaction_Count"]
        )

        # Sort by total amount descending
        matrix = matrix.sort_values("Total_Amount", ascending=False)

        self._customer_product_df = matrix.reset_index()
        logger.info(
            f"✅ Created matrix with {len(matrix)} "
            "customer-product combinations"
        )

        return self._customer_product_df

    def get_top_products(self, n: int = 10) -> pd.DataFrame:
        """
        Get top N products by net sales amount.

        Args:
            n: Number of top products to return

        Returns:
            DataFrame with top products
        """
        if self._product_summary_df is None:
            self.create_product_summary()

        return self._product_summary_df.head(n)

    def get_top_customers(self, n: int = 10) -> pd.DataFrame:
        """
        Get top N customers by total sales amount.

        Args:
            n: Number of top customers to return

        Returns:
            DataFrame with top customers
        """
        if self._transactions_df is None:
            self.extract_transactions()

        customer_summary = self._transactions_df.groupby("Customer").agg({
            "Amount": "sum",
            "Num": "count"
        }).rename(columns={
            "Amount": "Total_Amount",
            "Num": "Transaction_Count"
        }).sort_values("Total_Amount", ascending=False)

        return customer_summary.head(n).reset_index()

    def create_backordered_items(self) -> pd.DataFrame:
        """
        Create backordered items report.
        
        Items with Qty=0 are considered backordered.
        One row per invoice number.
        
        Returns:
            DataFrame with backordered items
        """
        if self._transactions_df is None:
            self.extract_transactions()

        logger.info("📊 Creating backordered items report")
        
        # Filter transactions with Qty = 0 (backordered)
        backordered = self._transactions_df[
            self._transactions_df["Qty"] == 0
        ].copy()
        
        if len(backordered) == 0:
            logger.info("✅ No backordered items found")
            return pd.DataFrame(
                columns=["Product_Code", "Product_Name", "Num", "Customer"]
            )
        
        # Select and rename columns
        backordered_report = backordered[
            ["Product_Code", "Product_Name", "Num", "Customer"]
        ].copy()
        
        # Rename Num to Invoice_Number for clarity
        backordered_report = backordered_report.rename(
            columns={"Num": "Invoice_Number"}
        )
        
        # Remove duplicates (one row per invoice number + product)
        backordered_report = backordered_report.drop_duplicates()
        
        # Sort by Invoice_Number
        backordered_report = backordered_report.sort_values(
            "Invoice_Number"
        )
        
        logger.info(
            f"✅ Found {len(backordered_report)} backordered items"
        )
        return backordered_report

    def create_transaction_summary(self) -> pd.DataFrame:
        """
        Create transaction-level summary.

        Groups by transaction number (Num) and shows date, customer,
        and total amount for each transaction.

        Returns:
            DataFrame with transaction summaries
        """
        if self._transactions_df is None:
            self.extract_transactions()

        logger.info("📊 Creating transaction summary")

        # Group by transaction number
        transaction_summary = self._transactions_df.groupby("Num").agg({
            "Date": "first",
            "Type": "first",
            "Name": "first",
            "Amount": "sum"
        }).rename(columns={
            "Name": "Customer",
            "Amount": "Transaction_Total"
        })

        # Sort by date and transaction number
        transaction_summary = transaction_summary.sort_values(
            ["Date", "Num"], ascending=[True, True]
        )

        logger.info(
            f"✅ Created summary for {len(transaction_summary)} "
            "transactions"
        )
        return transaction_summary.reset_index()

    def export_all_dataframes(self) -> Dict[str, pd.DataFrame]:
        """
        Generate all DataFrames and return as dictionary.

        Returns:
            Dictionary with all extracted DataFrames
        """
        logger.info("📦 Generating all DataFrames")

        return {
            "transactions": self.extract_transactions(),
            "product_summary": self.create_product_summary(),
            "customer_product_matrix": self.create_customer_product_matrix(),
            "transaction_summary": self.create_transaction_summary(),
            "backordered_items": self.create_backordered_items(),
            "top_products": self.get_top_products(),
            "top_customers": self.get_top_customers()
        }


def extract_sales_data(csv_path: Path) -> Dict[str, pd.DataFrame]:
    """
    Convenience function to extract all sales data.

    Args:
        csv_path: Path to QuickBooks Item Sales Detail CSV

    Returns:
        Dictionary with all extracted DataFrames
    """
    extractor = ItemSalesDetailExtractor(csv_path)
    return extractor.export_all_dataframes()
