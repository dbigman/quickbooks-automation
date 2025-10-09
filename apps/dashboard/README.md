# Sales Analytics Dashboard

Interactive Streamlit-based dashboard for visualizing and analyzing sales data from Excel files.

## Overview

The Sales Analytics Dashboard provides real-time insights into sales performance with interactive visualizations, key metrics, and automatic data refresh capabilities. It reads Excel files from the output directory and presents comprehensive analytics including revenue metrics, top products, and weekly trends.

## Features

- **📊 Key Metrics**: Total revenue and units sold with formatted displays
- **🏆 Top Products**: Top 5 products by revenue and units with horizontal bar charts
- **📈 Weekly Trends**: Interactive line charts showing revenue and units by weekday
- **🔄 Data Refresh**: Manual refresh button and automatic hourly polling
- **📁 File Selection**: Easy file selection from dropdown in sidebar
- **⚡ Performance**: Optimized data loading with caching for files up to 10MB
- **🎨 Professional UI**: Clean, responsive layout with Streamlit

## Quick Start

### Prerequisites

- Python 3.9+
- Excel files (.xlsx) in the `output` directory
- Required Python packages (see Installation)

### Installation

```bash
# Install dependencies
pip install streamlit pandas openpyxl plotly

# Or install from project root
pip install -e .
```

### Running the Dashboard

```bash
# From project root
streamlit run apps/dashboard/Home.py

# Or with custom port
streamlit run apps/dashboard/Home.py --server.port 8502
```

The dashboard will open in your default browser at `http://localhost:8501`

## Required Excel Columns

Your Excel files must contain the following columns:

| Column Name        | Type    | Description                    |
| ------------------ | ------- | ------------------------------ |
| Transaction_Total  | Numeric | Total transaction amount       |
| Sales_Amount       | Numeric | Sales amount per line item     |
| Sales_Qty          | Numeric | Quantity sold                  |
| Date (optional)    | Date    | Transaction date for trends    |
| Product (optional) | Text    | Product name for aggregations  |

**Note**: If `Date` column is present, the dashboard will automatically extract weekday names for trend analysis.

## Configuration

### Environment Variables

Configure the dashboard by setting environment variables in your `.env` file:

```bash
# Dashboard Configuration
DASHBOARD_OUTPUT_DIR=output              # Directory to scan for Excel files
DASHBOARD_POLL_INTERVAL=3600             # Auto-refresh interval (seconds)
DASHBOARD_MAX_FILE_SIZE_MB=10            # Maximum file size to process
DASHBOARD_TOP_N_PRODUCTS=5               # Number of top products to display
```

### Configuration File

Dashboard settings are defined in `src/quickbooks_autoreport/dashboard/config.py`:

```python
OUTPUT_DIR = Path("output")              # Excel files directory
POLL_INTERVAL_SECONDS = 3600             # 1 hour polling
TOP_N_PRODUCTS = 5                       # Top products count
REQUIRED_COLUMNS = [                     # Required Excel columns
    'Transaction_Total',
    'Sales_Amount',
    'Sales_Qty'
]
```

## Usage

### File Selection

1. **Select File**: Use the dropdown in the sidebar to choose an Excel file
2. **View Metrics**: Dashboard automatically loads and displays analytics
3. **Change Files**: Select a different file to analyze different data

### Data Refresh

#### Manual Refresh

Click the **"🔄 Refresh Data"** button in the sidebar to reload the current file immediately.

**Use cases:**
- File was updated externally
- Want to see latest data without waiting for auto-refresh
- Troubleshooting data issues

#### Automatic Polling

The dashboard automatically checks for file modifications every hour (configurable).

**Behavior:**
- Checks file modification timestamp every hour
- Auto-reloads if file changed since last load
- Non-blocking - doesn't interfere with UI interactions
- Displays notification when auto-reload occurs
- Errors logged silently without disrupting dashboard

**Configuration:**
```bash
# Set polling interval (in seconds)
DASHBOARD_POLL_INTERVAL=3600  # 1 hour (default)
DASHBOARD_POLL_INTERVAL=1800  # 30 minutes
DASHBOARD_POLL_INTERVAL=300   # 5 minutes
```

### Dashboard Sections

#### Key Metrics

Displays two primary metrics:

- **Sales Revenue**: Sum of all `Transaction_Total` values
- **Units Sold**: Sum of all `Sales_Qty` values

Both metrics are formatted with appropriate symbols and thousand separators.

#### Top Products

Shows top 5 products in two categories:

- **By Revenue**: Products with highest `Sales_Amount`
- **By Units**: Products with highest `Sales_Qty`

Displayed as horizontal bar charts for easy comparison.

#### Weekly Trends

Interactive line charts showing:

- **Weekly Revenue**: `Sales_Amount` aggregated by weekday
- **Weekly Units**: `Sales_Qty` aggregated by weekday

**Features:**
- Weekdays displayed in chronological order (Monday-Sunday)
- Hover tooltips show exact values
- Zoom and pan capabilities
- Multi-week data automatically aggregated

## Troubleshooting

### Common Issues

#### No Excel Files Found

**Symptom**: "No Excel files found in 'output' folder"

**Solutions:**
1. Create the `output` directory in project root
2. Add .xlsx files to the directory
3. Verify file permissions
4. Check `DASHBOARD_OUTPUT_DIR` environment variable

```bash
# Create output directory
mkdir output

# Copy Excel files
cp /path/to/sales_data.xlsx output/
```

#### Missing Required Columns

**Symptom**: "Required columns missing: [column_list]"

**Solutions:**
1. Verify Excel file contains required columns:
   - Transaction_Total
   - Sales_Amount
   - Sales_Qty
2. Check column name spelling (case-sensitive)
3. Ensure columns contain numeric data
4. Remove any extra spaces in column names

**Example Fix:**
```python
# If your Excel has different column names, rename them:
import pandas as pd
df = pd.read_excel('sales.xlsx')
df.rename(columns={
    'Total': 'Transaction_Total',
    'Amount': 'Sales_Amount',
    'Quantity': 'Sales_Qty'
}, inplace=True)
df.to_excel('output/sales_fixed.xlsx', index=False)
```

#### File Cannot Be Read

**Symptom**: "Unable to read file: [filename]"

**Solutions:**
1. Ensure file is not open in Excel
2. Check file is not corrupted
3. Verify file format is .xlsx (not .xls)
4. Check file permissions
5. Try opening file in Excel to verify it's valid

#### Dashboard Loads Slowly

**Symptom**: Dashboard takes long time to load data

**Solutions:**
1. Check file size (should be < 10MB)
2. Reduce data by filtering date range
3. Remove unnecessary columns from Excel
4. Increase `DASHBOARD_MAX_FILE_SIZE_MB` if needed

**Performance Tips:**
```bash
# Increase max file size
DASHBOARD_MAX_FILE_SIZE_MB=20

# Reduce polling frequency
DASHBOARD_POLL_INTERVAL=7200  # 2 hours
```

#### Weekday Charts Not Showing

**Symptom**: Weekly trend charts are empty or missing

**Solutions:**
1. Verify Excel file contains `Date` column
2. Check date format is recognized by pandas
3. Ensure dates are valid (not text or errors)
4. Add `Date` column if missing

**Date Format Examples:**
- 2025-10-09
- 10/09/2025
- 2025-10-09 14:30:00

#### Auto-Refresh Not Working

**Symptom**: Dashboard doesn't reload when file changes

**Solutions:**
1. Check `DASHBOARD_POLL_INTERVAL` setting
2. Verify file modification time changes when updated
3. Check dashboard logs for polling errors
4. Use manual refresh button as alternative

**Debug Polling:**
```python
# Check if file modification is detected
from pathlib import Path
from datetime import datetime

file = Path("output/sales.xlsx")
print(f"Last modified: {datetime.fromtimestamp(file.stat().st_mtime)}")
```

### Error Messages

#### "Output directory not found"

**Cause**: The `output` directory doesn't exist

**Fix**: Create the directory
```bash
mkdir output
```

#### "File not found. Please select a valid file."

**Cause**: Selected file was moved or deleted

**Fix**: 
1. Refresh file list by reloading dashboard
2. Select a different file
3. Restore the missing file

#### "Data validation error: Invalid data format"

**Cause**: Column contains non-numeric data

**Fix**:
1. Open Excel file
2. Check numeric columns contain only numbers
3. Remove text, formulas, or errors from numeric columns
4. Save and reload

#### "Unexpected error: [error message]"

**Cause**: Various issues (corrupted file, memory, etc.)

**Fix**:
1. Check dashboard logs for details
2. Try with a smaller file
3. Restart dashboard
4. Verify Excel file opens correctly in Excel

### Logging

Dashboard logs are written to console with emoji indicators:

- 📥 Loading data
- 📊 Processing calculations
- ✅ Success
- ❌ Error
- ⚠️ Warning

**View Logs:**
```bash
# Run dashboard with visible logs
streamlit run apps/dashboard/Home.py

# Logs appear in terminal where dashboard was started
```

## Performance Optimization

### Caching

The dashboard uses Streamlit's caching to optimize performance:

- **Data Loading**: Cached based on filepath and modification time
- **Metrics Calculation**: Cached when data unchanged
- **Chart Generation**: Cached configurations

**Cache Behavior:**
- Automatically cleared when file changes
- Persists across dashboard reruns
- Improves response time for repeated views

### Best Practices

1. **File Size**: Keep Excel files under 10MB for best performance
2. **Data Filtering**: Pre-filter data to relevant date ranges
3. **Column Selection**: Include only necessary columns
4. **Polling Interval**: Use longer intervals (1+ hours) for large files
5. **Browser**: Use modern browsers (Chrome, Firefox, Edge)

### Performance Targets

- **Load Time**: < 3 seconds for files under 10MB
- **Switch Time**: < 2 seconds when changing files
- **Polling**: Non-blocking, doesn't affect UI responsiveness
- **Chart Rendering**: < 1 second for standard datasets

## Development

### Project Structure

```
apps/dashboard/
├── Home.py                    # Main entry point
└── README.md                  # This file

src/quickbooks_autoreport/dashboard/
├── __init__.py
├── config.py                  # Configuration constants
├── data_loader.py             # File scanning and Excel loading
├── metrics.py                 # Metrics calculation
├── charts.py                  # Chart generation
├── sidebar.py                 # Sidebar UI component
├── metrics_display.py         # Metrics UI component
├── charts_display.py          # Charts UI component
└── utils.py                   # Utility functions

src/quickbooks_autoreport/domain/
└── sales_data.py              # Data models

tests/unit/
├── test_data_loader.py
├── test_metrics.py
├── test_charts.py
├── test_sidebar.py
├── test_metrics_display.py
└── test_charts_display.py
```

### Running Tests

```bash
# Run all dashboard tests
pytest tests/unit/test_*.py -v

# Run specific test file
pytest tests/unit/test_metrics.py -v

# Run with coverage
pytest tests/unit/ --cov=src/quickbooks_autoreport/dashboard
```

### Adding New Features

1. **New Metric**: Add calculation to `MetricsCalculator` class
2. **New Chart**: Add generation to `ChartGenerator` class
3. **New UI Section**: Create new component in dashboard package
4. **New Configuration**: Add to `config.py` and `.env.example`

### Code Quality

The dashboard follows project standards:

- Type hints for all functions
- Comprehensive error handling
- Detailed logging with emoji indicators
- Unit tests for all components
- Docstrings for public functions

## Architecture

### Design Patterns

- **Separation of Concerns**: Data, business logic, and UI in separate layers
- **Dependency Injection**: Components receive dependencies explicitly
- **Factory Pattern**: SalesData.from_file() for data creation
- **Observer Pattern**: Streamlit session state for reactive updates

### Data Flow

```
Excel File → FileScanner → ExcelLoader → SalesData
                                            ↓
                                    MetricsCalculator
                                            ↓
                                    ChartGenerator
                                            ↓
                                    UI Components
```

### Session State

Dashboard maintains state across reruns:

- `current_file`: Selected Excel file path
- `sales_data`: Loaded SalesData instance
- `last_update`: Timestamp of last data load
- `last_file_mtime`: File modification time
- `error_message`: Current error message (if any)

## Integration

### QuickBooks Auto Reporter

The dashboard integrates with QuickBooks Auto Reporter:

1. **Data Source**: Reads Excel files generated by Auto Reporter
2. **Output Directory**: Shares `output` directory configuration
3. **File Format**: Compatible with Auto Reporter Excel output
4. **Columns**: Uses same column names as Auto Reporter reports

### Workflow

```
QuickBooks → Auto Reporter → Excel Files → Dashboard → Analytics
```

## Future Enhancements

Potential improvements:

- **Multi-file Comparison**: Compare metrics across multiple files
- **Date Range Filtering**: Filter data by date range
- **Export Functionality**: Export filtered data or charts
- **Custom Aggregations**: User-defined grouping and calculations
- **Real-time Notifications**: Alert on significant metric changes
- **User Preferences**: Save preferred settings and views

## Support

For issues or questions:

1. Check this README's Troubleshooting section
2. Review dashboard logs in terminal
3. Verify Excel file format and columns
4. Test with sample data file
5. Check Streamlit documentation: https://docs.streamlit.io

## Version

Sales Analytics Dashboard v1.0

Part of QuickBooks Auto Reporter project.

## License

This dashboard maintains compatibility with QuickBooks Auto Reporter license requirements.
