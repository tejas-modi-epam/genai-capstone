# app/tools.py
import pandas as pd
from .bq_client import run_query
from .config import FACT_SALES_TABLE

def analyze_trends_last_30_days() -> pd.DataFrame:
    """
    Returns daily total net_sales for last 30 days.
    """
    query = f"""
    SELECT
      sale_date,
      SUM(net_sales) AS total_sales
    FROM `{FACT_SALES_TABLE}`
    WHERE sale_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY sale_date
    ORDER BY sale_date
    """
    rows = run_query(query)
    df = pd.DataFrame([dict(r) for r in rows])
    return df

def compare_stores_last_30_days() -> pd.DataFrame:
    """
    Returns total net_sales per store for last 30 days.
    """
    query = f"""
    SELECT
      store_id,
      SUM(net_sales) AS total_sales
    FROM `{FACT_SALES_TABLE}`
    WHERE sale_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY store_id
    ORDER BY total_sales DESC
    """
    rows = run_query(query)
    df = pd.DataFrame([dict(r) for r in rows])
    return df

def simulate_promo_uplift(discount_increase_pct: float = 10.0) -> pd.DataFrame:
    query = f"""
    SELECT
      sale_date,
      SUM(units_sold) AS units_sold,
      SUM(net_sales) AS net_sales
    FROM `{FACT_SALES_TABLE}`
    WHERE sale_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY sale_date
    ORDER BY sale_date
    """
    rows = run_query(query)
    df = pd.DataFrame([dict(r) for r in rows])
    if df.empty:
        return df

    uplift_factor = 1.0 + 0.5 * (discount_increase_pct / 10.0)
    df["sim_units_sold"] = df["units_sold"] * uplift_factor
    # assume proportional net_sales change
    df["sim_net_sales"] = df["net_sales"] * uplift_factor
    return df
