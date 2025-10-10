"""
Sidebar UI component for the sales dashboard.

This module provides the sidebar rendering functionality including
file selection, refresh controls, and status display.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import streamlit as st

from .config import LOG_EMOJI_LOADING, LOG_EMOJI_SUCCESS, LOG_EMOJI_WARNING
from .utils import format_datetime

logger = logging.getLogger(__name__)


def render_sidebar(
    available_files: List[Path],
    current_file: Optional[Path],
    last_update: Optional[datetime],
    success_message: Optional[str] = None
) -> Tuple[Optional[Path], bool]:
    """
    Render sidebar with file selector, refresh button, and status.

    This function creates the sidebar UI with:
    - File selection dropdown
    - Refresh data button
    - Latest update timestamp
    - Currently selected filename
    - Success message (if provided)

    Args:
        available_files: List of available Excel files to select from
        current_file: Currently selected file path (if any)
        last_update: Timestamp of last data update (if any)
        success_message: Success message to display (if any)

    Returns:
        Tuple of (selected_file, refresh_clicked) where:
            - selected_file: Path to selected file or None
            - refresh_clicked: True if refresh button was clicked

    Requirements:
        - 5.2: File selector dropdown
        - 5.3: File selection triggers data load
        - 6.3: Manual refresh button
        - 6.4: Refresh updates data and timestamp
        - 7.1: Display latest update timestamp
        - 7.2: Use readable timestamp format
        - 7.4: Show current filename
        - 8.1-8.5: Sidebar organization and labels
    """
    with st.sidebar:
        # Dashboard title at top of sidebar
        st.title("📊 Sales Analytics Dashboard")
        st.divider()
        
        st.header("📁 Data Selection")

        # File selector dropdown
        selected_file = _render_file_selector(available_files, current_file)

        st.divider()

        # Refresh button
        st.header("🔄 Controls")
        refresh_clicked = st.button(
            "Refresh Data",
            use_container_width=True,
            type="primary",
            help="Reload the currently selected file"
        )

        st.divider()

        # Status section
        st.header("ℹ️ Status")
        
        # Display success message if provided
        if success_message:
            st.success(success_message)
        
        _render_status_section(current_file, last_update)

        logger.debug(
            f"{LOG_EMOJI_LOADING} Sidebar rendered - "
            f"Selected: {selected_file}, Refresh: {refresh_clicked}"
        )

        return selected_file, refresh_clicked


def _render_file_selector(
    available_files: List[Path],
    current_file: Optional[Path]
) -> Optional[Path]:
    """
    Render file selection dropdown.

    Args:
        available_files: List of available Excel files
        current_file: Currently selected file

    Returns:
        Selected file path or None if no files available
    """
    if not available_files:
        st.warning("No Excel files found in output directory")
        st.info(
            "📝 Please add .xlsx files to the 'output' folder "
            "to get started."
        )
        return None

    # Create display names (filename only)
    file_names = [f.name for f in available_files]

    # Determine default index
    default_index = 0
    if current_file and current_file in available_files:
        default_index = available_files.index(current_file)

    # Render selectbox
    selected_name = st.selectbox(
        "Select Data File",
        options=file_names,
        index=default_index,
        help="Choose an Excel file to analyze"
    )

    # Find corresponding Path object
    selected_file = None
    for file_path in available_files:
        if file_path.name == selected_name:
            selected_file = file_path
            break

    return selected_file


def _render_status_section(
    current_file: Optional[Path],
    last_update: Optional[datetime]
) -> None:
    """
    Render status information section.

    Args:
        current_file: Currently selected file
        last_update: Timestamp of last update
    """
    # Display last update timestamp with smaller font
    if last_update:
        formatted_time = format_datetime(last_update)
        st.caption(f"Latest Update: {formatted_time}")
        logger.debug(
            f"{LOG_EMOJI_SUCCESS} Status displayed - "
            f"Last update: {last_update}"
        )
    else:
        st.caption("No data loaded yet")


def render_file_metadata(
    filepath: Path,
    show_size: bool = True,
    show_modified: bool = True
) -> None:
    """
    Render file metadata information.

    This function displays file size and last modified time
    for the given file path.

    Args:
        filepath: Path to file
        show_size: Whether to display file size (default: True)
        show_modified: Whether to display last modified time (default: True)

    Requirements:
        - 7.5: Show file metadata
        - 9.3: Display file information
    """
    if not filepath.exists():
        st.warning(f"File not found: {filepath.name}")
        return

    st.subheader("📄 File Information")

    # Get file stats
    file_stats = filepath.stat()

    # Display file size
    if show_size:
        size_bytes = file_stats.st_size
        size_mb = size_bytes / (1024 * 1024)

        if size_mb < 1:
            size_kb = size_bytes / 1024
            size_str = f"{size_kb:.2f} KB"
        else:
            size_str = f"{size_mb:.2f} MB"

        st.metric(label="File Size", value=size_str)

    # Display last modified time
    if show_modified:
        modified_timestamp = datetime.fromtimestamp(file_stats.st_mtime)
        st.metric(
            label="Last Modified",
            value=format_datetime(modified_timestamp)
        )

    logger.debug(
        f"{LOG_EMOJI_LOADING} File metadata displayed for "
        f"{filepath.name}"
    )


def render_loading_indicator(message: str = "Loading data...") -> None:
    """
    Display loading spinner with message.

    Args:
        message: Loading message to display

    Requirements:
        - 7.5: Loading spinner during data load
        - 9.3: Loading indicators
    """
    with st.spinner(message):
        logger.info(f"{LOG_EMOJI_LOADING} {message}")


def render_success_indicator(message: str) -> None:
    """
    Display success message.

    Args:
        message: Success message to display

    Requirements:
        - 7.5: Success indicators
        - 9.3: Status feedback
    """
    st.success(f"✅ {message}")
    logger.info(f"{LOG_EMOJI_SUCCESS} {message}")


def render_error_indicator(message: str) -> None:
    """
    Display error message.

    Args:
        message: Error message to display

    Requirements:
        - 7.5: Error indicators
        - 9.3: Error feedback
    """
    st.error(f"❌ {message}")
    logger.error(f"❌ {message}")


def render_warning_indicator(message: str) -> None:
    """
    Display warning message.

    Args:
        message: Warning message to display

    Requirements:
        - 7.5: Warning indicators
        - 9.3: Warning feedback
    """
    st.warning(f"{LOG_EMOJI_WARNING} {message}")
    logger.warning(f"{LOG_EMOJI_WARNING} {message}")
