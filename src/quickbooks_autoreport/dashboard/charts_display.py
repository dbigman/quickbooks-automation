"""
Charts display UI component for the sales dashboard.

This module provides the render_charts_section function for displaying
interactive charts in the Streamlit dashboard.
"""

import logging

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .charts import ChartGenerator
from .metrics import MetricsCalculator
from .config import (
    LOG_EMOJI_PROCESSING,
    LOG_EMOJI_SUCCESS,
    LOG_EMOJI_ERROR,
)

logger = logging.getLogger(__name__)


def render_charts_section(calculator: MetricsCalculator) -> None:
    """
    Render charts section with weekly revenue and units trends.

    Creates and displays two line charts:
    1. Weekly revenue trend (Sales_Amount by weekday)
    2. Weekly units movement (Sales_Qty by weekday)

    Charts include:
    - Chronologically ordered weekdays (Monday-Sunday)
    - Appropriate y-axis scaling
    - Interactive hover tooltips
    - Zoom and pan capabilities
    - Responsive design

    Args:
        calculator: MetricsCalculator instance with loaded sales data

    Requirements:
        - 3.1: Line chart with weekday names on x-axis
        - 3.2: Sum Sales_Amount for each weekday
        - 3.3: Chronological weekday ordering (Monday-Sunday)
        - 3.4: Clear labels, gridlines, appropriate scaling
        - 4.1: Line chart with weekday names on x-axis
        - 4.2: Sum Sales_Qty for each weekday
        - 4.3: Chronological weekday ordering (Monday-Sunday)
        - 4.4: Clear labels, gridlines, appropriate scaling
        - 10.4: Responsive charts
    """
    logger.info(f"{LOG_EMOJI_PROCESSING} Rendering charts section")

    try:
        # Get weekday aggregations
        revenue_by_weekday = calculator.aggregate_by_weekday(
            value_column="Sales_Amount", weekday_column="Weekday"
        )

        units_by_weekday = calculator.aggregate_by_weekday(
            value_column="Sales_Qty", weekday_column="Weekday"
        )

        # Filter for Monday-Friday only
        weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        if not revenue_by_weekday.empty:
            revenue_by_weekday = revenue_by_weekday[
                revenue_by_weekday['Weekday'].isin(weekdays_order)
            ]
        
        if not units_by_weekday.empty:
            units_by_weekday = units_by_weekday[
                units_by_weekday['Weekday'].isin(weekdays_order)
            ]

        # Check if data is available
        if revenue_by_weekday.empty and units_by_weekday.empty:
            st.info(
                "📊 No weekly trend data available. Ensure your data "
                "includes weekday information for Monday-Friday."
            )
            logger.warning(
                f"{LOG_EMOJI_ERROR} No weekday data available for charts"
            )
            return

        # Render charts side by side using columns
        col1, col2 = st.columns(2)
        
        with col1:
            if not revenue_by_weekday.empty:
                _render_revenue_trend_chart(revenue_by_weekday)
            else:
                st.warning("⚠️ No revenue data available for weekly trend")
        
        with col2:
            if not units_by_weekday.empty:
                _render_units_trend_chart(units_by_weekday)
            else:
                st.warning("⚠️ No units data available for weekly trend")

        logger.info(
            f"{LOG_EMOJI_SUCCESS} Charts section rendered successfully"
        )

    except Exception as e:
        error_msg = f"Error rendering charts section: {str(e)}"
        logger.error(f"{LOG_EMOJI_ERROR} {error_msg}", exc_info=True)
        st.error(f"❌ {error_msg}")


def _render_revenue_trend_chart(data: pd.DataFrame) -> None:
    """
    Render weekly revenue trend line chart.

    Args:
        data: DataFrame with 'Weekday' and 'Sales_Amount' columns
    """

    # Create chart configuration
    chart_config = ChartGenerator.create_weekday_line_chart(
        data=data,
        x_column="Weekday",
        y_column="Sales_Amount",
        title="Revenue by Weekday",
        y_label="Revenue ($)",
    )

    # Create Plotly figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_config["data"]["Weekday"],
            y=chart_config["data"]["Sales_Amount"],
            mode="lines+markers",
            name="Revenue",
            line=dict(
                color=chart_config["color"],
                width=3,
                shape=chart_config["line_shape"],
            ),
            marker=dict(
                size=8,
                color=chart_config["color"],
                line=dict(color="white", width=2),
            ),
            hovertemplate=(
                "<b>%{x}</b><br>" "Revenue: $%{y:,.2f}<br>" "<extra></extra>"
            ),
        )
    )

    # Configure layout
    fig.update_layout(
        title=dict(
            text=chart_config["title"], font=dict(size=18, color="#333333")
        ),
        xaxis=dict(
            title=dict(text="Day of Week", font=dict(size=14)),
            showgrid=True,
            gridcolor="#E5E5E5",
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text=chart_config["y_label"], font=dict(size=14)),
            showgrid=True,
            gridcolor="#E5E5E5",
            zeroline=False,
            tickformat="$,.0f",
        ),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=400,
        margin=dict(l=60, r=40, t=60, b=60),
        showlegend=False,
    )

    # Display chart with full width
    st.plotly_chart(fig, use_container_width=True)

    logger.debug("Revenue trend chart rendered")


def _render_units_trend_chart(data: pd.DataFrame) -> None:
    """
    Render weekly units movement line chart.

    Args:
        data: DataFrame with 'Weekday' and 'Sales_Qty' columns
    """

    # Create chart configuration
    chart_config = ChartGenerator.create_weekday_line_chart(
        data=data,
        x_column="Weekday",
        y_column="Sales_Qty",
        title="Units Sold by Weekday",
        y_label="Units",
    )

    # Create Plotly figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_config["data"]["Weekday"],
            y=chart_config["data"]["Sales_Qty"],
            mode="lines+markers",
            name="Units",
            line=dict(
                color="#2ca02c",  # Green color for units
                width=3,
                shape=chart_config["line_shape"],
            ),
            marker=dict(
                size=8, color="#2ca02c", line=dict(color="white", width=2)
            ),
            hovertemplate=(
                "<b>%{x}</b><br>" "Units: %{y:,.0f}<br>" "<extra></extra>"
            ),
        )
    )

    # Configure layout
    fig.update_layout(
        title=dict(
            text=chart_config["title"], font=dict(size=18, color="#333333")
        ),
        xaxis=dict(
            title=dict(text="Day of Week", font=dict(size=14)),
            showgrid=True,
            gridcolor="#E5E5E5",
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text=chart_config["y_label"], font=dict(size=14)),
            showgrid=True,
            gridcolor="#E5E5E5",
            zeroline=False,
            tickformat=",.0f",
        ),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=400,
        margin=dict(l=60, r=40, t=60, b=60),
        showlegend=False,
    )

    # Display chart with full width
    st.plotly_chart(fig, use_container_width=True)

    logger.debug("Units trend chart rendered")
