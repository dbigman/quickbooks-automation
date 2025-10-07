---
inclusion: always
---

# MPS Calculator Logging Guidelines

## Core Logging Architecture

The MPS Calculator uses a centralized logging system with dual output (console + file) and timestamped log files for debugging and audit trails.

### Logger Setup Pattern

**Always use the centralized logger setup:**

```python
from logger import setup_logging

# At the start of main execution
logger = setup_logging()
```

**For class constructors, inject the logger:**

```python
class MPSCalculator:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

class OdooConnector:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
```

### Log File Management

- **Location**: All logs go to `logs/` directory (auto-created)
- **Naming**: `mps_calculator_YYYYMMDD_HHMMSS.log`
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Encoding**: UTF-8 for international character support

## Logging Levels & Usage

### INFO Level - Process Flow

Use for major process milestones and user-facing status:

```python
logger.info("📥 Fetching data from Odoo...")
logger.info("🎯 Processing MPS calculations...")
logger.info("📊 Exporting Excel reports...")
logger.info(f"✅ Retrieved {len(df)} sales order lines")
```

### WARNING Level - Non-Critical Issues

Use for missing data or configuration issues that don't stop execution:

```python
logger.warning("No sales orders found in QuickBooks CSV")
logger.warning(f"Missing locations: {list(missing_locations)}")
```

### ERROR Level - Critical Failures

Use for exceptions and failures that prevent normal operation:

```python
logger.error(f"Error during MPS calculation: {e}")
logger.error("Connection to Odoo timed out during authentication")
logger.error(f"Odoo API error for {model}.{method}: {error_msg}")
```

## Message Formatting Standards

### Use Emojis for Process Steps

- 📥 Data fetching operations
- 🎯 Processing/calculation steps
- 📊 Export/reporting operations
- ✅ Successful completions
- ❌ Failures and errors

### Include Metrics in Success Messages

```python
logger.info(f"✅ Retrieved {len(df)} sales order lines")
logger.info(f"Found {len(found_locations)} warehouse locations: {found_locations}")
logger.info(f"Date range: {date_from} to {date_to}")
```

### Provide Context in Error Messages

```python
logger.error(f"Unable to connect to Odoo at {self.url} (timeout). Check network connectivity.")
logger.error(f"Missing Odoo configuration: {missing}")
```

## Integration Points

### Odoo API Operations

Log all major API calls with timing and results:

```python
logger.info("Authenticating with Odoo...")
logger.info(f"✅ Authenticated. UID={self.uid}")
logger.info("Fetching sales orders from Odoo...")
logger.info("Fetching inventory levels from Odoo...")
```

### Excel Export Operations

Log export progress and file locations:

```python
logger.info("📊 Exporting Excel reports...")
logger.info(f"Exported comprehensive report: {filename}")
```

### Error Handling Pattern

Always log errors before raising exceptions:

```python
try:
    # operation
except Exception as e:
    logger.error(f"Error during operation: {e}")
    raise
```

## Performance Logging

### Data Processing Metrics

Include counts and timing for large operations:

```python
logger.info(f"Processing {len(orders)} orders with {algorithm} algorithm")
logger.info(f"Calculated material requirements for {len(products)} products")
```

### Memory and Resource Usage

Log significant data transformations:

```python
logger.info(f"Optimized data types for {len(df)} records")
logger.info(f"Filtered inventory for {len(target_locations)} locations")
```

## Debugging Support

### Include Relevant Context

When logging errors, include enough context for troubleshooting:

```python
logger.error(f"JSON parsing error for {model}.{method}: {e}")
logger.info(f"CSV columns: {list(orders_df.columns)}")
logger.info(f"Data sources: {data_sources.to_dict()}")
```

### Log Configuration Details

Include configuration information for debugging:

```python
logger.info(f"Algorithm: {algorithm}")
logger.info(f"Initializing Odoo connector for {self.url}")
```
