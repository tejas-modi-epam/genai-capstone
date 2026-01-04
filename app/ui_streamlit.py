# app/ui_streamlit.py
import streamlit as st
from app.tools import (
    analyze_trends_last_30_days,
    compare_stores_last_30_days,
    simulate_promo_uplift,
)
from app.agent import run_agent

st.set_page_config(page_title="Retail Decision Support Agent", layout="wide")

st.title("Retail Decision Support Agent (BigQuery + OpenAI + LangChain)")

tab1, tab2, tab3 = st.tabs(["Trends", "Compare Stores", "Chat Agent"])

with tab1:
    st.subheader("Last 30 days sales trend")
    if st.button("Load trend from BigQuery"):
        df = analyze_trends_last_30_days()
        if df.empty:
            st.warning("No data found.")
        else:
            st.dataframe(df)
            st.line_chart(df, x="sale_date", y="total_sales")

with tab2:
    st.subheader("Store comparison (last 30 days)")
    if st.button("Load store comparison"):
        df = compare_stores_last_30_days()
        if df.empty:
            st.warning("No data found.")
        else:
            st.dataframe(df)

    st.subheader("Promo Simulation (Naive)")
    discount = st.slider("Discount increase (%)", min_value=0.0, max_value=50.0, value=10.0, step=5.0)
    if st.button("Run promo simulation"):
        df_sim = simulate_promo_uplift(discount)
        if df_sim.empty:
            st.warning("No data found.")
        else:
            st.dataframe(df_sim)

with tab3:
    st.subheader("Ask the Retail Agent")
    default_q = "Analyze my last 30 days trend and suggest which stores need promo support."
    user_input = st.text_area("Ask a question", default_q)
    if st.button("Ask Agent"):
        if not user_input.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                answer = run_agent(user_input)
            st.markdown("**Answer:**")
            st.write(answer)
