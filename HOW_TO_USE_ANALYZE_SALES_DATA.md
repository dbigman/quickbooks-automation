# How to Use analyze_sales_data.py

## Quick Start

### 1. Prerequisites

**Required:**
- Python 3.8 or higher
- pandas library
- numpy library
- openpyxl library (for Excel export)

**Install dependencies:**
```bash
pip install pandas numpy openpyxl
```

### 2. Prepare Your Data

**Export from QuickBooks:**
1. Open QuickBooks Desktop
2. Go to Reports → Sales → Item Sales Detail
3. Set your date range
4. Export to CSV (File → Export → CSV)
5. Save the CSV file anywhere on your computer

### 3. Run the Script

**Basic Usage:**
```bash
python analyze_sales_data.py <input_file.csv>
```

**With Custom Output Directory:**
```bash
python analyze_sales_data.py <input_file.csv> --output <directory>
```

**Examples:**
```bash
# Default output to 'output' folder
python analyze_sales_data.py data/report.csv

# Custom output directory
python analyze_sales_data.py data/report.csv --output results

# Absolute path
python analyze_sales_data.py "C:/Reports/sales_report.csv" -o "C:/Analysis"
```

### 4. Find Your Results

**Output Location:**
```
<output_directory>/sales_analysis_<filename>_YYYYMMDD_HHMMSS.xlsx
```

Examples:
- `output/sales_analysis_report_20251008_155000.xlsx`
- `results/sales_analysis_wk_41w_20251008_155000.xlsx`
- `C:/Analysis/sales_analysis_sales_report_20251008_155000.xlsx`

## What You Get

### Excel File with 5 Sheets

#### 1. Transactions
All individual transaction lines with:
- Product codes and names
- Customer information
- Quantities and amounts
- Transaction types (Invoice, Credit Memo, etc.)

**Use for:** Detailed transaction lookup, audit trail

#### 2. Product Summary
Aggregated product sales with:
- Sales quantities and amounts
- Return quantities and amounts
- Net quantities and amounts
- Average unit prices

**Use for:** Product performance analysis, top sellers

#### 3. Customer-Product
Customer × Product matrix showing:
- Which customers buy which products
- Total quantities and amounts per customer-product pair
- Average transaction amounts

**Use for:** Customer buying patterns, key account analysis

#### 4. Transaction Summary
Invoice-level totals with:
- Transaction numbers
- Dates and types
- Customer names
- Total amounts per transaction

**Use for:** Invoice verification, daily sales tracking

#### 5. Backordered
Items with Qty=0 (out of stock) showing:
- Product codes and names
- Invoice numbers
- Affected customers

**Use for:** Inventory management, stock-out tracking

## Console Output

While running, you'll see:

```
============================================================
EXTRACTING SALES DATA
============================================================
📥 Loading data from data\item sales detail wk 41w.CSV
✅ Extracted 86 transaction lines
📊 Creating product summary
✅ Created summary for 47 products
📊 Creating customer-product matrix
✅ Created matrix with 67 combinations
📊 Creating transaction summary
✅ Created summary for 33 transactions
📊 Creating backordered items report
✅ Found 13 backordered items

============================================================
TRANSACTIONS OVERVIEW
============================================================
Total transactions: 86
Date range: 2025-10-06 00:00:00 to 2025-10-08 00:00:00
Total sales amount: $46,019.31

Transaction types:
Type
Invoice        84
Credit Memo     2

============================================================
TOP 10 PRODUCTS BY NET SALES
============================================================
[Product list displayed]

============================================================
TOP 10 CUSTOMERS BY TOTAL SALES
============================================================
[Customer list displayed]

============================================================
BACKORDERED ITEMS
============================================================
Total backordered items: 13
[Backordered items list displayed]

📊 Saving all DataFrames to output\sales_analysis_20251008_155000.xlsx
✅ Analysis complete! Output saved to output\sales_analysis_20251008_155000.xlsx
```

## Command Line Options

### View Help
```bash
python analyze_sales_data.py --help
```

### Arguments

**Required:**
- `input_file` - Path to QuickBooks CSV file

**Optional:**
- `-o, --output` - Output directory (default: `output`)

### Examples

**Process single file:**
```bash
python analyze_sales_data.py data/weekly_sales.csv
```

**Specify output directory:**
```bash
python analyze_sales_data.py data/weekly_sales.csv --output weekly_reports
```

**Use short option:**
```bash
python analyze_sales_data.py data/weekly_sales.csv -o reports
```

**Absolute paths:**
```bash
python analyze_sales_data.py "C:/QuickBooks/Exports/sales.csv" -o "C:/Reports"
```

## Advanced Usage

### Programmatic Usage

**Import and use functions:**

```python
from pathlib import Path
import pandas as pd
from analyze_sales_data import (
    extract_transactions,
    create_product_summary,
    create_customer_product_matrix,
    create_transaction_summary,
    create_backordered_items
)

# Load data
csv_path = Path("data/item sales detail wk 41w.CSV")
transactions = extract_transactions(csv_path)

# Create specific reports
products = create_product_summary(transactions)
backorders = create_backordered_items(transactions)

# Analyze
print(f"Total products: {len(products)}")
print(f"Backordered items: {len(backorders)}")

# Filter and export
top_10 = products.head(10)
top_10.to_excel("output/top_10_products.xlsx", index=False)
```

### Batch Processing

**Process multiple files:**

```python
from pathlib import Path
from analyze_sales_data import extract_transactions, create_product_summary

data_dir = Path("data")
csv_files = data_dir.glob("*.CSV")

for csv_file in csv_files:
    print(f"Processing {csv_file.name}...")
    transactions = extract_transactions(csv_file)
    products = create_product_summary(transactions)
    
    # Save with original filename
    output_name = f"analysis_{csv_file.stem}.xlsx"
    products.to_excel(f"output/{output_name}", index=False)
```

## Common Tasks

### 1. Find Top Selling Products

```python
import pandas as pd

df = pd.read_excel('output/sales_analysis_20251008_155000.xlsx', 
                   sheet_name='Product Summary')

# Top 10 by net amount
top_10 = df.nlargest(10, 'Net_Amount')
print(top_10[['Product_Code', 'Product_Name', 'Net_Amount']])
```

### 2. Analyze Customer Purchases

```python
import pandas as pd

df = pd.read_excel('output/sales_analysis_20251008_155000.xlsx',
                   sheet_name='Customer-Product')

# All purchases by specific customer
customer = "Sudoc, LLC"
customer_purchases = df[df['Customer'] == customer]
print(f"Products purchased by {customer}:")
print(customer_purchases[['Product_Name', 'Total_Qty', 'Total_Amount']])
```

### 3. Check Backordered Items

```python
import pandas as pd

df = pd.read_excel('output/sales_analysis_20251008_155000.xlsx',
                   sheet_name='Backordered')

# Count by product
backorder_counts = df.groupby('Product_Name').size()
print("Most frequently backordered:")
print(backorder_counts.sort_values(ascending=False).head(10))
```

### 4. Calculate Return Rate

```python
import pandas as pd

df = pd.read_excel('output/sales_analysis_20251008_155000.xlsx',
                   sheet_name='Product Summary')

# Add return rate column
df['Return_Rate'] = (df['Return_Qty'] / df['Total_Qty'] * 100).round(2)

# Products with high return rates
high_returns = df[df['Return_Rate'] > 10].sort_values('Return_Rate', 
                                                       ascending=False)
print("Products with >10% return rate:")
print(high_returns[['Product_Name', 'Return_Rate', 'Return_Qty']])
```

### 5. Daily Sales Summary

```python
import pandas as pd

df = pd.read_excel('output/sales_analysis_20251008_155000.xlsx',
                   sheet_name='Transaction Summary')

# Group by date
df['Date'] = pd.to_datetime(df['Date'])
daily_sales = df.groupby(df['Date'].dt.date)['Transaction_Total'].sum()

print("Daily sales:")
print(daily_sales)
```

## Troubleshooting

### Error: "File not found"

**Problem:** CSV file not in `data/` directory

**Solution:**
```bash
# Check if file exists
dir data\*.CSV

# Or on Linux/Mac
ls data/*.CSV

# Make sure the filename matches exactly
```

### Error: "UnicodeDecodeError"

**Problem:** CSV encoding issue

**Solution:** The script uses `latin-1` encoding which handles Spanish characters. If you still have issues, try:
```python
# In analyze_sales_data.py, line ~27, change:
raw_df = pd.read_csv(csv_path, encoding="latin-1")

# To:
raw_df = pd.read_csv(csv_path, encoding="utf-8")
# or
raw_df = pd.read_csv(csv_path, encoding="cp1252")
```

### Error: "ModuleNotFoundError: No module named 'pandas'"

**Problem:** Required libraries not installed

**Solution:**
```bash
pip install pandas numpy openpyxl
```

### No Output File Created

**Problem:** Script ran but no Excel file

**Solution:**
1. Check for error messages in console
2. Verify `output/` directory exists (it should be auto-created)
3. Check file permissions

### Empty Sheets in Excel

**Problem:** Some sheets are empty

**Solution:** This is normal if:
- No backordered items → Backordered sheet empty
- No returns → Return columns will be 0
- Check console output for counts

## Tips & Best Practices

### 1. Regular Backups
```bash
# Keep old reports
mkdir output\archive
move output\sales_analysis_*.xlsx output\archive\
```

### 2. Automate with Task Scheduler

**Windows Task Scheduler:**
1. Create batch file `run_analysis.bat`:
```batch
@echo off
cd C:\path\to\quickbooks-automation
python analyze_sales_data.py
```

2. Schedule to run daily/weekly

### 3. Compare Time Periods

```python
import pandas as pd

# Load two reports
current = pd.read_excel('output/sales_analysis_20251008.xlsx',
                        sheet_name='Product Summary')
previous = pd.read_excel('output/sales_analysis_20251001.xlsx',
                         sheet_name='Product Summary')

# Compare
comparison = current.merge(previous, on='Product_Code', 
                          suffixes=('_current', '_previous'))
comparison['Growth'] = (
    (comparison['Net_Amount_current'] - comparison['Net_Amount_previous']) 
    / comparison['Net_Amount_previous'] * 100
)

print("Top growing products:")
print(comparison.nlargest(10, 'Growth')[['Product_Name_current', 'Growth']])
```

### 4. Export to Other Formats

```python
import pandas as pd

df = pd.read_excel('output/sales_analysis_20251008.xlsx',
                   sheet_name='Product Summary')

# Export to CSV
df.to_csv('output/product_summary.csv', index=False)

# Export to JSON
df.to_json('output/product_summary.json', orient='records')

# Export to HTML
df.to_html('output/product_summary.html', index=False)
```

## Getting Help

### Check Documentation
- `docs/item_sales_detail_extractor.md` - Full documentation
- `SALES_DATA_EXTRACTOR_SUMMARY.md` - Feature overview
- `BACKORDERED_FEATURE.md` - Backordered items details

### View Sample Output
Run the script with the included sample data to see expected output.

### Common Questions

**Q: Can I change the output directory?**
A: Yes, edit line ~295 in `analyze_sales_data.py`:
```python
output_dir = Path("your_directory")
```

**Q: Can I customize which sheets are included?**
A: Yes, comment out sheets you don't need in the Excel writer section (lines ~300-320)

**Q: How do I process multiple weeks at once?**
A: Export multiple reports from QuickBooks and use the batch processing example above

**Q: Can I schedule this to run automatically?**
A: Yes, use Windows Task Scheduler or cron (Linux/Mac) with the batch file example above
