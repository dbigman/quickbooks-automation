# Requirements Document

## Introduction

This feature implements a Streamlit-based sales analytics dashboard that visualizes sales data from Excel files. The dashboard provides real-time insights into sales revenue, product performance, and weekly trends. Users can select data files, view key metrics, and monitor data freshness through automatic polling or manual refresh.

The dashboard serves as a business intelligence tool for analyzing sales transactions, identifying top-performing products, and tracking sales patterns over time.

## Requirements

### Requirement 1: Sales Revenue Metrics Display

**User Story:** As a sales analyst, I want to view total sales revenue and revenue by product, so that I can quickly assess overall performance and identify top revenue-generating products.

#### Acceptance Criteria

1. WHEN the dashboard loads THEN the system SHALL display the total sum of 'Transaction_Total' as "Sales Revenue"
2. WHEN calculating revenue by product THEN the system SHALL aggregate 'Sales_Amount' by product and display the top 5 products
3. WHEN displaying revenue metrics THEN the system SHALL format currency values with appropriate symbols and decimal places
4. IF no data is available THEN the system SHALL display a meaningful message indicating no data to show

### Requirement 2: Units Sold Metrics Display

**User Story:** As a sales analyst, I want to view total units sold and units sold by product, so that I can understand sales volume and identify best-selling products by quantity.

#### Acceptance Criteria

1. WHEN the dashboard loads THEN the system SHALL display the total sum of 'Sales_Qty' as "Units Sold"
2. WHEN calculating units by product THEN the system SHALL aggregate 'Sales_Qty' by product and display the top 5 products
3. WHEN displaying unit metrics THEN the system SHALL format quantities as whole numbers with thousand separators
4. IF a product has zero or negative quantity THEN the system SHALL handle it gracefully without errors

### Requirement 3: Weekly Revenue Trend Visualization

**User Story:** As a sales analyst, I want to see a line chart of revenue by weekday, so that I can identify daily sales patterns and peak sales days.

#### Acceptance Criteria

1. WHEN displaying weekly revenue THEN the system SHALL create a line chart with weekday names on the x-axis
2. WHEN aggregating data THEN the system SHALL sum 'Sales_Amount' for each weekday
3. WHEN ordering weekdays THEN the system SHALL display them in chronological order (Monday through Sunday)
4. WHEN rendering the chart THEN the system SHALL use clear labels, gridlines, and appropriate scaling
5. IF data spans multiple weeks THEN the system SHALL aggregate all occurrences of each weekday

### Requirement 4: Weekly Product Movement Visualization

**User Story:** As a sales analyst, I want to see a line chart of units sold by weekday, so that I can understand volume patterns throughout the week.

#### Acceptance Criteria

1. WHEN displaying weekly movement THEN the system SHALL create a line chart with weekday names on the x-axis
2. WHEN aggregating data THEN the system SHALL sum 'Sales_Qty' for each weekday
3. WHEN ordering weekdays THEN the system SHALL display them in chronological order (Monday through Sunday)
4. WHEN rendering the chart THEN the system SHALL use clear labels, gridlines, and appropriate scaling
5. IF data spans multiple weeks THEN the system SHALL aggregate all occurrences of each weekday

### Requirement 5: File Selection and Data Loading

**User Story:** As a user, I want to select which Excel file to analyze from the output folder, so that I can view data from different time periods or reports.

#### Acceptance Criteria

1. WHEN the dashboard starts THEN the system SHALL scan the 'output' folder for .xlsx files
2. WHEN displaying file options THEN the system SHALL present a dropdown or file selector in the sidebar
3. WHEN a user selects a file THEN the system SHALL load the data and refresh all visualizations
4. IF the output folder is empty THEN the system SHALL display a message prompting the user to add files
5. IF a file cannot be read THEN the system SHALL display a clear error message with troubleshooting guidance
6. WHEN loading data THEN the system SHALL validate that required columns exist ('Transaction_Total', 'Sales_Amount', 'Sales_Qty')

### Requirement 6: Data Refresh and Polling

**User Story:** As a user, I want the dashboard to automatically detect file changes or manually refresh data, so that I always see the most current information without restarting the application.

#### Acceptance Criteria

1. WHEN the dashboard is running THEN the system SHALL check for file modifications every hour
2. WHEN a file modification is detected THEN the system SHALL automatically reload the data and update visualizations
3. WHEN the sidebar is displayed THEN the system SHALL include a manual "Refresh Data" button
4. WHEN the user clicks "Refresh Data" THEN the system SHALL immediately reload the selected file and update all metrics
5. WHEN data is refreshed THEN the system SHALL update the "Latest Update" timestamp
6. IF polling fails THEN the system SHALL log the error but continue running with existing data

### Requirement 7: Status and Metadata Display

**User Story:** As a user, I want to see when the data was last updated, so that I can trust the freshness of the information displayed.

#### Acceptance Criteria

1. WHEN the dashboard loads data THEN the system SHALL display a "Latest Update" timestamp
2. WHEN displaying the timestamp THEN the system SHALL use a clear, readable format (e.g., "2025-10-08 17:00:04")
3. WHEN data is refreshed THEN the system SHALL update the timestamp to the current time
4. WHEN displaying status THEN the system SHALL show the currently selected file name
5. IF data loading fails THEN the system SHALL display the last successful update time with an error indicator

### Requirement 8: Sidebar Navigation and Controls

**User Story:** As a user, I want a sidebar with all controls and settings, so that I can easily configure the dashboard without cluttering the main view.

#### Acceptance Criteria

1. WHEN the dashboard loads THEN the system SHALL display a sidebar on the left side
2. WHEN the sidebar is rendered THEN the system SHALL include the file selector control
3. WHEN the sidebar is rendered THEN the system SHALL include the "Refresh Data" button
4. WHEN the sidebar is rendered THEN the system SHALL display the "Latest Update" timestamp
5. WHEN the sidebar is rendered THEN the system SHALL display the current file name
6. WHEN organizing controls THEN the system SHALL group related items logically with clear labels

### Requirement 9: Error Handling and User Feedback

**User Story:** As a user, I want clear feedback when errors occur, so that I can understand what went wrong and how to fix it.

#### Acceptance Criteria

1. WHEN a file cannot be loaded THEN the system SHALL display a user-friendly error message
2. WHEN required columns are missing THEN the system SHALL list which columns are missing
3. WHEN data is being loaded THEN the system SHALL display a loading indicator
4. IF the output folder doesn't exist THEN the system SHALL provide instructions to create it
5. WHEN an error occurs THEN the system SHALL continue running and allow the user to select a different file

### Requirement 10: Performance and Responsiveness

**User Story:** As a user, I want the dashboard to load quickly and respond smoothly, so that I can efficiently analyze data without delays.

#### Acceptance Criteria

1. WHEN loading files under 10MB THEN the system SHALL display data within 3 seconds
2. WHEN switching between files THEN the system SHALL update visualizations within 2 seconds
3. WHEN polling for changes THEN the system SHALL not block user interactions
4. WHEN rendering charts THEN the system SHALL use efficient plotting libraries (e.g., Plotly, Altair)
5. IF a file is very large THEN the system SHALL provide feedback about processing time
