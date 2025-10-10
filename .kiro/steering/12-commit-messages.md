---
inclusion: always
---

# Conventional Commits for Git

Commits **MUST** follow the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) specification:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types (correlate with SemVer)

* **feat:** Introduces a new feature (MINOR release)
* **fix:** Patches a bug (PATCH release)
* **build, chore, ci, docs, style, refactor, perf, test, etc.:** Other commit types (no SemVer impact unless BREAKING CHANGE)

## Scopes

* A scope **MAY** be provided in parentheses after the type, e.g.,:

  ```text
  feat(api): add new authentication endpoint
  ```

## Breaking Changes

* Indicate breaking changes by either:

  * Appending `!` after type or scope:

    ```text
    feat!: overhaul authentication flow
    ```

  * Or adding a footer:

    ```text
    BREAKING CHANGE: authentication now requires two-factor verification
    ```

## Message Structure Rules

1. **Prefix (REQUIRED):** `<type>[optional scope][!]: `
2. **Description (REQUIRED):** Brief summary after the colon.
3. **Body (OPTIONAL):** Detailed explanation separated by a blank line.
4. **Footers (OPTIONAL):** Metadata or references, one per line, separated by a blank line from the body.

## Examples

```text
fix(parser): handle empty input correctly

Introduce fallback behavior when no input is provided.

Reviewed-by: Jane Doe
Refs: #123
```

```text
feat(ui)!: redesign header component

BREAKING CHANGE: header now requires user authentication state to render.
```

```text
docs(spec): add sales dashboard specification

Create comprehensive spec for Streamlit sales analytics dashboard including
requirements, design, and implementation tasks.

- Add requirements.md with user stories and acceptance criteria
- Add design.md with architecture and component design
- Add tasks.md with detailed implementation plan
```

```text
chore(gitignore): exclude MCP configuration files

Add mcp.json files to .gitignore to prevent committing sensitive settings.
```

## Project-Specific Scopes

Common scopes used in this project:

* **spec:** Specification documents and planning
* **dashboard:** Streamlit dashboard application
* **analyzer:** Sales data analysis CLI tool (`analyze_sales_data.py`)
* **quickbooks:** QuickBooks integration and qbXML
* **odoo:** Odoo ERP integration
* **mps:** Material Planning System
* **config:** Configuration files and settings
* **mcp:** Model Context Protocol server configuration
* **deps:** Dependencies and package management
* **ui:** User interface components and styling
* **data:** Data processing and transformation logic

## Recent Commit Examples

```text
feat(analyzer): add backordered items report

Add new sheet to output Excel file showing items with Qty=0.
Includes Product_Code, Product_Name, Invoice_Number, and Customer.
```

```text
feat(analyzer): filter excluded product codes

Filter out DMM-FREIGHT, D-SAMPLES, DMS-00100, and blank product codes
from all output sheets. Log filtered count for transparency.
```

```text
refactor(dashboard): improve sidebar layout

- Remove "Current File:" display
- Reduce "Latest Update" font size using st.caption()
- Improve visual hierarchy and spacing
```

```text
chore(mcp): reorganize server configuration

Move common servers (context7, sequentialthinking, time, octocode,
spec-workflow) to global config. Keep project-specific servers
(filesystem, odoo, excel, redis) in project config.
```

```text
fix(mcp): correct Excel MCP server package name

Change from non-existent @pimzino/excel-mcp to excel-mcp-server.
Use uvx instead of npx for Python-based MCP server.
```

Use this format for all commit messages to maintain consistency and enable automated tooling.
