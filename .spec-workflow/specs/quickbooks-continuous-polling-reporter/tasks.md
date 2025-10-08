# Implementation Plan

- [x] 1. Set up project structure and configuration system
  - Create configuration module with REPORT_CONFIGS dictionary for all 9 report types
  - Implement load_settings() and save_settings() functions for user preferences persistence
  - Define constants for intervals, default directories, and qbXML versions
  - Create get_file_paths() utility for consistent file path management
  - _Requirements: 9_

- [x] 2. Implement QuickBooks integration layer
  - [x] 2.1 Create COM object management functions
    - Implement qb_request() with pythoncom initialization and cleanup
    - Use gencache.EnsureDispatch() for QBXMLRP2.RequestProcessor creation
    - Add proper try/finally blocks for resource cleanup
    - _Requirements: 1.1, 1.7_

  - [x] 2.2 Implement connection strategies with fallbacks
    - Create open_connection() with multiple local connection modes (1, 0, 2)
    - Implement try_begin_session() with multiple path/mode combinations
    - Add host_info() to query QuickBooks connection details
    - _Requirements: 1.1, 1.5_

  - [x] 2.3 Build error classification and user-friendly messaging
    - Create get_user_friendly_error() to convert COM errors to actionable messages
    - Define error types: SDK_NOT_INSTALLED, SDK_NOT_REGISTERED, ACCESS_DENIED, FILE_NOT_FOUND, CONNECTION_ERROR
    - Structure error responses with title, message, solutions, technical details
    - _Requirements: 1.2, 1.4, 10.2, 10.3, 10.4, 10.5_

- [x] 3. Build qbXML request generation system
  - [x] 3.1 Implement build_report_qbxml() for all query types
    - Support GeneralDetailReportQueryRq for detailed reports
    - Support GeneralSummaryReportQueryRq for summary reports
    - Support AgingReportQueryRq for aging reports
    - _Requirements: 2.2_

  - [x] 3.2 Add date parameter handling
    - Implement date range logic with FromReportDate and ToReportDate for standard reports
    - Implement AsOfReportDate logic for aging reports
    - Add date validation with fallback to current month
    - _Requirements: 2.3, 2.4_

  - [x] 3.3 Implement version negotiation
    - Try qbXML version 16.0 first
    - Fallback to version 13.0 on failure
    - Log version used for each request
    - _Requirements: 1.3_

- [x] 4. Create report processing pipeline
  - [x] 4.1 Implement qbXML response parsing
    - Create parse_qbxml_response() to extract rows and columns from XML
    - Handle missing columns gracefully with default values
    - Handle empty values and malformed XML
    - _Requirements: 2.5, 2.7_

  - [x] 4.2 Build main export_report() orchestration function
    - Generate qbXML request based on report configuration
    - Execute QuickBooks communication via qb_request()
    - Parse response and extract data
    - Compute data hash
    - Determine if snapshot needed
    - Export to CSV and Excel
    - Create timestamped snapshots if data changed
    - Update status via callback
    - _Requirements: 2.1, 2.2, 2.5_

  - [x] 4.3 Add request/response logging
    - Log qbXML request to {report_key}_request.xml
    - Log qbXML response to {report_key}_response.xml
    - Include in qb_request() function
    - _Requirements: 2.6, 8.3, 8.4_

- [x] 5. Implement change detection system
  - [x] 5.1 Create hash computation function
    - Implement compute_data_hash() using SHA-256
    - Concatenate all row data for consistent hashing
    - Handle encoding issues gracefully
    - _Requirements: 4.1, 4.7_

  - [x] 5.2 Build hash comparison logic
    - Implement should_create_snapshot() to compare hashes
    - Read stored hash from .hash file
    - Return True if hash differs or file missing
    - _Requirements: 4.2, 4.3_

  - [x] 5.3 Implement snapshot creation
    - Create timestamped filenames with format: {Report_Name}_YYYYMMDD_HHMMSS
    - Copy CSV and Excel files to timestamped versions
    - Update hash file with new hash value
    - Always update base files regardless of hash
    - _Requirements: 4.4, 4.5, 4.6_

- [x] 6. Build multi-format export system
  - [x] 6.1 Implement CSV export
    - Create export_to_csv() function
    - Use standard CSV format with proper quoting
    - Write header row from columns
    - Write data rows
    - Use UTF-8 encoding
    - _Requirements: 5.1, 5.2_

  - [x] 6.2 Implement Excel export with openpyxl
    - Create export_to_excel() function using openpyxl
    - Apply corporate blue header (#4472C4) with white text
    - Make headers bold and centered
    - Auto-size all columns to fit content
    - Apply Excel table formatting with filters
    - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.6_

- [x] 7. Create scheduling and polling engine
  - [x] 7.1 Implement scheduler thread class
    - Create SchedulerThread extending threading.Thread
    - Add interval configuration (5, 15, 30, 60 minutes)
    - Implement run() method with polling loop
    - Add stop() method for graceful shutdown
    - Use threading.Event for interruptible sleep
    - _Requirements: 3.1, 3.2, 3.5_

  - [x] 7.2 Add timer display and next run calculation
    - Calculate next scheduled run time
    - Display countdown in UI
    - Update on interval change
    - _Requirements: 3.3_

  - [x] 7.3 Implement error handling in polling loop
    - Catch exceptions during report generation
    - Log errors and continue to next cycle
    - Don't stop polling on individual report failures
    - _Requirements: 3.6_

  - [x] 7.4 Add start/stop controls
    - Implement start_auto() to begin polling
    - Implement stop_auto() to halt polling
    - Ensure current operation completes before stopping
    - _Requirements: 3.4, 3.7_

- [x] 8. Build GUI interface with Tkinter
  - [x] 8.1 Create main window layout
    - Set up main Tkinter window with title and icon
    - Create frames for controls and status display
    - Add status bar at bottom
    - _Requirements: 6.1_

  - [x] 8.2 Implement output folder selection
    - Add "Select Output Folder" button
    - Open folder picker dialog on click
    - Display current output directory
    - Save preference to settings file
    - _Requirements: 6.3, 6.4_

  - [x] 8.3 Add date range configuration controls
    - Create DateEntry widgets for FromDate and ToDate
    - Initialize with current month by default
    - Save date preferences to settings file
    - _Requirements: 6.5_

  - [x] 8.4 Implement interval selection dropdown
    - Create dropdown with options: 5, 15, 30, 60 minutes
    - Load saved preference on startup
    - Save preference on change
    - _Requirements: 6.5_

  - [x] 8.5 Add control buttons
    - Create "Start Auto" / "Stop Auto" toggle button
    - Add "Export All Now" button for immediate export
    - Add "Open Folder" button to open output directory in Explorer
    - Wire buttons to appropriate handler functions
    - _Requirements: 6.6, 6.7, 6.8_

  - [x] 8.6 Build report status grid
    - Create grid with 9 rows (one per report)
    - Add columns: Report Name, Status, Row Count, Excel Status
    - Initialize all reports to "Idle" status
    - _Requirements: 6.2_

  - [x] 8.7 Implement real-time status updates
    - Create status callback function for report processing
    - Update status labels during report execution
    - Show "Running" during processing
    - Show "Success" with row count on completion
    - Show "Error" with error message on failure
    - Use color coding: Green (Success), Red (Error), Yellow (Running), Gray (Idle)
    - _Requirements: 6.9, 6.10_

  - [x] 8.8 Add threading for background operations
    - Use threading.Thread for report generation
    - Use queue.Queue for thread-safe UI updates
    - Use root.after() to update UI from worker threads
    - Ensure UI remains responsive during operations
    - _Requirements: 6.9_

- [x] 9. Implement CLI interface
  - [x] 9.1 Add command-line argument parsing
    - Use argparse for argument handling
    - Add --gui flag for GUI mode
    - Add --diagnose flag for diagnostics
    - Add --test-xml flag for XML validation
    - _Requirements: 7.1, 7.3, 7.4_

  - [x] 9.2 Implement CLI mode operation
    - Display text-based status updates with emoji indicators
    - Show progress for each report
    - Display error messages with troubleshooting guidance
    - Return appropriate exit codes (0 for success, 1 for error)
    - _Requirements: 7.2, 7.6_

  - [x] 9.3 Create diagnostic mode
    - Run comprehensive diagnostics when --diagnose flag provided
    - Generate quickbooks_diagnostics.json
    - Generate QuickBooks_Diagnostic_Report.xlsx
    - Display results in console
    - _Requirements: 7.5_

- [x] 10. Build logging and diagnostics system
  - [x] 10.1 Implement logging function
    - Create log() function with timestamp formatting
    - Write to QuickBooks_Auto_Reports.log
    - Use emoji indicators: 📥 📊 🎯 ✅ ❌
    - Ensure thread-safe file writing
    - _Requirements: 8.1, 8.2_

  - [x] 10.2 Create QuickBooks installation checker
    - Implement check_quickbooks_installation() using Windows registry
    - Check both 32-bit and 64-bit registry paths
    - Return installation status and registry paths
    - _Requirements: 8.5_

  - [x] 10.3 Create SDK installation checker
    - Implement check_sdk_installation() using COM registration
    - Try to get CLSID for QBXMLRP2.RequestProcessor
    - Return registration status and CLSID or error
    - _Requirements: 8.5_

  - [x] 10.4 Build comprehensive diagnostic function
    - Create diagnose_quickbooks_connection() function
    - Collect system information (platform, Python version, architecture)
    - Check QuickBooks installation
    - Check SDK installation
    - Test COM object creation
    - Test connection to QuickBooks
    - Generate recommendations based on findings
    - _Requirements: 8.5, 8.7_

  - [x] 10.5 Implement diagnostic report generation
    - Save diagnostic data to quickbooks_diagnostics.json
    - Create create_diagnostic_excel_report() function
    - Generate formatted Excel report with diagnostic results
    - Use openpyxl for Excel creation
    - Include system info, component status, connectivity tests, recommendations
    - _Requirements: 8.7_

  - [x] 10.6 Add detailed error logging
    - Log error type, message, stack trace, context
    - Include COM error codes in logs
    - Log solutions and troubleshooting steps
    - _Requirements: 8.6_

- [x] 11. Implement configuration persistence
  - [x] 11.1 Create settings file management
    - Define SETTINGS_FILE path in user home directory
    - Implement load_settings() with default values
    - Implement save_settings() with JSON serialization
    - _Requirements: 9.1, 9.2, 9.3_

  - [x] 11.2 Add settings initialization on startup
    - Load settings when application starts
    - Apply loaded settings to UI controls
    - Use defaults if settings file doesn't exist
    - _Requirements: 9.4_

  - [x] 11.3 Handle corrupted settings gracefully
    - Catch JSON parsing errors
    - Use default values on corruption
    - Log warning about corrupted settings
    - Create new settings file on next save
    - _Requirements: 9.5, 9.6_

- [x] 12. Add error handling and recovery
  - [x] 12.1 Implement COM error handling
    - Wrap all COM operations in try/except blocks
    - Use get_user_friendly_error() for error classification
    - Log technical details for debugging
    - Display user-friendly messages in UI
    - _Requirements: 10.1_

  - [x] 12.2 Add connection retry logic
    - Implement multiple connection strategies in open_connection()
    - Try different local connection modes
    - Try different session paths and modes
    - Log each attempt for debugging
    - _Requirements: 10.6_

  - [x] 12.3 Implement graceful degradation
    - Continue processing other reports if one fails
    - Log errors and continue polling on failure
    - Ensure CSV is created even if Excel fails
    - Provide fallback error messages for unknown errors
    - _Requirements: 10.7_

- [x] 13. Create application entry point and main flow
  - [x] 13.1 Implement main() function
    - Parse command-line arguments
    - Route to GUI mode or CLI mode based on --gui flag
    - Route to diagnostic mode if --diagnose flag provided
    - Handle test XML mode if --test-xml flag provided
    - _Requirements: 7.1, 7.3, 7.4_

  - [x] 13.2 Add GUI mode initialization
    - Create Tkinter root window
    - Initialize all GUI components
    - Load settings and apply to UI
    - Start main event loop
    - _Requirements: 6.1_

  - [x] 13.3 Add CLI mode execution
    - Display startup message
    - Execute report generation for all reports
    - Display results with emoji indicators
    - Exit with appropriate exit code
    - _Requirements: 7.2_

  - [x] 13.4 Implement export_all_reports() function
    - Iterate through all 9 report configurations
    - Call export_report() for each
    - Collect results and display summary
    - Handle errors for individual reports without stopping
    - _Requirements: 2.1, 6.7_

- [x] 14. Add Windows Explorer integration
  - [x] 14.1 Implement open_folder() function
    - Use subprocess to open Windows Explorer
    - Pass output directory path
    - Handle errors if directory doesn't exist
    - _Requirements: 6.8_

- [x] 15. Create executable build system
  - [x] 15.1 Create PyInstaller spec file
    - Define entry point as quickbooks_autoreport.py
    - Include all dependencies
    - Set application name and icon
    - Configure for Windows platform
    - _Requirements: Deployment_

  - [x] 15.2 Create build script
    - Implement build_exe.py to automate PyInstaller build
    - Clean previous builds
    - Run PyInstaller with spec file
    - Verify executable creation
    - _Requirements: Deployment_

- [x] 16. Write comprehensive tests
  - [x]* 16.1 Create XML generation tests
    - Test build_report_qbxml() for all 9 report types
    - Validate XML structure and syntax
    - Test date parameter handling
    - Test version negotiation
    - _Requirements: 2.2, 2.3, 2.4_

  - [x]* 16.2 Create configuration tests
    - Test load_settings() with valid data
    - Test save_settings() functionality
    - Test handling of missing settings file
    - Test handling of corrupted settings file
    - Test default value fallbacks
    - _Requirements: 9.1, 9.2, 9.4, 9.5, 9.6_

  - [x]* 16.3 Create data processing tests
    - Test parse_qbxml_response() with sample XML
    - Test handling of missing columns
    - Test handling of empty values
    - Test compute_data_hash() consistency
    - _Requirements: 2.5, 2.7, 4.1_

  - [x]* 16.4 Create change detection tests
    - Test should_create_snapshot() logic
    - Test hash comparison with matching hashes
    - Test hash comparison with different hashes
    - Test handling of missing hash files
    - _Requirements: 4.2, 4.3, 4.7_

  - [x]* 16.5 Create file export tests
    - Test CSV export with sample data
    - Test Excel export with sample data
    - Test timestamped snapshot creation
    - Test file naming conventions
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x]* 16.6 Create error handling tests
    - Test get_user_friendly_error() for each error type
    - Test error classification logic
    - Test error message formatting
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_