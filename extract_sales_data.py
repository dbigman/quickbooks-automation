"""
Demo script to extract and analyze QuickBooks Item Sales Detail data.

Usage:
    python extract_sales_data.py
"""

import logging
import sys
from pathlib import Path

# Add src to path to avoid full package imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from quickbooks_autoreport.extractors.item_sales_detail_extractor import (
    ItemSalesDetailExtractor,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Extract and display sales data analysis."""
    csv_path = Path("data/item sales detail wk 41w.CSV")

    if not csv_path.exists():
        logger.error(f"❌ CSV file not found: {csv_path}")
        return

    # Initialize extractor
    extractor = ItemSalesDetailExtractor(csv_path)

    # Extract all data
    logger.info("=" * 60)
    logger.info("EXTRACTING SALES DATA")
    logger.info("=" * 60)

    dataframes = extractor.export_all_dataframes()

    # Display results
    logger.info("\n" + "=" * 60)
    logger.info("TRANSACTIONS OVERVIEW")
    logger.info("=" * 60)
    transactions = dataframes["transactions"]
    logger.info(f"Total transactions: {len(transactions)}")
    date_min = transactions["Date"].min()
    date_max = transactions["Date"].max()
    logger.info(f"Date range: {date_min} to {date_max}")
    total_amount = transactions["Amount"].sum()
    logger.info(f"Total sales amount: ${total_amount:,.2f}")
    type_counts = transactions["Type"].value_counts()
    logger.info(f"\nTransaction types:\n{type_counts}")

    logger.info("\n" + "=" * 60)
    logger.info("TOP 10 PRODUCTS BY NET SALES")
    logger.info("=" * 60)
    top_products = dataframes["top_products"]
    cols = ["Product_Name", "Net_Qty", "Net_Amount", "Avg_Unit_Price"]
    print(top_products[cols].to_string(index=False))

    logger.info("\n" + "=" * 60)
    logger.info("TOP 10 CUSTOMERS BY TOTAL SALES")
    logger.info("=" * 60)
    top_customers = dataframes["top_customers"]
    print(top_customers.to_string(index=False))

    logger.info("\n" + "=" * 60)
    logger.info("PRODUCT SUMMARY STATISTICS")
    logger.info("=" * 60)
    product_summary = dataframes["product_summary"]
    logger.info(f"Total unique products: {len(product_summary)}")
    net_sales = product_summary["Net_Amount"].sum()
    logger.info(f"Total net sales: ${net_sales:,.2f}")
    net_qty = product_summary["Net_Qty"].sum()
    logger.info(f"Total net quantity: {net_qty:,.0f}")
    returns_count = (product_summary["Return_Qty"] > 0).sum()
    logger.info(f"Products with returns: {returns_count}")

    logger.info("\n" + "=" * 60)
    logger.info("CUSTOMER-PRODUCT MATRIX SAMPLE")
    logger.info("=" * 60)
    matrix = dataframes["customer_product_matrix"]
    logger.info(f"Total customer-product combinations: {len(matrix)}")
    print(matrix.head(10).to_string(index=False))

    # Save to Excel for further analysis
    output_path = Path("data/sales_analysis_output.xlsx")
    logger.info(f"\n📊 Saving all DataFrames to {output_path}")

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        dataframes["transactions"].to_excel(
            writer, sheet_name="Transactions", index=False
        )
        dataframes["product_summary"].to_excel(
            writer, sheet_name="Product Summary", index=False
        )
        dataframes["customer_product_matrix"].to_excel(
            writer, sheet_name="Customer-Product", index=False
        )
        dataframes["top_products"].to_excel(
            writer, sheet_name="Top Products", index=False
        )
        dataframes["top_customers"].to_excel(
            writer, sheet_name="Top Customers", index=False
        )

    logger.info(f"✅ Analysis complete! Output saved to {output_path}")


if __name__ == "__main__":
    import pandas as pd
    main()
