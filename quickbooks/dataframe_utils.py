from __future__ import annotations

import pandas as pd


def optimize_dataframe_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Heuristic dtype optimization: numeric coercion, categories, datetimes."""
    try:
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    df[col] = pd.to_numeric(df[col])
                    continue
                except (ValueError, TypeError):
                    pass
                if df[col].nunique(dropna=False) < len(df) * 0.5:
                    df[col] = df[col].astype("category")
        for col in [
            "Date",
            "Due_Date",
            "order_date",
            "delivery_date",
            "entry_date",
        ]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        for col in [
            "amount",
            "open_balance",
            "invoiced_amount",
            "Qty",
            "Open_Qty",
            "Open_Balance",
        ]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    except Exception:
        return df
