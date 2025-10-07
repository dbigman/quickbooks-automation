---
inclusion: always
---

# MPS Calculator Debugging Guidelines

## Debugging Priority Order

1. **Check Logs First**: `logs/mps_calculator_YYYYMMDD_HHMMSS.log` for ERROR/WARNING messages
2. **Validate Environment**: Verify `.env` configuration (ODOO_URL, credentials, database)
3. **Test Data Sources**: Confirm Odoo connectivity and data integrity
4. **Fix Root Cause**: Address underlying issues rather than masking symptoms

## Common Issue Patterns

### Odoo Integration Failures
- **Authentication**: Test credentials in Odoo web interface first
- **Permissions**: Verify access to required models (sale.order, stock.quant, mrp.bom)
- **Network**: Check connectivity with ping/telnet to Odoo server
- **Database**: Ensure database name matches exactly (case-sensitive)

### Data Processing Issues
- **Memory**: Monitor DataFrame memory usage for large datasets (>1000 records)
- **Data Types**: Validate numeric columns, handle NaN values in calculations
- **Location Mapping**: Check warehouse location hierarchy matches Odoo configuration
- **Required Fields**: Validate presence of critical columns before processing

### Excel Export Problems
- **File Permissions**: Ensure output directory is writable and files aren't open
- **Memory Limits**: Process large datasets in chunks for Excel generation
- **Compatibility**: Test with Excel 365 and LibreOffice

## Debugging Code Patterns

### Essential Logging
```python
# Connection debugging (never log passwords)
logger.info(f"Testing connection to {ODOO_URL}")
logger.info(f"Database: {ODOO_DATABASE}, Username: {ODOO_USERNAME}")

# Data validation
logger.info(f"DataFrame shape: {df.shape}, Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
logger.warning(f"Missing locations: {missing_locations}")

# Performance monitoring
start_time = time.time()
# ... operation ...
logger.info(f"Operation completed in {time.time() - start_time:.2f} seconds")
```

### Data Validation
```python
# Validate required columns
required_cols = ['product_id', 'quantity', 'delivery_date']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    logger.error(f"Missing required columns: {missing_cols}")
    raise ValueError(f"Missing columns: {missing_cols}")

# Check business logic constraints
negative_qty = df[df['quantity'] < 0]
if not negative_qty.empty:
    logger.warning(f"Found {len(negative_qty)} records with negative quantities")
```

## Systematic Debugging Process

1. **Reproduce**: Create minimal test case that reproduces the issue
2. **Isolate**: Identify failing component (connector, calculator, exporter)
3. **Validate**: Check input data quality and required field presence
4. **Test**: Use unit tests to validate individual components
5. **Document**: Record findings in `scripts/debug/` for complex issues

## Debug File Organization

Create targeted debug scripts in `scripts/debug/`:
- `debug_odoo_connection.py`: Test API connectivity and authentication
- `debug_data_processing.py`: Validate data transformations and calculations
- `debug_excel_export.py`: Test report generation with sample data

## Log Analysis Commands

```bash
# Find specific error patterns (Windows cmd)
findstr /n "ERROR" logs\mps_calculator_*.log
findstr /n "Connection" logs\mps_calculator_*.log
findstr /n "Authentication" logs\mps_calculator_*.log
```

## Prevention Strategies

- **Input Validation**: Validate all external data before processing
- **Retry Logic**: Implement exponential backoff for network operations
- **Memory Optimization**: Use `pd.to_numeric()` early for large datasets
- **Progress Indicators**: Add progress logging for long-running operations
- **Automated Testing**: Create tests for critical business logic paths
