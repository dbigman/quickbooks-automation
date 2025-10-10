feat(analyzer): filter excluded products and add backordered report

Add filtering for excluded product codes and create backordered items report.

Changes:
- Filter out DMM-FREIGHT, D-SAMPLES, DMS-00100, and blank product codes from all sheets
- Add backordered items report (Qty=0) as separate sheet
- Exclude Qty=0 transactions from main Transactions sheet
- Add transaction summary report with date, customer, and totals
- Log filtered row count for transparency

refactor(dashboard): improve sidebar layout and status display

Simplify sidebar UI and improve visual hierarchy.

Changes:
- Remove "Current File:" display section
- Reduce "Latest Update" font size using st.caption()
- Fix "Latest Update" display issue with proper Streamlit component
- Improve spacing and visual hierarchy

chore(mcp): reorganize server configuration and add Excel support

Reorganize MCP servers between global and project configs for better maintainability.

Changes:
- Move common servers to global config (~/.kiro/settings/mcp.json):
  * sequentialthinking, time, context7, octocode, spec-workflow
- Keep project-specific servers in project config (.kiro/settings/mcp.json):
  * filesystem, odoo, excel, redis, mermaid, puppeteer, desktop-commander
- Add Excel MCP server (excel-mcp-server via uvx)
- Remove duplicate server definitions

docs(changelog): update with recent changes

Update CHANGELOG.md with analyzer filtering, dashboard improvements, and MCP configuration changes.

docs(commit): add recent examples and new scopes

Update commit message guidance with new scopes (analyzer, mcp, ui, data) and real examples from recent work.
