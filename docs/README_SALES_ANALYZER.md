# QuickBooks Sales Data Analyzer

Quick reference guide for analyzing QuickBooks Item Sales Detail reports.

## Quick Start (3 Steps)

### 1. Install Requirements
```bash
pip install pandas numpy openpyxl
```

### 2. Export from QuickBooks
- Reports → Sales → Item Sales Detail
- Export to CSV
- Save anywhere on your computer

### 3. Run Analysis
```bash
python analyze_sales_data.py <input_file.csv>
```

**Examples:**
```bash
# Default output directory
python analyze_sales_data.py data/report.csv

# Custom output directory
python analyze_sales_data.py data/report.csv --output results

# Short option
python analyze_sales_data.py data/report.csv -o reports
```

**Output:** `<output_dir>/sales_analysis_<filename>_YYYYMMDD_HHMMSS.xlsx`

## What You Get

### 📊 5 Excel Sheets

| Sheet | Description | Use For |
|-------|-------------|---------|
| **Transactions** | All transaction lines | Detailed lookup, audit |
| **Product Summary** | Sales by product | Top sellers, performance |
| **Customer-Product** | Customer buying patterns | Key accounts, cross-sell |
| **Transaction Summary** | Invoice totals | Daily sales, verification |
| **Backordered** | Out-of-stock items | Inventory management |

## Key Features

✅ **Product Code Extraction** - Automatically extracts item codes  
✅ **Return Analysis** - Tracks returns and calculates net sales  
✅ **Backorder Tracking** - Identifies out-of-stock items  
✅ **Customer Analysis** - Shows who buys what  
✅ **Timestamp Output** - Never overwrites previous reports  

## Common Tasks

### Find Top 10 Products
```python
import pandas as pd
df = pd.read_excel('output/sales_analysis_*.xlsx', sheet_name='Product Summary')
print(df.head(10)[['Product_Name', 'Net_Amount']])
```

### Check Backordered Items
```python
df = pd.read_excel('output/sales_analysis_*.xlsx', sheet_name='Backordered')
print(f"Backordered items: {len(df)}")
```

### Analyze Customer Purchases
```python
df = pd.read_excel('output/sales_analysis_*.xlsx', sheet_name='Customer-Product')
customer_data = df[df['Customer'] == 'Your Customer Name']
print(customer_data)
```

## Command Line Usage

```bash
python analyze_sales_data.py <input_file.csv> [--output <directory>]
```

**Arguments:**
- `input_file` - Path to QuickBooks CSV file (required)
- `-o, --output` - Output directory (optional, default: `output`)

**View help:**
```bash
python analyze_sales_data.py --help
```

## File Structure

```
quickbooks-automation/
├── data/                          # Example input CSV files
│   └── item sales detail wk 41w.CSV
├── output/                        # Default output directory
│   └── sales_analysis_*.xlsx
├── analyze_sales_data.py          # CLI tool
└── docs/                          # Documentation
    ├── HOW_TO_USE_ANALYZE_SALES_DATA.md
    └── item_sales_detail_extractor.md
```

## Documentation

- **[HOW_TO_USE_ANALYZE_SALES_DATA.md](HOW_TO_USE_ANALYZE_SALES_DATA.md)** - Complete usage guide
- **[docs/item_sales_detail_extractor.md](docs/item_sales_detail_extractor.md)** - Technical documentation
- **[SALES_DATA_EXTRACTOR_SUMMARY.md](SALES_DATA_EXTRACTOR_SUMMARY.md)** - Feature overview
- **[BACKORDERED_FEATURE.md](BACKORDERED_FEATURE.md)** - Backorder tracking details

## Troubleshooting

| Problem | Solution |
|---------|----------|
| File not found | Check CSV is in `data/` folder |
| Module not found | Run `pip install pandas numpy openpyxl` |
| Encoding error | CSV should be exported from QuickBooks |
| Empty sheets | Normal if no data for that category |

## Sample Output

### Product Summary
```
Product_Code  Product_Name                                          Net_Qty  Net_Amount
D18015        DOT Mold Deep Stain and Extra Strength Cleaner 1 gal.   2900    10440.00
D11222        Hand Soap Lotion 4/1 gal. (NO ETIQUETA)                  189     3322.62
```

### Backordered Items
```
Product_Code  Product_Name                                          Invoice_Number  Customer
D60000        SPARKKLE Heavy Duty Degreaser 4/1 gal.               INV25-10798     Méndez & Company
A00626        GASCÓ Golden Egg 12/32 oz.                           INV25-10786     Mays Ochoa Chemical
```

## Advanced Usage

### Batch Processing
```python
from pathlib import Path
from analyze_sales_data import extract_transactions, create_product_summary

for csv_file in Path("data").glob("*.CSV"):
    transactions = extract_transactions(csv_file)
    products = create_product_summary(transactions)
    products.to_excel(f"output/analysis_{csv_file.stem}.xlsx")
```

### Custom Analysis
```python
import pandas as pd

# Load data
df = pd.read_excel('output/sales_analysis_*.xlsx', sheet_name='Product Summary')

# Calculate return rate
df['Return_Rate'] = (df['Return_Qty'] / df['Total_Qty'] * 100).round(2)

# Find high return products
high_returns = df[df['Return_Rate'] > 10]
print(high_returns[['Product_Name', 'Return_Rate']])
```

## Support

For detailed help, see [HOW_TO_USE_ANALYZE_SALES_DATA.md](HOW_TO_USE_ANALYZE_SALES_DATA.md)

## Version

Current version includes:
- Product code extraction
- Return analysis
- Backorder tracking
- Customer-product matrix
- Transaction summaries
- Timestamped output files
