# agents/insight_agent.py
from collections import Counter, defaultdict
import datetime
from loguru import logger

class InsightAgent:
    def __init__(self, vector_client=None, postgres_client=None):
        self.vector_client = vector_client
        self.postgres_client = postgres_client

    def aggregate(self, analyzer_outputs):
        # analyzer_outputs: list of dicts each with tone, reasoning, entities, implications, published
        tone_counts = Counter()
        entity_counts = Counter()
        timeline = defaultdict(list)
        for o in analyzer_outputs:
            tone = o.get("tone","unknown")
            tone_counts[tone]+=1
            for ent in o.get("entities", []):
                entity_counts[ent]+=1
            # bucket by date
            dt = o.get("published", datetime.datetime.utcnow().isoformat())
            day = dt.split("T")[0]
            timeline[day].append(tone)

        # tone over time (simple)
        tone_over_time = {day: dict(Counter(timeline[day])) for day in timeline}

        top_entities = entity_counts.most_common(20)
        top_tones = tone_counts.most_common(10)

        summary = {
            "top_entities": top_entities,
            "top_tones": top_tones,
            "tone_over_time": tone_over_time
        }
        logger.info("InsightAgent aggregated insights")
        return summary
