---
inclusion: always
---

# Master Production Schedule Calculator - Product Requirements

## Core Product Principles

### Business Domain
- **Manufacturing Focus**: Small-to-medium manufacturers using Odoo 14 ERP systems
- **Factory Physics Foundation**: Apply scientific manufacturing principles (WIP control, variability management, decoupling buffers)
- **Data-Driven Decisions**: Replace manual planning with automated, algorithm-based scheduling

### Key Algorithms & Classifications
- **Order Prioritization**: Priority (default), FIFO, LIFO, EDD algorithms
- **Shortage Classification**: OK, MINOR, MODERATE, CRITICAL based on days of supply
- **Capacity Management**: Discrete production lines and tank capacities with buffer allocation

## Architecture Patterns

### Modular Design
- **Separation of Concerns**: Data retrieval (connector.py), calculation engine (calculator.py), reporting (exporter.py)
- **Single Responsibility**: Each class handles one primary function with logger injection
- **Error Handling**: Comprehensive try/catch with graceful degradation and detailed logging

### Data Flow Pattern
1. **Orchestration** (main.py): CLI interface and process coordination
2. **Data Fetching** (connector.py): Odoo 14 JSON-RPC API integration
3. **Calculation** (calculator.py): MPS/MRP algorithms and scheduling logic
4. **Export** (exporter.py): Excel report generation with formatting

## Code Style & Conventions

### Python Standards
- **Type Hints**: Required for all function signatures and class attributes
- **Pandas/NumPy**: Primary data structures for calculations and analysis
- **Error Handling**: Specific exception types with meaningful error messages
- **Logging**: Centralized logger configuration with timestamped file outputs

### File Naming & Structure
- **Output Files**: `MPS_SheetName_YYYYMMDD_HHMMSS.xlsx` format
- **Log Files**: `mps_calculator_YYYYMMDD_HHMMSS.log` format
- **Configuration**: Environment variables in `.env` file (never committed)

## Integration Requirements

### Odoo 14 API
- **Authentication**: Load credentials from `.env` file (`ODOO_URL`, `ODOO_DB`, `ODOO_USERNAME`, `ODOO_PASSWORD`)
- **Data Sources**: Sales orders, inventory levels, BOM structures via JSON-RPC
- **Real-time**: Fetch current data for each MPS calculation run

### Excel Export Standards
- **Multi-sheet Reports**: Comprehensive overview plus individual analysis sheets
- **Formatting**: Corporate styling, frozen headers, conditional formatting
- **Charts**: Embedded pivot charts and KPI visualizations
- **Compatibility**: Excel 365 and LibreOffice support required

## Performance & Quality Standards

### Performance Targets
- **Processing Speed**: Complete MPS run for 1,000 SKUs within 2 minutes
- **Accuracy**: Schedule outputs within 5% tolerance of manual calculations
- **Reliability**: >98% successful completion rate for valid input data

### Quality Assurance
- **Test Coverage**: >90% unit and integration test coverage required
- **Code Quality**: Black formatting, flake8 linting, mypy type checking
- **Documentation**: Comprehensive README, CLI usage guides, architecture notes

## CLI Interface Standards

### Command Structure
- **Consistent Flags**: Use `--start-date`, `--algorithm`, `--output-dir` pattern
- **Progress Feedback**: Progress bars and status messages for long operations
- **Error Messages**: Clear, actionable error descriptions with suggested fixes
- **Help System**: Comprehensive `--help` documentation for all commands

### Interactive Mode
- **User Guidance**: Step-by-step prompts for configuration
- **Validation**: Input validation with clear error messages
- **Confirmation**: Summary of actions before execution

## Manufacturing Domain Rules

### Factory Physics Implementation
- **WIP Control**: Implement CONWIP-style tokens for pull control when WIP limits are active
- **Variability Management**: Use P-K equation for queueing delay estimation
- **Decoupling Buffers**: Set buffer sizes based on variability and service levels
- **Push/Pull Coordination**: Balance endogenous pull signals with exogenous scheduling

### Production Constraints
- **Capacity Respect**: Honor discrete production line and tank capacities
- **Buffer Integration**: Incorporate buffers to absorb demand/supply variability
- **Multi-level BOM**: Handle complex bill-of-materials with nested components
- **Inventory Awareness**: Consider on-hand stock and pending receipts in calculations

## Data Validation & Error Handling

### Input Validation
- **Odoo Data Integrity**: Validate BOM completeness and inventory accuracy
- **Date Range Logic**: Ensure scheduling dates are logical and achievable
- **Capacity Constraints**: Verify production capacity data is realistic
- **Algorithm Parameters**: Validate prioritization algorithm inputs

### Error Recovery
- **Graceful Degradation**: Continue processing when non-critical errors occur
- **Detailed Logging**: Capture sufficient detail for troubleshooting
- **User Feedback**: Provide actionable error messages with suggested fixes
- **Rollback Capability**: Allow recovery from partial processing failures