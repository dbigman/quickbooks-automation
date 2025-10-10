# Commit Message

```
fix(dashboard): use Transactions sheet with column aliases for weekday analysis

Fix dashboard to read from 'Transactions' sheet which contains Date column
needed for weekday trend analysis. Add column aliases in analyzer output
(Sales_Amount, Sales_Qty, Transaction_Total) for dashboard compatibility.

Changes:
- Analyzer adds column aliases to Transactions sheet for dashboard compatibility
- Dashboard config updated to read from 'Transactions' sheet
- Required columns: Date, Product_Name, Sales_Amount, Sales_Qty
- Error messages updated to reference 'Transactions' sheet

Benefits:
- Dashboard now has access to Date column for weekday trend charts
- Monday-Friday revenue and units charts now functional
- Product-level metrics work correctly (top products by revenue/units)
- Transaction-level data enables time-series analysis

Files modified:
- analyze_sales_data.py
- src/quickbooks_autoreport/dashboard/config.py
- apps/dashboard/Home.py
- CHANGELOG.md

Refs: #dashboard #weekday-analysis #bugfix
```

## Alternative Short Version

```
fix(dashboard): enable weekday charts with Transactions sheet

Switch dashboard to read from Transactions sheet (has Date column) and
add column aliases in analyzer for compatibility.

- Add Sales_Amount, Sales_Qty, Transaction_Total aliases in analyzer
- Update dashboard to load Transactions sheet
- Fix weekday trend charts (Monday-Friday)

Refs: #dashboard
```

## Conventional Commit Format

```
fix(dashboard): enable weekday analysis with transaction-level data

Switch dashboard from Transaction Summary to Transactions sheet to access
Date column for weekday trend analysis. Add column aliases in analyzer
output for dashboard compatibility.

Fixes weekday revenue and units charts that were non-functional due to
missing Date column in Transaction Summary sheet.
```

## Usage

Choose one of the above formats based on your commit message preferences:

1. **Detailed version** - Use for comprehensive documentation
2. **Short version** - Use for concise commit history
3. **Conventional Commit** - Use for automated changelog generation

All formats follow Conventional Commits specification with:
- Type: `fix` (bug fix)
- Scope: `dashboard`
- Fixes critical functionality (weekday charts)
