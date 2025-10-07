---
inclusion: always
---

# Code Quality & Standards

## Python Code Standards

### Type Safety & Documentation

- **Type hints required** for all function signatures, class attributes, and return types
- Use `from typing import` for complex types (List, Dict, Optional, Union)
- Document complex algorithms, API integrations, and business logic with comprehensive docstrings
- Avoid `Any` type; use specific types or Union types when needed

### Code Organization & Structure

- **File size limit**: Keep modules under 300 lines; refactor into focused, single-responsibility units
- **Class design**: Constructor injection for dependencies (especially logger)
- **Separation of concerns**: Data retrieval, calculation logic, and reporting in separate modules
- **Error handling**: Use specific exception types with meaningful error messages

### Manufacturing Domain Patterns

- **Data processing**: Use pandas/numpy for all data manipulation and calculations
- **Inventory tracking**: Include warehouse location columns (WH1/Stock, WH2/Stock, rack locations)
- **Memory optimization**: Convert data types early using `pd.to_numeric()` for large datasets
- **Business logic**: Implement FIFO, LIFO, EDD, and Priority algorithms for order scheduling

### File Naming Conventions

- **Python modules**: snake_case (e.g., `sales_order_extractor.py`)
- **Output files**: `MPS_SheetName_YYYYMMDD_HHMMSS.xlsx` format
- **Log files**: `mps_calculator_YYYYMMDD_HHMMSS.log` format
- **Test files**: `test_` prefix matching module name

## Code Quality Requirements

### Formatting & Linting

- **Black**: 4 spaces indentation, 80 character line limit, double quotes for strings
- **Flake8**: Style checking and linting compliance
- **MyPy**: Static type checking with strict mode
- **Import order**: Standard library, third-party, local imports (separated by blank lines)

### Testing Standards

- **Coverage**: >90% for core modules (calculator.py, connector.py, exporter.py)
- **Performance**: Complete MPS runs within 2 minutes for 1000+ SKUs
- **Error scenarios**: Test network failures, malformed data, missing configurations
- **Business logic**: Validate manufacturing algorithms and inventory calculations

### Pattern Consistency

- **Logging**: Use centralized logger setup with emoji indicators (📥 fetching, 🎯 processing, 📊 exporting, ✅ success)
- **Configuration**: Environment variables in `.env` file, never commit credentials
- **Data validation**: Validate external data at entry points with meaningful error messages
- **API integration**: Implement retry logic and graceful degradation for Odoo connectivity

## Integration Standards

### MCP Tool Usage

- **Context7**: Use for documentation research and library best practices
- **Fetch**: For retrieving up-to-date technical documentation
- **Excel MCP**: For advanced Excel formatting and report generation
- Always leverage MCP tools for enhanced code generation and validation

### Manufacturing Business Rules

- **Warehouse locations**: Support 8 active locations with rack-level tracking
- **Product categories**: Handle Packaging Material, Materia Prima, Formulas, etc.
- **BOM processing**: Multi-level component explosion with shortage classification
- **Capacity constraints**: Respect production line limits and buffer requirements

### Performance & Security

- **Memory management**: Process large datasets efficiently, achieve >20% memory reduction
- **Database**: SQLite for persistent storage with proper indexing
- **Caching**: Redis-based caching with appropriate TTL values
- **Security**: Input validation, secure credential management, no hardcoded secrets
