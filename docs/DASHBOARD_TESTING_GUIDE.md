# Sales Dashboard Testing Guide

Complete guide for testing the Sales Analytics Dashboard, including automated tests, manual testing, and test data preparation.

## Quick Start

```bash
# Run all dashboard tests
pytest tests/integration/test_dashboard_e2e.py -v

# Run with coverage
pytest tests/integration/test_dashboard_e2e.py --cov=src/quickbooks_autoreport/dashboard --cov-report=html

# Run specific test class
pytest tests/integration/test_dashboard_e2e.py::TestEndToEndFlow -v

# Run real data tests
pytest tests/integration/test_dashboard_real_data.py -v
```

## Test Structure

### Integration Tests

Located in `tests/integration/`:

```
tests/integration/
├── test_dashboard_e2e.py          # End-to-end workflow tests
├── test_dashboard_real_data.py    # Real data validation tests
└── REAL_DATA_TEST_NOTE.md         # Test findings documentation
```

### Test Classes

#### 1. TestEndToEndFlow (test_dashboard_e2e.py)

Tests complete dashboard workflows:

**test_file_selection_to_metrics_display**
- Complete flow: file selection → data load → metrics display
- Validates all metrics calculations
- Tests weekday aggregations
- Requirements: 5.3, 6.4, 9.1

```bash
pytest tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_file_selection_to_metrics_display -v
```

**test_manual_refresh_functionality**
- Tests manual data refresh
- Validates timestamp updates
- Requirements: 6.4

**test_automatic_polling_detection**
- Tests file modification detection
- Validates debouncing (5 seconds)
- Tests stability checks (2 seconds)
- Requirements: 6.4

**test_error_missing_file**
- Tests FileNotFoundError handling
- Requirements: 9.1

**test_error_missing_columns**
- Tests column validation
- Verifies missing column detection
- Requirements: 9.1, 9.2

**test_error_empty_file**
- Tests empty file handling
- Requirements: 9.1, 1.4, 2.4

**test_error_bad_data_types**
- Tests invalid data type handling
- Validates NaN handling
- Requirements: 9.2

#### 2. TestRealDataScenarios (test_dashboard_e2e.py)

Tests with various data patterns:

**test_multiweek_data**
- 3 weeks of data aggregation
- Validates weekday totals across weeks
- Requirements: 3.5, 4.5

**test_single_day_data**
- Single day aggregation
- Requirements: 3.5, 4.5

**test_large_file_performance**
- 1000 rows performance test
- Load time < 3 seconds
- Calculation time < 2 seconds
- Requirements: 10.1, 10.2, 10.5

#### 3. TestEdgeCases (test_dashboard_e2e.py)

Tests boundary conditions:

**test_zero_values**
- All zero amounts and quantities

**test_negative_values**
- Returns/refunds handling

**test_duplicate_products**
- Product name aggregation

#### 4. TestRealDataFiles (test_dashboard_real_data.py)

Tests with actual output files:

**test_load_real_sales_file**
- Loads actual files from output directory
- Validates format checking
- Requirements: 10.1

**test_calculate_metrics_with_real_data**
- Metrics with real data
- Requirements: 10.2

**test_charts_render_with_real_data**
- Chart generation validation
- Requirements: 10.4

**test_performance_with_large_real_file**
- Performance with largest file
- Requirements: 10.1, 10.2, 10.5

**test_data_integrity_with_real_file**
- Data structure validation
- Type checking
- Null value detection

## Running Tests

### Run All Tests

```bash
# All dashboard integration tests
pytest tests/integration/ -v

# With detailed output
pytest tests/integration/ -v -s

# With coverage report
pytest tests/integration/ --cov=src/quickbooks_autoreport/dashboard --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Run Specific Tests

```bash
# Single test
pytest tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_file_selection_to_metrics_display -v

# Test class
pytest tests/integration/test_dashboard_e2e.py::TestEdgeCases -v

# By keyword
pytest tests/integration/ -k "error" -v  # All error tests
pytest tests/integration/ -k "performance" -v  # All performance tests
```

### Run with Options

```bash
# Stop on first failure
pytest tests/integration/ -x

# Show local variables on failure
pytest tests/integration/ -l

# Verbose with traceback
pytest tests/integration/ -v --tb=short

# Quiet mode (less output)
pytest tests/integration/ -q

# Show print statements
pytest tests/integration/ -s
```

## Test Data Preparation

### Creating Test Files

The tests automatically create temporary test files. To create your own test data:

#### 1. Valid Sales File

```python
import pandas as pd
from pathlib import Path

# Create test data
data = {
    'Transaction_Total': [100.0, 200.0, 150.0, 300.0, 250.0],
    'Sales_Amount': [90.0, 180.0, 135.0, 270.0, 225.0],
    'Sales_Qty': [10, 20, 15, 30, 25],
    'Product': ['Product A', 'Product B', 'Product C', 'Product A', 'Product B'],
    'Date': pd.date_range('2025-01-06', periods=5, freq='D')  # Monday-Friday
}
df = pd.DataFrame(data)

# Save to output directory
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)
df.to_excel(output_dir / 'test_sales_data.xlsx', index=False)
```

#### 2. Multi-Week Data

```python
# Create 3 weeks of data
dates = []
for week in range(3):
    week_start = pd.Timestamp('2025-01-06') + pd.Timedelta(weeks=week)
    dates.extend(pd.date_range(week_start, periods=7, freq='D'))

data = {
    'Transaction_Total': [100.0] * len(dates),
    'Sales_Amount': [90.0] * len(dates),
    'Sales_Qty': [10] * len(dates),
    'Product': ['Product A'] * len(dates),
    'Date': dates
}
df = pd.DataFrame(data)
df.to_excel('output/test_multiweek.xlsx', index=False)
```

#### 3. Large Performance Test File

```python
# Create 1000 rows for performance testing
num_rows = 1000
data = {
    'Transaction_Total': [100.0] * num_rows,
    'Sales_Amount': [90.0] * num_rows,
    'Sales_Qty': [10] * num_rows,
    'Product': [f'Product {i % 50}' for i in range(num_rows)],
    'Date': pd.date_range('2025-01-01', periods=num_rows, freq='h')
}
df = pd.DataFrame(data)
df.to_excel('output/test_large_file.xlsx', index=False)
```

### Required Columns

All test files must have these columns:

- **Transaction_Total** (float): Total transaction amount
- **Sales_Amount** (float): Sales amount per product
- **Sales_Qty** (int/float): Quantity sold
- **Product** (string): Product name
- **Date** (datetime): Transaction date

## Manual Testing

### 1. Launch Dashboard

```bash
streamlit run apps/dashboard/Home.py
```

### 2. Test File Selection

1. Open dashboard in browser (usually http://localhost:8501)
2. Check sidebar shows "Select Sales Data File"
3. Verify dropdown lists Excel files from output directory
4. Select a file from dropdown
5. Verify "Load Data" button appears

### 3. Test Data Loading

1. Click "Load Data" button
2. Verify loading spinner appears
3. Check for success message: "✅ Data loaded successfully!"
4. Verify file info displays:
   - File name
   - Number of rows
   - Last updated timestamp

### 4. Test Metrics Display

Verify all metrics show correctly:

**Key Metrics Section:**
- Total Revenue (formatted with $ and commas)
- Total Units Sold (formatted with commas)

**Top Products Section:**
- Top 5 Products by Revenue (horizontal bar chart)
- Top 5 Products by Units (horizontal bar chart)
- Charts should be interactive (hover, zoom, pan)

**Weekly Trends Section:**
- Revenue by Weekday (line chart)
- Units by Weekday (line chart)
- Weekdays in chronological order (Mon-Sun)

### 5. Test Manual Refresh

1. Click "🔄 Refresh Data" button in sidebar
2. Verify loading spinner
3. Check timestamp updates
4. Verify metrics recalculate

### 6. Test Automatic Polling

1. Load a file in dashboard
2. Modify the Excel file externally (add/change data)
3. Wait 5+ seconds (debounce period)
4. Dashboard should detect change and show reload prompt
5. Click reload to see updated data

### 7. Test Error Scenarios

**Missing File:**
1. Delete the selected file
2. Try to refresh
3. Verify error message displays

**Invalid Data:**
1. Create file with missing columns
2. Try to load
3. Verify validation error shows missing columns

**Empty File:**
1. Create empty Excel file
2. Try to load
3. Verify appropriate error message

### 8. Test Performance

**Load Time:**
1. Create file with 1000+ rows
2. Time the load operation
3. Should complete in < 3 seconds

**Calculation Time:**
1. After loading large file
2. Observe metrics calculation
3. Should complete in < 2 seconds

**UI Responsiveness:**
1. Dashboard should remain responsive during operations
2. No freezing or blocking

## Expected Test Results

### All Tests Passing

```
tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_file_selection_to_metrics_display PASSED
tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_manual_refresh_functionality PASSED
tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_automatic_polling_detection PASSED
tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_error_missing_file PASSED
tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_error_missing_columns PASSED
tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_error_empty_file PASSED
tests/integration/test_dashboard_e2e.py::TestEndToEndFlow::test_error_bad_data_types PASSED
tests/integration/test_dashboard_e2e.py::TestRealDataScenarios::test_multiweek_data PASSED
tests/integration/test_dashboard_e2e.py::TestRealDataScenarios::test_single_day_data PASSED
tests/integration/test_dashboard_e2e.py::TestRealDataScenarios::test_large_file_performance PASSED
tests/integration/test_dashboard_e2e.py::TestEdgeCases::test_zero_values PASSED
tests/integration/test_dashboard_e2e.py::TestEdgeCases::test_negative_values PASSED
tests/integration/test_dashboard_e2e.py::TestEdgeCases::test_duplicate_products PASSED

13 passed in ~15 seconds
```

### Coverage Report

Expected coverage for dashboard modules:

- `data_loader.py`: 80%+
- `metrics.py`: 69%+
- `sales_data.py`: 71%+
- `charts.py`: 25%+ (UI components harder to test)

## Troubleshooting Tests

### Tests Fail with Import Errors

```bash
# Ensure you're in the project root
cd quickbooks-automation

# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run tests
pytest tests/integration/ -v
```

### Tests Fail with Module Not Found

```bash
# Install project in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%\src  # Windows
```

### Tests Timeout

```bash
# Increase timeout for slow systems
pytest tests/integration/ -v --timeout=60
```

### Streamlit Cache Issues

If tests fail due to Streamlit caching:

```bash
# Clear Streamlit cache
streamlit cache clear

# Run tests again
pytest tests/integration/ -v
```

### Windows-Specific Issues

Tests mock Windows COM modules (`pythoncom`, `win32com`). If you see import errors:

```python
# These are automatically mocked in tests
sys.modules['pythoncom'] = MagicMock()
sys.modules['win32com'] = MagicMock()
sys.modules['win32com.client'] = MagicMock()
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Dashboard Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/integration/test_dashboard_e2e.py -v --cov=src/quickbooks_autoreport/dashboard --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
```

## Test Maintenance

### Adding New Tests

1. **Create test function** in appropriate test class
2. **Add docstring** with requirements reference
3. **Use fixtures** for test data
4. **Add assertions** with clear messages
5. **Run test** to verify it works
6. **Update this guide** with new test info

### Updating Tests

When dashboard features change:

1. **Update test expectations** to match new behavior
2. **Add new test cases** for new features
3. **Update fixtures** if data structure changes
4. **Run full test suite** to catch regressions
5. **Update documentation** to reflect changes

## Performance Benchmarks

Expected performance on typical hardware:

| Operation | Target | Typical |
|-----------|--------|---------|
| Load 100 rows | < 3s | 0.1s |
| Load 1000 rows | < 3s | 0.5s |
| Calculate metrics (1000 rows) | < 2s | 0.05s |
| Generate charts | < 1s | 0.1s |
| File scan | < 1s | 0.05s |

## Additional Resources

- **Test Implementation Summary**: `TASK_13_IMPLEMENTATION_SUMMARY.md`
- **Real Data Test Notes**: `tests/integration/REAL_DATA_TEST_NOTE.md`
- **Dashboard Documentation**: `apps/dashboard/README.md`
- **Design Document**: `.kiro/specs/sales-dashboard/design.md`
- **Requirements**: `.kiro/specs/sales-dashboard/requirements.md`

## Support

If tests fail unexpectedly:

1. Check test output for specific error messages
2. Review `tests/integration/REAL_DATA_TEST_NOTE.md` for known issues
3. Verify test data format matches expected columns
4. Check Python version (3.7+ required)
5. Ensure all dependencies installed: `pip install -r requirements.txt`
6. Clear Streamlit cache: `streamlit cache clear`

For questions or issues, refer to the main README.md or project documentation.
