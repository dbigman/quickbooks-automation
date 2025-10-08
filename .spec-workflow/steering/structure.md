# Codebase Structure

## Directory Organization

### Root Level Structure

```
quickbooks-automation/
├── quickbooks_autoreport.py       # Main application entry point
├── requirements.txt               # Core Python dependencies
├── pyproject.toml                 # Modern Python project configuration
├── README.md                      # Comprehensive user documentation
├── product.md                     # Product vision and business objectives
├── tech.md                        # Technical architecture and decisions
├── structure.md                   # Codebase organization and architecture
├── PROJECT_COMPLETE.md            # Project completion status
│
├── build_exe.py                   # Executable build script
├── QuickBooks_Auto_Reporter.spec  # PyInstaller configuration
│
├── debug_reports.py               # Debugging utility
├── fix_build_issues.py            # Build issue resolution
├── test_xml_generation.py         # XML validation testing
│
├── .kiro/                         # Kiro IDE configuration and specs
├── docs/                          # Additional documentation
├── tests/                         # Test suite
└── .gitignore                     # Git ignore rules
```

### Core Application Structure

**Monolithic Design Philosophy**
The application follows a monolithic architecture with a single main file (`quickbooks_autoreport.py`) that contains all functionality. This approach was chosen for:

- Simplicity of deployment and distribution
- Reduced complexity for a focused business tool
- Easier debugging and maintenance
- Minimal external dependencies

**Internal Module Organization**
Within the main file, code is organized into logical sections:

1. **Imports and Constants** (Lines 1-152)
2. **Configuration Management** (Lines 155-203)
3. **Logging and Utilities** (Lines 205-267)
4. **QuickBooks Integration** (Lines 580-687)
5. **qbXML Request Building** (Lines 689-877)
6. **Report Processing** (Lines 879-1040)
7. **Excel Export** (Lines 1041-1387)
8. **Analytics Integration** (Lines 1443-1648)
9. **Report Orchestration** (Lines 1650-1920)
10. **GUI Interface** (Lines 1922-2425)
11. **Application Entry Point** (Lines 2427-2598)

## Configuration Architecture

### Report Configuration System

**Centralized Configuration Dictionary**
```python
REPORT_CONFIGS = {
    "report_key": {
        "name": str,              # Display name for UI
        "qbxml_type": str,        # QuickBooks report type
        "query": str,             # Query type (GeneralDetail/GeneralSummary/Aging)
        "csv_filename": str,      # Base CSV filename
        "excel_filename": str,    # Base Excel filename
        "hash_filename": str,     # Hash storage filename
        "request_log": str,       # Request XML log filename
        "response_log": str,      # Response XML log filename
        "uses_date_range": bool   # Whether report requires date range
    }
}
```

**Configuration Benefits**
- Single source of truth for all report metadata
- Easy addition of new report types without code changes
- Consistent behavior across all report types
- Simplified testing and maintenance

### User Settings Management

**Settings File Structure**
```python
{
    "output_dir": str,           # User-selected output directory
    "interval": str,             # Polling interval (e.g., "15 minutes")
    "report_date_from": str,     # Start date (YYYY-MM-DD)
    "report_date_to": str        # End date (YYYY-MM-DD)
}
```

**Settings Persistence**
- Location: `~/.qb_auto_reporter_settings.json`
- Automatic saving on preference changes
- Graceful handling of missing or corrupted files
- Default value fallbacks for new installations

## Module Architecture

### 1. Configuration Management Module

**Purpose**: Centralized configuration for reports, user preferences, and application settings

**Key Functions**:
- `load_settings()`: Load user preferences from JSON file
- `save_settings()`: Persist user preferences to file
- `get_file_paths()`: Generate all file paths based on configuration

**Design Principles**:
- Configuration-driven approach for extensibility
- Graceful degradation for missing settings
- Type validation and error handling
- Backward compatibility for settings migration

### 2. QuickBooks Integration Module

**Purpose**: Handle all communication with QuickBooks Desktop via qbXML API

**Key Functions**:
- `qb_request()`: Execute qbXML request with comprehensive error handling
- `open_connection()`: Establish connection with multiple fallback strategies
- `try_begin_session()`: Begin QuickBooks session with path/mode attempts
- `host_info()`: Query QuickBooks host information
- `check_quickbooks_installation()`: Verify QuickBooks installation
- `check_sdk_installation()`: Verify SDK COM registration

**Connection Strategy**:
1. Try local connection modes: 1 (single-user), 0 (auto), 2 (multi-user)
2. Try with empty path (open file) and configured COMPANY_FILE path
3. Fallback through combinations until successful
4. Comprehensive error handling with user-friendly messages

### 3. qbXML Request Builder Module

**Purpose**: Generate valid qbXML requests for different report types

**Key Functions**:
- `build_report_qbxml()`: Build qbXML based on report configuration
- `build_salesorder_query()`: Fallback query for Open Sales Orders
- `validate_xml_against_examples()`: XML validation against working examples

**Query Types Supported**:
- **GeneralDetailReportQueryRq**: Detailed transaction-level reports
- **GeneralSummaryReportQueryRq**: Summary-level reports
- **AgingReportQueryRq**: Aging analysis reports

**Date Handling**:
- Date range reports: `<ReportPeriod>` with `<FromReportDate>` and `<ToReportDate>`
- Aging reports: `<ReportPeriod>` with `<ToReportDate>` and `<ReportAgingAsOf>`
- Non-dated reports: No date parameters

### 4. Report Processing Pipeline Module

**Purpose**: Orchestrate the complete report generation workflow

**Key Functions**:
- `export_report()`: Main export function for single reports
- `export_all_reports()`: Orchestrate all 9 report types
- `parse_report_rows()`: Parse qbXML response into structured data
- `_write_outputs()`: Handle file writing with change detection

**Processing Steps**:
1. Request Generation: Build qbXML request based on configuration
2. QuickBooks Communication: Send request and receive response
3. Response Parsing: Extract rows and columns from XML
4. Hash Computation: Calculate SHA-256 hash of normalized data
5. Change Detection: Compare with stored hash
6. File Export: Generate CSV and Excel files
7. Snapshot Creation: Create timestamped copies if data changed

### 5. Change Detection System Module

**Purpose**: Avoid redundant file creation by detecting actual data changes

**Key Functions**:
- `sha256_text()`: Compute SHA-256 hash of text data
- `snapshot_filename()`: Generate timestamped snapshot filename
- Hash comparison logic integrated into export pipeline

**Implementation Details**:
- Compute SHA-256 hash of all report data concatenated
- Store hash in `.hash` file alongside report files
- Compare new hash with stored hash
- Create timestamped snapshots only when hash differs

**File Naming Conventions**:
- Base files (always updated): `{Report_Name}.csv`, `{Report_Name}.xlsx`
- Timestamped snapshots: `{Report_Name}_YYYYMMDD_HHMMSS.csv`, `{Report_Name}_YYYYMMDD_HHMMSS.xlsx`
- Hash storage: `{Report_Name}.hash`

### 6. Multi-Format Export System Module

**Purpose**: Generate both CSV and Excel formats with professional styling

**Key Functions**:
- `render_csv()`: Generate CSV format output
- `create_excel_report()`: Create professionally formatted Excel files
- `create_enhanced_excel_report()`: Enhanced Excel with charts and analytics

**CSV Export Features**:
- Standard CSV format with proper quoting and escaping
- UTF-8 encoding for international character support
- Header row from report columns
- Efficient streaming for large datasets

**Excel Export Features**:
- Corporate blue header styling (#4472C4) with white text
- Bold header fonts and professional appearance
- Auto-sized columns with reasonable width limits
- Table formatting with filters enabled
- Alternating row colors for readability
- Frozen header row for large datasets

### 7. Analytics Integration Module

**Purpose**: Generate business insights and chart recommendations

**Key Functions**:
- `generate_context7_insights()`: Analyze report data for business metrics
- `get_chart_recommendations()`: Suggest appropriate chart types
- Context7 MCP integration for enhanced analytics

**Analytics Features**:
- Data quality analysis and completeness metrics
- Business-specific insights for each report type
- Chart recommendations based on data structure
- JSON-based insight storage for integration

### 8. Scheduling and Polling Engine Module

**Purpose**: Manage continuous polling with configurable intervals

**Key Functions**:
- Threading implementation for non-blocking operation
- Timer display and status updates
- Start/Stop controls with proper cleanup
- Interval configuration (5, 15, 30, 60 minutes)

**Threading Considerations**:
- Background worker threads for report generation
- Thread-safe UI updates using `root.after()`
- Proper thread cleanup and resource management
- Cancellable operations with graceful shutdown

### 9. GUI Interface Module

**Purpose**: Provide user-friendly graphical interface for configuration and monitoring

**Key Components**:
- **Main Application Class** (`App`): Primary GUI controller
- **Configuration Widgets**: Folder selection, date ranges, intervals
- **Control Buttons**: Start/Stop, Export Now, Open Folder
- **Status Display**: Real-time report status and progress
- **Report Grid**: Individual report status for all 9 types

**GUI Architecture**:
- Tkinter-based with custom styling
- Responsive design with status callbacks
- Settings persistence and automatic loading
- Error display with user-friendly messages

### 10. CLI Interface Module

**Purpose**: Support automation, scripting, and headless operation

**Key Functions**:
- Command-line argument parsing
- Text-based status output with emoji indicators
- Diagnostic mode execution
- Test mode for XML validation

**CLI Features**:
- `--gui`: Launch GUI mode
- `--diagnose`: Run comprehensive diagnostics
- `--test-xml`: Validate XML generation
- Interactive and non-interactive operation modes

### 11. Logging and Diagnostics Module

**Purpose**: Comprehensive observability for troubleshooting and monitoring

**Key Functions**:
- `log()`: Centralized logging with timestamps and emoji indicators
- `diagnose_quickbooks_connection()`: Comprehensive connectivity testing
- `get_user_friendly_error()`: Convert technical errors to actionable messages
- `create_diagnostic_excel_report()`: Generate professional diagnostic reports

**Logging Features**:
- Log file: `QuickBooks_Auto_Reports.log`
- Emoji indicators: 📥 (fetch), 🎯 (process), 📊 (export), ✅ (success), ❌ (error)
- Request/response XML logging for debugging
- Structured error information with solutions

## Data Flow Architecture

### Report Generation Flow

```
User Action (GUI/CLI)
    │
    ▼
Configuration Loading
    │
    ▼
Scheduler Trigger (if automatic)
    │
    ▼
For Each Report Type:
    │
    ├─ Build qbXML Request
    │   │
    │   └─ Validate XML Structure
    │
    ├─ QuickBooks Connection
    │   │
    │   ├─ Try Multiple Connection Strategies
    │   └─ Handle Connection Errors
    │
    ├─ Send Request → QuickBooks
    │   │
    │   └─ Receive XML Response
    │
    ├─ Parse Response to Data Structure
    │   │
    │   ├─ Extract Headers and Rows
    │   └─ Handle Missing/Malformed Data
    │
    ├─ Compute Data Hash
    │   │
    │   └─ Compare with Stored Hash
    │
    ├─ Change Detection
    │   │
    │   ├─ If Unchanged → Update Base Files Only
    │   └─ If Changed → Create Timestamped Snapshots
    │
    ├─ Export to CSV and Excel
    │   │
    │   ├─ Generate Business Insights
    │   └─ Apply Professional Formatting
    │
    └─ Update Status and Log Results
```

### Error Handling Flow

```
Error Occurrence
    │
    ▼
Error Classification
    │
    ├─ COM Error → Identify Specific Type
    ├─ File System Error → Check Permissions/Space
    ├─ Data Error → Validate and Sanitize
    └─ Unknown Error → Log and Report
    │
    ▼
Generate User-Friendly Message
    │
    ├─ Title: Clear Problem Description
    ├─ Message: What Went Wrong
    ├─ Solutions: Actionable Steps
    └─ Technical Details: Debug Information
    │
    ▼
Display Error
    │
    ├─ GUI: Error Dialog with Guidance
    ├─ CLI: Formatted Text Output
    └─ Log: Detailed Error Information
    │
    ▼
Recovery Strategy
    │
    ├─ Continue with Other Reports
    ├─ Retry with Different Parameters
    ├─ Graceful Degradation
    └─ User Intervention Required
```

## File Organization Patterns

### Configuration Files

**pyproject.toml**
- Modern Python project configuration
- Build system requirements and metadata
- Development dependencies and tools
- Code quality tool configuration

**requirements.txt**
- Minimal core dependencies for runtime
- Essential packages: pywin32, openpyxl
- Optional dependencies commented out
- Version constraints for stability

### Utility Scripts

**build_exe.py**
- PyInstaller-based executable creation
- Cross-platform build considerations
- Dependency bundling and optimization
- Distribution package generation

**debug_reports.py**
- Individual report debugging utilities
- QuickBooks connection testing
- XML request/response validation
- Performance analysis tools

**test_xml_generation.py**
- XML structure validation
- Report configuration testing
- qbXML compliance checking
- Development-time testing

### Documentation Structure

**docs/ Directory**
- Additional technical documentation
- Change summaries and release notes
- Troubleshooting guides
- Development procedures

**Kiro Specifications (.kiro/)**
- Structured feature specifications
- Requirements documentation
- Technical design documents
- Implementation task tracking

## Code Quality and Standards

### Naming Conventions

**Functions and Variables**
- snake_case for function and variable names
- Descriptive names that indicate purpose
- Consistent prefixes for related functions
- No abbreviations except common ones

**Constants and Configuration**
- UPPER_CASE for constant values
- Descriptive names with clear meaning
- Grouped by functionality
- Comprehensive documentation

**Classes and Objects**
- PascalCase for class names
- Descriptive names indicating purpose
- Inheritance hierarchy clear from names
- Interface names when appropriate

### Documentation Standards

**Function Documentation**
- Comprehensive docstrings for all public functions
- Parameter types and descriptions
- Return value documentation
- Exception documentation
- Usage examples where appropriate

**Inline Comments**
- Business logic explanations
- Complex algorithm descriptions
- QuickBooks-specific nuance explanations
- Error handling rationale

**Code Organization**
- Logical grouping of related functions
- Clear section headers
- Consistent indentation and spacing
- Minimal function complexity

### Error Handling Patterns

**Structured Error Response**
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

**Exception Handling Strategy**
- Specific exception types for different error categories
- Graceful degradation for non-critical errors
- Comprehensive logging for debugging
- User-friendly error messages

## Testing Architecture

### Test Organization

**tests/ Directory Structure**
```
tests/
├── test_basic.py              # Core functionality tests
├── test_enhanced_features.py  # Advanced feature tests
├── test_xml_generation.py     # XML validation tests
└── conftest.py               # Test configuration and fixtures
```

**Test Categories**
- Unit tests for individual functions
- Integration tests for workflow validation
- Mock-based tests for QuickBooks simulation
- End-to-end tests for complete scenarios

### Test Data Management

**Mock Data Structures**
- Sample qbXML responses for each report type
- Test configuration files
- Simulated error conditions
- Performance benchmark data

**Test Utilities**
- QuickBooks connection mocking
- File system simulation
- Configuration test helpers
- XML validation utilities

## Deployment and Distribution

### Build Process

**Source Distribution**
- Python package with dependencies
- Installation via pip
- Cross-platform compatibility
- Development environment support

**Executable Distribution**
- PyInstaller-based standalone executable
- All dependencies bundled
- Windows-specific optimizations
- Minimal installation requirements

### Configuration Management

**Environment Variables**
- `QB_COMPANY_FILE`: Optional company file path
- Development and production configurations
- Sensitive data externalization
- Deployment flexibility

**Settings Persistence**
- User preference storage
- Automatic settings migration
- Backward compatibility
- Default value management

## Future Architecture Evolution

### Modularization Plans

**Phase 1: Internal Module Separation**
- Clear module boundaries within monolith
- Interface definition for future separation
- Dependency injection preparation
- Testing isolation improvements

**Phase 2: Physical Module Separation**
- Separate modules for distinct functionality
- Package-based organization
- Import dependency management
- Interface versioning

**Phase 3: Microservices Transition**
- Service boundaries definition
- API design and implementation
- Container-based deployment
- Scalability improvements

### Scalability Considerations

**Performance Optimizations**
- Parallel report processing
- Caching mechanisms
- Memory usage optimization
- I/O efficiency improvements

**Multi-User Support**
- Concurrent user handling
- Resource sharing management
- Security isolation
- Permission systems

**Platform Expansion**
- Cross-platform compatibility
- Cloud deployment options
- Mobile interface development
- API-first architecture

## Maintenance and Evolution

### Code Maintenance Strategies

**Regular Refactoring**
- Code quality improvements
- Performance optimization
- Security enhancement
- Dependency updates

**Documentation Maintenance**
- API documentation updates
- Architecture evolution tracking
- Best practice documentation
- Developer onboarding materials

**Technical Debt Management**
- Regular code reviews
- Quality metric tracking
- Refactoring prioritization
- Investment planning

### Knowledge Management

**Architecture Decision Records**
- Design rationale documentation
- Alternative consideration
- Decision impact analysis
- Evolution tracking

**Developer Resources**
- Code style guides
- Testing best practices
- Debugging procedures
- Performance optimization guides