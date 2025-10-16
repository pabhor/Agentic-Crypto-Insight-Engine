# agents/scraper_agent.py
import feedparser
import requests
from newspaper import Article
from bs4 import BeautifulSoup
from typing import List, Dict
from core.config import DEFAULT_RSS
from core.utils import clean_text, fingerprint, iso_now
from loguru import logger
import json
from pathlib import Path

SAVE_DIR = Path("data/raw")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

class ScraperAgent:
    def __init__(self, rss_list=None):
        self.rss_list = rss_list or DEFAULT_RSS

    def fetch_rss(self, url: str):
        try:
            feed = feedparser.parse(url)
            entries = []
            for e in feed.entries:
                entries.append(e)
            return entries
        except Exception as e:
            logger.error(f"RSS fetch failed for {url}: {e}")
            return []

    def extract_article(self, url: str) -> Dict:
        try:
            art = Article(url)
            art.download()
            art.parse()
            text = art.text or ""
            if not text:
                # fallback: simple requests + soup
                r = requests.get(url, timeout=10)
                soup = BeautifulSoup(r.text, "html.parser")
                text = " ".join([p.get_text() for p in soup.find_all("p")])
            text = clean_text(text)
            return {"url": url, "text": text, "fetched_at": iso_now()}
        except Exception as e:
            logger.warning(f"Article extraction failed for {url}: {e}")
            return {"url": url, "text": "", "fetched_at": iso_now()}

    def run(self) -> List[Dict]:
        results = []
        for rss in self.rss_list:
            entries = self.fetch_rss(rss)
            for e in entries:
                url = e.get("link") or e.get("guid") or None
                if not url:
                    continue
                article = self.extract_article(url)
                title = e.get("title", "")[:250]
                item = {
                    "title": title,
                    "url": url,
                    "published": e.get("published", iso_now()),
                    "source": e.get("source", {}).get("title") if e.get("source") else "",
                    "text": article["text"],
                }
                # dedupe fingerprint
                fp = fingerprint(item["text"] + item["url"])
                item["fingerprint"] = fp
                filename = SAVE_DIR / f"{fp}.json"
                if not filename.exists():
                    filename.write_text(json.dumps(item, ensure_ascii=False))
                    results.append(item)
                else:
                    logger.debug(f"Duplicate skipped: {url}")
        logger.info(f"ScraperAgent fetched {len(results)} new items")
        return results

if __name__ == "__main__":
    s = ScraperAgent()
    out = s.run()
    print(f"Fetched {len(out)} articles")
