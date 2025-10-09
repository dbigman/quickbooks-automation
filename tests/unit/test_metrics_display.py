"""
Unit tests for metrics display UI component.

Tests the render_metrics_section and render_top_products_section functions
for proper display of metrics and charts.
"""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.quickbooks_autoreport.dashboard.metrics import MetricsCalculator
from src.quickbooks_autoreport.dashboard.metrics_display import (
    _render_revenue_chart,
    _render_units_chart,
    render_metrics_section,
    render_top_products_section,
)


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def sample_sales_data():
    """Create sample sales data for testing."""
    return pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        'Transaction_Total': [1000.0, 800.0, 600.0, 400.0, 200.0],
        'Sales_Amount': [900.0, 700.0, 500.0, 300.0, 100.0],
        'Sales_Qty': [50, 40, 30, 20, 10],
        'Weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    })


@pytest.fixture
def calculator(sample_sales_data):
    """Create MetricsCalculator instance with sample data."""
    return MetricsCalculator(sample_sales_data)


@pytest.fixture
def empty_calculator():
    """Create MetricsCalculator instance with empty data."""
    empty_df = pd.DataFrame(columns=[
        'Product', 'Transaction_Total', 'Sales_Amount', 'Sales_Qty'
    ])
    return MetricsCalculator(empty_df)


# ============================================================================
# Metrics Section Tests
# ============================================================================


class TestRenderMetricsSection:
    """Tests for render_metrics_section function."""

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    def test_render_metrics_section_basic(self, mock_st, calculator):
        """Test basic metrics section rendering."""
        # Mock st.columns to return mock column contexts
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        # Call function
        render_metrics_section(calculator)

        # Verify st.columns was called
        mock_st.columns.assert_called_once_with(2)

        # Verify metric calls were made
        assert mock_st.metric.call_count == 2

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    def test_render_metrics_section_formats_currency(self, mock_st, calculator):
        """Test that revenue is formatted as currency."""
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        render_metrics_section(calculator)

        # Check that metric was called with formatted currency
        calls = mock_st.metric.call_args_list
        revenue_call = calls[0]

        assert revenue_call[1]['label'] == "💰 Sales Revenue"
        assert '$' in revenue_call[1]['value']
        assert ',' in revenue_call[1]['value']  # Thousand separator

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    def test_render_metrics_section_formats_units(self, mock_st, calculator):
        """Test that units are formatted with thousand separators."""
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        render_metrics_section(calculator)

        # Check that metric was called with formatted units
        calls = mock_st.metric.call_args_list
        units_call = calls[1]

        assert units_call[1]['label'] == "📦 Units Sold"
        # Units should be formatted as integer with commas
        assert ',' in units_call[1]['value'] or units_call[1]['value'].isdigit()

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    def test_render_metrics_section_with_zero_values(self, mock_st, empty_calculator):
        """Test metrics section with zero values."""
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        render_metrics_section(empty_calculator)

        # Should still render metrics with zero values
        assert mock_st.metric.call_count == 2

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    def test_render_metrics_section_custom_top_n(self, mock_st, calculator):
        """Test metrics section with custom top_n parameter."""
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        # Should not raise error with custom top_n
        render_metrics_section(calculator, top_n=3)

        assert mock_st.metric.call_count == 2


# ============================================================================
# Top Products Section Tests
# ============================================================================


class TestRenderTopProductsSection:
    """Tests for render_top_products_section function."""

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    @patch('src.quickbooks_autoreport.dashboard.metrics_display._render_revenue_chart')
    @patch('src.quickbooks_autoreport.dashboard.metrics_display._render_units_chart')
    def test_render_top_products_section_basic(
        self, mock_units_chart, mock_revenue_chart, mock_st, calculator
    ):
        """Test basic top products section rendering."""
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        render_top_products_section(calculator)

        # Verify columns created
        mock_st.columns.assert_called_once_with(2)

        # Verify subheaders called
        assert mock_st.subheader.call_count == 2

        # Verify chart rendering functions called
        mock_revenue_chart.assert_called_once()
        mock_units_chart.assert_called_once()

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    @patch('src.quickbooks_autoreport.dashboard.metrics_display._render_revenue_chart')
    @patch('src.quickbooks_autoreport.dashboard.metrics_display._render_units_chart')
    def test_render_top_products_section_custom_top_n(
        self, mock_units_chart, mock_revenue_chart, mock_st, calculator
    ):
        """Test top products section with custom top_n."""
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        render_top_products_section(calculator, top_n=3)

        # Verify subheaders show correct top_n
        calls = mock_st.subheader.call_args_list
        assert "Top 3" in calls[0][0][0]
        assert "Top 3" in calls[1][0][0]

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    @patch('src.quickbooks_autoreport.dashboard.metrics_display._render_revenue_chart')
    @patch('src.quickbooks_autoreport.dashboard.metrics_display._render_units_chart')
    def test_render_top_products_section_with_empty_data(
        self, mock_units_chart, mock_revenue_chart, mock_st, empty_calculator
    ):
        """Test top products section with empty data."""
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        render_top_products_section(empty_calculator)

        # Should still call chart rendering functions
        mock_revenue_chart.assert_called_once()
        mock_units_chart.assert_called_once()


# ============================================================================
# Revenue Chart Tests
# ============================================================================


class TestRenderRevenueChart:
    """Tests for _render_revenue_chart function."""

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    @patch('plotly.express.bar')
    def test_render_revenue_chart_with_data(self, mock_bar, mock_st):
        """Test revenue chart rendering with valid data."""
        data = pd.DataFrame({
            'Product': ['Product A', 'Product B', 'Product C'],
            'Sales_Amount': [1000.0, 800.0, 600.0]
        })

        mock_fig = MagicMock()
        mock_bar.return_value = mock_fig

        _render_revenue_chart(data)

        # Verify plotly bar chart created
        mock_bar.assert_called_once()

        # Verify chart displayed
        mock_st.plotly_chart.assert_called_once()

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    def test_render_revenue_chart_with_empty_data(self, mock_st):
        """Test revenue chart with empty data shows info message."""
        empty_data = pd.DataFrame(columns=['Product', 'Sales_Amount'])

        _render_revenue_chart(empty_data)

        # Should show info message
        mock_st.info.assert_called_once()
        assert "No revenue data available" in mock_st.info.call_args[0][0]

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    @patch('plotly.express.bar')
    def test_render_revenue_chart_handles_errors(self, mock_bar, mock_st):
        """Test revenue chart handles rendering errors gracefully."""
        data = pd.DataFrame({
            'Product': ['Product A'],
            'Sales_Amount': [1000.0]
        })

        # Simulate error in chart creation
        mock_bar.side_effect = Exception("Chart error")

        _render_revenue_chart(data)

        # Should show error message
        mock_st.error.assert_called_once()
        assert "Error rendering revenue chart" in mock_st.error.call_args[0][0]


# ============================================================================
# Units Chart Tests
# ============================================================================


class TestRenderUnitsChart:
    """Tests for _render_units_chart function."""

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    @patch('plotly.express.bar')
    def test_render_units_chart_with_data(self, mock_bar, mock_st):
        """Test units chart rendering with valid data."""
        data = pd.DataFrame({
            'Product': ['Product A', 'Product B', 'Product C'],
            'Sales_Qty': [50, 40, 30]
        })

        mock_fig = MagicMock()
        mock_bar.return_value = mock_fig

        _render_units_chart(data)

        # Verify plotly bar chart created
        mock_bar.assert_called_once()

        # Verify chart displayed
        mock_st.plotly_chart.assert_called_once()

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    def test_render_units_chart_with_empty_data(self, mock_st):
        """Test units chart with empty data shows info message."""
        empty_data = pd.DataFrame(columns=['Product', 'Sales_Qty'])

        _render_units_chart(empty_data)

        # Should show info message
        mock_st.info.assert_called_once()
        assert "No units data available" in mock_st.info.call_args[0][0]

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    @patch('plotly.express.bar')
    def test_render_units_chart_handles_errors(self, mock_bar, mock_st):
        """Test units chart handles rendering errors gracefully."""
        data = pd.DataFrame({
            'Product': ['Product A'],
            'Sales_Qty': [50]
        })

        # Simulate error in chart creation
        mock_bar.side_effect = Exception("Chart error")

        _render_units_chart(data)

        # Should show error message
        mock_st.error.assert_called_once()
        assert "Error rendering units chart" in mock_st.error.call_args[0][0]


# ============================================================================
# Integration Tests
# ============================================================================


class TestMetricsDisplayIntegration:
    """Integration tests for metrics display components."""

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    @patch('plotly.express.bar')
    def test_full_metrics_display_workflow(self, mock_bar, mock_st, calculator):
        """Test complete metrics display workflow."""
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        mock_fig = MagicMock()
        mock_bar.return_value = mock_fig

        # Render metrics section
        render_metrics_section(calculator)

        # Render top products section
        render_top_products_section(calculator)

        # Verify all components rendered
        assert mock_st.metric.call_count == 2
        assert mock_st.subheader.call_count == 2
        assert mock_bar.call_count == 2
        assert mock_st.plotly_chart.call_count == 2

    @patch('src.quickbooks_autoreport.dashboard.metrics_display.st')
    def test_metrics_display_with_missing_columns(self, mock_st):
        """Test metrics display handles missing columns gracefully."""
        # Create data with missing columns
        incomplete_df = pd.DataFrame({
            'Product': ['Product A', 'Product B'],
            'Sales_Amount': [1000.0, 800.0]
            # Missing Transaction_Total and Sales_Qty
        })

        calc = MetricsCalculator(incomplete_df)

        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        # Should not raise error
        render_metrics_section(calc)

        # Metrics should still be displayed (with zero values)
        assert mock_st.metric.call_count == 2
