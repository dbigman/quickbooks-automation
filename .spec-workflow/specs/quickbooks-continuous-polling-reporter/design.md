# Design Document

## Overview

The QuickBooks Auto Reporter is a Windows desktop application that provides automated, continuous extraction of business reports from QuickBooks Desktop. The system operates as a standalone application with both GUI and CLI interfaces, connecting directly to QuickBooks Desktop via the qbXML API to extract 9 different report types on configurable schedules.

The design follows a monolithic architecture with clear separation between QuickBooks integration, report processing, change detection, file export, and user interface layers. The application is designed for reliability, with comprehensive error handling, diagnostic capabilities, and graceful degradation when optional features are unavailable.

### Key Design Goals

1. **Reliability**: Robust error handling with automatic fallback mechanisms
2. **Usability**: User-friendly interfaces (GUI and CLI) with clear status feedback
3. **Efficiency**: Change detection to avoid redundant exports and file system overhead
4. **Maintainability**: Configuration-driven report definitions for easy extensibility
5. **Observability**: Comprehensive logging and diagnostic capabilities

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │   GUI (Tkinter)      │    │   CLI Interface      │      │
│  │  - Report Status     │    │  - Text Output       │      │
│  │  - Configuration     │    │  - Diagnostics       │      │
│  │  - Controls          │    │  - Automation        │      │
│  └──────────────────────┘    └──────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Application Core                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Scheduler & Polling Engine                    │  │
│  │  - Configurable intervals (5/15/30/60 min)           │  │
│  │  - Threading for non-blocking operation              │  │
│  │  - Status callbacks to UI                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Report Processing Pipeline                    │  │
│  │  1. qbXML Request Generation                         │  │
│  │  2. QuickBooks Communication                         │  │
│  │  3. Response Parsing                                 │  │
│  │  4. Change Detection (Hash Comparison)               │  │
│  │  5. Multi-Format Export (CSV + Excel)                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              QuickBooks Integration Layer                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         qbXML API Communication                       │  │
│  │  - COM object management (QBXMLRP2)                  │  │
│  │  - Connection strategies (multiple fallbacks)        │  │
│  │  - Session management                                │  │
│  │  - Version negotiation (16.0 → 13.0)                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  External Systems                            │
│  ┌──────────────────┐    ┌──────────────────────────────┐  │
│  │  QuickBooks      │    │  File System                  │  │
│  │  Desktop         │    │  - CSV exports                │  │
│  │  (via qbXML)     │    │  - Excel exports              │  │
│  │                  │    │  - Hash files                 │  │
│  │                  │    │  - Logs                       │  │
│  └──────────────────┘    └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
User Action (GUI/CLI)
    │
    ▼
Scheduler triggers report generation
    │
    ▼
Build qbXML request for report type
    │
    ▼
Establish QuickBooks connection
    │
    ▼
Send qbXML request → QuickBooks Desktop
    │
    ▼
Receive and parse qbXML response
    │
    ▼
Compute data hash
    │
    ▼
Compare with stored hash
    │
    ├─ Hash matches → Update base files only
    │
    └─ Hash differs → Create timestamped snapshots + update base files
    │
    ▼
Export to CSV and Excel formats
    │
    ▼
Update UI status / Log results
```

## Components and Interfaces

### 1. Configuration Management

**Purpose**: Centralized configuration for reports, user preferences, and application settings

**Key Components**:

- `REPORT_CONFIGS`: Dictionary defining all 9 report types with metadata
- `load_settings()`: Load user preferences from JSON file
- `save_settings()`: Persist user preferences
- `SETTINGS_FILE`: User settings location (`~/.qb_auto_reporter_settings.json`)

**Report Configuration Structure**:

```python
{
    "report_key": {
        "name": str,              # Display name
        "qbxml_type": str,        # QuickBooks report type
        "query": str,             # Query type (GeneralDetail/GeneralSummary/Aging)
        "csv_filename": str,      # Base CSV filename
        "excel_filename": str,    # Base Excel filename
        "hash_filename": str,     # Hash storage filename
        "request_log": str,       # qbXML request log filename
        "response_log": str,      # qbXML response log filename
        "uses_date_range": bool   # Whether report requires date range
    }
}
```

**User Settings Structure**:

```python
{
    "output_dir": str,           # Selected output directory
    "interval": str,             # Polling interval (e.g., "15 minutes")
    "report_date_from": str,     # Start date (YYYY-MM-DD)
    "report_date_to": str        # End date (YYYY-MM-DD)
}
```

### 2. QuickBooks Integration Layer

**Purpose**: Handle all communication with QuickBooks Desktop via qbXML API

**Key Functions**:

- `qb_request(xml, out_dir, report_key)`: Execute qbXML request with error handling
- `open_connection(rp)`: Establish connection with multiple fallback strategies
- `try_begin_session(rp)`: Begin QuickBooks session with multiple path/mode attempts
- `host_info(rp, ticket)`: Query QuickBooks host information

**Connection Strategy**:

1. Try local connection modes: 1 (single-user), 0 (auto), 2 (multi-user)
2. Try with empty path (open file) and configured COMPANY_FILE path
3. Fallback through combinations until successful

**Error Handling**:

- `get_user_friendly_error(error)`: Convert COM errors to actionable user messages
- Structured error responses with title, message, solutions, technical details
- Error type classification: SDK_NOT_INSTALLED, SDK_NOT_REGISTERED, ACCESS_DENIED, FILE_NOT_FOUND, CONNECTION_ERROR, UNKNOWN_ERROR

**COM Object Management**:

- Use `pythoncom.CoInitialize()` / `CoUninitialize()` for thread safety
- Use `gencache.EnsureDispatch("QBXMLRP2.RequestProcessor")` for COM object creation
- Proper cleanup with try/finally blocks

### 3. qbXML Request Builder

**Purpose**: Generate valid qbXML requests for different report types

**Key Function**:

- `build_report_qbxml(version, report_type, date_from, date_to, report_key)`: Build qbXML based on report configuration

**Query Types**:

1. **GeneralDetailReportQueryRq**: Detailed transaction-level reports
   - Open Sales Orders by Item
   - Profit & Loss Detail
   - Sales by Item Detail
   - Sales by Rep Detail
   - Purchases by Vendor Detail

2. **GeneralSummaryReportQueryRq**: Summary-level reports
   - Profit & Loss Standard
   - Sales by Item Summary

3. **AgingReportQueryRq**: Aging analysis reports
   - AP Aging Detail
   - AR Aging Detail

**Date Handling**:

- Date range reports: Use `<ReportPeriod>` with `<FromReportDate>` and `<ToReportDate>`
- Aging reports: Use `<ReportPeriod>` with `<ToReportDate>` and `<ReportAgingAsOf>`
- Non-dated reports: No date parameters

**Version Negotiation**:

- Primary: qbXML 16.0 (QuickBooks 2019+)
- Fallback: qbXML 13.0 (older versions)

### 4. Report Processing Pipeline

**Purpose**: Orchestrate the complete report generation workflow

**Key Functions**:

- `export_report(report_key, out_dir, date_from, date_to, status_callback)`: Main export function
- `parse_qbxml_response(xml_string)`: Parse qbXML response into structured data
- `compute_data_hash(rows)`: Generate SHA-256 hash of report data
- `should_create_snapshot(current_hash, hash_file)`: Determine if data changed

**Processing Steps**:

1. **Request Generation**: Build qbXML request based on report configuration
2. **QuickBooks Communication**: Send request and receive response
3. **Response Parsing**: Extract rows and columns from XML
4. **Data Validation**: Handle missing columns, empty values, malformed data
5. **Hash Computation**: Calculate SHA-256 hash of normalized data
6. **Change Detection**: Compare with stored hash
7. **File Export**: Generate CSV and Excel files
8. **Snapshot Creation**: Create timestamped copies if data changed
9. **Status Update**: Notify UI/CLI of results

**Error Recovery**:

- Log request/response XML for debugging
- Continue processing other reports if one fails
- Provide detailed error context in logs

### 5. Change Detection System

**Purpose**: Avoid redundant file creation by detecting actual data changes

**Implementation**:

- Compute SHA-256 hash of report data (all rows concatenated)
- Store hash in `.hash` file alongside report files
- Compare new hash with stored hash
- Create timestamped snapshots only when hash differs

**Hash Computation**:

```python
def compute_data_hash(rows):
    # Concatenate all row data
    data_string = "".join("".join(str(cell) for cell in row) for row in rows)
    # Return SHA-256 hash
    return hashlib.sha256(data_string.encode("utf-8", "ignore")).hexdigest()
```

**File Naming Convention**:

- Base files (always updated): `{Report_Name}.csv`, `{Report_Name}.xlsx`
- Timestamped snapshots (created on change): `{Report_Name}_YYYYMMDD_HHMMSS.csv`, `{Report_Name}_YYYYMMDD_HHMMSS.xlsx`
- Hash storage: `{Report_Name}.hash`

### 6. Multi-Format Export System

**Purpose**: Generate both CSV and Excel formats with professional styling

**CSV Export**:

- Standard CSV format with proper quoting
- UTF-8 encoding
- Header row from report columns
- Data rows from parsed qbXML response

**Excel Export**:

- Use `openpyxl` library for Excel file creation
- Corporate blue header (#4472C4) with white text
- Bold header font
- Auto-sized columns
- Excel table formatting with filters
- Professional appearance for business use

**Export Functions**:

- `export_to_csv(rows, csv_path)`: Write CSV file
- `export_to_excel(rows, excel_path)`: Create formatted Excel file
- `create_timestamped_snapshot(base_path, timestamp)`: Copy to timestamped filename

### 7. Scheduling and Polling Engine

**Purpose**: Manage continuous polling with configurable intervals

**Key Components**:

- Threading for non-blocking operation
- Configurable intervals: 5, 15, 30, 60 minutes
- Timer display showing next scheduled run
- Start/Stop controls

**Implementation**:

```python
class SchedulerThread(threading.Thread):
    def __init__(self, interval_seconds, callback):
        self.interval = interval_seconds
        self.callback = callback
        self.running = True
        self.stop_event = threading.Event()
    
    def run(self):
        while self.running:
            self.callback()  # Execute report generation
            self.stop_event.wait(self.interval)  # Wait for interval
    
    def stop(self):
        self.running = False
        self.stop_event.set()
```

**Status Callbacks**:

- Report start: Update UI to "Running"
- Report success: Update UI with row count, "Success" status
- Report error: Update UI with error message, "Error" status
- Next run time: Calculate and display countdown

### 8. GUI Interface (Tkinter)

**Purpose**: Provide user-friendly graphical interface for configuration and monitoring

**Main Window Components**:

1. **Output Folder Selection**
   - Button to open folder picker
   - Display current output directory
   - Save preference on change

2. **Date Range Configuration**
   - From Date picker (DateEntry widget)
   - To Date picker (DateEntry widget)
   - Apply to all date-based reports

3. **Interval Selection**
   - Dropdown with options: 5, 15, 30, 60 minutes
   - Save preference on change

4. **Control Buttons**
   - "Start Auto": Begin scheduled polling
   - "Stop Auto": Halt polling
   - "Export All Now": Immediate one-time export
   - "Open Folder": Open output directory in Explorer
   - "Run Diagnostics": Execute diagnostic tests

5. **Report Status Grid**
   - One row per report (9 total)
   - Columns: Report Name, Status, Row Count, Excel Status
   - Real-time updates during execution
   - Color coding: Green (Success), Red (Error), Yellow (Running), Gray (Idle)

6. **Status Bar**
   - Connection information
   - Next scheduled run time
   - Current operation status

**Threading Considerations**:

- Use `threading.Thread` for background operations
- Use `queue.Queue` for thread-safe UI updates
- Call `root.after()` to update UI from worker threads

### 9. CLI Interface

**Purpose**: Support automation, scripting, and headless operation

**Command-Line Arguments**:

- `--gui`: Launch GUI mode (default: CLI mode)
- `--diagnose`: Run diagnostics and generate report
- `--test-xml`: Validate XML generation without QuickBooks connection

**CLI Operation**:

- Text-based status output with emoji indicators
- Progress messages for each report
- Error messages with troubleshooting guidance
- Exit codes: 0 (success), 1 (error)

**Output Format**:

```
📥 Fetching Open Sales Orders by Item...
🎯 Processing 150 rows...
📊 Exporting to CSV and Excel...
✅ Success: Open_Sales_Orders_By_Item.xlsx (150 rows)

📥 Fetching Profit & Loss...
❌ Error: Cannot connect to QuickBooks Desktop
💡 Solutions:
   1. Make sure QuickBooks Desktop is running
   2. Install QuickBooks SDK
   ...
```

### 10. Logging and Diagnostics

**Purpose**: Comprehensive observability for troubleshooting and monitoring

**Logging System**:

- Log file: `QuickBooks_Auto_Reports.log`
- Timestamp format: `[YYYY-MM-DD HH:MM:SS]`
- Emoji indicators: 📥 (fetch), 🎯 (process), 📊 (export), ✅ (success), ❌ (error)
- Log levels: Info, Warning, Error

**Log Function**:

```python
def log(msg: str, out_dir: str = None) -> None:
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(out_dir, "QuickBooks_Auto_Reports.log")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
```

**qbXML Request/Response Logging**:

- Request log: `{report_key}_request.xml`
- Response log: `{report_key}_response.xml`
- Logged for every report execution
- Essential for debugging qbXML issues

**Diagnostic System**:

- `diagnose_quickbooks_connection()`: Comprehensive connectivity tests
- `check_quickbooks_installation()`: Verify QuickBooks installation via registry
- `check_sdk_installation()`: Verify SDK COM registration
- Output: `quickbooks_diagnostics.json` and `QuickBooks_Diagnostic_Report.xlsx`

**Diagnostic Report Contents**:

```python
{
    "timestamp": "ISO-8601 timestamp",
    "system_info": {
        "platform": "win32",
        "python_version": "3.x.x",
        "architecture": "64-bit"
    },
    "quickbooks_installation": {
        "installed": true/false,
        "details": ["registry paths"],
        "status": "✅ Found" or "❌ Not Found"
    },
    "sdk_installation": {
        "installed": true/false,
        "details": "CLSID or error message",
        "status": "✅ Registered" or "❌ Not Registered"
    },
    "connectivity_test": {
        "com_object_creation": "✅ Success" or "❌ Failed",
        "connection_test": "✅ Success" or "❌ Failed",
        "connection_error": {error_info}
    },
    "recommendations": ["actionable steps"]
}
```

## Data Models

### Report Configuration Model

```python
ReportConfig = {
    "name": str,              # Display name for UI
    "qbxml_type": str,        # QuickBooks report type identifier
    "query": str,             # Query type: GeneralDetail, GeneralSummary, Aging
    "csv_filename": str,      # Base CSV filename
    "excel_filename": str,    # Base Excel filename
    "hash_filename": str,     # Hash storage filename
    "request_log": str,       # Request XML log filename
    "response_log": str,      # Response XML log filename
    "uses_date_range": bool   # Whether report requires date parameters
}
```

### Report Data Model

```python
ReportData = {
    "columns": List[str],     # Column headers
    "rows": List[List[Any]],  # Data rows (list of lists)
    "row_count": int,         # Number of data rows
    "hash": str               # SHA-256 hash of data
}
```

### User Settings Model

```python
UserSettings = {
    "output_dir": str,           # Output directory path
    "interval": str,             # Polling interval (e.g., "15 minutes")
    "report_date_from": str,     # Start date (YYYY-MM-DD)
    "report_date_to": str        # End date (YYYY-MM-DD)
}
```

### Error Information Model

```python
ErrorInfo = {
    "title": str,                # User-friendly error title
    "message": str,              # User-friendly error message
    "solutions": List[str],      # Actionable troubleshooting steps
    "technical_details": str,    # Technical error details for debugging
    "error_type": str            # Error classification
}
```

### Diagnostic Result Model

```python
DiagnosticResult = {
    "timestamp": str,            # ISO-8601 timestamp
    "system_info": Dict,         # System information
    "quickbooks_installation": Dict,  # QB installation status
    "sdk_installation": Dict,    # SDK installation status
    "connectivity_test": Dict,   # Connection test results
    "recommendations": List[str] # Actionable recommendations
}
```

## Error Handling

### Error Classification

1. **SDK_NOT_INSTALLED**: QuickBooks SDK not installed or not registered
2. **SDK_NOT_REGISTERED**: SDK components not properly registered
3. **ACCESS_DENIED**: Permission issues accessing QuickBooks
4. **FILE_NOT_FOUND**: QuickBooks company file not found or inaccessible
5. **CONNECTION_ERROR**: Network or connection issues
6. **UNKNOWN_ERROR**: Unclassified errors

### Error Handling Strategy

**Layered Error Handling**:

1. **COM Layer**: Catch COM errors, classify, provide user-friendly messages
2. **Connection Layer**: Multiple fallback strategies for connection/session
3. **Request Layer**: Log request/response, continue with other reports on failure
4. **Application Layer**: Display errors in UI, log to file, provide troubleshooting guidance

**Error Response Structure**:

```python
{
    "title": "User-friendly title",
    "message": "Clear explanation of what went wrong",
    "solutions": [
        "Step 1: Specific action to try",
        "Step 2: Alternative action",
        "Step 3: Escalation path"
    ],
    "technical_details": "Full error message for debugging",
    "error_type": "ERROR_TYPE_ENUM"
}
```

**Graceful Degradation**:

- If one report fails, continue processing other reports
- If QuickBooks connection fails, provide diagnostic guidance
- If file write fails, log error and continue
- If Excel creation fails, ensure CSV is still created

### Retry Logic

**Connection Retries**:

- Try multiple local connection modes: 1, 0, 2
- Try multiple session paths/modes
- No automatic retries for failed requests (user-initiated retry)

**No Exponential Backoff**:

- Polling is user-controlled with fixed intervals
- Failed reports are logged and skipped until next cycle
- User can manually retry via "Export All Now" button

## Testing Strategy

### Unit Testing

**Test Coverage Areas**:

1. **Configuration Management**
   - Load/save settings with valid data
   - Handle missing settings file
   - Handle corrupted settings file
   - Default value fallbacks

2. **qbXML Request Builder**
   - Generate valid XML for each report type
   - Handle date range parameters correctly
   - Handle aging report parameters correctly
   - Validate XML structure

3. **Data Processing**
   - Parse qbXML responses correctly
   - Handle missing columns gracefully
   - Handle empty values
   - Compute hashes consistently

4. **Change Detection**
   - Detect data changes correctly
   - Handle missing hash files
   - Handle corrupted hash files

5. **File Export**
   - Create valid CSV files
   - Create valid Excel files
   - Handle file write errors
   - Create timestamped snapshots correctly

**Test Framework**: `pytest`

**Test Files**:

- `tests/test_xml_generation.py`: XML generation validation
- `tests/test_basic.py`: Basic functionality tests
- `tests/test_enhanced_features.py`: Advanced feature tests

### Integration Testing

**Test Scenarios**:

1. **QuickBooks Connection**
   - Connect to QuickBooks Desktop
   - Handle QuickBooks not running
   - Handle SDK not installed
   - Handle access denied

2. **Report Generation**
   - Generate each of 9 report types
   - Handle date range parameters
   - Handle aging report parameters
   - Parse responses correctly

3. **End-to-End Workflow**
   - Full report generation cycle
   - Change detection workflow
   - Timestamped snapshot creation
   - Multi-format export

**Test Environment**:

- Windows machine with QuickBooks Desktop installed
- QuickBooks SDK installed and registered
- Test company file with sample data

### Manual Testing

**GUI Testing**:

- Folder selection and persistence
- Date range configuration
- Interval selection
- Start/Stop auto mode
- Export All Now button
- Open Folder button
- Status display updates
- Error message display

**CLI Testing**:

- Command-line argument parsing
- Diagnostic mode
- Test XML mode
- Output formatting
- Exit codes

**Error Scenario Testing**:

- QuickBooks not running
- SDK not installed
- Access denied
- File not found
- Network errors
- Disk full
- Invalid date ranges

### Performance Testing

**Metrics**:

- Report generation time per report type
- Memory usage during execution
- File I/O performance
- UI responsiveness during background operations

**Targets**:

- Each report generation: < 30 seconds
- All 9 reports: < 5 minutes
- Memory usage: < 200 MB
- UI remains responsive during background operations

## Security Considerations

### Credential Management

- No credentials stored in application
- QuickBooks SDK handles authentication
- Company file path configurable via environment variable
- No sensitive data in logs (except qbXML which may contain business data)

### File System Security

- Output directory user-configurable
- Files created with default Windows permissions
- No elevation required for normal operation
- Administrator rights only needed for SDK installation/registration

### Data Privacy

- Report data contains business-sensitive information
- Files written to user-specified directory
- No data transmitted over network (local QuickBooks connection only)
- qbXML request/response logs contain full report data

### Input Validation

- Date range validation (YYYY-MM-DD format)
- File path validation
- XML normalization to prevent injection
- Error message sanitization

## Performance Optimization

### Efficient Data Processing

- Stream-based XML parsing for large responses
- Minimal data transformations
- Direct CSV writing without intermediate structures
- Efficient hash computation

### File I/O Optimization

- Batch file operations
- Avoid redundant file writes
- Use buffered I/O for logs
- Minimize disk seeks

### Memory Management

- Process reports sequentially (not in parallel)
- Release COM objects promptly
- Clear large data structures after use
- Avoid loading entire files into memory

### UI Responsiveness

- Background threading for long operations
- Non-blocking UI updates
- Progress callbacks during processing
- Cancellable operations

## Deployment Considerations

### Installation Requirements

- Windows operating system (7, 10, 11)
- Python 3.7+ (for source distribution)
- QuickBooks Desktop 2019+ installed
- QuickBooks SDK installed and registered
- Administrator rights for SDK installation

### Distribution Options

1. **Source Distribution**
   - Requires Python installation
   - Install dependencies via `pip install -r requirements.txt`
   - Run with `python quickbooks_autoreport.py`

2. **Executable Distribution**
   - PyInstaller-based standalone executable
   - No Python installation required
   - Includes all dependencies
   - Larger file size (~50-100 MB)

### Configuration

- Environment variable: `QB_COMPANY_FILE` (optional)
- Settings file: `~/.qb_auto_reporter_settings.json` (auto-created)
- Output directory: User-configurable via GUI

### Maintenance

- Log file rotation (manual)
- Periodic cleanup of timestamped snapshots (manual)
- QuickBooks SDK updates (manual)
- Application updates (manual)

## Future Extensibility

### Adding New Report Types

1. Add configuration to `REPORT_CONFIGS` dictionary
2. Specify qbXML type, query type, filenames
3. Update XML validation mapping in tests
4. No code changes required (configuration-driven)

### Enhanced Features

- Email notifications on report completion
- Web dashboard for remote monitoring
- REST API for programmatic access
- Database storage option (in addition to files)
- PDF export format
- Scheduled report distribution
- Data transformation pipelines
- Integration with BI tools

### Scalability Considerations

- Current design: Single-threaded report processing
- Future: Parallel report generation with thread pool
- Current design: Local file storage
- Future: Cloud storage integration (S3, Azure Blob)
- Current design: Single QuickBooks instance
- Future: Multi-company support with connection pooling