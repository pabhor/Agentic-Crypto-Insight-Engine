# main.py
import asyncio
from agents.scraper_agent import ScraperAgent
from agents.preprocess_agent import PreprocessAgent
from agents.embed_agent import EmbedAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.insight_agent import InsightAgent
from agents.reporter_agent import ReporterAgent
from core.utils import iso_now
from core.logger import logger

async def pipeline_run():
    scraper = ScraperAgent()
    pre = PreprocessAgent()
    embedder = EmbedAgent()
    analyzer = AnalyzerAgent()
    insight = InsightAgent()
    reporter = ReporterAgent()

    # 1. Scrape
    raw_articles = scraper.run()
    if not raw_articles:
        logger.info("No new articles found.")
        return

    # 2. Preprocess
    normalized = pre.run_batch(raw_articles)

    # 3. Embed + store
    embedder.add_documents(normalized)

    # 4. Analyze each new article (could be async/gpu-batched)
    analyzer_outputs = []
    for art in normalized:
        res = analyzer.analyze(art["text_clean"])
        # attach metadata
        res["title"] = art.get("title")
        res["url"] = art.get("url")
        res["published"] = art.get("published")
        analyzer_outputs.append(res)

    # 5. Aggregate insights
    summary = insight.aggregate(analyzer_outputs)
    summary["generated_at"] = iso_now()
    summary["sample_articles"] = analyzer_outputs[:10]

    # 6. Save / report
    saved = reporter.save_daily_report(summary)
    logger.info(f"Pipeline finished; report saved: {saved}")

if __name__ == "__main__":
    asyncio.run(pipeline_run())
    main()