# agents/reporter_agent.py
import json
from loguru import logger
from core.config import PROCESSED_DIR
from pathlib import Path

OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

class ReporterAgent:
    def __init__(self):
        pass

    def save_daily_report(self, insights):
        ts = insights.get("generated_at", None) or "report"
        fname = OUT_DIR / f"insight_{ts}.json"
        fname.write_text(json.dumps(insights, ensure_ascii=False, indent=2))
        logger.info(f"Saved report to {fname}")
        return str(fname)

    def format_for_dashboard(self, insights):
        # Return a JSON-ready object for the Streamlit UI
        return insights
