# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Column aliases in Transactions sheet for dashboard compatibility (Sales_Amount, Sales_Qty, Transaction_Total)
- Sales Dashboard specification with comprehensive requirements, design, and implementation plan
- `.kiro/specs/sales-dashboard/requirements.md` - User stories and acceptance criteria for dashboard features
- `.kiro/specs/sales-dashboard/design.md` - Technical architecture and component design
- `.kiro/specs/sales-dashboard/tasks.md` - Detailed implementation task breakdown
- Sales Dashboard Streamlit application (`apps/dashboard/Home.py`)
- Dashboard modules for data loading, metrics calculation, and chart generation
- Integration tests for dashboard E2E workflows (`tests/integration/test_dashboard_e2e.py`)
- Integration tests for real data validation (`tests/integration/test_dashboard_real_data.py`)
- Dashboard testing guide (`docs/DASHBOARD_TESTING_GUIDE.md`)
- Test data creation script (`create_test_sales_data.py`)
- MCP configuration files (`mcp.json`) added to `.gitignore` to prevent committing sensitive settings
- Excel MCP server (`excel-mcp-server`) for Excel file manipulation
- Backordered items report in analyzer output (items with Qty=0)
- Transaction summary report showing transaction-level aggregates

### Changed

- Updated `.gitignore` to exclude all `mcp.json` files throughout the repository
- **Dashboard now reads from 'Transactions' sheet** with transaction-level data for weekday analysis
- Dashboard configuration updated to use `Product_Name` column instead of `Product`
- Required columns changed to: `Date`, `Product_Name`, `Sales_Amount`, `Sales_Qty`
- Analyzer now adds column aliases (Sales_Amount, Sales_Qty, Transaction_Total) to Transactions sheet
- Dashboard layout improved: title moved to sidebar, section headers removed
- Weekly trend charts now show Monday-Friday only and display side-by-side
- Success messages now display in sidebar instead of main content area
- Dashboard sidebar: removed "Current File:" display, reduced "Latest Update" font size
- MCP server organization: moved common servers (context7, sequentialthinking, time, octocode, spec-workflow) to global config
- Analyzer now filters out excluded product codes (DMM-FREIGHT, D-SAMPLES, DMS-00100) and blank product codes from all output sheets
- Analyzer excludes transactions with Qty=0 from Transactions sheet output (moved to Backordered sheet)

### Fixed

- Dashboard data loader now correctly reads from Transactions sheet with transaction-level data
- Dashboard now has access to Date column for weekday trend analysis
- Column name compatibility between analyzer output and dashboard expectations
- Error messages updated to reflect 'Transactions' sheet requirement
- Dashboard sidebar "Latest Update" now displays correctly using `st.caption()`

### Security

- Prevented accidental commit of MCP configuration files that may contain sensitive settings

### Performance

- Dashboard efficiently aggregates transaction-level data for metrics and charts
- Optimized data type conversions in ExcelLoader for faster processing
