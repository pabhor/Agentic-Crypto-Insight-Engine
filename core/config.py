# core/config.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EMBED_DIR = DATA_DIR / "embeddings"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
EMBED_DIR.mkdir(parents=True, exist_ok=True)

# Models
EMBED_MODEL_NAME = os.environ.get("EMBED_MODEL", "sentence-transformers/all-mpnet-base-v2")
LLM_MODEL_NAME = os.environ.get("LLM_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")  # changeable
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_DIR", str(BASE_DIR / "storage" / "chroma"))

# Scraping
DEFAULT_RSS = [
    "https://news.google.com/rss/search?q=cryptocurrency",
    "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
    "https://cointelegraph.com/rss",
]

# DB connections
POSTGRES_DSN = os.environ.get("POSTGRES_DSN", "postgresql://user:pass@localhost:5432/crypto_insights")

# Other
MAX_ARTICLE_LENGTH = 20000
