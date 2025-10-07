---
inclusion: always
---

# Python Code Style & Architecture Guidelines

## Core Python Standards

### Type Hints & Documentation

- **Required**: All function signatures, class attributes, and return types must include type hints
- **Imports**: Use `from typing import` for complex types (List, Dict, Optional, Union)
- **Documentation**: Document complex algorithms, API integrations, and business logic with docstrings

### Code Formatting (Black + Flake8)

- **Line Length**: 80 characters maximum
- **Indentation**: 4 spaces (no tabs)
- **String Quotes**: Double quotes for strings, single quotes for dict keys
- **Import Order**: Standard library, third-party, local imports (separated by blank lines)

### File Organization

- **Size Limit**: Keep files under 300 lines; refactor large modules into smaller, focused units
- **Single Responsibility**: Each class/module should have one clear purpose
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_SNAKE_CASE for constants

## MPS Calculator Architecture Patterns

### Class Design

- **Constructor Injection**: All classes take `logger: logging.Logger` in `__init__`
- **Error Handling**: Use specific exception types with meaningful messages
- **Data Processing**: Use pandas/numpy for all data manipulation and calculations

### Core Module Structure

- **main.py**: CLI orchestration only, delegate to specialized classes
- **calculator.py**: Pure calculation logic, no I/O operations
- **connector.py**: Odoo API integration, handle authentication and data fetching
- **exporter.py**: Excel generation with formatting, no business logic
- **logger.py**: Centralized logging setup, used by all modules

### Data Flow Patterns

```python
# Standard pattern for data processing
def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Process data with error handling and logging."""
    try:
        self.logger.info(f"Processing {len(df)} records")
        # Data processing logic
        result = df.copy()  # Always work on copies
        # ... processing steps ...
        self.logger.info(f"✅ Processed {len(result)} records")
        return result
    except Exception as e:
        self.logger.error(f"Error processing data: {e}")
        raise
```

## Manufacturing Domain Rules

### Inventory Management

- **Location Tracking**: Always include warehouse location columns (WH1/Stock, WH2/Stock, etc.)
- **Quantity Calculations**: Separate available_qty and total_qty, calculate reserved as difference
- **Memory Optimization**: Convert data types early using `pd.to_numeric()` for large datasets

### Order Processing

- **Priority Algorithms**: Support FIFO, LIFO, EDD, and Priority scoring methods
- **Date Handling**: Use pandas datetime for all date operations, validate date ranges
- **Customer Data**: Include customer names, salesperson, and delivery requirements

### BOM & MRP Calculations

- **Component Tracking**: Handle multi-level BOMs with nested component requirements
- **Shortage Classification**: Use OK, MINOR, MODERATE, CRITICAL based on days of supply
- **Production Constraints**: Respect capacity limits and buffer requirements

## File Naming Conventions

### Output Files

- **Excel Reports**: `MPS_SheetName_YYYYMMDD_HHMMSS.xlsx`
- **Log Files**: `mps_calculator_YYYYMMDD_HHMMSS.log`
- **Database**: `mps.db` with backups in `data/backups/`

### Code Files

- **Python Modules**: snake_case (e.g., `sales_order_extractor.py`)
- **Test Files**: `test_` prefix matching module name (e.g., `test_calculator.py`)
- **Notebooks**: Descriptive names (e.g., `MPS_tests.ipynb`, `odoo_operations.ipynb`)

## Error Handling & Logging

### Exception Patterns

```python
# Always log before raising
try:
    result = risky_operation()
except SpecificError as e:
    self.logger.error(f"Operation failed: {e}")
    raise
except Exception as e:
    self.logger.error(f"Unexpected error: {e}")
    raise
```

### Logging Standards

- **Process Flow**: Use INFO with emojis (📥 fetching, 🎯 processing, 📊 exporting, ✅ success)
- **Metrics**: Include counts and timing in success messages
- **Context**: Provide enough detail for troubleshooting in error messages

## Testing Requirements

### Test Coverage

- **Unit Tests**: All calculation logic, data processing functions
- **Integration Tests**: Odoo API connectivity, Excel export functionality
- **Data Validation**: Test with realistic datasets, handle edge cases
- **Error Scenarios**: Test connection failures, malformed data, missing configurations

### Test Patterns

```python
def test_calculation_with_valid_data(self):
    """Test MPS calculation with realistic input data."""
    # Arrange
    orders_df = create_test_orders()
    inventory_df = create_test_inventory()

    # Act
    result = calculator.calculate_mps(orders_df, inventory_df)

    # Assert
    assert len(result) > 0
    assert 'priority_score' in result.columns
```

## Performance Guidelines

### Memory Management

- **Large Datasets**: Process in chunks when handling 1000+ records
- **Data Types**: Optimize pandas dtypes early in processing pipeline
- **Caching**: Use Redis for expensive operations (inventory, BOM data)

### Processing Efficiency

- **Vectorization**: Use pandas/numpy operations instead of loops
- **Database**: Use SQLite for persistent storage with proper indexing
- **API Calls**: Batch Odoo requests when possible, implement retry logic

## Integration Standards

### Odoo API

- **Authentication**: Load credentials from `.env`, handle session expiration
- **Error Handling**: Graceful degradation for network issues, log API errors
- **Data Validation**: Validate BOM completeness, inventory accuracy before processing

### Excel Export

- **Multi-sheet Reports**: Separate sheets for different stakeholders (summary, inventory, shortages)
- **Formatting**: Corporate styling, frozen headers, conditional formatting
- **Compatibility**: Ensure Excel 365 and LibreOffice compatibility
