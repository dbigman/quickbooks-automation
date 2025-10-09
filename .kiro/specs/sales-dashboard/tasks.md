# Implementation Plan

- [x] 1. Set up project structure and dependencies

  - Create `apps/dashboard/` directory structure
  - Create `src/yourapp/dashboard/` module structure
  - Add Streamlit, pandas, openpyxl, and plotly to `pyproject.toml`
  - Create configuration file with constants (output directory, polling interval, required columns)
  - _Requirements: 5.1, 5.4, 10.4_

- [x] 2. Implement data access layer

  - [x] 2.1 Create FileScanner class

    - Implement `list_excel_files()` to scan output directory for .xlsx files
    - Implement `get_file_modified_time()` to check file timestamps
    - Implement `file_exists()` validation
    - _Requirements: 5.1, 5.2, 6.2_

  - [x] 2.2 Create ExcelLoader class

    - Implement `load_file()` to read Excel files with pandas
    - Implement `validate_columns()` to check for required columns
    - Implement `add_weekday_column()` to extract weekday names from dates
    - Add error handling for file read failures
    - _Requirements: 5.3, 5.5, 5.6, 9.1, 9.2_

  - [x] 2.3 Write unit tests for data access layer

    - Test FileScanner with empty directory, single file, multiple files
    - Test ExcelLoader with valid data, missing columns, corrupted files
    - Test weekday extraction with various date formats
    - _Requirements: 5.5, 9.1, 9.2_

- [x] 3. Implement domain models

  - [x] 3.1 Create SalesData dataclass

    - Define dataclass with df, filepath, loaded_at, row_count fields
    - Implement `from_file()` factory method

    - Implement `get_date_range()` method
    - Add type hints for all fields
    - _Requirements: 5.6, 10.1_

  - [x] 3.2 Create DashboardState dataclass

    - Define session state fields (current_file, sales_data, last_update, etc.)
    - Implement `should_reload()` method to check for file modifications
    - Add type hints for all fields
    - _Requirements: 6.1, 6.2, 6.5_

- [x] 4. Implement business logic layer

  - [x] 4.1 Create MetricsCalculator class

    - Implement `calculate_total_revenue()` summing Transaction_Total
    - Implement `calculate_total_units()` summing Sales_Qty
    - Implement `get_top_products_by_revenue()` with top N filtering
    - Implement `get_top_products_by_units()` with top N filtering
    - Implement `aggregate_by_weekday()` with chronological ordering
    - Add data type conversion for numeric columns
    - _Requirements: 1.1, 1.2, 2.1, 2.2, 3.2, 3.3, 4.2, 4.3_

  - [x] 4.2 Write unit tests for MetricsCalculator

    - Test revenue calculations with sample data
    - Test units calculations with zero and negative values
    - Test top N products with various dataset sizes
    - Test weekday aggregation with multi-week data
    - _Requirements: 1.4, 2.4, 3.5, 4.5_

  - [x] 4.3 Create ChartGenerator class

    - Implement `create_weekday_line_chart()` for trend visualization
    - Implement `create_bar_chart()` for top products display
    - Configure chart styling (labels, gridlines, colors)
    - Ensure weekday ordering is chronological (Monday-Sunday)
    - _Requirements: 3.1, 3.4, 4.1, 4.4_

  - [x] 4.4 Write unit tests for ChartGenerator

    - Test chart configuration generation
    - Test data formatting for charts
    - Test weekday ordering in chart data
    - _Requirements: 3.3, 3.4, 4.3, 4.4_

- [x] 5. Implement utility functions

  - Create formatting utilities for currency and numbers
  - Create date/time formatting utilities
  - Create error message formatting utilities
  - Add logging setup with emoji indicators (📥 📊 ✅)
  - _Requirements: 1.3, 2.3, 7.2, 9.1_

- [x] 6. Implement sidebar UI component

  - [x] 6.1 Create render_sidebar function

    - Implement file selector dropdown using st.selectbox
    - Implement "Refresh Data" button using st.button
    - Display "Latest Update" timestamp with formatted date
    - Display currently selected filename
    - Add section headers and labels
    - _Requirements: 5.2, 5.3, 6.3, 6.4, 7.1, 7.2, 7.4, 8.1, 8.2, 8.3, 8.4, 8.5_

  - [x] 6.2 Add status indicators

    - Display loading spinner during data load
    - Display success/error indicators
    - Show file metadata (size, last modified)
    - _Requirements: 7.5, 9.3_

- [x] 7. Implement metrics display UI component

  - [x] 7.1 Create render_metrics_section function

    - Display total revenue metric card using st.metric
    - Display total units metric card using st.metric
    - Format currency values with $ symbol and commas
    - Format unit values with thousand separators
    - _Requirements: 1.1, 1.3, 2.1, 2.3_

  - [x] 7.2 Add top products display

    - Create horizontal bar chart for top 5 products by revenue
    - Create horizontal bar chart for top 5 products by units
    - Add chart titles and axis labels
    - Handle empty data gracefully
    - _Requirements: 1.2, 2.2, 1.4, 2.4_

- [x] 8. Implement charts display UI component

  - [x] 8.1 Create render_charts_section function

    - Create line chart for weekly revenue trend
    - Create line chart for weekly units movement
    - Configure x-axis with weekday names in order
    - Configure y-axis with appropriate scaling
    - Add chart titles and labels
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4_

  - [x] 8.2 Add chart interactivity

    - Enable hover tooltips with data values
    - Add zoom and pan capabilities
    - Ensure charts are responsive
    - _Requirements: 3.4, 4.4, 10.4_

- [x] 9. Implement main dashboard application

  - [x] 9.1 Create Home.py entry point

    - Set page configuration (title, icon, layout)
    - Initialize session state with DashboardState
    - Add main title and description
    - _Requirements: 8.1_

  - [x] 9.2 Implement file selection logic

    - Scan output directory for Excel files
    - Handle empty directory case with user message
    - Update session state when file selected
    - _Requirements: 5.1, 5.2, 5.4, 9.4_

  - [x] 9.3 Implement data loading logic

    - Load selected file using ExcelLoader
    - Validate required columns exist
    - Create SalesData instance
    - Update session state with loaded data
    - Handle file read errors with clear messages
    - _Requirements: 5.3, 5.5, 5.6, 9.1, 9.2_

  - [x] 9.4 Implement manual refresh functionality

    - Detect "Refresh Data" button click
    - Reload current file
    - Update last_update timestamp
    - Update all visualizations
    - _Requirements: 6.3, 6.4, 6.5_

  - [x] 9.5 Implement automatic polling

    - Check file modification time every hour
    - Compare with last known modification time
    - Auto-reload if file changed
    - Update timestamp on successful reload
    - Log polling errors without crashing
    - _Requirements: 6.1, 6.2, 6.5, 6.6_

  - [x] 9.6 Wire up all UI components

    - Render sidebar with file selector and controls
    - Render metrics section with calculations
    - Render charts section with visualizations
    - Ensure proper layout and spacing
    - _Requirements: 8.6_

- [x] 10. Implement error handling and user feedback

  - Add try-catch blocks around file operations
  - Display user-friendly error messages with st.error
  - Show missing columns list when validation fails
  - Provide instructions for empty directory case
  - Add loading indicators during data processing
  - Log errors for debugging
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 11. Implement performance optimizations

  - [x] 11.1 Add caching for data loading

    - Use @st.cache_data decorator on load_file function
    - Cache based on filepath and modification time
    - Clear cache when file changes detected
    - _Requirements: 10.1, 10.2_

  - [x] 11.2 Optimize data processing

    - Convert numeric columns early with pd.to_numeric
    - Filter unnecessary columns after loading
    - Use efficient pandas groupby operations
    - _Requirements: 10.1, 10.3, 10.5_

  - [x] 11.3 Optimize polling mechanism

    - Check modification time before reloading
    - Avoid blocking UI during polling
    - Debounce rapid file changes
    - _Requirements: 6.1, 10.3_

- [x] 12. Create configuration and documentation

  - Create .env.example with dashboard configuration variables
  - Document required columns in README
  - Add usage instructions for running dashboard
  - Document polling behavior and refresh options
  - Add troubleshooting guide for common errors
  - _Requirements: 5.4, 9.4, 9.5_

- [x] 13. Integration testing and validation


  - [x] 13.1 Test end-to-end flow

    - Test file selection → data load → metrics display
    - Test manual refresh functionality
    - Test automatic polling detection
    - Test error scenarios (missing file, bad data)
    - _Requirements: 5.3, 6.4, 9.1_

  - [x] 13.2 Test with real data

    - Use actual sales Excel file from output directory
    - Verify all metrics calculate correctly
    - Verify charts render properly
    - Test with large files (performance validation)
    - _Requirements: 10.1, 10.2, 10.5_

  - [x] 13.3 Test edge cases

    - Empty Excel file
    - File with missing columns
    - File with invalid data types
    - Multiple weeks of data
    - Single day of data
    - _Requirements: 1.4, 2.4, 3.5, 4.5, 9.2_
