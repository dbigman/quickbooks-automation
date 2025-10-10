# Output Directory Change

## Overview

Changed the Excel output location from `data/` to `output/` directory with automatic directory creation.

## Changes Made

### Before
```
data/sales_analysis_output.xlsx
```

### After
```
output/sales_analysis_output.xlsx
```

## Implementation

### Automatic Directory Creation
```python
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "sales_analysis_output.xlsx"
```

The `mkdir(exist_ok=True)` ensures:
- Directory is created if it doesn't exist
- No error if directory already exists
- Works on all operating systems (Windows, Linux, macOS)

## Benefits

1. **Separation of Concerns**
   - Input data: `data/` directory
   - Output results: `output/` directory
   - Clear distinction between source and generated files

2. **Clean Organization**
   - All analysis outputs in one place
   - Easy to find generated reports
   - Simple to clean up outputs (delete `output/` folder)

3. **Git-Friendly**
   - `output/` directory added to `.gitignore`
   - Generated files won't be committed
   - Keeps repository clean

4. **Automatic Setup**
   - No manual directory creation needed
   - Script handles everything automatically
   - Works on first run

## File Structure

```
quickbooks-automation/
├── data/                          # Input data (CSV files)
│   └── item sales detail wk 41w.CSV
├── output/                        # Generated outputs (auto-created)
│   └── sales_analysis_output.xlsx
├── analyze_sales_data.py
└── ...
```

## Usage

No changes required to usage:

```bash
python analyze_sales_data.py
```

The script will:
1. Check if `output/` directory exists
2. Create it if needed
3. Save Excel file to `output/sales_analysis_output.xlsx`
4. Display confirmation message

## Output Message

```
📊 Saving all DataFrames to output\sales_analysis_output.xlsx
✅ Analysis complete! Output saved to output\sales_analysis_output.xlsx
```

## Files Updated

1. **`analyze_sales_data.py`**
   - Changed output path from `data/` to `output/`
   - Added automatic directory creation

2. **`.gitignore`**
   - Added `/output/` to ignore generated files

3. **Documentation**
   - Updated `docs/item_sales_detail_extractor.md`
   - Updated `TRANSACTION_SUMMARY_FEATURE.md`
   - Updated `SALES_DATA_EXTRACTOR_SUMMARY.md`
   - Created `OUTPUT_DIRECTORY_CHANGE.md`

## Verification

Tested and confirmed:
- ✅ `output/` directory created automatically
- ✅ Excel file saved to `output/sales_analysis_output.xlsx`
- ✅ All 4 sheets present in output file
- ✅ No errors or warnings
- ✅ Works on Windows (tested)

## Backward Compatibility

If you have existing scripts or processes that reference the old location:

### Old Path
```python
df = pd.read_excel("data/sales_analysis_output.xlsx")
```

### New Path
```python
df = pd.read_excel("output/sales_analysis_output.xlsx")
```

Simply update the path in your code.

## Cleanup

To remove all generated outputs:

```bash
# Windows
rmdir /s /q output

# Linux/macOS
rm -rf output
```

The directory will be recreated on next run.
