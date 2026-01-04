# app/llm_layer.py
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_trend(text: str) -> str:
    """
    Summarize a trend description in business language.
    """
    prompt = (
        "You are a CPG retail analytics expert. "
        "Summarize the following sales trend for a business head in 3-4 bullet points:\n\n"
        f"{text}"
    )
    resp = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()

def strategy_memo(text: str) -> str:
    """
    Generate a short strategy memo (1-2 paragraphs) based on analysis text.
    """
    prompt = (
        "You are a sales strategy consultant for a CPG retail company. "
        "Based on the analysis below, write a concise strategy memo (1-2 paragraphs) "
        "with clear actions:\n\n"
        f"{text}"
    )
    resp = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()
