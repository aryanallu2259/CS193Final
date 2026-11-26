from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

CSV_PATH = Path(__file__).resolve().parent.parent / "Data" / "pushups.csv"

def load_data():
    if not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0:
        return None
    return pd.read_csv(CSV_PATH, parse_dates=["timestamp"])

st.title("Pushup Tracker")

df = load_data()
if df is None or df.empty:
    st.info("No pushups logged yet. Run: python src/log.py 20")
else:
    st.dataframe(df)
    fig = px.bar(df, x="timestamp", y="reps", title="Pushups per set")
    st.plotly_chart(fig)