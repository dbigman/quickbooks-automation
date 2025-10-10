"""
Metrics calculation logic for the sales dashboard.

This module provides the MetricsCalculator class for computing
sales metrics, aggregations, and top product rankings.
"""

import logging

import pandas as pd

from .config import (
    TOP_N_PRODUCTS,
    WEEKDAY_ORDER,
    LOG_EMOJI_PROCESSING,
    LOG_EMOJI_ERROR,
)

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """
    Calculates sales metrics and aggregations from sales data.

    This class provides methods to compute revenue, units sold,
    top products, and weekday aggregations.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize MetricsCalculator with sales data.

        Note: Numeric columns are expected to be pre-converted by
        ExcelLoader for optimal performance. This avoids redundant
        type conversions.

        Args:
            df: pandas DataFrame containing sales data with required columns
                and pre-converted numeric types

        Requirements:
            - 10.1: Efficient data processing
            - 10.3: Optimize pandas operations
            - 10.5: Use efficient groupby operations
        """
        # Use copy to avoid modifying original DataFrame
        self.df = df.copy()
        logger.info(
            f"{LOG_EMOJI_PROCESSING} MetricsCalculator initialized "
            f"with {len(self.df)} rows"
        )

    def calculate_total_revenue(self) -> float:
        """
        Calculate total sales revenue.

        Sums the Transaction_Total column to compute total revenue.

        Returns:
            Total revenue as float. Returns 0.0 if column missing or empty.
        """
        if 'Transaction_Total' not in self.df.columns:
            logger.warning(
                f"{LOG_EMOJI_ERROR} Transaction_Total column not found"
            )
            return 0.0

        total = self.df['Transaction_Total'].sum()

        # Handle NaN result
        if pd.isna(total):
            total = 0.0

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Calculated total revenue: ${total:,.2f}"
        )
        return float(total)

    def calculate_total_units(self) -> int:
        """
        Calculate total units sold.

        Sums the Sales_Qty column to compute total units.

        Returns:
            Total units as integer. Returns 0 if column missing or empty.
        """
        if 'Sales_Qty' not in self.df.columns:
            logger.warning(
                f"{LOG_EMOJI_ERROR} Sales_Qty column not found"
            )
            return 0

        total = self.df['Sales_Qty'].sum()

        # Handle NaN result
        if pd.isna(total):
            total = 0

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Calculated total units: {int(total):,}"
        )
        return int(total)

    def get_top_products_by_revenue(
        self,
        top_n: int = TOP_N_PRODUCTS,
        product_column: str = 'Product_Name'
    ) -> pd.DataFrame:
        """
        Get top N products by revenue.

        Aggregates sales by product and returns top N sorted by total revenue.

        Args:
            top_n: Number of top products to return (default from config)
            product_column: Name of product column (default: 'Product_Name')

        Returns:
            DataFrame with columns [product_column, 'Sales_Amount']
            sorted by revenue descending. Returns empty DataFrame if
            required columns missing.
        """
        if 'Sales_Amount' not in self.df.columns:
            logger.warning(
                f"{LOG_EMOJI_ERROR} Sales_Amount column not found"
            )
            return pd.DataFrame(columns=[product_column, 'Sales_Amount'])

        if product_column not in self.df.columns:
            logger.warning(
                f"{LOG_EMOJI_ERROR} Product column '{product_column}' "
                f"not found"
            )
            return pd.DataFrame(columns=[product_column, 'Sales_Amount'])

        # Aggregate by product and sum revenue
        product_revenue = (
            self.df.groupby(product_column)['Sales_Amount']
            .sum()
            .reset_index()
            .sort_values('Sales_Amount', ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Retrieved top {top_n} products "
            f"by revenue"
        )
        return product_revenue

    def get_top_products_by_units(
        self,
        top_n: int = TOP_N_PRODUCTS,
        product_column: str = 'Product_Name'
    ) -> pd.DataFrame:
        """
        Get top N products by units sold.

        Aggregates sales by product and returns top N sorted by total units.

        Args:
            top_n: Number of top products to return (default from config)
            product_column: Name of product column (default: 'Product_Name')

        Returns:
            DataFrame with columns [product_column, 'Sales_Qty']
            sorted by units descending. Returns empty DataFrame if
            required columns missing.
        """
        if 'Sales_Qty' not in self.df.columns:
            logger.warning(
                f"{LOG_EMOJI_ERROR} Sales_Qty column not found"
            )
            return pd.DataFrame(columns=[product_column, 'Sales_Qty'])

        if product_column not in self.df.columns:
            logger.warning(
                f"{LOG_EMOJI_ERROR} Product column '{product_column}' "
                f"not found"
            )
            return pd.DataFrame(columns=[product_column, 'Sales_Qty'])

        # Aggregate by product and sum units
        product_units = (
            self.df.groupby(product_column)['Sales_Qty']
            .sum()
            .reset_index()
            .sort_values('Sales_Qty', ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Retrieved top {top_n} products "
            f"by units"
        )
        return product_units

    def aggregate_by_weekday(
        self,
        value_column: str,
        weekday_column: str = 'Weekday'
    ) -> pd.DataFrame:
        """
        Aggregate values by weekday in chronological order.

        Groups data by weekday and sums the specified value column,
        returning results in Monday-Sunday order.

        Args:
            value_column: Name of column to aggregate (e.g., 'Sales_Amount')
            weekday_column: Name of weekday column (default: 'Weekday')

        Returns:
            DataFrame with columns [weekday_column, value_column]
            ordered Monday through Sunday. Returns empty DataFrame if
            required columns missing.
        """
        if value_column not in self.df.columns:
            logger.warning(
                f"{LOG_EMOJI_ERROR} Value column '{value_column}' "
                f"not found"
            )
            return pd.DataFrame(columns=[weekday_column, value_column])

        if weekday_column not in self.df.columns:
            logger.warning(
                f"{LOG_EMOJI_ERROR} Weekday column '{weekday_column}' "
                f"not found"
            )
            return pd.DataFrame(columns=[weekday_column, value_column])

        # Aggregate by weekday
        weekday_agg = (
            self.df.groupby(weekday_column)[value_column]
            .sum()
            .reset_index()
        )

        # Create categorical type with proper ordering
        weekday_agg[weekday_column] = pd.Categorical(
            weekday_agg[weekday_column],
            categories=WEEKDAY_ORDER,
            ordered=True
        )

        # Sort by weekday order
        weekday_agg = weekday_agg.sort_values(weekday_column).reset_index(
            drop=True
        )

        logger.info(
            f"{LOG_EMOJI_PROCESSING} Aggregated {value_column} by weekday"
        )
        return weekday_agg
