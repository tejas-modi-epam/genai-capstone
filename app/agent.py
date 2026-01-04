# app/agent.py
import pandas as pd
from langchain.tools import StructuredTool
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI

from .tools import (
    analyze_trends_last_30_days,
    compare_stores_last_30_days,
    simulate_promo_uplift,
)

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.3,
)

def _tool_trend_last_30_days() -> str:
    df = analyze_trends_last_30_days()
    if df.empty:
        return "No data available for the last 30 days."
    text = f"Trend for the last 30 days (sale_date, total_sales):\n{df.to_markdown(index=False)}"
    return text

def _tool_compare_stores_last_30_days() -> str:
    df = compare_stores_last_30_days()
    if df.empty:
        return "No data available for store comparison."
    text = f"Store comparison (store_id, total_sales) for last 30 days:\n{df.to_markdown(index=False)}"
    return text

def _tool_simulate_promo(discount_increase_pct: float = 10.0) -> str:
    df = simulate_promo_uplift(discount_increase_pct)
    if df.empty:
        return "No data available to simulate promo."
    text = (
        f"Promo simulation with discount increase of {discount_increase_pct}% "
        f"(sale_date, units_sold, net_sales, sim_units_sold, sim_net_sales):\n"
        f"{df.to_markdown(index=False)}"
    )
    return text

trend_tool = StructuredTool.from_function(
    func=_tool_trend_last_30_days,
    name="trend_last_30_days",
    description="Get total net sales trend for the last 30 days.",
)

store_compare_tool = StructuredTool.from_function(
    func=_tool_compare_stores_last_30_days,
    name="compare_stores_last_30_days",
    description="Compare total net sales per store in the last 30 days.",
)

promo_sim_tool = StructuredTool.from_function(
    func=_tool_simulate_promo,
    name="simulate_promo",
    description="Simulate promo uplift given a discount increase percentage.",
)

_agent = initialize_agent(
    tools=[trend_tool, store_compare_tool, promo_sim_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

def run_agent(user_query: str) -> str:

    return _agent.run(user_query)
