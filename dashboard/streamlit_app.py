# dashboard/streamlit_app.py
import streamlit as st
import json
from pathlib import Path
import pandas as pd
import altair as alt

st.set_page_config(page_title="Agentic AI Crypto Insights", layout="wide")

DATA_DIR = Path("data/processed")

def latest_report():
    files = sorted(DATA_DIR.glob("insight_*.json"), reverse=True)
    if not files:
        return None
    return files[0]

st.title("Agentic AI Crypto Market Insight Engine")

report_file = latest_report()
if not report_file:
    st.info("No reports found. Run main.py pipeline to generate a report.")
    st.stop()

with open(report_file, "r", encoding="utf-8") as f:
    report = json.load(f)

# Top entities
st.header("Top Entities")
entities = report.get("top_entities", [])
if entities:
    df_entities = pd.DataFrame(entities, columns=["entity", "count"])
    st.bar_chart(df_entities.set_index("entity")["count"])

# Top tones
st.header("Top Tones")
tones = report.get("top_tones", [])
if tones:
    df_tones = pd.DataFrame(tones, columns=["tone", "count"])
    st.altair_chart(alt.Chart(df_tones).mark_bar().encode(
        x="tone", y="count"
    ), use_container_width=True)

# Tone over time
st.header("Tone Over Time")
tot = report.get("tone_over_time", {})
if tot:
    rows=[]
    for day,v in tot.items():
        for tone,str_count in v.items():
            rows.append({"date":day,"tone":tone,"count":str_count})
    df = pd.DataFrame(rows)
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='date:T',
        y='count:Q',
        color='tone:N'
    )
    st.altair_chart(chart, use_container_width=True)

st.header("Sample Article Analysis")
for art in report.get("sample_articles", []):
    st.subheader(art.get("title"))
    st.write(art.get("reasoning"))
    st.write("Entities:", art.get("entities"))
    st.write("Implications:", art.get("implications"))
    st.markdown(f"[Original article]({art.get('url')})")
    st.write("---")
