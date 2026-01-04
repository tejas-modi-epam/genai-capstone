# app/bq_client.py
from google.cloud import bigquery
from .config import PROJECT_ID

def get_bq_client() -> bigquery.Client:
    return bigquery.Client(project=PROJECT_ID)

def run_query(query: str):
    client = get_bq_client()
    job = client.query(query)
    return job.result()
