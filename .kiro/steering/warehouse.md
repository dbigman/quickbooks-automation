# Warehouse & Inventory Management

## Warehouse Structure

### Physical Locations

The system tracks inventory across 8 active warehouse locations:

**Warehouse 1 (WH1)**

- **WH1/Stock**: Main warehouse 1 stock area
- **WH1/Stock/A1A, A1B, A1C**: Rack locations in section A1
- **WH1/Stock/A2A, A2B, A2C**: Rack locations in section A2

**Warehouse 2 (WH2)**

- **WH2/Stock**: Main warehouse 2 stock area

**Missing Locations** (configured but not found in Odoo):

- WH1/Stock/Pasillo 1 - Piso
- WH1/Stock/Pasillo 2 - Piso

### Inventory Data Structure

Each product record includes:

- **Location-specific quantities**: Separate columns for available and total quantities per location
- **Summary totals**: `total_available_qty` and `total_qty` across all locations
- **Reserved quantities**: Calculated as difference between total and available
- **Product metadata**: Category, production location, responsible person

## Current Inventory Statistics

### Overall Metrics

- **Total Products**: 809 products with active inventory
- **Total Available**: 3,227,228.48 units available for use
- **Total On-Hand**: 3,265,209.86 units in warehouse
- **Reserved Quantity**: 37,981.38 units reserved for orders
- **Stock Availability**: 94.4% of products have available inventory

### Product Categories (Top 10)

1. **Packaging Material / Labels**: 224 products (27.7%)
2. **Materia Prima**: 110 products (13.6%)
3. **Packaging Material / Container**: 76 products (9.4%)
4. **Materia Prima / Materia Prima/Alimento**: 45 products (5.6%)
5. **Formulas Detergentes**: 42 products (5.2%)
6. **Packaging Material**: 35 products (4.3%)
7. **Samples / MULTIPURPOSE / 4/1 GAL**: 16 products (2.0%)
8. **Formulas Alimentos**: 14 products (1.7%)
9. **Materia Prima / Materia Prima/Detergente**: 11 products (1.4%)
10. **Food Sales / VANILLA / 4/1 GAL**: 11 products (1.4%)

### Production Responsibility

- **Administrator**: 373 products (46.1%)
- **Yahaira Arroyo**: 312 products (38.6%)
- **Allyson Cotto**: 41 products (5.1%)
- **Elizabeth Vazquez**: 41 products (5.1%)
- **Other managers**: 42 products (5.2%)

## High-Value Inventory Items

### Top 10 by Available Quantity

1. **SAL INDUSTRIAL MARINE** (ID: 4364): 156,640.37 units
2. **28-400 FINE RIBBED CAP WHITE** (ID: 975): 122,670.00 units
3. **28-400 PCO 1881, WHITE PP** (ID: 974): 119,983.92 units
4. **VINAGRE GITANA 16 OZ PCO 1881** (ID: 952): 82,944.00 units
5. **1-12042 MAGNUM 4CC PUMP** (ID: 957): 75,266.00 units
6. **32 Oz OBLONG CLEAR PET BOTTLE** (ID: 3270): 74,653.66 units
7. **Dichlor, 10 lbs** (ID: 3403): 74,110.71 units
8. **28-400 TWO FINGER TRIGGER SPRAYER** (ID: 3665): 71,034.11 units
9. **SALT INDUSTRIAL W/O YODO/FLUOR-BAGS** (ID: 3676): 61,498.39 units
10. **ALCOHOL 16 OZ PET** (ID: 944): 49,684.88 units

## Inventory Management Patterns

### Data Processing

- **Memory Optimization**: Automatic conversion to efficient data types
- **Location Aggregation**: Individual location tracking with summary totals
- **Real-time Updates**: Fresh data from Odoo on each calculation run
- **Error Handling**: Graceful handling of missing locations or data

### Reporting Features

- **Location-specific Reports**: Separate columns for each warehouse location
- **Utilization Analysis**: Percentage breakdown by location and category
- **Stock Alerts**: Zero stock and low stock identification
- **Responsibility Tracking**: Inventory breakdown by production managers

### Business Rules

- **Stock Classification**: Products classified as 'product' type for storability
- **Availability Calculation**: Available = Total - Reserved quantities
- **Location Hierarchy**: Warehouse > Section > Rack level tracking
- **Category Management**: Product categorization for planning and analysis

## Integration Points

### Odoo ERP Integration

- **Stock Quants**: Real-time inventory levels from stock.quant model
- **Product Details**: Product names, categories, and responsible persons
- **Location Mapping**: Complete warehouse location hierarchy
- **Reserved Quantities**: Automatic calculation of reserved stock

### MPS Calculator Integration

- **Material Requirements**: Inventory feeds into MRP calculations
- **Shortage Analysis**: Available quantities determine material shortages
- **Production Planning**: Stock levels influence production scheduling
- **Delivery Planning**: Available inventory affects delivery commitments

## Warehouse Efficiency Metrics

### Key Performance Indicators

- **Stock Availability Rate**: 94.4% (764 of 809 products in stock)
- **Inventory Utilization**: 98.8% (available vs total ratio)
- **Reservation Rate**: 1.2% (reserved vs total ratio)
- **Average Stock per Product**: 3,990 units per product

### Operational Insights

- **Zero Stock Items**: 45 products requiring immediate attention
- **Low Stock Items**: Products with less than 10 units available
- **High Utilization**: Main warehouse locations well-utilized
- **Category Distribution**: Balanced mix of raw materials and packaging

## Recommendations for Code Implementation

### When Working with Inventory Data

1. **Always use `get_inventory_levels()`** method from OdooConnector
2. **Check for `total_available_qty` column** - it's the primary availability metric
3. **Filter by `type == 'product'`** for storable products only
4. **Use location-specific columns** for detailed warehouse analysis
5. **Handle missing locations gracefully** - some configured locations may not exist

### Memory and Performance

1. **Convert data types early** - use pandas numeric conversion for efficiency
2. **Process large datasets in chunks** if needed
3. **Cache inventory data** when possible (60-second TTL recommended)
4. **Log location warnings** for missing warehouse locations

### Error Handling

1. **Validate column existence** before accessing inventory columns
2. **Handle empty DataFrames** gracefully
3. **Provide meaningful error messages** for inventory issues
4. **Log detailed information** for troubleshooting warehouse data problems
