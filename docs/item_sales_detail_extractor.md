# Item Sales Detail Extractor

## Overview

Extracts and analyzes QuickBooks Item Sales Detail report data, organizing it into structured pandas DataFrames for analysis.

## Gasco Convention

**Important**: The `Memo` field in the CSV is treated as the **Product Name** (Gasco-specific convention).

## Files

### Standalone Script

**`analyze_sales_data.py`** - Standalone script that doesn't require package imports

```bash
python analyze_sales_data.py
```

### Package Module

**`src/quickbooks_autoreport/extractors/item_sales_detail_extractor.py`** - Reusable class for integration

```python
from pathlib import Path
from quickbooks_autoreport.extractors.item_sales_detail_extractor import (
    ItemSalesDetailExtractor
)

extractor = ItemSalesDetailExtractor(Path("data/report.csv"))
dataframes = extractor.export_all_dataframes()
```

## Output DataFrames

### 1. Transactions
All transaction lines with:
- Type, Date, Num, Product_Code, Product_Name (from Memo), Customer, Qty, Amount
- Derived fields: Is_Return, Realized_Unit_Price, Customer, Job

### 2. Product Summary
Product-level aggregation with:
- Product_Code (extracted from Type column)
- Sales_Qty, Sales_Amount, Sales_Transactions
- Return_Qty, Return_Amount, Return_Transactions
- Total_Qty (absolute sum: Sales_Qty + Return_Qty)
- Net_Qty, Net_Amount, Avg_Unit_Price

### 3. Customer-Product Matrix
Customer × Product combinations with:
- Product_Code (extracted from Type column)
- Total_Qty, Total_Amount, Transaction_Count
- Avg_Transaction_Amount

### 4. Top Products
Top 10 products by net sales amount

### 5. Transaction Summary
Transaction-level aggregation with:
- Num (transaction number)
- Date, Type, Customer
- Transaction_Total (sum of all line amounts for that transaction)

### 6. Backordered Items
Items with Qty=0 (backordered/out of stock):
- Product_Code, Product_Name
- Invoice_Number, Customer
- One row per invoice number + product combination

## Excel Output

All DataFrames are saved to `output/sales_analysis_YYYYMMDD_HHMMSS.xlsx` with separate sheets:
- Transactions
- Product Summary
- Customer-Product
- Transaction Summary
- Backordered

The `output` directory is automatically created if it doesn't exist.

**Filename Format**: `sales_analysis_20251008_143719.xlsx`
- Timestamp format: YYYYMMDD_HHMMSS
- Prevents overwriting previous analyses
- Easy to track when reports were generated

## Column Definitions

See `docs/quickbooks_item_sales_detail_columns_gasco.md` for detailed column semantics.

## Sample Output

### Top Products by Net Sales

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

**Note**: `Total_Qty` = `Sales_Qty` + `Return_Qty` (absolute sum of all transaction volumes)

### Transaction Summary

```
        Num       Date        Type                               Customer  Transaction_Total
INV25-10792 2025-10-07     Invoice                             Sudoc, LLC           12811.00
INV25-10790 2025-10-07     Invoice                             Sudoc, LLC            8193.00
INV25-10778 2025-10-06     Invoice                          Prime Lab LLC            3322.62
INV25-10777 2025-10-06     Invoice Colegio Aguadeño San Francisco de Asis            3173.30
  CR25-0536 2025-10-06 Credit Memo                 Mister Price, Mayagüez           -1232.79
```

## Key Features

- **Product code extraction**: Extracts item codes from Type column (e.g., "A00403" from "A00403 (Product Name)")
- **Encoding handling**: Uses `latin-1` encoding for QuickBooks CSV exports
- **Return detection**: Identifies Credit Memos and Refund Receipts
- **Customer/Job splitting**: Separates customer and job from Name field
- **Net calculations**: Computes net sales after returns
- **Realized pricing**: Calculates actual unit prices from Amount/Qty

## Usage Example

```python
from pathlib import Path
import pandas as pd

# Load and analyze
csv_path = Path("data/item sales detail wk 41w.CSV")

# Using standalone functions
from analyze_sales_data import (
    extract_transactions,
    create_product_summary,
    create_customer_product_matrix
)

transactions = extract_transactions(csv_path)
products = create_product_summary(transactions)
matrix = create_customer_product_matrix(transactions)

# Top 10 products
print(products.head(10))
```

## Performance

- Processes 86 transactions in < 1 second
- Handles 6,000+ line items efficiently
- Memory-efficient pandas operations
