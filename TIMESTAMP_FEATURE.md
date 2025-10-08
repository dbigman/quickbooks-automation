# Timestamp in Output Filename

## Overview

Added automatic timestamp to the output Excel filename to prevent overwriting previous analyses and provide clear tracking of when reports were generated.

## Implementation

### Filename Format

**Before:**
```
output/sales_analysis_output.xlsx
```

**After:**
```
output/sales_analysis_20251008_143719.xlsx
```

### Timestamp Format

- **Pattern**: `YYYYMMDD_HHMMSS`
- **Example**: `20251008_143719` = October 8, 2025 at 2:37:19 PM
- **Timezone**: Local system time

### Code Implementation

```python
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = output_dir / f"sales_analysis_{timestamp}.xlsx"
```

## Benefits

### 1. No Overwriting
- Each run creates a new file
- Previous analyses are preserved
- Easy to compare different runs

### 2. Clear Tracking
- Know exactly when each report was generated
- Useful for audit trails
- Easy to identify the latest report

### 3. Historical Analysis
- Keep multiple versions for comparison
- Track changes over time
- Useful for debugging or verification

### 4. Organized Output
- All reports in one directory
- Chronologically sortable by filename
- Easy to clean up old reports

## Usage

No changes to usage - timestamp is automatic:

```bash
python analyze_sales_data.py
```

Output:
```
📊 Saving all DataFrames to output\sales_analysis_20251008_143719.xlsx
✅ Analysis complete! Output saved to output\sales_analysis_20251008_143719.xlsx
```

## File Management

### List Recent Reports

```bash
# Windows
dir output\sales_analysis_*.xlsx /O-D

# Linux/macOS
ls -lt output/sales_analysis_*.xlsx
```

### Keep Only Latest N Reports

```bash
# Windows PowerShell - Keep latest 10
Get-ChildItem output\sales_analysis_*.xlsx | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -Skip 10 | 
    Remove-Item

# Linux/macOS - Keep latest 10
ls -t output/sales_analysis_*.xlsx | tail -n +11 | xargs rm
```

### Clean Up Old Reports

```bash
# Windows - Delete files older than 30 days
forfiles /P output /M sales_analysis_*.xlsx /D -30 /C "cmd /c del @path"

# Linux/macOS - Delete files older than 30 days
find output -name "sales_analysis_*.xlsx" -mtime +30 -delete
```

## Examples

### Multiple Runs

```
output/
├── sales_analysis_20251008_143719.xlsx  # Latest
├── sales_analysis_20251008_120530.xlsx  # Earlier today
├── sales_analysis_20251007_165432.xlsx  # Yesterday
└── sales_analysis_20251006_093015.xlsx  # Two days ago
```

### Programmatic Access

```python
from pathlib import Path
import pandas as pd

# Get latest report
output_dir = Path("output")
latest_file = max(
    output_dir.glob("sales_analysis_*.xlsx"),
    key=lambda p: p.stat().st_mtime
)

# Read latest report
df = pd.read_excel(latest_file, sheet_name="Product Summary")
print(f"Reading: {latest_file.name}")
```

### Compare Two Reports

```python
from pathlib import Path
import pandas as pd

# Get two most recent reports
output_dir = Path("output")
reports = sorted(
    output_dir.glob("sales_analysis_*.xlsx"),
    key=lambda p: p.stat().st_mtime,
    reverse=True
)

if len(reports) >= 2:
    latest = pd.read_excel(reports[0], sheet_name="Product Summary")
    previous = pd.read_excel(reports[1], sheet_name="Product Summary")
    
    # Compare
    print(f"Latest: {reports[0].name}")
    print(f"Previous: {reports[1].name}")
    print(f"Products in latest: {len(latest)}")
    print(f"Products in previous: {len(previous)}")
```

## Timestamp Parsing

To extract timestamp from filename:

```python
from datetime import datetime
from pathlib import Path

filename = "sales_analysis_20251008_143719.xlsx"
timestamp_str = filename.replace("sales_analysis_", "").replace(".xlsx", "")
timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

print(f"Report generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
# Output: Report generated: 2025-10-08 14:37:19
```

## Files Updated

1. **`analyze_sales_data.py`**
   - Added `from datetime import datetime` import
   - Changed output filename to include timestamp
   - Updated log messages

2. **Documentation**
   - Updated `docs/item_sales_detail_extractor.md`
   - Updated `TRANSACTION_SUMMARY_FEATURE.md`
   - Updated `SALES_DATA_EXTRACTOR_SUMMARY.md`
   - Created `TIMESTAMP_FEATURE.md`

## Testing

Verified:
- ✅ Timestamp format is correct (YYYYMMDD_HHMMSS)
- ✅ File is created with timestamp
- ✅ Multiple runs create different files
- ✅ All 4 sheets present in timestamped file
- ✅ Data integrity maintained
- ✅ No errors or warnings

## Backward Compatibility

If you have scripts that reference the old filename:

### Old Code
```python
df = pd.read_excel("output/sales_analysis_output.xlsx")
```

### New Code (Get Latest)
```python
from pathlib import Path

output_dir = Path("output")
latest_file = max(
    output_dir.glob("sales_analysis_*.xlsx"),
    key=lambda p: p.stat().st_mtime
)
df = pd.read_excel(latest_file)
```

## Future Enhancements

Potential additions:
- Add source filename to output (e.g., `sales_analysis_wk41_20251008_143719.xlsx`)
- Add date range from data to filename
- Option to specify custom output filename
- Automatic cleanup of old reports (keep last N)
- Summary report listing all generated reports
