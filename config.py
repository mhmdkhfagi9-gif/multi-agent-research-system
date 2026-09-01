import os
from langchain_groq import ChatGroq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required.")

LLM_MODEL = "openai/gpt-oss-120b"
LLM_TEMPERATURE = 0

def get_llm():
    return ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        api_key=GROQ_API_KEY,
        timeout=30,
        max_retries=2,
    )

MAX_RETRIEVAL_RETRIES = 2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "data", "documents")
DATASETS_DIR = os.path.join(BASE_DIR, "data", "datasets")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")
DASHBOARD_PATH = os.path.join(BASE_DIR, "outputs", "dashboard.json")

EMAIL_DRY_RUN = True
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT", "recipient@example.com")

DEFAULT_API_URL = os.environ.get("DEFAULT_API_URL", "https://jsonplaceholder.typicode.com/posts")
