from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

CSV_PATH = Path(__file__).resolve().parent.parent / "Data" / "pushups.csv"

def load_data():
    if not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0:
        return None
    return pd.read_csv(CSV_PATH, parse_dates=["timestamp"])

st.title("Pushup Tracker")

def build_calendar_heatmap(df, weeks=26):
    daily = df.groupby(df["timestamp"].dt.normalize())["reps"].sum()

    end = pd.Timestamp.today().normalize()
    start = end - pd.Timedelta(weeks=weeks)

    start -= pd.Timedelta(days=(start.weekday() + 1) % 7)
    days = pd.date_range(start, end)

    grid = pd.DataFrame({
        "week": (days - start).days // 7,
        "weekday": (days.weekday + 1) % 7,
        "reps": daily.reindex(days, fill_value=0).values,
        "label": days.strftime("%b %d, %Y"),
    })

    reps_grid = grid.pivot(index="weekday", columns="week", values="reps")
    label_grid = grid.pivot(index="weekday", columns="week", values="label")

    fig = go.Figure(go.Heatmap(
        z=reps_grid.values,
        text=label_grid.values,
        hovertemplate="%{text}: %{z} pushups<extra></extra>",
        colorscale=[[0, "#161b22"], [0.01, "#0e4429"], [1, "#39d353"]],
        zmin=0,
        xgap=3,
        ygap=3,
        showscale=False,
    ))
    fig.update_yaxes(
        tickvals=[1, 3, 5],
        ticktext=["Mon", "Wed", "Fri"],
        autorange="reversed",
        scaleanchor="x",
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(height=220, margin=dict(t=20, b=20))
    return fig


df = load_data()
if df is None or df.empty:
    st.info("No pushups logged yet. Run: python src/log.py 20")
else:
    st.subheader("Activity")
    st.plotly_chart(build_calendar_heatmap(df))
    st.dataframe(df)
    fig = px.bar(df, x="timestamp", y="reps", title="Pushups per set")
    st.plotly_chart(fig)

