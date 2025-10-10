# QuickBooks Item Sales Detail Extractor - Complete Summary

## Overview

Complete solution for extracting, analyzing, and organizing QuickBooks Item Sales Detail report data into structured pandas DataFrames with comprehensive business intelligence features.

## Features Implemented

### 1. Product Code Extraction ✅

- Extracts item codes from Type column (e.g., "A00403" from "A00403 (Product Name)")
- Uses regex pattern: `^([A-Z0-9\-]+)\s*\(`
- Forward-fills codes to all transaction rows
- Included in all relevant DataFrames

### 2. Total Quantity Calculation ✅

- `Total_Qty` = `Sales_Qty` + `Return_Qty`
- Shows absolute sum of all transaction volumes
- Useful for inventory turnover and return rate analysis
- Helps identify high-activity products

### 3. Transaction Summary ✅

- Groups line items by transaction number (Num)
- Shows date, customer, type, and total amount per transaction
- Validates that sum of line items = sum of transaction totals
- Enables transaction-level analysis and verification

### 4. Comprehensive Data Organization ✅

- Handles latin-1 encoding for Spanish characters
- Separates sales from returns
- Calculates net values (sales - returns)
- Splits customer and job from Name field
- Computes realized unit prices

## Output DataFrames

### 1. Transactions (86 rows)

All transaction line items with:

- Product_Code, Product_Name, Customer, Job
- Type, Date, Num, Qty, Amount
- Is_Return, Realized_Unit_Price

### 2. Product Summary (59 products)

Product-level aggregation with:

- Product_Code, Product_Name
- Sales_Qty, Sales_Amount, Sales_Transactions
- Return_Qty, Return_Amount, Return_Transactions
- **Total_Qty** (Sales_Qty + Return_Qty)
- Net_Qty, Net_Amount, Avg_Unit_Price

### 3. Customer-Product Matrix (67 combinations)

Customer × Product analysis with:

- Customer, Product_Name, Product_Code
- Total_Qty, Total_Amount, Transaction_Count
- Avg_Transaction_Amount

### 4. Transaction Summary (33 transactions) ⭐ NEW

Transaction-level totals with:

- Num, Date, Type, Customer
- **Transaction_Total** (sum of all line amounts)

## Excel Output

All data saved to `output/sales_analysis_YYYYMMDD_HHMMSS.xlsx` with 5 sheets:

1. Transactions
2. Product Summary
3. Customer-Product
4. Transaction Summary
5. **Backordered** ⭐ NEW

## Sample Results

### Top Products

```
Product_Code                                          Product_Name  Total_Qty  Net_Qty  Net_Amount
      D18015 DOT Mold Deep Stain and Extra Strength Cleaner 1 gal.       2900     2900    10440.00
      D60016          PROFESSIONAL SERVICES MRS ANDREA  SEPT. 2025        160      160     5376.00
      D11222               Hand Soap Lotion 4/1 gal. (NO ETIQUETA)        189      189     3322.62
```

### Products with Returns

```
Product_Code                            Product_Name  Sales_Qty  Return_Qty  Total_Qty  Net_Qty
      A00609          GASCÓ Vainilla Flavor 4/1 gal.         27          46         73      -19
      A00403 BELCA Vinagre Imitación Blanco 4/1 gal.          0         109        109     -109
```

### Transaction Summary

```
        Num       Date        Type                               Customer  Transaction_Total
INV25-10792 2025-10-07     Invoice                             Sudoc, LLC           12811.00
INV25-10790 2025-10-07     Invoice                             Sudoc, LLC            8193.00
INV25-10778 2025-10-06     Invoice                          Prime Lab LLC            3322.62
  CR25-0536 2025-10-06 Credit Memo                 Mister Price, Mayagüez           -1232.79
```

## Key Statistics

From test data (`data/item sales detail wk 41w.CSV`):

- **Total line items**: 86
- **Unique products**: 59
- **Unique transactions**: 33
- **Customer-product combinations**: 67
- **Total sales amount**: $46,019.31
- **Products with returns**: 2
- **Average lines per transaction**: 2.6
- **Largest transaction**: $12,811.00
- **Top customer**: Sudoc, LLC ($21,790.05)

## Business Intelligence Use Cases

### 1. Return Rate Analysis

```python
Return_Rate = Return_Qty / Total_Qty * 100
# Example: GASCÓ Vainilla has 63% return rate (46/73)
```

### 2. Product Activity Ranking

Sort by Total_Qty to identify busiest products regardless of sales direction

### 3. Transaction Verification

Verify invoice totals match expected amounts using Transaction Summary

### 4. Customer Analysis

- Top customers by total sales
- Customer-product purchase patterns
- Transaction frequency and average size

### 5. Problem Detection

- High Total_Qty with low/negative Net_Qty indicates return issues
- Products with only returns (Net_Qty < 0)
- Unusual transaction patterns

## Files Structure

### Scripts

- **`analyze_sales_data.py`** - Standalone script (recommended)
- **`extract_sales_data.py`** - Alternative script using package imports

### Package Module

- **`src/quickbooks_autoreport/extractors/item_sales_detail_extractor.py`** - Reusable class

### Documentation

- **`docs/item_sales_detail_extractor.md`** - Main documentation
- **`docs/quickbooks_item_sales_detail_columns_gasco.md`** - Column definitions
- **`PRODUCT_CODE_EXTRACTION.md`** - Product code feature
- **`TOTAL_QTY_FEATURE.md`** - Total quantity feature
- **`TRANSACTION_SUMMARY_FEATURE.md`** - Transaction summary feature
- **`SALES_DATA_EXTRACTOR_SUMMARY.md`** - This file

## Usage

### Quick Start

```bash
python analyze_sales_data.py
```

### Programmatic Usage

```python
from pathlib import Path
from analyze_sales_data import (
    extract_transactions,
    create_product_summary,
    create_customer_product_matrix,
    create_transaction_summary
)

# Load and analyze
csv_path = Path("data/item sales detail wk 41w.CSV")
transactions = extract_transactions(csv_path)
products = create_product_summary(transactions)
trans_summary = create_transaction_summary(transactions)

# Analyze
print(f"Total products: {len(products)}")
print(f"Total transactions: {len(trans_summary)}")
print(f"Total sales: ${products['Net_Amount'].sum():,.2f}")
```

### Using the Class

```python
from pathlib import Path
from quickbooks_autoreport.extractors.item_sales_detail_extractor import (
    ItemSalesDetailExtractor
)

extractor = ItemSalesDetailExtractor(Path("data/report.csv"))
dataframes = extractor.export_all_dataframes()

# Access DataFrames
transactions = dataframes["transactions"]
products = dataframes["product_summary"]
trans_summary = dataframes["transaction_summary"]
```

## Technical Details

### Encoding

- Uses `latin-1` encoding for QuickBooks CSV exports
- Handles Spanish characters (ñ, á, é, í, ó, ú, ü)

### Data Types

- Dates: datetime64
- Quantities: float64
- Amounts: float64
- Strings: object

### Performance

- Processes 86 transactions in < 1 second
- Handles 6,000+ line items efficiently
- Memory-efficient pandas operations

### Validation

- Sum of line items = Sum of transaction totals ✓
- Product codes correctly assigned ✓
- Return calculations accurate ✓
- No data loss in transformations ✓

## Testing

All features tested with real QuickBooks data:

- ✅ Product code extraction
- ✅ Total quantity calculation
- ✅ Transaction summary generation
- ✅ Return detection and processing
- ✅ Customer/Job splitting
- ✅ Excel export with all sheets
- ✅ Data validation and totals verification

## Future Enhancements

Potential additions:

- Time series analysis (daily/weekly/monthly trends)
- Customer segmentation (RFM analysis)
- Product category analysis
- Profit margin calculations (if cost data available)
- Forecasting and trend prediction
- Interactive dashboard (Streamlit/Dash)

## Support

For issues or questions:

1. Check documentation files
2. Review sample output in Excel
3. Verify CSV format matches QuickBooks Item Sales Detail export
4. Ensure latin-1 encoding for Spanish characters
