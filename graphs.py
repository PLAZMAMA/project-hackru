from code import interact
from typing import List
import plotly.express as px
from plotly.graph_objs._figure import Figure
from pandas import DataFrame
import pandas as pd
from code import interact
from datetime import datetime


def render_eye_tracking_pie(eye_tracking_df: DataFrame) -> Figure:
    # Preprocessing
    state_columns = [
        "looking_right",
        "looking_left",
        "looking_center",
        "looking_up",
        "looking_down",
    ]
    state_counts = eye_tracking_df[state_columns].sum().reset_index()
    state_counts.columns = ["State", "Count"]

    # Filter out zero counts
    state_counts = state_counts[state_counts["Count"] > 0]

    # Create a pie chart for the states
    fig_pie = px.pie(
        state_counts, title="Counts of Looking States", names="State", values="Count"
    )

    return fig_pie

    
def render_daily_summary_timeline(activity_df: DataFrame) -> Figure:
    # Create a bar chart
    fig_timeline = px.timeline(
        activity_df,
        x_start="start_time",
        x_end="end_time",
        y="app_name",
        color="productive",
        height=100,
    )

    # Remove y-axis title and any title or subtitle
    fig_timeline.update_layout(
        yaxis_title=None,
        title=None,
        yaxis=dict(tickvals=[], ticktext=[]),
        xaxis=dict(
            tickmode="array",
            tickvals=[f"{i:02}:00" for i in range(24)],
            ticktext=[f"{i}:00" for i in range(24)],
            range=["00:00", "24:00"],
        ),
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    # Update layout for white background
    fig_timeline.update_layout(
        plot_bgcolor="white",  # Background color of the plot area
        paper_bgcolor="white",  # Background color of the entire figure
    )

    return fig_timeline

def render_productivity_bar_char(eye_tracking_df: DataFrame, app_usage_df: DataFrame) -> Figure:
    productivity_df = app_usage_df[["productive", "timedelta"]].groupby("productive")["timedelta"].sum()
    return px.bar(productivity_df, color=productivity_df.index, x=productivity_df.index, y="timedelta", color_discrete_map={True: "green", False: "red"})

