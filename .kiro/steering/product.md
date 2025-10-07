# Master Production Schedule Calculator

A Python command-line tool that integrates with Odoo 18 ERP systems to calculate Master Production Schedules (MPS). The system fetches sales orders, inventory levels, and Bill of Materials (BOM) data from Odoo, then performs Material Requirements Planning (MRP) calculations to generate production schedules and delivery plans.

## Core Functionality

- **Odoo 18 API Integration**: Connects via JSON-RPC to fetch real-time business data
- **Order Prioritization**: Supports multiple algorithms (Priority, FIFO, LIFO, EDD) for order scheduling
- **Material Requirements Planning (MRP)**: Calculates component needs based on BOMs and inventory levels
- **Inventory Shortage Analysis**: Identifies and classifies material shortages by severity
- **Production Scheduling**: Generates daily production plans with configurable capacity constraints
- **Excel Reporting**: Exports comprehensive reports and individual analysis sheets
- **Delivery Scheduling**: Creates logistics-focused delivery schedules
- **KPI Analytics**: Calculates delivery performance metrics and operational insights

## Key Business Value

The tool helps manufacturing companies optimize production planning by providing data-driven insights into order prioritization, material shortages, and delivery schedules. It bridges the gap between ERP data and actionable production planning.

## Target Users

Manufacturing companies using Odoo 18 who need automated production planning and scheduling capabilities with detailed shortage analysis and Excel-based reporting.

## Current Implementation Status

### ✅ Implemented Features
- **Odoo 18 Integration**: Full JSON-RPC API connectivity with authentication
- **Inventory Management**: Multi-location warehouse tracking (WH1/WH2 with rack-level detail)
- **Order Processing**: Sales order extraction with customer and product details
- **Priority Algorithms**: FIFO, LIFO, EDD, and multi-factor Priority scoring
- **Excel Export**: Comprehensive reporting with multiple sheets and formatting
- **Delivery Scheduling**: Dedicated logistics planning sheets
- **Memory Optimization**: Efficient data processing for large datasets
- **Error Handling**: Robust error management with detailed logging

### 🔄 Current Capabilities
- **809 Products**: Active inventory tracking across warehouse locations
- **3.2M+ Units**: Total available inventory management
- **8 Warehouse Locations**: Detailed location-specific inventory tracking
- **Multiple Product Categories**: Packaging materials, raw materials, formulas
- **Production Responsibility**: Tracking by production managers/responsible persons

### 📊 Reporting Outputs
1. **Comprehensive Report**: All-in-one Excel workbook with multiple sheets
2. **Delivery Schedule**: Logistics-focused planning sheet with urgency indicators
3. **Inventory Analysis**: Location-specific stock levels and availability
4. **Shortage Analysis**: Material requirements and procurement needs
5. **Production Schedule**: Daily production planning with capacity constraints
6. **KPI Dashboard**: Performance metrics and operational insights

### 🎯 Business Impact
- **Inventory Optimization**: Real-time visibility into 809 products across multiple locations
- **Order Prioritization**: Automated scoring based on urgency, value, and customer importance
- **Delivery Planning**: Dedicated logistics sheets with color-coded urgency levels
- **Shortage Prevention**: Proactive identification of material shortages
- **Performance Tracking**: KPI monitoring for delivery and production metrics

### 🔧 Technical Architecture
- **Modular Design**: Separate classes for connector, calculator, and exporter
- **Configuration Management**: Environment-based settings with Redis caching
- **Data Processing**: Pandas/NumPy for efficient data manipulation
- **Export Flexibility**: Multiple output formats and individual sheet exports
- **Logging**: Comprehensive logging with configurable levels and file rotation

### 📈 Performance Metrics
- **Processing Speed**: Handles 1,000+ SKUs efficiently
- **Memory Optimization**: Automatic data type conversion for large datasets
- **Error Recovery**: Graceful degradation with detailed error reporting
- **Cache Integration**: Redis-based caching for improved performance
