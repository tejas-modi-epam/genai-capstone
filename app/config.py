# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
BQ_DATASET = os.getenv("BQ_DATASET", "cpg_retail")
BQ_LOCATION = os.getenv("BQ_LOCATION", "US")

FACT_SALES_TABLE = f"{PROJECT_ID}.{BQ_DATASET}.fact_sales"
DIM_STORE_TABLE = f"{PROJECT_ID}.{BQ_DATASET}.dim_store"
DIM_SKU_TABLE = f"{PROJECT_ID}.{BQ_DATASET}.dim_sku"
DIM_DATE_TABLE = f"{PROJECT_ID}.{BQ_DATASET}.dim_date"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
