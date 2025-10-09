"""
Chart generation logic for the sales dashboard.

This module provides the ChartGenerator class for creating
chart configurations for Streamlit visualization.
"""

import logging
from typing import Any, Dict

import pandas as pd

from .config import (
    WEEKDAY_ORDER,
    LOG_EMOJI_PROCESSING,
    LOG_EMOJI_ERROR,
)

logger = logging.getLogger(__name__)


class ChartGenerator:
    """
    Generates chart configurations for Streamlit visualization.

    This class provides static methods to create chart configurations
    for line charts and bar charts using Plotly-compatible formats.
    """

    @staticmethod
    def create_weekday_line_chart(
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str,
        y_label: str
    ) -> Dict[str, Any]:
        """
        Create line chart configuration for weekday trends.

        Generates a Plotly-compatible chart configuration for displaying
        trends across weekdays (Monday-Sunday).

        Args:
            data: DataFrame with weekday and value columns
            x_column: Name of column for x-axis (weekday names)
            y_column: Name of column for y-axis (values)
            title: Chart title
            y_label: Label for y-axis

        Returns:
            Dictionary containing chart configuration with:
                - data: Chart data
                - x_column: X-axis column name
                - y_column: Y-axis column name
                - title: Chart title
                - y_label: Y-axis label
                - chart_type: 'line'

        Raises:
            ValueError: If required columns are missing from data
        """
        if x_column not in data.columns:
            error_msg = f"X column '{x_column}' not found in data"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg)

        if y_column not in data.columns:
            error_msg = f"Y column '{y_column}' not found in data"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg)

        # Ensure weekday ordering
        if x_column.lower() in ['weekday', 'day', 'day_name']:
            # Create categorical with proper ordering
            data = data.copy()
            data[x_column] = pd.Categorical(
                data[x_column],
                categories=WEEKDAY_ORDER,
                ordered=True
            )
            data = data.sort_values(x_column).reset_index(drop=True)

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Created line chart config: {title}"
        )

        return {
            'data': data,
            'x_column': x_column,
            'y_column': y_column,
            'title': title,
            'y_label': y_label,
            'chart_type': 'line',
            'markers': True,
            'line_shape': 'linear',
            'color': '#1f77b4',  # Default blue
        }

    @staticmethod
    def create_bar_chart(
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str,
        orientation: str = 'h'
    ) -> Dict[str, Any]:
        """
        Create bar chart configuration for top products display.

        Generates a Plotly-compatible chart configuration for displaying
        horizontal or vertical bar charts.

        Args:
            data: DataFrame with category and value columns
            x_column: Name of column for x-axis (or y-axis if horizontal)
            y_column: Name of column for y-axis (or x-axis if horizontal)
            title: Chart title
            orientation: Chart orientation - 'h' for horizontal (default),
                        'v' for vertical

        Returns:
            Dictionary containing chart configuration with:
                - data: Chart data
                - x_column: X-axis column name
                - y_column: Y-axis column name
                - title: Chart title
                - orientation: Chart orientation
                - chart_type: 'bar'

        Raises:
            ValueError: If required columns are missing from data or
                       invalid orientation specified
        """
        if x_column not in data.columns:
            error_msg = f"X column '{x_column}' not found in data"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg)

        if y_column not in data.columns:
            error_msg = f"Y column '{y_column}' not found in data"
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg)

        if orientation not in ['h', 'v']:
            error_msg = (
                f"Invalid orientation '{orientation}'. "
                f"Must be 'h' or 'v'"
            )
            logger.error(f"{LOG_EMOJI_ERROR} {error_msg}")
            raise ValueError(error_msg)

        # For horizontal bars, reverse order so highest is on top
        if orientation == 'h':
            data = data.iloc[::-1].reset_index(drop=True)

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Created bar chart config: {title}"
        )

        return {
            'data': data,
            'x_column': x_column,
            'y_column': y_column,
            'title': title,
            'orientation': orientation,
            'chart_type': 'bar',
            'color': '#ff7f0e',  # Default orange
            'show_values': True,
        }
