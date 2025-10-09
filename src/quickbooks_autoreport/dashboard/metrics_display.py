"""
Metrics display UI component for the sales dashboard.

This module provides functions to render metrics sections including
total revenue, total units, and top products displays.
"""

import logging

import pandas as pd
import streamlit as st

from .charts import ChartGenerator
from .config import LOG_EMOJI_ERROR, LOG_EMOJI_PROCESSING, TOP_N_PRODUCTS
from .metrics import MetricsCalculator
from .utils import format_currency, format_units

logger = logging.getLogger(__name__)


def render_metrics_section(
    calculator: MetricsCalculator,
    top_n: int = TOP_N_PRODUCTS
) -> None:
    """
    Render the metrics section with revenue and units KPIs.

    Displays total revenue and total units sold as metric cards
    using st.metric with proper formatting.

    Args:
        calculator: MetricsCalculator instance with loaded data
        top_n: Number of top products to display (default from config)

    Examples:
        >>> calc = MetricsCalculator(df)
        >>> render_metrics_section(calc)  # doctest: +SKIP
    """
    logger.info(f"{LOG_EMOJI_PROCESSING} Rendering metrics section")

    # Calculate metrics
    total_revenue = calculator.calculate_total_revenue()
    total_units = calculator.calculate_total_units()

    # Display metrics in columns
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="💰 Sales Revenue",
            value=format_currency(total_revenue)
        )

    with col2:
        st.metric(
            label="📦 Units Sold",
            value=format_units(total_units)
        )

    logger.info(
        f"{LOG_EMOJI_PROCESSING} Displayed metrics: "
        f"Revenue={format_currency(total_revenue)}, "
        f"Units={format_units(total_units)}"
    )


def render_top_products_section(
    calculator: MetricsCalculator,
    top_n: int = TOP_N_PRODUCTS
) -> None:
    """
    Render top products section with horizontal bar charts.

    Displays top N products by revenue and by units sold as
    horizontal bar charts with proper formatting and labels.

    Args:
        calculator: MetricsCalculator instance with loaded data
        top_n: Number of top products to display (default from config)

    Examples:
        >>> calc = MetricsCalculator(df)
        >>> render_top_products_section(calc)  # doctest: +SKIP
    """
    logger.info(
        f"{LOG_EMOJI_PROCESSING} Rendering top products section "
        f"(top {top_n})"
    )

    # Get top products data
    top_revenue = calculator.get_top_products_by_revenue(top_n=top_n)
    top_units = calculator.get_top_products_by_units(top_n=top_n)

    # Display in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Top {top_n} Products by Revenue")
        _render_revenue_chart(top_revenue)

    with col2:
        st.subheader(f"Top {top_n} Products by Units")
        _render_units_chart(top_units)


def _render_revenue_chart(data: pd.DataFrame) -> None:
    """
    Render horizontal bar chart for top products by revenue.

    Args:
        data: DataFrame with Product and Sales_Amount columns
    """
    if data.empty:
        st.info("No revenue data available to display.")
        logger.warning(f"{LOG_EMOJI_ERROR} No revenue data for chart")
        return

    try:
        # Create chart configuration
        chart_config = ChartGenerator.create_bar_chart(
            data=data,
            x_column='Sales_Amount',
            y_column='Product_Name',
            title='',  # Title already in subheader
            orientation='h'
        )

        # Render using Plotly
        import plotly.express as px

        fig = px.bar(
            chart_config['data'],
            x=chart_config['x_column'],
            y=chart_config['y_column'],
            orientation=chart_config['orientation'],
            text=chart_config['x_column'],
            color_discrete_sequence=[chart_config['color']]
        )

        # Format text labels as currency
        fig.update_traces(
            texttemplate='$%{text:,.2f}',
            textposition='outside'
        )

        # Update layout
        fig.update_layout(
            xaxis_title="Revenue ($)",
            yaxis_title="",
            showlegend=False,
            height=300,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Rendered revenue chart "
            f"with {len(data)} products"
        )

    except Exception as e:
        st.error(f"Error rendering revenue chart: {str(e)}")
        logger.error(
            f"{LOG_EMOJI_ERROR} Failed to render revenue chart: {str(e)}"
        )


def _render_units_chart(data: pd.DataFrame) -> None:
    """
    Render horizontal bar chart for top products by units.

    Args:
        data: DataFrame with Product and Sales_Qty columns
    """
    if data.empty:
        st.info("No units data available to display.")
        logger.warning(f"{LOG_EMOJI_ERROR} No units data for chart")
        return

    try:
        # Create chart configuration
        chart_config = ChartGenerator.create_bar_chart(
            data=data,
            x_column='Sales_Qty',
            y_column='Product_Name',
            title='',  # Title already in subheader
            orientation='h'
        )

        # Render using Plotly
        import plotly.express as px

        fig = px.bar(
            chart_config['data'],
            x=chart_config['x_column'],
            y=chart_config['y_column'],
            orientation=chart_config['orientation'],
            text=chart_config['x_column'],
            color_discrete_sequence=[chart_config['color']]
        )

        # Format text labels as integers with commas
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )

        # Update layout
        fig.update_layout(
            xaxis_title="Units Sold",
            yaxis_title="",
            showlegend=False,
            height=300,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Rendered units chart "
            f"with {len(data)} products"
        )

    except Exception as e:
        st.error(f"Error rendering units chart: {str(e)}")
        logger.error(
            f"{LOG_EMOJI_ERROR} Failed to render units chart: {str(e)}"
        )
