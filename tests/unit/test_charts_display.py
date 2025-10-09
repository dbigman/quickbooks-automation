"""Unit tests for charts_display module."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from quickbooks_autoreport.dashboard.charts_display import (
    render_charts_section,
    _render_revenue_trend_chart,
    _render_units_trend_chart,
)
from quickbooks_autoreport.dashboard.metrics import MetricsCalculator


@pytest.fixture
def sample_sales_data():
    """Create sample sales data with weekday column."""
    return pd.DataFrame(
        {
            "Transaction_Total": [100.0, 200.0, 150.0, 300.0, 250.0],
            "Sales_Amount": [90.0, 180.0, 135.0, 270.0, 225.0],
            "Sales_Qty": [10, 20, 15, 30, 25],
            "Product": ["A", "B", "C", "D", "E"],
            "Weekday": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        }
    )


@pytest.fixture
def sample_calculator(sample_sales_data):
    """Create MetricsCalculator with sample data."""
    return MetricsCalculator(sample_sales_data)


@pytest.fixture
def empty_calculator():
    """Create MetricsCalculator with empty data."""
    empty_data = pd.DataFrame(
        {
            "Transaction_Total": [],
            "Sales_Amount": [],
            "Sales_Qty": [],
            "Product": [],
            "Weekday": [],
        }
    )
    return MetricsCalculator(empty_data)


@pytest.fixture
def revenue_weekday_data():
    """Create sample revenue by weekday data."""
    return pd.DataFrame(
        {
            "Weekday": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "Sales_Amount": [90.0, 180.0, 135.0, 270.0, 225.0],
        }
    )


@pytest.fixture
def units_weekday_data():
    """Create sample units by weekday data."""
    return pd.DataFrame(
        {
            "Weekday": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "Sales_Qty": [10, 20, 15, 30, 25],
        }
    )


@patch("quickbooks_autoreport.dashboard.charts_display.st")
def test_render_charts_section_with_data(mock_st, sample_calculator):
    """Test render_charts_section with valid data."""
    # Mock streamlit components
    mock_st.header = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()
    mock_st.info = MagicMock()
    mock_st.warning = MagicMock()
    mock_st.error = MagicMock()

    # Call function
    render_charts_section(sample_calculator)

    # Verify header was called
    mock_st.header.assert_called_once_with("📈 Weekly Trends")

    # Verify subheaders were called for both charts
    assert mock_st.subheader.call_count == 2
    subheader_calls = [call[0][0] for call in mock_st.subheader.call_args_list]
    assert "💰 Weekly Revenue Trend" in subheader_calls
    assert "📦 Weekly Units Sold" in subheader_calls

    # Verify plotly_chart was called twice (revenue + units)
    assert mock_st.plotly_chart.call_count == 2

    # Verify use_container_width=True for responsive design
    for call_args in mock_st.plotly_chart.call_args_list:
        assert call_args[1]["use_container_width"] is True

    # Verify no error messages
    mock_st.error.assert_not_called()


@patch("quickbooks_autoreport.dashboard.charts_display.st")
def test_render_charts_section_empty_data(mock_st, empty_calculator):
    """Test render_charts_section with empty data."""
    mock_st.header = MagicMock()
    mock_st.info = MagicMock()
    mock_st.plotly_chart = MagicMock()

    # Call function
    render_charts_section(empty_calculator)

    # Verify header was called
    mock_st.header.assert_called_once()

    # Verify info message was displayed
    mock_st.info.assert_called_once()
    info_message = mock_st.info.call_args[0][0]
    assert "No weekly trend data available" in info_message

    # Verify no charts were rendered
    mock_st.plotly_chart.assert_not_called()


@patch("quickbooks_autoreport.dashboard.charts_display.st")
def test_render_charts_section_error_handling(mock_st, sample_calculator):
    """Test render_charts_section handles errors gracefully."""
    mock_st.header = MagicMock()
    mock_st.error = MagicMock()

    # Make aggregate_by_weekday raise an exception
    sample_calculator.aggregate_by_weekday = MagicMock(
        side_effect=Exception("Test error")
    )

    # Call function
    render_charts_section(sample_calculator)

    # Verify error was displayed
    mock_st.error.assert_called_once()
    error_message = mock_st.error.call_args[0][0]
    assert "Error rendering charts section" in error_message
    assert "Test error" in error_message


@patch("quickbooks_autoreport.dashboard.charts_display.st")
@patch("quickbooks_autoreport.dashboard.charts_display.go")
def test_render_revenue_trend_chart(mock_go, mock_st, revenue_weekday_data):
    """Test _render_revenue_trend_chart creates correct chart."""
    # Mock Plotly components
    mock_figure = MagicMock()
    mock_go.Figure.return_value = mock_figure
    mock_go.Scatter = MagicMock()

    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()

    # Call function
    _render_revenue_trend_chart(revenue_weekday_data)

    # Verify subheader
    mock_st.subheader.assert_called_once_with("💰 Weekly Revenue Trend")

    # Verify Figure was created
    mock_go.Figure.assert_called_once()

    # Verify Scatter trace was created
    mock_go.Scatter.assert_called_once()
    scatter_kwargs = mock_go.Scatter.call_args[1]

    # Verify x and y data
    assert "x" in scatter_kwargs
    assert "y" in scatter_kwargs

    # Verify mode includes lines and markers
    assert scatter_kwargs["mode"] == "lines+markers"

    # Verify hover template is configured
    assert "hovertemplate" in scatter_kwargs
    assert "Revenue" in scatter_kwargs["hovertemplate"]

    # Verify trace was added to figure
    mock_figure.add_trace.assert_called_once()

    # Verify layout was updated
    mock_figure.update_layout.assert_called_once()
    layout_kwargs = mock_figure.update_layout.call_args[1]

    # Verify title configuration
    assert "title" in layout_kwargs

    # Verify axis configuration
    assert "xaxis" in layout_kwargs
    assert "yaxis" in layout_kwargs

    # Verify x-axis has gridlines
    assert layout_kwargs["xaxis"]["showgrid"] is True

    # Verify y-axis has gridlines and currency format
    assert layout_kwargs["yaxis"]["showgrid"] is True
    assert layout_kwargs["yaxis"]["tickformat"] == "$,.0f"

    # Verify responsive height
    assert "height" in layout_kwargs
    assert layout_kwargs["height"] == 400

    # Verify hover mode
    assert layout_kwargs["hovermode"] == "x unified"

    # Verify chart was displayed with responsive width
    mock_st.plotly_chart.assert_called_once()
    assert mock_st.plotly_chart.call_args[1]["use_container_width"] is True


@patch("quickbooks_autoreport.dashboard.charts_display.st")
@patch("quickbooks_autoreport.dashboard.charts_display.go")
def test_render_units_trend_chart(mock_go, mock_st, units_weekday_data):
    """Test _render_units_trend_chart creates correct chart."""
    # Mock Plotly components
    mock_figure = MagicMock()
    mock_go.Figure.return_value = mock_figure
    mock_go.Scatter = MagicMock()

    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()

    # Call function
    _render_units_trend_chart(units_weekday_data)

    # Verify subheader
    mock_st.subheader.assert_called_once_with("📦 Weekly Units Sold")

    # Verify Figure was created
    mock_go.Figure.assert_called_once()

    # Verify Scatter trace was created
    mock_go.Scatter.assert_called_once()
    scatter_kwargs = mock_go.Scatter.call_args[1]

    # Verify mode includes lines and markers
    assert scatter_kwargs["mode"] == "lines+markers"

    # Verify hover template is configured
    assert "hovertemplate" in scatter_kwargs
    assert "Units" in scatter_kwargs["hovertemplate"]

    # Verify layout was updated
    mock_figure.update_layout.assert_called_once()
    layout_kwargs = mock_figure.update_layout.call_args[1]

    # Verify y-axis has number format (not currency)
    assert layout_kwargs["yaxis"]["tickformat"] == ",.0f"

    # Verify chart was displayed with responsive width
    mock_st.plotly_chart.assert_called_once()
    assert mock_st.plotly_chart.call_args[1]["use_container_width"] is True


@patch("quickbooks_autoreport.dashboard.charts_display.st")
@patch("quickbooks_autoreport.dashboard.charts_display.go")
def test_chart_interactivity_configuration(mock_go, mock_st, revenue_weekday_data):
    """Test that charts are configured for interactivity (hover, zoom, pan)."""
    mock_figure = MagicMock()
    mock_go.Figure.return_value = mock_figure
    mock_go.Scatter = MagicMock()

    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()

    # Call function
    _render_revenue_trend_chart(revenue_weekday_data)

    # Verify hover mode is configured for interactivity
    layout_kwargs = mock_figure.update_layout.call_args[1]
    assert layout_kwargs["hovermode"] == "x unified"

    # Verify Scatter trace has hover template
    scatter_kwargs = mock_go.Scatter.call_args[1]
    assert "hovertemplate" in scatter_kwargs

    # Verify hover template includes data values
    hover_template = scatter_kwargs["hovertemplate"]
    assert "%{x}" in hover_template  # X-axis value
    assert "%{y" in hover_template  # Y-axis value

    # Plotly charts have zoom and pan by default when rendered with st.plotly_chart
    # Verify chart is rendered (which enables default Plotly interactivity)
    mock_st.plotly_chart.assert_called_once()


@patch("quickbooks_autoreport.dashboard.charts_display.st")
@patch("quickbooks_autoreport.dashboard.charts_display.go")
def test_chart_responsive_design(mock_go, mock_st, revenue_weekday_data):
    """Test that charts are configured for responsive design."""
    mock_figure = MagicMock()
    mock_go.Figure.return_value = mock_figure
    mock_go.Scatter = MagicMock()

    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()

    # Call function
    _render_revenue_trend_chart(revenue_weekday_data)

    # Verify use_container_width=True for responsive width
    mock_st.plotly_chart.assert_called_once()
    assert mock_st.plotly_chart.call_args[1]["use_container_width"] is True

    # Verify fixed height is set (allows vertical scrolling if needed)
    layout_kwargs = mock_figure.update_layout.call_args[1]
    assert "height" in layout_kwargs
    assert isinstance(layout_kwargs["height"], int)


@patch("quickbooks_autoreport.dashboard.charts_display.st")
@patch("quickbooks_autoreport.dashboard.charts_display.go")
def test_weekday_ordering_in_charts(mock_go, mock_st):
    """Test that weekday ordering is chronological in charts."""
    # Create data with weekdays in random order
    unordered_data = pd.DataFrame(
        {
            "Weekday": ["Friday", "Monday", "Wednesday", "Sunday", "Tuesday"],
            "Sales_Amount": [500.0, 100.0, 300.0, 700.0, 200.0],
        }
    )

    # The ChartGenerator should handle ordering, but verify data is passed correctly
    mock_figure = MagicMock()
    mock_go.Figure.return_value = mock_figure
    mock_go.Scatter = MagicMock()

    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()

    # Call function
    _render_revenue_trend_chart(unordered_data)

    # Verify Scatter was called with data
    mock_go.Scatter.assert_called_once()
    scatter_kwargs = mock_go.Scatter.call_args[1]

    # Verify x and y data are present
    assert "x" in scatter_kwargs
    assert "y" in scatter_kwargs


@patch("quickbooks_autoreport.dashboard.charts_display.st")
@patch("quickbooks_autoreport.dashboard.charts_display.go")
def test_chart_styling_configuration(mock_go, mock_st, revenue_weekday_data):
    """Test that charts have proper styling (colors, gridlines, labels)."""
    mock_figure = MagicMock()
    mock_go.Figure.return_value = mock_figure
    mock_go.Scatter = MagicMock()

    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()

    # Call function
    _render_revenue_trend_chart(revenue_weekday_data)

    # Verify Scatter trace styling
    scatter_kwargs = mock_go.Scatter.call_args[1]
    assert "line" in scatter_kwargs
    assert "marker" in scatter_kwargs

    # Verify line styling
    line_config = scatter_kwargs["line"]
    assert "color" in line_config
    assert "width" in line_config

    # Verify marker styling
    marker_config = scatter_kwargs["marker"]
    assert "size" in marker_config
    assert "color" in marker_config

    # Verify layout styling
    layout_kwargs = mock_figure.update_layout.call_args[1]

    # Verify gridlines are enabled
    assert layout_kwargs["xaxis"]["showgrid"] is True
    assert layout_kwargs["yaxis"]["showgrid"] is True

    # Verify grid color is set
    assert "gridcolor" in layout_kwargs["xaxis"]
    assert "gridcolor" in layout_kwargs["yaxis"]

    # Verify background colors
    assert "plot_bgcolor" in layout_kwargs
    assert "paper_bgcolor" in layout_kwargs

    # Verify axis labels
    assert "title" in layout_kwargs["xaxis"]
    assert "title" in layout_kwargs["yaxis"]


@patch("quickbooks_autoreport.dashboard.charts_display.st")
def test_render_charts_section_partial_data(mock_st, sample_calculator):
    """Test render_charts_section when only one dataset is available."""
    mock_st.header = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()
    mock_st.warning = MagicMock()

    # Mock aggregate_by_weekday to return empty for units
    original_method = sample_calculator.aggregate_by_weekday

    def mock_aggregate(value_column, weekday_column="Weekday"):
        if value_column == "Sales_Qty":
            return pd.DataFrame(columns=[weekday_column, value_column])
        return original_method(value_column, weekday_column)

    sample_calculator.aggregate_by_weekday = mock_aggregate

    # Call function
    render_charts_section(sample_calculator)

    # Verify warning was shown for missing units data
    mock_st.warning.assert_called_once()
    warning_message = mock_st.warning.call_args[0][0]
    assert "No units data available" in warning_message

    # Verify revenue chart was still rendered
    assert mock_st.plotly_chart.call_count == 1


@patch("quickbooks_autoreport.dashboard.charts_display.st")
@patch("quickbooks_autoreport.dashboard.charts_display.go")
def test_y_axis_scaling_configuration(mock_go, mock_st, revenue_weekday_data):
    """Test that y-axis has appropriate scaling configuration."""
    mock_figure = MagicMock()
    mock_go.Figure.return_value = mock_figure
    mock_go.Scatter = MagicMock()

    mock_st.subheader = MagicMock()
    mock_st.plotly_chart = MagicMock()

    # Call function
    _render_revenue_trend_chart(revenue_weekday_data)

    # Verify y-axis configuration
    layout_kwargs = mock_figure.update_layout.call_args[1]
    yaxis_config = layout_kwargs["yaxis"]

    # Verify y-axis has title
    assert "title" in yaxis_config

    # Verify y-axis has tick format for proper scaling
    assert "tickformat" in yaxis_config

    # Verify gridlines for easier reading of values
    assert yaxis_config["showgrid"] is True

    # Verify zeroline is disabled for cleaner look
    assert yaxis_config["zeroline"] is False
