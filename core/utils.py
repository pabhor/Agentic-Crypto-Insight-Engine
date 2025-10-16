# core/utils.py
import re
import hashlib
from datetime import datetime
from core.config import MAX_ARTICLE_LENGTH
from loguru import logger

def fingerprint(text: str) -> str:
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    return h.hexdigest()

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    # remove weird characters
    text = text.replace("\x0c", " ")
    text = text.strip()
    if len(text) > MAX_ARTICLE_LENGTH:
        text = text[:MAX_ARTICLE_LENGTH]
    return text

def iso_now():
    return datetime.utcnow().isoformat() + "Z"
