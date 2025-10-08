"""
CLI tool to extract and analyze QuickBooks Item Sales Detail.

Usage:
    python analyze_sales_data.py <input_file.csv> [--output <directory>]

Examples:
    python analyze_sales_data.py data/report.csv
    python analyze_sales_data.py data/report.csv --output results
    python analyze_sales_data.py data/report.csv -o C:/Reports
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def extract_transactions(csv_path: Path) -> pd.DataFrame:
    """Extract transaction-level data from CSV."""
    logger.info(f"📥 Loading data from {csv_path}")
    raw_df = pd.read_csv(csv_path, encoding="latin-1")

    # Extract product codes from Type column
    # Pattern: "A00403 (BELCA Vinagre...)" -> extract "A00403"
    product_code_pattern = r'^([A-Z0-9\-]+)\s*\('
    raw_df["Product_Code"] = raw_df["Type"].str.extract(
        product_code_pattern, expand=False
    )

    # Identify section breaks (Parts, Service, Other Charges, etc.)
    # These are rows where Type is not a transaction type and not a total
    section_markers = [
        "Parts", "Service", "Other Charges", "TOTAL"
    ]
    raw_df["Is_Section_Break"] = raw_df["Type"].isin(section_markers)

    # Create section groups - reset at each section break
    raw_df["Section"] = raw_df["Is_Section_Break"].cumsum()

    # Forward fill product codes only within each section
    raw_df["Product_Code"] = raw_df.groupby("Section")[
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
    transactions = raw_df[raw_df["Type"].isin(valid_types)].copy()

    # Map product codes to transaction rows
    transactions["Product_Code"] = transactions.index.map(
        raw_df["Product_Code"]
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

    # Clean up Memo field (Product Name per Gasco convention)
    transactions["Product_Name"] = transactions["Memo"].str.strip()

    # Add derived fields
    transactions["Is_Return"] = transactions["Type"].isin(
        ["Credit Memo", "Refund Receipt"]
    )

    # Split customer and job
    split_result = transactions["Name"].str.split(":", n=1, expand=True)
    transactions["Customer"] = split_result[0]

    # Drop unnecessary columns
    columns_to_drop = ["Job", "Is_Section_Break", "Section"]
    transactions = transactions.drop(
        columns=[col for col in columns_to_drop if col in transactions.columns],
        errors="ignore"
    )

    logger.info(f"✅ Extracted {len(transactions)} transaction lines")
    return transactions


def create_backordered_items(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Create backordered items report.
    
    Items with Qty=0 are considered backordered.
    One row per invoice number.
    
    Returns:
        DataFrame with backordered items
    """
    logger.info("📊 Creating backordered items report")
    
    # Filter transactions with Qty = 0 (backordered)
    backordered = transactions[transactions["Qty"] == 0].copy()
    
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
    backordered_report = backordered_report.sort_values("Invoice_Number")
    
    logger.info(f"✅ Found {len(backordered_report)} backordered items")
    return backordered_report


def create_product_summary(transactions: pd.DataFrame) -> pd.DataFrame:
    """Create product-level summary."""
    logger.info("📊 Creating product summary")

    # Separate sales and returns
    sales = transactions[~transactions["Is_Return"]].copy()
    returns = transactions[transactions["Is_Return"]].copy()

    # Aggregate sales (include Product_Code)
    sales_agg = sales.groupby("Product_Name").agg({
        "Qty": "sum",
        "Amount": "sum",
        "Num": "count",
        "Product_Code": lambda x: (
            x.dropna().iloc[0] if len(x.dropna()) > 0 else ""
        )
    }).rename(columns={
        "Qty": "Sales_Qty",
        "Amount": "Sales_Amount",
        "Num": "Sales_Transactions"
    })

    # Aggregate returns (convert to positive)
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
    summary["Net_Qty"] = summary["Sales_Qty"] - summary["Return_Qty"]
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

    logger.info(f"✅ Created summary for {len(summary)} products")
    return summary.reset_index()


def create_customer_product_matrix(
    transactions: pd.DataFrame
) -> pd.DataFrame:
    """Create customer-product matrix."""
    logger.info("📊 Creating customer-product matrix")

    matrix = transactions.groupby(["Customer", "Product_Name"]).agg({
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

    matrix["Avg_Transaction_Amount"] = (
        matrix["Total_Amount"] / matrix["Transaction_Count"]
    )

    matrix = matrix.sort_values("Total_Amount", ascending=False)

    logger.info(f"✅ Created matrix with {len(matrix)} combinations")
    return matrix.reset_index()


def get_top_customers(transactions: pd.DataFrame, n: int = 10):
    """Get top N customers by total sales."""
    customer_summary = transactions.groupby("Customer").agg({
        "Amount": "sum",
        "Num": "count"
    }).rename(columns={
        "Amount": "Total_Amount",
        "Num": "Transaction_Count"
    }).sort_values("Total_Amount", ascending=False)

    return customer_summary.head(n).reset_index()


def create_transaction_summary(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Create transaction-level summary.

    Groups by transaction number (Num) and shows date, customer,
    and total amount for each transaction.

    Returns:
        DataFrame with transaction summaries
    """
    logger.info("📊 Creating transaction summary")

    # Group by transaction number
    transaction_summary = transactions.groupby("Num").agg({
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
        f"✅ Created summary for {len(transaction_summary)} transactions"
    )
    return transaction_summary.reset_index()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze QuickBooks Item Sales Detail reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_sales_data.py data/report.csv
  python analyze_sales_data.py data/report.csv --output results
  python analyze_sales_data.py data/report.csv -o C:/Reports
        """
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to QuickBooks Item Sales Detail CSV file"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output",
        help="Output directory for Excel file (default: output)"
    )
    
    return parser.parse_args()


def main():
    """Extract and display sales data analysis."""
    # Parse command line arguments
    args = parse_arguments()
    
    csv_path = Path(args.input_file)
    output_dir = Path(args.output)

    # Validate input file
    if not csv_path.exists():
        logger.error(f"❌ CSV file not found: {csv_path}")
        logger.error(f"   Please check the file path and try again.")
        sys.exit(1)
    
    if not csv_path.suffix.lower() == '.csv':
        logger.error(f"❌ Input file must be a CSV file: {csv_path}")
        sys.exit(1)

    # Extract data
    logger.info("=" * 60)
    logger.info("EXTRACTING SALES DATA")
    logger.info("=" * 60)

    transactions = extract_transactions(csv_path)
    product_summary = create_product_summary(transactions)
    customer_product = create_customer_product_matrix(transactions)
    top_customers = get_top_customers(transactions)
    transaction_summary = create_transaction_summary(transactions)
    backordered_items = create_backordered_items(transactions)

    # Display results
    logger.info("\n" + "=" * 60)
    logger.info("TRANSACTIONS OVERVIEW")
    logger.info("=" * 60)
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
    cols = [
        "Product_Code",
        "Product_Name",
        "Total_Qty",
        "Net_Qty",
        "Net_Amount",
        "Avg_Unit_Price"
    ]
    print(product_summary.head(10)[cols].to_string(index=False))

    logger.info("\n" + "=" * 60)
    logger.info("TOP 10 CUSTOMERS BY TOTAL SALES")
    logger.info("=" * 60)
    print(top_customers.to_string(index=False))

    logger.info("\n" + "=" * 60)
    logger.info("PRODUCT SUMMARY STATISTICS")
    logger.info("=" * 60)
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
    logger.info(f"Total combinations: {len(customer_product)}")
    print(customer_product.head(10).to_string(index=False))

    logger.info("\n" + "=" * 60)
    logger.info("TRANSACTION SUMMARY SAMPLE")
    logger.info("=" * 60)
    logger.info(f"Total transactions: {len(transaction_summary)}")
    cols = ["Num", "Date", "Type", "Customer", "Transaction_Total"]
    print(transaction_summary.head(15)[cols].to_string(index=False))

    logger.info("\n" + "=" * 60)
    logger.info("BACKORDERED ITEMS")
    logger.info("=" * 60)
    logger.info(f"Total backordered items: {len(backordered_items)}")
    if len(backordered_items) > 0:
        print(backordered_items.head(20).to_string(index=False))
    else:
        logger.info("No backordered items found")

    # Save to Excel with timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Use input filename in output
    input_stem = csv_path.stem.replace(" ", "_")
    output_path = output_dir / f"sales_analysis_{input_stem}_{timestamp}.xlsx"
    
    logger.info(f"\n📊 Saving all DataFrames to {output_path}")

    # Filter transactions for output: remove rows with Qty == 0
    transactions_output = transactions[transactions["Qty"] != 0].copy()
    logger.info(
        f"📋 Filtered transactions: {len(transactions_output)} rows "
        f"(removed {len(transactions) - len(transactions_output)} with Qty=0)"
    )

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        transactions_output.to_excel(
            writer, sheet_name="Transactions", index=False
        )
        product_summary.to_excel(
            writer, sheet_name="Product Summary", index=False
        )
        customer_product.to_excel(
            writer, sheet_name="Customer-Product", index=False
        )
        transaction_summary.to_excel(
            writer, sheet_name="Transaction Summary", index=False
        )
        backordered_items.to_excel(
            writer, sheet_name="Backordered", index=False
        )

    logger.info(f"✅ Analysis complete! Output saved to {output_path}")


if __name__ == "__main__":
    main()
