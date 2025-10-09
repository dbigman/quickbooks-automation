"""
Sales Analytics Dashboard - Home Page

Main entry point for the Streamlit sales analytics dashboard.
Provides interactive visualization and analysis of sales data.
"""

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from quickbooks_autoreport.dashboard.charts_display import (
    render_charts_section,
)
from quickbooks_autoreport.dashboard.config import OUTPUT_DIR
from quickbooks_autoreport.dashboard.data_loader import (
    ExcelLoader,
    FileScanner,
)
from quickbooks_autoreport.dashboard.metrics import MetricsCalculator
from quickbooks_autoreport.dashboard.metrics_display import (
    render_metrics_section,
    render_top_products_section,
)
from quickbooks_autoreport.dashboard.sidebar import render_sidebar
from quickbooks_autoreport.dashboard.utils import (
    format_error_message,
    log_error,
    log_loading,
    log_success,
    setup_logger,
)
from quickbooks_autoreport.domain.sales_data import (
    DashboardState,
    SalesData,
)

# Setup logging
logger = setup_logger(__name__)

# ============================================================================
# Page Configuration (Sub-task 9.1)
# ============================================================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# Session State Initialization (Sub-task 9.1)
# ============================================================================


def initialize_session_state() -> None:
    """
    Initialize session state with DashboardState.

    Creates a DashboardState instance in session state if it
    doesn't exist. This maintains state across Streamlit reruns.

    Requirements:
        - 8.1: Initialize session state
    """
    if "dashboard_state" not in st.session_state:
        st.session_state.dashboard_state = DashboardState()
        logger.info("📥 Initialized dashboard session state")


# ============================================================================
# File Selection Logic (Sub-task 9.2)
# ============================================================================


def scan_and_select_file(
    file_scanner: FileScanner, state: DashboardState
) -> None:
    """
    Scan output directory for Excel files and handle selection.

    Scans the output directory for .xlsx files and renders the
    sidebar with file selection controls. Updates session state
    when a file is selected.

    Args:
        file_scanner: FileScanner instance for discovering files
        state: Current dashboard state

    Requirements:
        - 5.1: Scan output folder for .xlsx files
        - 5.2: Present dropdown in sidebar
        - 5.4: Handle empty directory case
        - 9.4: Display user message for empty directory
    """
    try:
        # Scan for Excel files
        available_files = file_scanner.list_excel_files()

        # Get success message from session state if available
        success_message = st.session_state.get("success_message", None)
        
        # Render sidebar and get user selections
        selected_file, refresh_clicked = render_sidebar(
            available_files=available_files,
            current_file=state.current_file,
            last_update=state.last_update,
            success_message=success_message,
        )

        # Store refresh click in session state for processing
        st.session_state.refresh_clicked = refresh_clicked

        # Check if file selection changed
        if selected_file and selected_file != state.current_file:
            log_loading(logger, f"File selected: {selected_file.name}")
            state.current_file = selected_file
            state.error_message = None
            # Clear success message when selecting new file
            st.session_state.success_message = None
            # Trigger data load by clearing existing data
            state.sales_data = None

    except FileNotFoundError:
        # Directory doesn't exist
        st.error(
            f"❌ Output directory not found: {OUTPUT_DIR}\n\n"
            "Please create the directory and add Excel files to analyze."
        )
        log_error(logger, f"Output directory not found: {OUTPUT_DIR}")
    except Exception as e:
        error_msg = format_error_message(e, "scanning for files")
        st.error(f"❌ {error_msg}")
        log_error(logger, error_msg)


# ============================================================================
# Data Loading Logic (Sub-task 9.3)
# ============================================================================


def load_data(
    excel_loader: ExcelLoader, state: DashboardState
) -> None:
    """
    Load selected file and update session state.

    Loads the selected Excel file, validates required columns,
    creates a SalesData instance, and updates the dashboard state.

    Args:
        excel_loader: ExcelLoader instance for loading data
        state: Current dashboard state

    Requirements:
        - 5.3: Load selected file
        - 5.5: Validate required columns
        - 5.6: Create SalesData instance
        - 9.1: Handle file read errors
        - 9.2: Display clear error messages
    """
    if state.current_file is None:
        return

    # Check if data already loaded and no refresh requested
    if (
        state.sales_data is not None
        and not st.session_state.get("refresh_clicked", False)
    ):
        return

    try:
        # Show loading indicator
        with st.spinner(f"Loading {state.current_file.name}..."):
            log_loading(logger, f"Loading file: {state.current_file.name}")

            # Get file modification time for cache key
            file_mtime = state.current_file.stat().st_mtime

            # Load and validate data (with caching)
            sales_data = SalesData.from_file(
                state.current_file, excel_loader, file_mtime
            )

            # Add weekday column if Date column exists
            if "Date" in sales_data.df.columns:
                sales_data.df = excel_loader.add_weekday_column(
                    sales_data.df, date_column="Date"
                )

            # Update state
            state.sales_data = sales_data
            state.last_update = datetime.now()
            state.last_file_mtime = file_mtime
            state.error_message = None

            # Clear refresh flag
            st.session_state.refresh_clicked = False

            log_success(
                logger,
                f"Loaded {sales_data.row_count} rows from "
                f"{state.current_file.name}",
            )

            # Store success message in session state for sidebar display
            st.session_state.success_message = (
                f"✅ Successfully loaded {sales_data.row_count:,} rows "
                f"from {state.current_file.name}"
            )

    except ValueError as e:
        # Handle validation errors (missing columns, etc.)
        error_str = str(e)
        if "missing" in error_str.lower():
            # Extract missing columns if possible
            state.error_message = error_str
            st.error(f"❌ {error_str}")
            st.info(
                "💡 **Troubleshooting:** Ensure your Excel file "
                "has a 'Product Summary' sheet with columns: Product_Name, "
                "Sales_Amount, Sales_Qty"
            )
        else:
            state.error_message = format_error_message(e, "validating data")
            st.error(f"❌ {state.error_message}")

        log_error(logger, f"Data validation error: {error_str}")
        state.sales_data = None
        # Clear success message on error
        st.session_state.success_message = None

    except FileNotFoundError as e:
        error_msg = format_error_message(e, "loading file")
        state.error_message = error_msg
        st.error(f"❌ {error_msg}")
        st.info(
            "💡 **Troubleshooting:** The file may have been moved or deleted. "
            "Please select a different file."
        )
        log_error(logger, error_msg)
        state.sales_data = None
        # Clear success message on error
        st.session_state.success_message = None

    except Exception as e:
        error_msg = format_error_message(e, "loading data")
        state.error_message = error_msg
        st.error(f"❌ {error_msg}")
        st.info(
            "💡 **Troubleshooting:** The file may be corrupted or in an "
            "unsupported format. Please check the file and try again."
        )
        log_error(logger, error_msg)
        state.sales_data = None
        # Clear success message on error
        st.session_state.success_message = None


# ============================================================================
# Manual Refresh Functionality (Sub-task 9.4)
# ============================================================================


def handle_manual_refresh(state: DashboardState) -> None:
    """
    Handle manual refresh button click.

    Detects when the refresh button is clicked and triggers data reload
    by clearing the current sales data. The load_data function will then
    reload the file and update the timestamp.

    Args:
        state: Current dashboard state

    Requirements:
        - 6.3: Detect "Refresh Data" button click
        - 6.4: Reload current file
        - 6.5: Update last_update timestamp
    """
    if st.session_state.get("refresh_clicked", False):
        if state.current_file:
            log_loading(
                logger,
                f"Manual refresh triggered for "
                f"{state.current_file.name}"
            )
            # Clear sales data to trigger reload
            state.sales_data = None
        else:
            st.warning("⚠️ No file selected to refresh")


# ============================================================================
# Automatic Polling (Sub-task 9.5)
# ============================================================================


def check_file_modifications(
    file_scanner: FileScanner, state: DashboardState
) -> None:
    """
    Check for file modifications and auto-reload if changed.

    Checks the modification time of the current file with optimized
    polling that includes debouncing to avoid excessive checks and
    rapid reloads. The check is non-blocking and won't interfere
    with UI interactions.

    Args:
        file_scanner: FileScanner instance for checking file times
        state: Current dashboard state

    Requirements:
        - 6.1: Check file modification time (optimized with debouncing)
        - 6.2: Auto-reload if file changed
        - 6.5: Update timestamp on successful reload
        - 6.6: Log polling errors without crashing
        - 10.3: Avoid blocking UI during polling
    """
    try:
        # Check if we should reload based on file modification
        # Uses debouncing to avoid excessive checks (5 second minimum)
        if state.should_reload(file_scanner, debounce_seconds=5):
            log_loading(
                logger,
                f"File modification detected for {state.current_file.name}",
            )
            st.info(
                f"🔄 File modification detected. Reloading "
                f"{state.current_file.name}..."
            )
            # Clear sales data to trigger reload
            state.sales_data = None

    except Exception as e:
        # Log error but don't crash the dashboard
        log_error(logger, f"Polling error: {str(e)}")
        # Don't display error to user - continue with existing data


# ============================================================================
# UI Components Rendering (Sub-task 9.6)
# ============================================================================


def render_dashboard_content(state: DashboardState) -> None:
    """
    Render all dashboard UI components with proper layout.

    Renders the main dashboard content including metrics section,
    top products section, and charts section with proper spacing.

    Args:
        state: Current dashboard state with loaded sales data

    Requirements:
        - 8.6: Wire up all UI components
        - Proper layout and spacing
    """
    if state.sales_data is None:
        # No data loaded yet
        st.info(
            "👈 **Get Started:** Select an Excel file from the sidebar "
            "to view your sales analytics."
        )
        return

    try:
        # Create metrics calculator
        calculator = MetricsCalculator(state.sales_data.df)

        # Render metrics section (no header)
        render_metrics_section(calculator)

        st.divider()

        # Render top products section (no header)
        render_top_products_section(calculator)

        st.divider()

        # Render charts section (no header)
        render_charts_section(calculator)

    except Exception as e:
        error_msg = format_error_message(e, "rendering dashboard")
        st.error(f"❌ {error_msg}")
        log_error(logger, error_msg)


# ============================================================================
# Main Application
# ============================================================================


def main() -> None:
    """
    Main application entry point.

    Orchestrates the dashboard workflow:
    1. Initialize session state
    2. Display title and description
    3. Scan and select files
    4. Handle manual refresh
    5. Check for file modifications (polling)
    6. Load data if needed
    7. Render dashboard content

    Requirements:
        - 8.1: Set page configuration, initialize session state, add title
        - All sub-tasks 9.1-9.6
    """
    # Initialize session state
    initialize_session_state()
    state = st.session_state.dashboard_state

    # Title moved to sidebar - no title in main area

    # Initialize components
    file_scanner = FileScanner(directory=OUTPUT_DIR)
    excel_loader = ExcelLoader()

    # Scan and select file (Sub-task 9.2)
    scan_and_select_file(file_scanner, state)

    # Handle manual refresh (Sub-task 9.4)
    handle_manual_refresh(state)

    # Check for file modifications (Sub-task 9.5)
    check_file_modifications(file_scanner, state)

    # Load data if needed (Sub-task 9.3)
    load_data(excel_loader, state)

    # Render dashboard content (Sub-task 9.6)
    render_dashboard_content(state)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
