# Project Structure

## Core Architecture

The project follows a modular architecture with clear separation of concerns:

- **main.py**: Entry point with CLI interface and orchestration logic
- **calculator.py**: Core MPS calculation engine (`MPSCalculator` class)
- **connector.py**: Odoo API integration (`OdooConnector` class)
- **exporter.py**: Excel report generation (`ExcelExporter` class)
- **logger.py**: Centralized logging configuration
- **utils.py**: Shared utility functions
- **sales_order_extractor.py**: Specialized sales order processing

## Directory Organization

```
├── .env                    # Environment configuration (not in git)
├── main.py                 # CLI entry point and orchestration
├── calculator.py           # MPS calculation engine
├── connector.py            # Odoo API integration
├── exporter.py            # Excel export functionality
├── logger.py              # Logging setup
├── utils.py               # Shared utilities
├── sales_order_extractor.py # Sales order processing
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── mcp.json               # Model Context Protocol configuration
├── tests/                 # Unit tests
│   ├── test_calculator.py
│   └── test_main.py
├── notebooks/             # Jupyter analysis notebooks
│   ├── MPS_tests.ipynb
│   ├── odoo_operations.ipynb
│   ├── connector.py       # Notebook-specific connector
│   ├── improvement_walkthrough.ipynb
│   └── utils.py
├── logs/                  # Application logs (auto-created)
├── output/                # Generated Excel reports (auto-created)
├── data/                  # Database and backups
│   ├── mps.db            # SQLite database
│   └── backups/          # Database backups
├── docs/                  # Documentation and reference files
│   ├── DELIVERY_SCHEDULE_GUIDE.md
│   ├── IMPROVEMENTS_SUMMARY.md
│   ├── INVENTORY_LOCATIONS_SUMMARY.md
│   └── algorithm MPS Calculator.md
├── __pycache__/           # Python bytecode cache
└── .kiro/                 # Kiro AI assistant configuration
    └── steering/          # AI guidance documents
```

## Code Organization Patterns

### Class Structure
- Each major component is a class that takes a logger in `__init__`
- Classes are focused on single responsibilities (SRP)
- Methods are small and focused on specific tasks
- Constructor injection for logger dependency

### Data Flow
1. **main.py** orchestrates the entire process
2. **OdooConnector** fetches data from Odoo API (sales orders, inventory, BOM)
3. **MPSCalculator** processes data through MPS algorithms
4. **ExcelExporter** generates formatted Excel reports with multiple sheets

### Warehouse Location Tracking
The system tracks inventory across specific warehouse locations:
- **WH1/Stock**: Main warehouse 1 stock
- **WH1/Stock/A1A, A1B, A1C**: Rack locations in warehouse 1
- **WH1/Stock/A2A, A2B, A2C**: Additional rack locations
- **WH2/Stock**: Warehouse 2 stock
- **Missing locations**: WH1/Stock/Pasillo 1 - Piso, WH1/Stock/Pasillo 2 - Piso

### Error Handling
- Comprehensive try/catch blocks with specific error types
- Graceful degradation when possible
- Detailed logging for debugging
- Input validation at entry points
- Memory optimization for large datasets

### Configuration Management
- Environment variables for sensitive data (.env)
- Default values with override capability
- Validation of required configuration parameters
- Redis caching configuration
- Performance and monitoring settings

### Testing
- Unit tests in `tests/` directory using pytest
- Import modules using `importlib.util` for isolated testing
- Test data uses pandas DataFrames with realistic scenarios

## Export Structure

### Comprehensive Report Sheets
1. **Summary**: KPI overview and key metrics
2. **Sales Orders**: Prioritized order list with delivery dates
3. **Inventory**: Current stock levels by location
4. **Material Requirements**: BOM-based component needs
5. **Shortages**: Items requiring procurement/production
6. **Production Schedule**: Daily production plan
7. **Delivery Schedule**: Logistics-focused delivery planning

### Individual Export Files
- **MPS_Summary_YYYYMMDD_HHMMSS.xlsx**: Executive summary
- **MPS_Delivery_Schedule_YYYYMMDD_HHMMSS.xlsx**: Logistics planning
- **MPS_Inventory_YYYYMMDD_HHMMSS.xlsx**: Warehouse management
- **MPS_Shortages_YYYYMMDD_HHMMSS.xlsx**: Procurement planning

## File Naming Conventions

- **Python files**: lowercase with underscores (snake_case)
- **Classes**: PascalCase (MPSCalculator, OdooConnector)
- **Functions/Methods**: snake_case (prioritize_orders, get_sales_orders)
- **Constants**: UPPER_SNAKE_CASE (LOG_LEVEL, ODOO_URL)
- **Variables**: snake_case (sales_orders, inventory_data)
- **Log files**: `mps_calculator_YYYYMMDD_HHMMSS.log`
- **Excel exports**: `MPS_SheetName_YYYYMMDD_HHMMSS.xlsx`
- **Documentation**: UPPERCASE.md for important docs, lowercase.md for others

## Data Processing Patterns

### Memory Optimization
- Automatic conversion to appropriate data types (numeric, datetime)
- Memory-efficient processing for large datasets
- Data type optimization for pandas DataFrames

### Inventory Processing
- Separate columns for each warehouse location
- Available vs total quantity tracking
- Reserved quantity calculations
- Product category and production location mapping

### Order Processing
- Multi-factor priority scoring (urgency, value, age)
- Support for FIFO, LIFO, EDD, and Priority algorithms
- Customer and salesperson tracking
- Delivery date management
