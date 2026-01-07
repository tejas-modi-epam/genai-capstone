# Retail Decision Support Agent - Capstone Deck

#Architecture & Tech Stack


# Retail Decision Support Agent
**GenAI + Agentic AI for CPG Retail Analytics**


# Problem & Goal
- Business has **multi-store, multi-SKU sales data** but no easy way to explore it
- Need a simple **Decision Support Agent** that:
  - Shows trends and store performance
  - Simulates "what-if" promo scenarios  
  - Answers questions in **natural language** 


# Simple Architecture

┌─────────────────┐
│   User Input    │
│  (Chat or UI)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   Streamlit UI          │
│  (3 tabs + Chat)        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  LangChain Agent        │
│  (Decides which tool)   │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Python Tools (3 functions)      │
│  ├─ Trend Analysis               │
│  ├─ Store Comparison             │
│  └─ Promo Simulation             │
└────────┬─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  BigQuery (SQL Queries) │
│  └─ fact_sales table    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  OpenAI (LLM)           │
│  (Makes answer readable)│
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Answer to User         │
│  (Chat or Table)        │
└─────────────────────────┘


---

# 5 Layers Explained

| Layer | Technology | What It Does |
|-------|-----------|-------------|
| **Data Layer** | BigQuery + SQL | Stores sales data (fact_sales, dims) |
| **Tool Layer** | Python Functions | trend, compare_stores, simulate_promo |
| **Agent Layer** | LangChain | Picks which tool to use based on question |
| **GenAI Layer** | OpenAI (gpt-4o-mini) | Turns raw data into human-friendly answers |
| **UI Layer** | Streamlit | Shows charts, tables, and chat interface |



# Tech Stack:

- **Language**: Python 3.10+
- **Data**: Google BigQuery (cloud warehouse)
- **Agent**: LangChain (tool orchestration)
- **LLM**: OpenAI API (gpt-4o-mini)
- **Frontend**: Streamlit (web UI)
- **Auth**: GCP Application Default Credentials



# Execution Flow, Code, & UI
==============================


# How the Agent Answers a Question

**Example User Question**: "Which stores need promo support?"

| Step | What Happens |
|------|-------------|
| 1 | User types question in Streamlit Chat tab |
| 2 | Streamlit calls `run_agent(question)` in app/agent.py |
| 3 | LangChain Agent reads question and picks tools ("I need store compare + trend") |
| 4 | Tools run SQL on BigQuery (returns tables as Pandas DataFrames) |
| 5 | Agent converts DataFrames to markdown text |
| 6 | OpenAI LLM reads markdown and writes a **business-friendly answer** |
| 7 | Streamlit shows the answer in the chat window |


# Code Walkthrough (File by File)

**`app/config.py`**

- Reads: GCP_PROJECT_ID, BQ_DATASET, OPENAI_API_KEY
- Builds: FACT_SALES_TABLE = "project.cpg_retail.fact_sales"


**`app/bq_client.py`**

- Creates: BigQuery client with GCP credentials
- Function: run_query(sql) → executes SQL, returns results


**`app/tools.py`**

- analyze_trends_last_30_days()
  → SQL: SUM(net_sales) per sale_date (last 30 days)
  
- compare_stores_last_30_days()
  → SQL: SUM(net_sales) per store_id (last 30 days)
  
- simulate_promo_uplift(discount_pct)
  → Gets units + sales, multiplies by elasticity factor


**`app/agent.py`**

- Create LLM: ChatOpenAI(model="gpt-4o-mini")
- Wrap tools: trend_tool, compare_stores_tool, promo_sim_tool
- Initialize: LangChain ZERO_SHOT_REACT_DESCRIPTION agent
- Function: run_agent(query) → calls tools + LLM → returns text


**`app/ui_streamlit.py`** 

- Create 3 tabs: "Trends", "Compare Stores", "Chat Agent"
- Tab 1 (Trends): Button → calls analyze_trends() → shows chart
- Tab 2 (Compare): Button → calls compare_stores() + simulate_promo()
- Tab 3 (Chat): Text box → calls run_agent() → shows answer


---

# UI Functionality 

# Tab 1: Trends
- **Purpose**: See overall sales trend
- **Action**: Click "Load trend from BigQuery"
- **Result**: Table + line chart of daily sales (last 30 days)
- **Note**: No LLM involved; pure data visualization

# Tab 2: Compare Stores
- **Purpose**: Compare store performance
- **Action**: Click "Load store comparison"
- **Result**: Table showing sales per store (sorted high to low)
- **Bonus**: Slider to simulate promo discount (0-50%)
  - Moves slider → sees predicted uplift in units and revenue

# Tab 3: Chat Agent
- **Purpose**: Ask business questions in plain English
- **Action**: Type a question + click "Ask Agent"
- **Examples**:
  - "Analyze my last 30 days and tell me which stores underperformed"
  - "Simulate a 15% discount and show impact"
  - "Where should I put promo budget?"
- **Result**: Natural language answer with recommendations

---

# Example Agent Conversation

**User asks**: "Which stores are underperforming?"

**Agent does internally**:
1. Calls `compare_stores_last_30_days()` (gets sales per store)
2. Identifies store with lowest sales (e.g., Store S003)
3. Calls `analyze_trends_last_30_days()` (gets overall trend)
4. Sends both results to OpenAI LLM as markdown

**Agent responds**:

"Based on the last 30 days of sales data:

• Store S003 (South region) sold only $90K in net sales, 
  which is 70% lower than top performer S001 ($300K).

• Overall trend shows stable sales (~$110K daily), 
  so the issue is localized to S003.

• Recommendation: Run a focused promo campaign at Store S003. 
  With a 10% discount on top 3 products, expect +25% uplift 
  in units and ~$18K additional revenue."


---

# Key Takeaway


User Question
    ↓
LangChain picks tool(s)
    ↓
Tools query BigQuery
    ↓
LLM makes it readable
    ↓
User gets business answer
    (not raw data, not SQL result – a recommendation)


