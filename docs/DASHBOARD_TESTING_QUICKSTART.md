# Dashboard Testing Quick Start

Quick reference for testing the Sales Analytics Dashboard.

## Run All Tests

```bash
# All dashboard integration tests
pytest tests/integration/test_dashboard_e2e.py -v

# With coverage report
pytest tests/integration/test_dashboard_e2e.py --cov=src/quickbooks_autoreport/dashboard --cov-report=html
```

## Run Specific Tests

```bash
# End-to-end workflow
pytest tests/integration/test_dashboard_e2e.py::TestEndToEndFlow -v

# Error handling
pytest tests/integration/ -k "error" -v

# Performance tests
pytest tests/integration/ -k "performance" -v

# Edge cases
pytest tests/integration/test_dashboard_e2e.py::TestEdgeCases -v
```

## Manual Testing

### 1. Launch Dashboard
```bash
streamlit run apps/dashboard/Home.py
```

### 2. Test Workflow
1. Open http://localhost:8501
2. Select file from dropdown
3. Click "Load Data"
4. Verify metrics display
5. Test refresh button
6. Check charts render

### 3. Test Error Handling
- Try loading file with missing columns
- Try loading empty file
- Delete file and try to refresh

## Create Test Data

```python
import pandas as pd
from pathlib import Path

# Create valid test file
data = {
    'Transaction_Total': [100.0, 200.0, 150.0],
    'Sales_Amount': [90.0, 180.0, 135.0],
    'Sales_Qty': [10, 20, 15],
    'Product': ['Product A', 'Product B', 'Product C'],
    'Date': pd.date_range('2025-01-06', periods=3, freq='D')
}
df = pd.DataFrame(data)

# Save to output directory
Path('output').mkdir(exist_ok=True)
df.to_excel('output/test_sales.xlsx', index=False)
```

## Expected Results

✅ **13 tests passing**
- 7 end-to-end workflow tests
- 3 real data scenario tests
- 3 edge case tests

✅ **Performance**
- Load time < 3 seconds
- Calculation time < 2 seconds

✅ **Coverage**
- data_loader.py: 80%
- metrics.py: 69%
- sales_data.py: 71%

## Troubleshooting

**Import errors:**
```bash
pip install pytest pytest-cov pytest-mock
```

**Module not found:**
```bash
pip install -e .
```

**Streamlit cache issues:**
```bash
streamlit cache clear
```

## Full Documentation

See `docs/DASHBOARD_TESTING_GUIDE.md` for complete testing documentation including:
- Detailed test descriptions
- Test data preparation
- Manual testing procedures
- Performance benchmarks
- CI/CD integration
- Troubleshooting guide
