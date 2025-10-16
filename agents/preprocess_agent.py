# agents/preprocess_agent.py
import re
from core.utils import clean_text, fingerprint
from loguru import logger

class PreprocessAgent:
    def __init__(self):
        pass

    def normalize(self, article):
        # article is dict with keys: title, url, text, published
        text = article.get("text", "")
        text = clean_text(text)
        # small heuristics: remove author lines
        text = re.sub(r"By [A-Z][a-z]+.*(\n|$)", "", text)
        article["text_clean"] = text
        article["len_text"] = len(text)
        article["fingerprint"] = fingerprint(text + article.get("url", ""))
        return article

    def run_batch(self, articles):
        normalized = []
        seen = set()
        for a in articles:
            na = self.normalize(a)
            if na["fingerprint"] in seen:
                logger.debug("Deduped in preprocess")
                continue
            seen.add(na["fingerprint"])
            normalized.append(na)
        logger.info(f"PreprocessAgent normalized {len(normalized)} articles")
        return normalized
