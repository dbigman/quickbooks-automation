# QuickBooks Auto Reporter

Automated multi-report generation for QuickBooks Desktop with scheduled execution, professional Excel formatting, and business analytics.

## Overview

QuickBooks Auto Reporter automates the generation of 9 different QuickBooks reports with configurable scheduling, change detection, and professional Excel output. The tool connects directly to QuickBooks Desktop via qbXML API and generates both CSV and formatted Excel reports.

## Features

- **9 Report Types**: Open Sales Orders, Profit & Loss, Sales by Item, AP/AR Aging, and more
- **Scheduled Execution**: Configurable intervals (5, 15, 30, or 60 minutes)
- **Multiple Formats**: CSV + professionally formatted Excel with corporate styling
- **Change Detection**: Only saves timestamped snapshots when data actually changes
- **Business Analytics**: Context7 MCP integration for insights (optional)
- **Professional Excel**: Corporate blue headers (#4472C4), auto-sized columns, table formatting
- **GUI Interface**: User-friendly interface with real-time status updates
- **Diagnostics**: Built-in QuickBooks connectivity testing and troubleshooting

## Supported Reports

| Report                    | qbXML Type              | Date Range | Description                    |
| ------------------------- | ----------------------- | ---------- | ------------------------------ |
| Open Sales Orders by Item | OpenSalesOrderByItem    | No         | Current open sales orders      |
| Profit & Loss             | ProfitAndLossStandard   | Yes        | Standard P&L statement         |
| Profit & Loss Detail      | ProfitAndLossDetail     | Yes        | Detailed P&L with transactions |
| Sales by Item             | SalesByItemSummary      | Yes        | Sales summary by item          |
| Sales by Item Detail      | SalesByItemDetail       | Yes        | Detailed sales by item         |
| Sales by Rep Detail       | SalesByRepDetail        | Yes        | Sales performance by rep       |
| Purchase by Vendor Detail | PurchasesByVendorDetail | Yes        | Purchase analysis by vendor    |
| AP Aging Detail           | APAgingDetail           | AsOf       | Accounts payable aging         |
| AR Aging Detail           | ARAgingDetail           | AsOf       | Accounts receivable aging      |

## Quick Start

### Prerequisites

- Windows operating system
- QuickBooks Desktop 2019+ installed
- QuickBooks SDK installed and registered
- Python 3.7+

### Installation

```bash
# Clone or download the repository
cd quickbooks-auto-reporter

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# GUI Mode (recommended)
python quickbooks_autoreport.py --gui

# Command Line Mode
python quickbooks_autoreport.py

# Run diagnostics
python quickbooks_autoreport.py --diagnose
```

## Usage

### GUI Interface

1. **Select Output Folder**: Choose where reports will be saved
2. **Configure Date Range**: Set report date range for date-based reports
3. **Choose Interval**: Select check interval (5, 15, 30, or 60 minutes)
4. **Start Auto**: Begin scheduled automatic reporting
5. **Export All Now**: Generate all reports immediately
6. **Open Folder**: Open output directory in Windows Explorer

### Status Display

The GUI shows real-time status for each report:

- Report status (Idle, Running, Success, Error)
- Row count from last export
- Excel generation confirmation
- Next scheduled run time
- Connection information

### Configuration

Settings are automatically saved to `~/.qb_auto_reporter_settings.json`:

- Output directory preference
- Check interval preference
- Report date ranges

## Output Files

For each report type, the following files are generated:

### Standard Files

- `{Report_Name}.csv` - CSV data export
- `{Report_Name}.xlsx` - Professional Excel report
- `{Report_Name}.hash` - Change detection hash

### Timestamped Snapshots

When data changes, timestamped copies are created:

- `{Report_Name}_YYYYMMDD_HHMMSS.csv`
- `{Report_Name}_YYYYMMDD_HHMMSS.xlsx`

### Log Files

- `QuickBooks_Auto_Reports.log` - Main application log
- `{report_key}_request.xml` - qbXML request log
- `{report_key}_response.xml` - qbXML response log

## QuickBooks Integration

### Connection Methods

The application attempts multiple connection strategies:

1. Open QuickBooks file (if available)
2. User-selected QuickBooks file
3. Fallback to configured company file path

### qbXML Versions

- Primary: qbXML 16.0
- Fallback: qbXML 13.0
- Compatible with QuickBooks Desktop 2019+

### Authentication

Uses QuickBooks SDK authentication with multiple local connection modes for maximum compatibility.

## Troubleshooting

### QuickBooks Connection Issues

**Symptoms**: "Cannot connect to QuickBooks Desktop"

**Solutions**:

1. Verify QuickBooks Desktop is running
2. Install QuickBooks SDK from Intuit Developer website
3. Run application as Administrator
4. Restart computer after SDK installation
5. Close QuickBooks before running reports

### Run Diagnostics

```bash
python quickbooks_autoreport.py --diagnose
```

Generates:

- `quickbooks_diagnostics.json` - Detailed diagnostic data
- `QuickBooks_Diagnostic_Report.xlsx` - Professional diagnostic report

### Common Errors

**COM Error -2147221005: Invalid class string**

- SDK not installed or not properly registered
- Install QuickBooks SDK
- Run as Administrator
- Restart computer

**COM Error -2147221164: Class not registered**

- SDK components not properly registered
- Reinstall QuickBooks SDK
- Run `regsvr32 qbxmlrp2.dll` as Administrator

**Access Denied**

- Run application as Administrator
- Check QuickBooks company file permissions
- Ensure QuickBooks is in single-user mode

**File Not Found**

- Verify QuickBooks installation
- Check QB_COMPANY_FILE environment variable
- Open company file in QuickBooks first

### Log Analysis

Check `QuickBooks_Auto_Reports.log` for detailed execution information with emoji indicators:

- 📥 Fetching data
- 🎯 Processing
- 📊 Exporting
- ✅ Success
- ❌ Error

## Environment Variables

```bash
# QuickBooks company file path (optional)
QB_COMPANY_FILE="C:\Path\To\Company.QBW"
```

## Project Structure

```
quickbooks-auto-reporter/
├── quickbooks_autoreport.py    # Main application
├── requirements.txt            # Python dependencies
├── requirements_exe.txt        # Dependencies for executable build
├── QuickBooks_Auto_Reporter.spec # PyInstaller spec
├── build_exe.py               # Executable builder
├── test_xml_generation.py     # XML validation tests
├── .kiro/                     # Kiro IDE configuration
│   ├── specs/                 # Feature specifications
│   │   └── quickbooks-continuous-polling-reporter/
│   │       ├── requirements.md  # Feature requirements
│   │       ├── design.md        # Technical design
│   │       └── tasks.md         # Implementation tasks
│   ├── settings/              # IDE settings
│   │   └── mcp.json          # MCP server configuration
│   └── steering/              # Development guidelines
├── docs/                      # Documentation
├── tests/                     # Test files
└── README.md                  # This file
```

## Kiro Specs

This project includes comprehensive Kiro specifications for structured development:

### Feature Spec: QuickBooks Continuous Polling Reporter

Located in `.kiro/specs/quickbooks-continuous-polling-reporter/`

**Requirements Document** (`requirements.md`)

- 10 comprehensive requirements with user stories
- EARS-format acceptance criteria
- Covers all core functionality:
  - QuickBooks Desktop Integration
  - Multi-Report Data Extraction (9 report types)
  - Scheduled Continuous Polling
  - Change Detection and Timestamped Snapshots
  - Multi-Format Export (CSV and Excel)
  - GUI and CLI Interfaces
  - Logging, Diagnostics, and Configuration
  - Error Handling and Recovery

**Design Document** (`design.md`)

- High-level architecture with component diagrams
- 10 major components with detailed interfaces
- Data models and error handling strategies
- Testing, security, and performance considerations
- Deployment and extensibility planning

**Implementation Tasks** (`tasks.md`)

- 16 main tasks with 60+ sub-tasks
- Each task references specific requirements
- Incremental development roadmap
- Test tasks marked as optional for MVP focus

### Using the Specs

The specs provide a complete blueprint for understanding and extending the application:

1. **For New Developers**: Read requirements.md → design.md to understand the system
2. **For Feature Development**: Reference tasks.md for implementation guidance
3. **For Architecture Decisions**: Consult design.md for component interactions
4. **For Testing**: Use requirements acceptance criteria as test cases

### Kiro IDE Integration

The project is configured with MCP (Model Context Protocol) servers for enhanced development:

- **Sequential Thinking**: Complex problem-solving and planning
- **Context7**: Up-to-date library documentation
- **Spec Workflow**: Structured feature development
- **Mermaid**: Diagram generation for documentation
- **Filesystem**: Project file access
- **Odoo**: ERP integration (optional)

Configuration: `.kiro/settings/mcp.json`

## Development

### Running Tests

```bash
# Test XML generation
python test_xml_generation.py

# Run with test mode
python quickbooks_autoreport.py --test-xml
```

### Building Executable

```bash
# Build standalone executable
python build_exe.py

# Or use batch file
build_exe.bat
```

### Code Quality

The application follows best practices:

- Type hints for function signatures
- Comprehensive error handling
- Detailed logging with timestamps
- Graceful degradation for optional features
- User-friendly error messages

## Dependencies

### Required

- `pywin32` - QuickBooks COM integration
- `openpyxl` - Excel file creation

## Technical Architecture

### Design Patterns

- **Strategy Pattern**: Different report types with common interface
- **Factory Pattern**: Report and format generation
- **Observer Pattern**: GUI status updates
- **Template Method**: Common export workflow with customization

### Core Components

- **QuickBooks Integration**: Direct qbXML API communication
- **Report Generation**: Multi-format output with change detection
- **Professional Formatting**: Corporate Excel styling
- **Scheduling System**: Configurable automated execution

### Error Handling

Robust fallback mechanisms:

- Multiple qbXML version attempts
- Alternative query methods for Open Sales Orders
- Graceful degradation when MCP services unavailable
- User-friendly error messages with solutions

## Comparison with Single-Report Tools

| Feature        | Auto Reporter           | Single Report Tools     |
| -------------- | ----------------------- | ----------------------- |
| Report Types   | 9 reports               | 1 report                |
| Output Formats | CSV + Excel             | CSV only or CSV + Excel |
| GUI Status     | Detailed per-report     | Basic overall status    |
| Formatting     | Corporate Excel styling | Basic or corporate      |
| Diagnostics    | Built-in comprehensive  | Basic or none           |

## License

This application maintains compatibility with QuickBooks Desktop SDK license requirements and usage terms.

## Support

For issues:

1. Run diagnostics: `python quickbooks_autoreport.py --diagnose`
2. Check `QuickBooks_Auto_Reports.log` for detailed error messages
3. Review qbXML request/response logs
4. Verify QuickBooks and SDK installation
5. Ensure QuickBooks Desktop is running and accessible

## Changelog

See `CHANGES_SUMMARY.md` for detailed change history.

## Version

QuickBooks Auto Reporter v1.0

## Contributing

When adding new report types:

1. Create working XML example
2. Add report configuration to `REPORT_CONFIGS`
3. Update XML validation mapping
4. Add chart recommendations
5. Test with `test_xml_generation.py`

## Future Enhancements

- Additional report types (Balance Sheet, Trial Balance)
- PDF export capabilities
- Email notification system
- Web dashboard interface
- REST API endpoints
- Webhook notifications
