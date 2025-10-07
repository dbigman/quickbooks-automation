---
inclusion: always
---

# MPS Calculator Feature Development Guidelines

## Feature Development Principles

### Manufacturing Domain Focus

- **Business Context**: All features must align with manufacturing operations (production scheduling, inventory management, order fulfillment)
- **Data-Driven**: Features should leverage real-time Odoo ERP data for accurate planning decisions
- **Performance Critical**: Manufacturing operations require sub-2-minute processing for 1000+ SKU datasets

### Architecture Patterns

- **Modular Design**: Maintain separation between data retrieval (connector.py), calculation engine (calculator.py), and reporting (exporter.py)
- **Error Handling**: Implement comprehensive try/catch with graceful degradation and detailed logging
- **Type Safety**: All functions must include type hints and pandas/numpy data structures

## Feature Categories & Priorities

### Core MPS Functionality (P0)

- **Order Prioritization**: FIFO, LIFO, EDD, and Priority algorithms for production scheduling
- **Inventory Management**: Multi-location warehouse tracking (WH1/Stock, WH2/Stock, rack-level detail)
- **Material Requirements Planning**: BOM-based component calculations with shortage analysis
- **Production Scheduling**: Daily production plans with capacity constraints

### Reporting & Analytics (P1)

- **Excel Export**: Multi-sheet reports with corporate formatting and conditional formatting
- **KPI Dashboards**: Delivery performance metrics and operational insights
- **Delivery Scheduling**: Logistics-focused planning with urgency indicators
- **Shortage Analysis**: Material requirements and procurement planning

### Integration & Performance (P2)

- **Odoo 14 API**: Enhanced JSON-RPC integration with retry logic and caching
- **Memory Optimization**: Efficient processing for large datasets with automatic data type conversion
- **Redis Caching**: Performance improvements for expensive operations
- **Database Integration**: SQLite for persistent storage with proper indexing

## Development Standards

### Code Quality Requirements

- **Test Coverage**: >90% for calculator.py, connector.py, exporter.py
- **Performance**: Complete MPS runs within 2 minutes for 1000+ SKUs
- **Memory Efficiency**: Achieve >20% memory reduction through data type optimization
- **Error Recovery**: Graceful handling of network failures and malformed data

### Manufacturing Data Standards

- **Warehouse Locations**: Support 8 active locations with rack-level tracking
- **Product Categories**: Handle Packaging Material, Materia Prima, Formulas, etc.
- **Inventory Tracking**: Separate available_qty and total_qty with reserved calculations
- **Production Lines**: Support 12 distinct production lines with capacity constraints

### Security & Configuration

- **Environment Variables**: Store sensitive data in .env (never commit credentials)
- **API Security**: Implement proper authentication and session management for Odoo
- **Data Validation**: Validate all external data before processing
- **Logging**: Comprehensive logging with configurable levels and file rotation

## Feature Implementation Guidelines

### New Feature Checklist

1. **Business Justification**: Align with manufacturing operations and user workflows
2. **Architecture Review**: Ensure modular design and proper separation of concerns
3. **Data Model**: Define pandas DataFrame structures and validation rules
4. **Error Handling**: Implement comprehensive error scenarios and recovery
5. **Testing**: Unit tests, integration tests, and performance validation
6. **Documentation**: Update README.md, API_REFERENCE.md, and usage examples

### Manufacturing Domain Validation

- **Inventory Accuracy**: Validate warehouse location hierarchy and stock calculations
- **BOM Completeness**: Ensure multi-level component explosion works correctly
- **Capacity Constraints**: Respect production line limits and buffer requirements
- **Delivery Logic**: Validate priority scoring and scheduling algorithms

### Performance & Scalability

- **Memory Management**: Process large datasets efficiently with chunking when needed
- **Database Optimization**: Use proper indexing and query optimization
- **Caching Strategy**: Implement Redis caching for expensive operations
- **API Efficiency**: Batch Odoo requests and implement retry logic

## Integration Points

### Odoo ERP Integration

- **Authentication**: Secure credential management with session handling
- **Data Sources**: Sales orders, inventory levels, BOM structures via JSON-RPC
- **Error Handling**: Network timeouts, API errors, and data validation
- **Performance**: Batch requests and implement caching where appropriate

### Excel Reporting

- **Multi-sheet Structure**: Summary, Orders, Inventory, Shortages, Production Schedule
- **Formatting Standards**: Corporate styling, frozen headers, conditional formatting
- **Compatibility**: Ensure Excel 365 and LibreOffice support
- **Performance**: Handle large reports without memory issues

### Database & Caching

- **SQLite**: Persistent storage for MPS data with proper schema design
- **Redis**: Caching for inventory, BOM, and order data with appropriate TTL
- **Backup Strategy**: Automated backups in data/backups/ directory
- **Migration**: Handle schema changes and data migrations

## Quality Assurance

### Testing Strategy

- **Unit Tests**: All calculation logic and data processing functions
- **Integration Tests**: Odoo API connectivity and Excel export functionality
- **Performance Tests**: Large dataset processing and memory usage validation
- **Error Scenarios**: Network failures, malformed data, missing configurations

### Code Review Standards

- **Type Hints**: Required for all function signatures and class attributes
- **Documentation**: Comprehensive docstrings for complex algorithms
- **Error Messages**: Clear, actionable error descriptions with suggested fixes
- **Logging**: Appropriate log levels with meaningful context

### Deployment & Monitoring

- **Configuration**: Environment-based settings with validation
- **Logging**: Centralized logging with timestamped file outputs
- **Performance**: Monitor processing times and memory usage
- **Error Tracking**: Comprehensive error reporting and alerting