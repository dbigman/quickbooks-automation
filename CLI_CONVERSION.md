# CLI Conversion Summary

## Overview

Converted `analyze_sales_data.py` from a hardcoded script to a flexible CLI application with command-line arguments.

## Changes Made

### Before (Hardcoded)

```python
csv_path = Path("data/item sales detail wk 41w.CSV")
output_dir = Path("output")
```

**Usage:**

```bash
python analyze_sales_data.py
```

**Limitations:**

- Fixed input file location
- Fixed output directory
- Required editing script to change paths

### After (CLI Application)

```python
args = parse_arguments()
csv_path = Path(args.input_file)
output_dir = Path(args.output)
```

**Usage:**

```bash
python analyze_sales_data.py <input_file.csv> [--output <directory>]
```

**Benefits:**

- Any input file location
- Custom output directory
- No script editing needed
- Standard CLI interface

## Command Line Interface

### Syntax

```bash
python analyze_sales_data.py <input_file> [-o OUTPUT]
```

### Arguments

**Positional (Required):**

- `input_file` - Path to QuickBooks Item Sales Detail CSV file

**Optional:**

- `-o, --output` - Output directory (default: `output`)
- `-h, --help` - Show help message

### Examples

**Basic usage (default output):**

```bash
python analyze_sales_data.py data/report.csv
```

Output: `output/sales_analysis_report_20251008_160334.xlsx`

**Custom output directory:**

```bash
python analyze_sales_data.py data/report.csv --output results
```

Output: `results/sales_analysis_report_20251008_160334.xlsx`

**Short option:**

```bash
python analyze_sales_data.py data/report.csv -o weekly_reports
```

Output: `weekly_reports/sales_analysis_report_20251008_160334.xlsx`

**Absolute paths:**

```bash
python analyze_sales_data.py "C:/QuickBooks/Exports/sales.csv" -o "C:/Reports"
```

Output: `C:/Reports/sales_analysis_sales_20251008_160334.xlsx`

**With spaces in path:**

```bash
python analyze_sales_data.py "data/item sales detail wk 41w.CSV"
```

Output: `output/sales_analysis_item_sales_detail_wk_41w_20251008_160334.xlsx`

## Features

### 1. Flexible Input

- Accept any CSV file path
- Support relative and absolute paths
- Handle paths with spaces

### 2. Custom Output

- Specify output directory
- Creates directory if doesn't exist
- Supports nested directories

### 3. Smart Naming

- Includes input filename in output
- Adds timestamp for uniqueness
- Replaces spaces with underscores

### 4. Error Handling

- Validates input file exists
- Checks file extension is .csv
- Provides clear error messages
- Returns proper exit codes

### 5. Help System

```bash
python analyze_sales_data.py --help
```

Output:

```
usage: analyze_sales_data.py [-h] [-o OUTPUT] input_file

Analyze QuickBooks Item Sales Detail reports

positional arguments:
  input_file            Path to QuickBooks Item Sales Detail CSV file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory for Excel file (default: output)

Examples:
  python analyze_sales_data.py data/report.csv
  python analyze_sales_data.py data/report.csv --output results
  python analyze_sales_data.py data/report.csv -o C:/Reports
```

## Implementation Details

### Argument Parsing

```python
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze QuickBooks Item Sales Detail reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples: ..."""
    )

    parser.add_argument("input_file", type=str,
                       help="Path to QuickBooks Item Sales Detail CSV file")

    parser.add_argument("-o", "--output", type=str, default="output",
                       help="Output directory for Excel file (default: output)")

    return parser.parse_args()
```

### Input Validation

```python
# Validate input file
if not csv_path.exists():
    logger.error(f"❌ CSV file not found: {csv_path}")
    logger.error(f"   Please check the file path and try again.")
    sys.exit(1)

if not csv_path.suffix.lower() == '.csv':
    logger.error(f"❌ Input file must be a CSV file: {csv_path}")
    sys.exit(1)
```

### Output Path Generation

```python
# Create output directory
output_dir.mkdir(parents=True, exist_ok=True)

# Generate filename with input name and timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
input_stem = csv_path.stem.replace(" ", "_")
output_path = output_dir / f"sales_analysis_{input_stem}_{timestamp}.xlsx"
```

## Use Cases

### 1. Weekly Reports

```bash
# Process each week's report
python analyze_sales_data.py data/week_40.csv -o reports/week_40
python analyze_sales_data.py data/week_41.csv -o reports/week_41
python analyze_sales_data.py data/week_42.csv -o reports/week_42
```

### 2. Multiple Locations

```bash
# Different store locations
python analyze_sales_data.py data/store_a.csv -o reports/store_a
python analyze_sales_data.py data/store_b.csv -o reports/store_b
```

### 3. Batch Processing

```bash
# Windows batch file
@echo off
for %%f in (data\*.csv) do (
    python analyze_sales_data.py "%%f" -o reports
)
```

```bash
# Linux/Mac shell script
#!/bin/bash
for file in data/*.csv; do
    python analyze_sales_data.py "$file" -o reports
done
```

### 4. Scheduled Tasks

```bash
# Windows Task Scheduler
python analyze_sales_data.py "C:/QuickBooks/Exports/daily_sales.csv" -o "C:/Reports/Daily"

# Cron job (Linux/Mac)
0 9 * * * python /path/to/analyze_sales_data.py /path/to/sales.csv -o /path/to/reports
```

### 5. Integration with Other Tools

```python
import subprocess

# Call from another Python script
result = subprocess.run([
    "python", "analyze_sales_data.py",
    "data/report.csv",
    "--output", "results"
], capture_output=True, text=True)

if result.returncode == 0:
    print("Analysis completed successfully")
else:
    print(f"Error: {result.stderr}")
```

## Backward Compatibility

### Old Way (Still Works)

If you have existing scripts that import functions:

```python
from analyze_sales_data import extract_transactions, create_product_summary

transactions = extract_transactions(Path("data/report.csv"))
products = create_product_summary(transactions)
```

This still works! The CLI interface is added on top, not replacing the functions.

## Testing

### Test Cases

**1. Valid input, default output:**

```bash
python analyze_sales_data.py "data/item sales detail wk 41w.CSV"
# ✅ Creates: output/sales_analysis_item_sales_detail_wk_41w_20251008_160334.xlsx
```

**2. Valid input, custom output:**

```bash
python analyze_sales_data.py "data/item sales detail wk 41w.CSV" --output reports
# ✅ Creates: reports/sales_analysis_item_sales_detail_wk_41w_20251008_160807.xlsx
```

**3. Non-existent file:**

```bash
python analyze_sales_data.py nonexistent.csv
# ❌ Error: CSV file not found: nonexistent.csv
# Exit code: 1
```

**4. Help display:**

```bash
python analyze_sales_data.py --help
# ✅ Shows usage information
```

## Files Updated

1. **`analyze_sales_data.py`**

   - Added `argparse` import
   - Added `parse_arguments()` function
   - Updated `main()` to use arguments
   - Added input validation
   - Updated output path generation

2. **Documentation**
   - Updated `HOW_TO_USE_ANALYZE_SALES_DATA.md`
   - Updated `README_SALES_ANALYZER.md`
   - Created `CLI_CONVERSION.md`

## Benefits

### For Users

- ✅ No script editing required
- ✅ Process any CSV file
- ✅ Organize outputs by project/period
- ✅ Easy to automate
- ✅ Standard CLI interface

### For Developers

- ✅ Professional CLI tool
- ✅ Easy to integrate
- ✅ Proper error handling
- ✅ Self-documenting (--help)
- ✅ Follows best practices

## Migration Guide

### If You Were Using

```bash
python analyze_sales_data.py
```

### Now Use

```bash
python analyze_sales_data.py "data/item sales detail wk 41w.CSV"
```

### If You Want Different Output

```bash
python analyze_sales_data.py "data/item sales detail wk 41w.CSV" --output results
```

That's it! The functionality is the same, just more flexible.
