"""
Central configuration for the Multi-Agent AI Research System.
Every agent and tool reads its settings from here instead of hardcoding
values, so changing the model, paths, or retry limits only needs to happen
in one place.
"""

import os
from langchain_groq import ChatGroq

# --- LLM ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")   # <-- set your real key (env var recommended)
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0


def get_llm():
    """Single shared LLM factory used by every agent."""
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    return ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        timeout=30,
        max_retries=2,
    )


# --- Orchestration ---
MAX_RETRIEVAL_RETRIES = 2   # how many times the Critic Agent can send the flow back to Retrieval

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "data", "documents")
DATASETS_DIR = os.path.join(BASE_DIR, "data", "datasets")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")
DASHBOARD_PATH = os.path.join(BASE_DIR, "outputs", "dashboard.json")

# --- Action Agent: Email ---
EMAIL_DRY_RUN = True   # True = log/print instead of actually sending (no real credentials needed to test)
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT", "recipient@example.com")

# --- API Agent ---
DEFAULT_API_URL = os.environ.get("DEFAULT_API_URL", "https://jsonplaceholder.typicode.com/posts")
