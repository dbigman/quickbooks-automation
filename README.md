# QuickBooks Order Exporter

A standalone Python tool for exporting QuickBooks sales orders to Excel with Odoo ERP enrichment.

## Features

- 📥 **CSV Import**: Parse QuickBooks CSV exports (by customer or by item format)
- 🔗 **Odoo Integration**: Enrich orders with real-time Odoo data (products, inventory, BOMs)
- 📊 **Excel Export**: Generate professional Excel reports with multiple sheets
- 🏭 **Production Planning**: Organize orders by production line with to_produce calculations
- 📅 **ETA Calculation**: Automatic ETA date calculation (10 business days from order date)
- 🎨 **Professional Formatting**: Corporate styling with tables, colors, and auto-sizing

## Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and configure your Odoo connection:

```bash
cp .env.example .env
```

Edit `.env` with your Odoo credentials:

```env
ODOO_URL=http://your-odoo-server:8069
ODOO_DATABASE=YourDatabase
ODOO_USERNAME=your.email@company.com
ODOO_PASSWORD=YourPassword
```

### 3. Run the Exporter

```bash
# Interactive mode (recommended)
python export_orders.py

# Or use the module directly
python -m quickbooks.cli
```

The script will:
1. Prompt you to select a QuickBooks CSV file
2. Parse the CSV and extract sales orders
3. Connect to Odoo to enrich the data
4. Generate Excel and JSON reports in the `output/` directory

## Output Files

The exporter generates two files in the `output/` directory:

1. **Excel Report** (`QuickBooks_Sales_Orders_Report_YYYYMMDD_HHMMSS.xlsx`)
   - **Orders_Summary**: Aggregated order totals by customer
   - **Line_Items_Detail**: Complete line item breakdown
   - **PL_[ProductionLine]**: Separate sheets for each production line
   - **to_produce_Food_Sales**: Food products to produce
   - **to_produce_Detergent_Sales**: Detergent products to produce

2. **JSON Data** (`QuickBooks_Sales_Orders_Report_YYYYMMDD_HHMMSS.json`)
   - Raw data export for integration with other systems

## CSV Format Support

The exporter supports two QuickBooks CSV export formats:

### Format 1: Sales Orders by Customer
```
Customer Name,Type,Date,Num,Memo,Amount,Open Balance
ACME Corp,Sales Order,01/15/2025,SO-12345,DELIVER 01-20-25,1500.00,1500.00
```

### Format 2: Sales Orders by Item
```
Item,Type,Date,Ship,Num,Name,Qty,Qty Invoiced,Qty Pending,Amount,Open Balance
Product A (SKU-001),Sales Order,01/15/2025,01/20/25,SO-12345,ACME Corp,100,0,100,1500.00,1500.00
```

## Odoo Integration

When Odoo is available, the exporter enriches orders with:

- ✅ Product details (name, code, category)
- ✅ Production line assignments
- ✅ BOM (Bill of Materials) information
- ✅ Formula names for manufactured products
- ✅ Inventory levels and availability
- ✅ Accurate delivery dates and ETA calculations

If Odoo is unavailable, the exporter will:
- ⚠️  Prompt you to continue with QuickBooks data only
- ⚠️  Mark missing fields as "Odoo info missing"
- ⚠️  Still generate a valid Excel report

## Production Line Sheets

Orders are automatically organized by production line:

- **Line A**: Detergent Gallon Production
- **Line B**: Detergent 32oz Production
- **Line D**: Detergent 5-Gallon Production
- **Line E**: Detergent Piston/Pump Production
- **Line F**: Detergent Manual/Bulk Production
- **Line G**: Food Gallon Production
- **Line H**: Food 16oz Production
- **Line I**: Food Powder Production
- **Line J**: Food Manual/Solid Production
- **Line K**: Food Liquid Manual Production
- **Line Z**: SUDOC Specialty Production

Each production line sheet includes:
- Order date and number
- Customer name
- ETA date (calculated)
- Product details
- Quantity to produce (with conversion factors applied)

## Troubleshooting

### Odoo Connection Issues

If you see "Odoo connection failed":

1. Verify Odoo server is running and accessible
2. Check `.env` file has correct credentials
3. Ensure network connectivity to Odoo server
4. Review `logs/` directory for detailed error messages

### CSV Parsing Issues

If CSV parsing fails:

1. Ensure CSV is exported from QuickBooks in supported format
2. Check for special characters or encoding issues
3. Try opening CSV in Excel to verify structure
4. Review `logs/` for specific parsing errors

### Missing Production Lines

If products show "Unknown" production line:

1. Ensure `docs/product_categorization.xlsx` exists
2. Verify product codes match between QuickBooks and Odoo
3. Check that production line mappings are configured

## Project Structure

```
quickbooks_order_exporter/
├── quickbooks/              # Main package
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── csv_reader.py       # QuickBooks CSV parser
│   ├── odoo_enrichment.py  # Odoo integration
│   ├── excel_export.py     # Excel report generator
│   └── dataframe_utils.py  # Data processing utilities
├── docs/                    # Documentation
├── output/                  # Generated reports
├── logs/                    # Application logs
├── tests/                   # Test files
├── logger.py               # Logging configuration
├── connector.py            # Odoo connector
├── export_orders.py        # Main entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=quickbooks --cov-report=html
```

### Code Quality

```bash
# Format code
black quickbooks/

# Lint code
flake8 quickbooks/

# Type checking
mypy quickbooks/
```

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **openpyxl**: Excel file generation
- **requests**: HTTP client for Odoo API
- **python-dotenv**: Environment variable management
- **python-dateutil**: Date parsing and manipulation

## License

This project is part of the MPS Calculator system.

## Support

For issues or questions:
1. Check the `logs/` directory for detailed error messages
2. Review the documentation in `docs/`
3. Ensure all dependencies are installed correctly
4. Verify Odoo connection settings in `.env`

## Changelog

See `docs/CHANGES_SUMMARY.md` for detailed change history.
