# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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

### Changed
- Updated `.gitignore` to exclude all `mcp.json` files throughout the repository
- **Dashboard now reads from 'Product Summary' sheet** instead of 'Transactions' sheet
- Dashboard configuration updated to use `Product_Name` column instead of `Product`
- Metrics calculator simplified to work with pre-aggregated data
- Required columns changed to: `Product_Name`, `Sales_Amount`, `Sales_Qty`
- Dashboard layout improved: title moved to sidebar, section headers removed
- Weekly trend charts now show Monday-Friday only and display side-by-side
- Success messages now display in sidebar instead of main content area

### Fixed
- Dashboard data loader now correctly reads from specified Excel sheet
- Product charts now use correct column names from Product Summary data
- Error messages updated to reflect 'Product Summary' sheet requirement

### Security
- Prevented accidental commit of MCP configuration files that may contain sensitive settings

### Performance
- Improved dashboard loading speed by using pre-aggregated Product Summary data
- Removed unnecessary groupby operations since data is already aggregated
