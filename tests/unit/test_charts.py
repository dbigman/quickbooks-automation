"""Unit tests for ChartGenerator class."""

import pandas as pd
import pytest

from quickbooks_autoreport.dashboard.charts import ChartGenerator


@pytest.fixture
def sample_weekday_data():
    """Create sample weekday data for testing."""
    return pd.DataFrame({
        'Weekday': ['Monday', 'Tuesday', 'Wednesday'],
        'Sales_Amount': [100.0, 200.0, 150.0]
    })


@pytest.fixture
def sample_product_data():
    """Create sample product data for testing."""
    return pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C'],
        'Sales_Amount': [500.0, 300.0, 200.0]
    })


def test_create_weekday_line_chart(sample_weekday_data):
    """Test weekday line chart creation."""
    chart_config = ChartGenerator.create_weekday_line_chart(
        data=sample_weekday_data,
        x_column='Weekday',
        y_column='Sales_Amount',
        title='Weekly Revenue',
        y_label='Revenue ($)'
    )
    
    assert chart_config['chart_type'] == 'line'
    assert chart_config['title'] == 'Weekly Revenue'
    assert chart_config['x_column'] == 'Weekday'
    assert chart_config['y_column'] == 'Sales_Amount'
    assert chart_config['y_label'] == 'Revenue ($)'
    assert 'data' in chart_config


def test_create_bar_chart_horizontal(sample_product_data):
    """Test horizontal bar chart creation."""
    chart_config = ChartGenerator.create_bar_chart(
        data=sample_product_data,
        x_column='Sales_Amount',
        y_column='Product',
        title='Top Products',
        orientation='h'
    )
    
    assert chart_config['chart_type'] == 'bar'
    assert chart_config['orientation'] == 'h'
    assert chart_config['title'] == 'Top Products'
    assert 'data' in chart_config


def test_create_bar_chart_vertical(sample_product_data):
    """Test vertical bar chart creation."""
    chart_config = ChartGenerator.create_bar_chart(
        data=sample_product_data,
        x_column='Product',
        y_column='Sales_Amount',
        title='Top Products',
        orientation='v'
    )
    
    assert chart_config['chart_type'] == 'bar'
    assert chart_config['orientation'] == 'v'


def test_create_line_chart_missing_column(sample_weekday_data):
    """Test line chart with missing column raises error."""
    with pytest.raises(ValueError, match="not found in data"):
        ChartGenerator.create_weekday_line_chart(
            data=sample_weekday_data,
            x_column='InvalidColumn',
            y_column='Sales_Amount',
            title='Test',
            y_label='Test'
        )


def test_create_bar_chart_invalid_orientation(sample_product_data):
    """Test bar chart with invalid orientation raises error."""
    with pytest.raises(ValueError, match="Invalid orientation"):
        ChartGenerator.create_bar_chart(
            data=sample_product_data,
            x_column='Product',
            y_column='Sales_Amount',
            title='Test',
            orientation='invalid'
        )


# Additional comprehensive tests for task 4.4


def test_line_chart_configuration_complete():
    """Test that line chart configuration contains all required fields."""
    data = pd.DataFrame({
        'Weekday': ['Monday', 'Tuesday'],
        'Revenue': [100.0, 200.0]
    })
    
    config = ChartGenerator.create_weekday_line_chart(
        data=data,
        x_column='Weekday',
        y_column='Revenue',
        title='Test Chart',
        y_label='Amount'
    )
    
    # Verify all expected configuration fields are present
    assert 'data' in config
    assert 'x_column' in config
    assert 'y_column' in config
    assert 'title' in config
    assert 'y_label' in config
    assert 'chart_type' in config
    assert 'markers' in config
    assert 'line_shape' in config
    assert 'color' in config
    
    # Verify field values
    assert config['chart_type'] == 'line'
    assert config['markers'] is True
    assert config['line_shape'] == 'linear'
    assert config['color'] == '#1f77b4'


def test_bar_chart_configuration_complete():
    """Test that bar chart configuration contains all required fields."""
    data = pd.DataFrame({
        'Product': ['A', 'B'],
        'Sales': [100.0, 200.0]
    })
    
    config = ChartGenerator.create_bar_chart(
        data=data,
        x_column='Sales',
        y_column='Product',
        title='Test Bar Chart',
        orientation='h'
    )
    
    # Verify all expected configuration fields are present
    assert 'data' in config
    assert 'x_column' in config
    assert 'y_column' in config
    assert 'title' in config
    assert 'orientation' in config
    assert 'chart_type' in config
    assert 'color' in config
    assert 'show_values' in config
    
    # Verify field values
    assert config['chart_type'] == 'bar'
    assert config['orientation'] == 'h'
    assert config['color'] == '#ff7f0e'
    assert config['show_values'] is True


def test_horizontal_bar_data_reversal():
    """Test that horizontal bar chart reverses data order (highest on top)."""
    data = pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C'],
        'Sales': [100.0, 200.0, 300.0]
    })
    
    config = ChartGenerator.create_bar_chart(
        data=data,
        x_column='Sales',
        y_column='Product',
        title='Top Products',
        orientation='h'
    )
    
    # Verify data is reversed (highest value should be first)
    result_data = config['data']
    assert result_data.iloc[0]['Product'] == 'Product C'
    assert result_data.iloc[1]['Product'] == 'Product B'
    assert result_data.iloc[2]['Product'] == 'Product A'
    assert result_data.iloc[0]['Sales'] == 300.0


def test_vertical_bar_data_not_reversed():
    """Test that vertical bar chart does not reverse data order."""
    data = pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C'],
        'Sales': [100.0, 200.0, 300.0]
    })
    
    config = ChartGenerator.create_bar_chart(
        data=data,
        x_column='Product',
        y_column='Sales',
        title='Top Products',
        orientation='v'
    )
    
    # Verify data is NOT reversed (original order maintained)
    result_data = config['data']
    assert result_data.iloc[0]['Product'] == 'Product A'
    assert result_data.iloc[1]['Product'] == 'Product B'
    assert result_data.iloc[2]['Product'] == 'Product C'


def test_weekday_ordering_chronological():
    """Test that weekday data is ordered chronologically (Monday-Sunday)."""
    # Create data in random order
    data = pd.DataFrame({
        'Weekday': ['Friday', 'Monday', 'Wednesday', 'Sunday', 'Tuesday'],
        'Sales': [500.0, 100.0, 300.0, 700.0, 200.0]
    })
    
    config = ChartGenerator.create_weekday_line_chart(
        data=data,
        x_column='Weekday',
        y_column='Sales',
        title='Weekly Sales',
        y_label='Sales ($)'
    )
    
    # Verify weekdays are in chronological order
    result_data = config['data']
    weekdays = result_data['Weekday'].tolist()
    
    assert weekdays == ['Monday', 'Tuesday', 'Wednesday', 'Friday', 'Sunday']
    
    # Verify corresponding sales values are correctly mapped
    assert result_data.iloc[0]['Sales'] == 100.0  # Monday
    assert result_data.iloc[1]['Sales'] == 200.0  # Tuesday
    assert result_data.iloc[2]['Sales'] == 300.0  # Wednesday
    assert result_data.iloc[3]['Sales'] == 500.0  # Friday
    assert result_data.iloc[4]['Sales'] == 700.0  # Sunday


def test_weekday_ordering_with_all_days():
    """Test weekday ordering with complete week (Monday-Sunday)."""
    data = pd.DataFrame({
        'Weekday': [
            'Sunday', 'Saturday', 'Friday', 'Thursday',
            'Wednesday', 'Tuesday', 'Monday'
        ],
        'Revenue': [700.0, 600.0, 500.0, 400.0, 300.0, 200.0, 100.0]
    })
    
    config = ChartGenerator.create_weekday_line_chart(
        data=data,
        x_column='Weekday',
        y_column='Revenue',
        title='Weekly Revenue',
        y_label='Revenue ($)'
    )
    
    result_data = config['data']
    weekdays = result_data['Weekday'].tolist()
    
    # Verify complete chronological order
    expected_order = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'
    ]
    assert weekdays == expected_order
    
    # Verify values are correctly mapped
    assert result_data.iloc[0]['Revenue'] == 100.0  # Monday
    assert result_data.iloc[6]['Revenue'] == 700.0  # Sunday


def test_weekday_ordering_case_insensitive_column():
    """Test weekday ordering works with different column name cases."""
    # Test with 'day' column name (lowercase)
    data = pd.DataFrame({
        'day': ['Friday', 'Monday', 'Wednesday'],
        'Units': [50, 10, 30]
    })
    
    config = ChartGenerator.create_weekday_line_chart(
        data=data,
        x_column='day',
        y_column='Units',
        title='Weekly Units',
        y_label='Units'
    )
    
    result_data = config['data']
    days = result_data['day'].tolist()
    
    assert days == ['Monday', 'Wednesday', 'Friday']


def test_non_weekday_column_no_reordering():
    """Test that non-weekday columns are not reordered."""
    data = pd.DataFrame({
        'Category': ['Z', 'A', 'M'],
        'Value': [100.0, 200.0, 300.0]
    })
    
    config = ChartGenerator.create_weekday_line_chart(
        data=data,
        x_column='Category',
        y_column='Value',
        title='Category Chart',
        y_label='Value'
    )
    
    # Verify original order is maintained (no weekday reordering)
    result_data = config['data']
    categories = result_data['Category'].tolist()
    assert categories == ['Z', 'A', 'M']


def test_empty_dataframe_handling():
    """Test chart generation with empty DataFrame."""
    empty_data = pd.DataFrame({
        'Weekday': [],
        'Sales': []
    })
    
    config = ChartGenerator.create_weekday_line_chart(
        data=empty_data,
        x_column='Weekday',
        y_column='Sales',
        title='Empty Chart',
        y_label='Sales'
    )
    
    # Should return valid config with empty data
    assert config['chart_type'] == 'line'
    assert len(config['data']) == 0


def test_bar_chart_missing_y_column():
    """Test bar chart with missing y column raises error."""
    data = pd.DataFrame({
        'Product': ['A', 'B'],
        'Sales': [100.0, 200.0]
    })
    
    with pytest.raises(ValueError, match="Y column 'InvalidColumn' not found"):
        ChartGenerator.create_bar_chart(
            data=data,
            x_column='Product',
            y_column='InvalidColumn',
            title='Test',
            orientation='h'
        )


def test_line_chart_missing_y_column():
    """Test line chart with missing y column raises error."""
    data = pd.DataFrame({
        'Weekday': ['Monday', 'Tuesday'],
        'Sales': [100.0, 200.0]
    })
    
    with pytest.raises(ValueError, match="Y column 'InvalidColumn' not found"):
        ChartGenerator.create_weekday_line_chart(
            data=data,
            x_column='Weekday',
            y_column='InvalidColumn',
            title='Test',
            y_label='Test'
        )
