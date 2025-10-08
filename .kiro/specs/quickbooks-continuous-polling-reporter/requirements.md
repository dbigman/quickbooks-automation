# Requirements Document

## Introduction

The QuickBooks Auto Reporter is an automated data extraction and reporting system designed to continuously monitor QuickBooks Desktop and export multiple report types to designated folders. The system provides scheduled execution with configurable intervals, change detection to avoid redundant exports, and professional Excel formatting. It serves as a bridge between QuickBooks Desktop and external data consumers, enabling automated data workflows without manual intervention.

The application supports 9 different report types including Open Sales Orders, Profit & Loss statements, Sales analytics, and Accounts Payable/Receivable aging reports. It features both GUI and command-line interfaces, and comprehensive diagnostics.

## Requirements

### Requirement 1: QuickBooks Desktop Integration

**User Story:** As a business user, I want the application to connect to QuickBooks Desktop automatically, so that I can extract report data without manual QuickBooks interaction.

#### Acceptance Criteria

1. WHEN the application starts THEN it SHALL attempt to connect to QuickBooks Desktop using the qbXML API
2. IF QuickBooks Desktop is not running THEN the application SHALL display a clear error message with troubleshooting steps
3. WHEN connecting to QuickBooks THEN the application SHALL attempt qbXML version 16.0 first, and IF that fails THEN it SHALL fallback to version 13.0
4. IF the QuickBooks SDK is not installed THEN the application SHALL detect this condition and provide installation guidance
5. WHEN multiple connection methods are available THEN the application SHALL try: (1) open QuickBooks file, (2) user-selected file, (3) configured company file path
6. WHEN authentication is required THEN the application SHALL use QuickBooks SDK authentication with local connection modes
7. IF connection fails after all attempts THEN the application SHALL log detailed error information including COM error codes

### Requirement 2: Multi-Report Data Extraction

**User Story:** As a business analyst, I want to extract 9 different report types from QuickBooks, so that I can analyze various aspects of business operations.

#### Acceptance Criteria

1. WHEN a report is requested THEN the application SHALL support the following report types: Open Sales Orders by Item, Profit & Loss Standard, Profit & Loss Detail, Sales by Item Summary, Sales by Item Detail, Sales by Rep Detail, Purchases by Vendor Detail, AP Aging Detail, AR Aging Detail
2. WHEN generating a report THEN the application SHALL construct valid qbXML requests according to the QuickBooks SDK specification
3. IF a report requires a date range THEN the application SHALL include configurable FromReportDate and ToReportDate parameters
4. IF a report uses "AsOf" date logic THEN the application SHALL include the appropriate ReportAsOfDate parameter
5. WHEN receiving qbXML responses THEN the application SHALL parse the XML and extract all data rows and columns
6. IF a qbXML request fails THEN the application SHALL log both the request XML and response XML for troubleshooting
7. WHEN parsing report data THEN the application SHALL handle missing columns, empty values, and malformed XML gracefully

### Requirement 3: Scheduled Continuous Polling

**User Story:** As a system administrator, I want the application to run continuously and check for report changes at configurable intervals, so that data exports stay current without manual triggering.

#### Acceptance Criteria

1. WHEN the user starts automatic mode THEN the application SHALL poll for report changes at the configured interval
2. WHEN configuring the interval THEN the user SHALL be able to select from: 5 minutes, 15 minutes, 30 minutes, or 60 minutes
3. WHEN a polling cycle begins THEN the application SHALL display the next scheduled run time
4. IF the user changes the interval THEN the application SHALL apply the new interval to subsequent polling cycles
5. WHEN the application is running THEN it SHALL continue polling until the user stops it or the application is closed
6. IF an error occurs during polling THEN the application SHALL log the error and continue with the next scheduled cycle
7. WHEN the user stops automatic mode THEN the application SHALL complete the current operation and then halt polling

### Requirement 4: Change Detection and Timestamped Snapshots

**User Story:** As a data consumer, I want the application to only save new report versions when data actually changes, so that I don't accumulate redundant duplicate files.

#### Acceptance Criteria

1. WHEN a report is generated THEN the application SHALL compute a hash of the report data
2. IF a hash file exists for the report THEN the application SHALL compare the new hash with the stored hash
3. WHEN the hash matches the previous hash THEN the application SHALL NOT create a timestamped snapshot
4. WHEN the hash differs from the previous hash THEN the application SHALL create timestamped CSV and Excel files with format: `{Report_Name}_YYYYMMDD_HHMMSS.csv` and `{Report_Name}_YYYYMMDD_HHMMSS.xlsx`
5. WHEN data changes are detected THEN the application SHALL update the hash file with the new hash value
6. WHEN generating reports THEN the application SHALL always update the non-timestamped base files (`{Report_Name}.csv` and `{Report_Name}.xlsx`)
7. IF hash computation fails THEN the application SHALL treat the report as changed and create a timestamped snapshot

### Requirement 5: Multi-Format Export (CSV and Excel)

**User Story:** As a data analyst, I want reports exported in both CSV and professionally formatted Excel formats, so that I can use the data in various tools and present it professionally.

#### Acceptance Criteria

1. WHEN exporting a report THEN the application SHALL generate both a CSV file and an Excel file
2. WHEN creating CSV files THEN the application SHALL use standard CSV format with proper quoting and escaping
3. WHEN creating Excel files THEN the application SHALL apply corporate blue header styling (#4472C4)
4. WHEN formatting Excel files THEN the application SHALL auto-size all columns to fit content
5. WHEN creating Excel tables THEN the application SHALL apply table formatting with filters enabled
6. WHEN creating Excel files THEN the application SHALL use openpyxl for professional formatting

### Requirement 6: GUI Interface with Real-Time Status

**User Story:** As a business user, I want a graphical interface that shows real-time status for each report, so that I can monitor the application without reading log files.

#### Acceptance Criteria

1. WHEN the application starts in GUI mode THEN it SHALL display a window with controls for all 9 reports
2. WHEN displaying report status THEN the application SHALL show: report name, current status (Idle/Running/Success/Error), row count from last export, Excel generation confirmation
3. WHEN the user clicks "Select Output Folder" THEN the application SHALL open a folder selection dialog
4. WHEN the user selects a folder THEN the application SHALL save this preference to the settings file
5. WHEN the user configures date ranges THEN the application SHALL provide date picker controls for FromDate and ToDate
6. WHEN the user clicks "Start Auto" THEN the application SHALL begin scheduled polling and update the button to "Stop Auto"
7. WHEN the user clicks "Export All Now" THEN the application SHALL immediately generate all 9 reports
8. WHEN the user clicks "Open Folder" THEN the application SHALL open the output directory in Windows Explorer
9. WHEN a report is running THEN the application SHALL update the status display in real-time
10. IF an error occurs THEN the application SHALL display the error status and provide access to error details

### Requirement 7: Command-Line Interface

**User Story:** As a system administrator, I want to run the application from the command line for automation and scripting, so that I can integrate it into scheduled tasks or CI/CD pipelines.

#### Acceptance Criteria

1. WHEN the application is run without `--gui` flag THEN it SHALL operate in command-line mode
2. WHEN running in command-line mode THEN the application SHALL display text-based status updates
3. WHEN the `--diagnose` flag is provided THEN the application SHALL run comprehensive diagnostics and generate a diagnostic report
4. WHEN the `--test-xml` flag is provided THEN the application SHALL validate XML generation without connecting to QuickBooks
5. WHEN running diagnostics THEN the application SHALL generate `quickbooks_diagnostics.json` and `QuickBooks_Diagnostic_Report.xlsx`
6. IF command-line arguments are invalid THEN the application SHALL display usage help and exit gracefully

### Requirement 8: Comprehensive Logging and Diagnostics

**User Story:** As a support engineer, I want detailed logs and diagnostic information, so that I can troubleshoot issues efficiently.

#### Acceptance Criteria

1. WHEN the application runs THEN it SHALL write logs to `QuickBooks_Auto_Reports.log`
2. WHEN logging events THEN the application SHALL use emoji indicators: 📥 (fetching), 🎯 (processing), 📊 (exporting), ✅ (success), ❌ (error)
3. WHEN a qbXML request is made THEN the application SHALL log the request XML to `{report_key}_request.xml`
4. WHEN a qbXML response is received THEN the application SHALL log the response XML to `{report_key}_response.xml`
5. WHEN diagnostics are run THEN the application SHALL check: QuickBooks installation, SDK registration, COM component availability, company file accessibility
6. WHEN errors occur THEN the application SHALL log: error type, error message, stack trace, context information
7. WHEN generating diagnostic reports THEN the application SHALL include: system information, QuickBooks version, SDK version, connection test results, error history

### Requirement 9: Configuration Persistence

**User Story:** As a business user, I want my preferences to be saved automatically, so that I don't have to reconfigure the application every time I use it.

#### Acceptance Criteria

1. WHEN the user changes the output directory THEN the application SHALL save this preference to `~/.qb_auto_reporter_settings.json`
2. WHEN the user changes the check interval THEN the application SHALL save this preference to the settings file
3. WHEN the user configures date ranges THEN the application SHALL save these preferences to the settings file
4. WHEN the application starts THEN it SHALL load preferences from the settings file
5. IF the settings file does not exist THEN the application SHALL use default values and create the settings file on first preference change
6. IF the settings file is corrupted THEN the application SHALL use default values and log a warning

### Requirement 10: Error Handling and Recovery

**User Story:** As a system administrator, I want the application to handle errors gracefully and provide clear recovery guidance, so that I can resolve issues quickly.

#### Acceptance Criteria

1. WHEN a COM error occurs THEN the application SHALL identify the error type and provide specific troubleshooting steps
2. IF COM error -2147221005 occurs THEN the application SHALL advise: SDK not installed, run as Administrator, restart computer
3. IF COM error -2147221164 occurs THEN the application SHALL advise: reinstall SDK, run regsvr32 qbxmlrp2.dll as Administrator
4. IF "Access Denied" occurs THEN the application SHALL advise: run as Administrator, check file permissions, ensure single-user mode
5. IF "File Not Found" occurs THEN the application SHALL advise: verify QuickBooks installation, check QB_COMPANY_FILE variable, open company file first
6. WHEN network or connection errors occur THEN the application SHALL implement retry logic with exponential backoff
7. WHEN unrecoverable errors occur THEN the application SHALL log the error, notify the user, and exit gracefully


