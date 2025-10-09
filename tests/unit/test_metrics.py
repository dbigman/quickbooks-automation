"""Unit tests for MetricsCalculator class."""

import pandas as pd
import pytest

from quickbooks_autoreport.dashboard.metrics import MetricsCalculator


@pytest.fixture
def sample_sales_data() -> pd.DataFrame:
    """Create sample sales data for testing."""
    return pd.DataFrame({
        'Product': [
            'Product A', 'Product B', 'Product C',
            'Product A', 'Product B'
        ],
        'Transaction_Total': [100.0, 200.0, 150.0, 50.0, 75.0],
        'Sales_Amount': [90.0, 180.0, 135.0, 45.0, 67.5],
        'Sales_Qty': [10, 20, 15, 5, 7],
        'Weekday': [
            'Monday', 'Tuesday', 'Monday', 'Wednesday', 'Tuesday'
        ]
    })


@pytest.fixture
def multiweek_sales_data() -> pd.DataFrame:
    """Create multi-week sales data for testing."""
    return pd.DataFrame({
        'Product': [
            'Product A', 'Product B', 'Product A', 'Product B',
            'Product A', 'Product B', 'Product A', 'Product B'
        ],
        'Transaction_Total': [
            100.0, 200.0, 150.0, 250.0,
            120.0, 180.0, 130.0, 220.0
        ],
        'Sales_Amount': [
            90.0, 180.0, 135.0, 225.0,
            108.0, 162.0, 117.0, 198.0
        ],
        'Sales_Qty': [10, 20, 15, 25, 12, 18, 13, 22],
        'Weekday': [
            'Monday', 'Monday', 'Tuesday', 'Tuesday',
            'Monday', 'Monday', 'Tuesday', 'Tuesday'
        ]
    })


@pytest.fixture
def edge_case_data() -> pd.DataFrame:
    """Create data with edge cases (zero, negative values)."""
    return pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C', 'Product D'],
        'Transaction_Total': [100.0, 0.0, -50.0, 200.0],
        'Sales_Amount': [90.0, 0.0, -45.0, 180.0],
        'Sales_Qty': [10, 0, -5, 20],
        'Weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
    })


@pytest.fixture
def large_dataset() -> pd.DataFrame:
    """Create large dataset with many products."""
    products = [f'Product {i}' for i in range(1, 21)]
    return pd.DataFrame({
        'Product': products,
        'Transaction_Total': [float(i * 100) for i in range(1, 21)],
        'Sales_Amount': [float(i * 90) for i in range(1, 21)],
        'Sales_Qty': [i * 10 for i in range(1, 21)],
        'Weekday': ['Monday'] * 20
    })


# Revenue Calculation Tests
def test_calculate_total_revenue(sample_sales_data: pd.DataFrame) -> None:
    """Test total revenue calculation with sample data."""
    calculator = MetricsCalculator(sample_sales_data)
    total_revenue = calculator.calculate_total_revenue()
    assert total_revenue == 575.0


def test_calculate_total_revenue_empty_dataframe() -> None:
    """Test revenue calculation with empty DataFrame."""
    empty_df = pd.DataFrame(columns=['Transaction_Total'])
    calculator = MetricsCalculator(empty_df)
    total_revenue = calculator.calculate_total_revenue()
    assert total_revenue == 0.0


def test_calculate_total_revenue_missing_column() -> None:
    """Test revenue calculation when column is missing."""
    df = pd.DataFrame({'Product': ['A', 'B']})
    calculator = MetricsCalculator(df)
    total_revenue = calculator.calculate_total_revenue()
    assert total_revenue == 0.0


def test_calculate_total_revenue_with_nan() -> None:
    """Test revenue calculation with NaN values."""
    df = pd.DataFrame({
        'Transaction_Total': [100.0, None, 200.0, float('nan')]
    })
    calculator = MetricsCalculator(df)
    total_revenue = calculator.calculate_total_revenue()
    assert total_revenue == 300.0


# Units Calculation Tests
def test_calculate_total_units(sample_sales_data: pd.DataFrame) -> None:
    """Test total units calculation with sample data."""
    calculator = MetricsCalculator(sample_sales_data)
    total_units = calculator.calculate_total_units()
    assert total_units == 57


def test_calculate_total_units_with_zero(edge_case_data: pd.DataFrame) -> None:
    """Test units calculation with zero values."""
    calculator = MetricsCalculator(edge_case_data)
    total_units = calculator.calculate_total_units()
    # 10 + 0 + (-5) + 20 = 25
    assert total_units == 25


def test_calculate_total_units_with_negative(
    edge_case_data: pd.DataFrame
) -> None:
    """Test units calculation handles negative values."""
    calculator = MetricsCalculator(edge_case_data)
    total_units = calculator.calculate_total_units()
    # Should include negative values in sum
    assert total_units == 25


def test_calculate_total_units_empty_dataframe() -> None:
    """Test units calculation with empty DataFrame."""
    empty_df = pd.DataFrame(columns=['Sales_Qty'])
    calculator = MetricsCalculator(empty_df)
    total_units = calculator.calculate_total_units()
    assert total_units == 0


def test_calculate_total_units_missing_column() -> None:
    """Test units calculation when column is missing."""
    df = pd.DataFrame({'Product': ['A', 'B']})
    calculator = MetricsCalculator(df)
    total_units = calculator.calculate_total_units()
    assert total_units == 0


# Top Products by Revenue Tests
def test_get_top_products_by_revenue(sample_sales_data: pd.DataFrame) -> None:
    """Test top products by revenue with default top_n."""
    calculator = MetricsCalculator(sample_sales_data)
    top_products = calculator.get_top_products_by_revenue(top_n=2)

    assert len(top_products) == 2
    assert top_products.iloc[0]['Product'] == 'Product B'
    assert top_products.iloc[0]['Sales_Amount'] == 247.5
    assert top_products.iloc[1]['Product'] == 'Product C'


def test_get_top_products_by_revenue_large_dataset(
    large_dataset: pd.DataFrame
) -> None:
    """Test top products with dataset larger than top_n."""
    calculator = MetricsCalculator(large_dataset)
    top_products = calculator.get_top_products_by_revenue(top_n=5)

    assert len(top_products) == 5
    # Should be sorted descending
    assert top_products.iloc[0]['Product'] == 'Product 20'
    assert top_products.iloc[0]['Sales_Amount'] == 1800.0
    assert top_products.iloc[4]['Product'] == 'Product 16'


def test_get_top_products_by_revenue_small_dataset() -> None:
    """Test top products when dataset smaller than top_n."""
    df = pd.DataFrame({
        'Product': ['A', 'B'],
        'Sales_Amount': [100.0, 200.0]
    })
    calculator = MetricsCalculator(df)
    top_products = calculator.get_top_products_by_revenue(top_n=5)

    # Should return only 2 products
    assert len(top_products) == 2


def test_get_top_products_by_revenue_missing_column() -> None:
    """Test top products when required column is missing."""
    df = pd.DataFrame({'Product': ['A', 'B']})
    calculator = MetricsCalculator(df)
    top_products = calculator.get_top_products_by_revenue()

    assert len(top_products) == 0
    assert 'Product' in top_products.columns
    assert 'Sales_Amount' in top_products.columns


# Top Products by Units Tests
def test_get_top_products_by_units(sample_sales_data: pd.DataFrame) -> None:
    """Test top products by units with default top_n."""
    calculator = MetricsCalculator(sample_sales_data)
    top_products = calculator.get_top_products_by_units(top_n=2)

    assert len(top_products) == 2
    assert top_products.iloc[0]['Product'] == 'Product B'
    assert top_products.iloc[0]['Sales_Qty'] == 27


def test_get_top_products_by_units_large_dataset(
    large_dataset: pd.DataFrame
) -> None:
    """Test top products by units with large dataset."""
    calculator = MetricsCalculator(large_dataset)
    top_products = calculator.get_top_products_by_units(top_n=5)

    assert len(top_products) == 5
    # Should be sorted descending
    assert top_products.iloc[0]['Product'] == 'Product 20'
    assert top_products.iloc[0]['Sales_Qty'] == 200


def test_get_top_products_by_units_with_zero(
    edge_case_data: pd.DataFrame
) -> None:
    """Test top products by units with zero values."""
    calculator = MetricsCalculator(edge_case_data)
    top_products = calculator.get_top_products_by_units(top_n=3)

    assert len(top_products) == 3
    # Product D should be first (20 units)
    assert top_products.iloc[0]['Product'] == 'Product D'
    assert top_products.iloc[0]['Sales_Qty'] == 20


def test_get_top_products_by_units_missing_column() -> None:
    """Test top products by units when required column is missing."""
    df = pd.DataFrame({'Product': ['A', 'B']})
    calculator = MetricsCalculator(df)
    top_products = calculator.get_top_products_by_units()

    assert len(top_products) == 0
    assert 'Product' in top_products.columns
    assert 'Sales_Qty' in top_products.columns


# Weekday Aggregation Tests
def test_aggregate_by_weekday(sample_sales_data: pd.DataFrame) -> None:
    """Test weekday aggregation with single week data."""
    calculator = MetricsCalculator(sample_sales_data)
    weekday_agg = calculator.aggregate_by_weekday('Sales_Amount')

    # Should have 3 weekdays
    assert len(weekday_agg) == 3

    # Check ordering (Monday should be first)
    assert weekday_agg.iloc[0]['Weekday'] == 'Monday'
    assert weekday_agg.iloc[1]['Weekday'] == 'Tuesday'
    assert weekday_agg.iloc[2]['Weekday'] == 'Wednesday'

    # Check values
    assert weekday_agg.iloc[0]['Sales_Amount'] == 225.0  # 90 + 135


def test_aggregate_by_weekday_multiweek(
    multiweek_sales_data: pd.DataFrame
) -> None:
    """Test weekday aggregation with multi-week data."""
    calculator = MetricsCalculator(multiweek_sales_data)
    weekday_agg = calculator.aggregate_by_weekday('Sales_Amount')

    # Should have 2 weekdays (Monday and Tuesday)
    assert len(weekday_agg) == 2

    # Check ordering
    assert weekday_agg.iloc[0]['Weekday'] == 'Monday'
    assert weekday_agg.iloc[1]['Weekday'] == 'Tuesday'

    # Check aggregated values across multiple weeks
    # Monday: 90 + 180 + 108 + 162 = 540
    assert weekday_agg.iloc[0]['Sales_Amount'] == 540.0
    # Tuesday: 135 + 225 + 117 + 198 = 675
    assert weekday_agg.iloc[1]['Sales_Amount'] == 675.0


def test_aggregate_by_weekday_units(
    multiweek_sales_data: pd.DataFrame
) -> None:
    """Test weekday aggregation with units column."""
    calculator = MetricsCalculator(multiweek_sales_data)
    weekday_agg = calculator.aggregate_by_weekday('Sales_Qty')

    # Monday: 10 + 20 + 12 + 18 = 60
    assert weekday_agg.iloc[0]['Sales_Qty'] == 60
    # Tuesday: 15 + 25 + 13 + 22 = 75
    assert weekday_agg.iloc[1]['Sales_Qty'] == 75


def test_aggregate_by_weekday_chronological_order() -> None:
    """Test weekday aggregation maintains chronological order."""
    df = pd.DataFrame({
        'Sales_Amount': [100, 200, 150, 175, 125, 180, 160],
        'Weekday': [
            'Sunday', 'Wednesday', 'Monday',
            'Friday', 'Tuesday', 'Saturday', 'Thursday'
        ]
    })
    calculator = MetricsCalculator(df)
    weekday_agg = calculator.aggregate_by_weekday('Sales_Amount')

    # Should be ordered Monday through Sunday
    expected_order = [
        'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]
    actual_order = weekday_agg['Weekday'].tolist()
    assert actual_order == expected_order


def test_aggregate_by_weekday_missing_value_column() -> None:
    """Test weekday aggregation when value column is missing."""
    df = pd.DataFrame({'Weekday': ['Monday', 'Tuesday']})
    calculator = MetricsCalculator(df)
    weekday_agg = calculator.aggregate_by_weekday('Sales_Amount')

    assert len(weekday_agg) == 0
    assert 'Weekday' in weekday_agg.columns
    assert 'Sales_Amount' in weekday_agg.columns


def test_aggregate_by_weekday_missing_weekday_column() -> None:
    """Test weekday aggregation when weekday column is missing."""
    df = pd.DataFrame({'Sales_Amount': [100, 200]})
    calculator = MetricsCalculator(df)
    weekday_agg = calculator.aggregate_by_weekday('Sales_Amount')

    assert len(weekday_agg) == 0
    assert 'Weekday' in weekday_agg.columns
    assert 'Sales_Amount' in weekday_agg.columns
