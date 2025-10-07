---
inclusion: always
---

# MPS Calculator Documentation Standards

## Documentation Hierarchy

### Core Documentation Files
- **README.md**: User-facing installation, usage, and quick start guide
- **CHANGELOG.md**: Version history following Keep a Changelog format
- **docs/**: Technical documentation organized by domain

### Domain-Specific Documentation
- **docs/API_REFERENCE.md**: Odoo integration endpoints and data models
- **docs/USAGE_EXAMPLES.md**: CLI commands and workflow examples
- **docs/DELIVERY_SCHEDULE_GUIDE.md**: Business process documentation
- **docs/WAREHOUSE_CONFIGURATION.md**: Inventory location setup

## Documentation Update Rules

### When Code Changes Require Documentation Updates
1. **New CLI flags or commands** → Update README.md and USAGE_EXAMPLES.md
2. **Odoo API integration changes** → Update API_REFERENCE.md
3. **Excel export format changes** → Update relevant guides in docs/
4. **Algorithm modifications** → Update algorithm documentation
5. **Configuration changes** → Update WAREHOUSE_CONFIGURATION.md or setup guides

### Manufacturing Domain Documentation
- **Warehouse Locations**: Document all 8 warehouse locations (WH1/Stock, WH2/Stock, rack locations)
- **Product Categories**: Maintain current category breakdown (Packaging Material, Materia Prima, etc.)
- **Algorithms**: Document FIFO, LIFO, EDD, and Priority scheduling algorithms
- **KPI Metrics**: Document calculation methods for delivery performance and operational insights

## File Naming Conventions

### Documentation Files
- **UPPERCASE.md**: Important project-level docs (README.md, CHANGELOG.md, LICENSE)
- **lowercase.md**: Technical and domain-specific docs
- **snake_case.md**: Multi-word technical docs (api_reference.md, usage_examples.md)

### Generated Reports Documentation
- Document Excel export formats: `MPS_SheetName_YYYYMMDD_HHMMSS.xlsx`
- Include sheet descriptions and business purpose
- Maintain examples of report outputs in docs/

## Version Control & Environment

### Git Hygiene for MPS Calculator
- **Commit Messages**: Follow Conventional Commits (feat, fix, docs, refactor)
- **Scope Tags**: Use project scopes (calculator, connector, exporter, cli)
- **Sensitive Data**: Never commit `.env` files containing Odoo credentials
- **Generated Files**: Exclude logs/, output/, __pycache__/ from version control

### Environment Documentation
- **Odoo Configuration**: Document required environment variables
- **Redis Setup**: Document caching configuration
- **Python Dependencies**: Keep requirements.txt and pyproject.toml synchronized
- **MCP Integration**: Document MCP server configurations in mcp.json

## Business Context Documentation

### Manufacturing Process Documentation
- **Production Scheduling**: Document capacity constraints and buffer management
- **Inventory Management**: Document multi-location tracking and shortage classification
- **Order Processing**: Document priority algorithms and customer requirements
- **Delivery Planning**: Document logistics scheduling and urgency indicators

### Integration Documentation
- **Odoo 14 API**: Document JSON-RPC endpoints, authentication, and data models
- **Excel Reporting**: Document multi-sheet structure and formatting standards
- **Database Schema**: Document SQLite structure for MPS data storage
- **Cache Strategy**: Document Redis usage patterns and TTL configurations
