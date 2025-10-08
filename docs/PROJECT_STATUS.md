# QuickBooks Auto Reporter - Project Status

**Date**: 2025-10-07  
**Status**: ✅ Cleanup Complete - Ready for Use

## Project Overview

QuickBooks Auto Reporter is now a focused, single-purpose tool for automated QuickBooks Desktop reporting.

## What This Tool Does

Automates generation of 9 different QuickBooks reports with:
- Scheduled execution (5, 15, 30, or 60 minute intervals)
- Professional Excel formatting with corporate styling
- Change detection (only saves snapshots when data changes)
- Business analytics via Context7 MCP (optional)
- Enhanced Excel features via Excel MCP (optional)
- Built-in diagnostics for troubleshooting
- User-friendly GUI interface

## Supported Reports

1. Open Sales Orders by Item
2. Profit & Loss (Standard)
3. Profit & Loss Detail
4. Sales by Item (Summary)
5. Sales by Item Detail
6. Sales by Rep Detail
7. Purchase by Vendor Detail
8. AP Aging Detail
9. AR Aging Detail

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Required: pywin32, openpyxl
# Optional: Context7 MCP, Excel MCP
```

## Usage

```bash
# GUI Mode (recommended)
python quickbooks_autoreport.py --gui

# Command Line Mode
python quickbooks_autoreport.py

# Run Diagnostics
python quickbooks_autoreport.py --diagnose
```

## Requirements

- Windows operating system
- QuickBooks Desktop 2019+ installed
- QuickBooks SDK installed and registered
- Python 3.7+

## Project Structure

```
quickbooks-auto-reporter/
├── quickbooks_autoreport.py    # Main application (2599 lines)
├── README.md                   # Comprehensive documentation
├── requirements.txt            # Minimal dependencies
├── pyproject.toml             # Project configuration
├── tests/
│   └── test_basic.py          # Unit tests
├── build_exe.py               # Executable builder
├── build_exe.bat              # Build script (Windows)
├── test_xml_generation.py     # XML validation
└── docs/                      # Additional documentation
```

## Testing

```bash
# Run unit tests
python tests/test_basic.py

# Test XML generation
python test_xml_generation.py

# Note: Tests require pywin32 to be installed
```

## Building Executable

```bash
# Build standalone .exe
python build_exe.py

# Or use batch file
build_exe.bat

# Output: dist/QuickBooks_Auto_Reporter.exe
```

## Key Features

### Multi-Report Automation
- Generate 9 different reports in one run
- Each report has its own CSV and Excel output
- Separate XML request/response logs per report

### Scheduling
- Configurable intervals: 5, 15, 30, or 60 minutes
- Automatic execution on schedule
- Manual "Export All Now" button

### Change Detection
- SHA256 hash comparison
- Only creates timestamped snapshots when data changes
- Reduces storage and clutter

### Professional Excel
- Corporate blue headers (#4472C4)
- Auto-sized columns
- Table formatting
- Clean, professional appearance

### Business Analytics (Optional)
- Context7 MCP integration
- Generates insights JSON files
- Top customers, items, patterns
- Data completeness metrics

### Diagnostics
- Built-in connectivity testing
- Checks QuickBooks installation
- Checks SDK registration
- Generates diagnostic reports
- User-friendly error messages

### GUI Interface
- Real-time status updates per report
- Row count display
- Excel generation confirmation
- Connection information
- Timer display (time since last check)
- Folder selection
- Interval configuration

## Configuration

Settings automatically saved to:
`~/.qb_auto_reporter_settings.json`

Includes:
- Output directory preference
- Check interval preference
- Report date ranges

## Output Files

For each report:
- `{Report_Name}.csv` - Current data
- `{Report_Name}.xlsx` - Professional Excel
- `{Report_Name}.hash` - Change detection
- `{Report_Name}_YYYYMMDD_HHMMSS.csv` - Snapshots (when changed)
- `{Report_Name}_YYYYMMDD_HHMMSS.xlsx` - Snapshots (when changed)

Logs:
- `QuickBooks_Auto_Reports.log` - Main log
- `{report_key}_request.xml` - qbXML requests
- `{report_key}_response.xml` - qbXML responses

Analytics (optional):
- `{report_key}_insights.json` - Business insights
- `{report_key}_enhanced_insights.json` - Chart recommendations

## Troubleshooting

### Common Issues

**"Cannot connect to QuickBooks"**
- Install QuickBooks SDK
- Run as Administrator
- Restart computer after SDK installation

**"COM Error -2147221005"**
- SDK not installed or not registered
- Download from Intuit Developer website

**"Access Denied"**
- Run as Administrator
- Check company file permissions
- Ensure single-user mode

### Diagnostics

Run built-in diagnostics:
```bash
python quickbooks_autoreport.py --diagnose
```

Generates:
- `quickbooks_diagnostics.json`
- `QuickBooks_Diagnostic_Report.xlsx`

### Logs

Check detailed logs:
- `QuickBooks_Auto_Reports.log` - Main application log
- `{report_key}_request.xml` - See what was sent to QuickBooks
- `{report_key}_response.xml` - See what QuickBooks returned

## Dependencies

### Required
- `pywin32>=305` - QuickBooks COM integration
- `openpyxl>=3.0.0` - Excel file generation

### Optional
- Context7 MCP - Business analytics
- Excel MCP - Enhanced Excel formatting

## Development

### Code Quality
- Type hints for function signatures
- Comprehensive error handling
- Detailed logging with emoji indicators
- User-friendly error messages
- Graceful degradation for optional features

### Testing
- Unit tests for core functionality
- XML generation validation
- Settings persistence tests
- Error handling tests

### Build Process
- PyInstaller for standalone executable
- Multiple build scripts for flexibility
- Spec files for customization

## Version History

- **v1.0** - Initial release with 9 reports, GUI, scheduling, diagnostics

## License

Compatible with QuickBooks Desktop SDK license requirements.

## Support

1. Check `QuickBooks_Auto_Reports.log`
2. Run diagnostics: `python quickbooks_autoreport.py --diagnose`
3. Review README.md troubleshooting section
4. Check qbXML request/response logs

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Verify QuickBooks and SDK installation
3. Run application: `python quickbooks_autoreport.py --gui`
4. Configure output folder and interval
5. Start scheduled reporting

## Success Criteria

✅ Single focused purpose (QuickBooks reporting automation)  
✅ Minimal dependencies (pywin32, openpyxl)  
✅ Comprehensive documentation  
✅ Built-in diagnostics  
✅ User-friendly GUI  
✅ Professional Excel output  
✅ Change detection  
✅ Scheduled execution  
✅ Multiple report types  
✅ Robust error handling  

## Project Health

- **Code Quality**: ✅ No syntax errors, clean structure
- **Documentation**: ✅ Comprehensive README, inline comments
- **Testing**: ✅ Unit tests available (requires pywin32)
- **Build**: ✅ Multiple build scripts, PyInstaller specs
- **Dependencies**: ✅ Minimal, well-defined
- **Focus**: ✅ Single clear purpose

## Conclusion

QuickBooks Auto Reporter is now a clean, focused, production-ready tool for automated QuickBooks Desktop reporting. All irrelevant code has been removed, documentation has been updated, and the project structure is clear and maintainable.
