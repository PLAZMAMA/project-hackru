from typing import List
import plotly.express as px
from plotly.graph_objs._figure import Figure
from pandas import DataFrame
import pandas as pd
from code import interact


def render_pie(eye_tracking_df: DataFrame) -> Figure:
    # Preprocessing
    state_columns = ['looking_right', 'looking_left', 'looking_center', 'looking_up', 'looking_down']
    state_counts = eye_tracking_df[state_columns].sum().reset_index()
    state_counts.columns = ['State', 'Count']

    # Filter out zero counts
    state_counts = state_counts[state_counts['Count'] > 0]

    # Create a pie chart for the states
    fig_pie = px.pie(
        state_counts,
        title='Counts of Looking States',
        names='State',
        values='Count'
    )

    return fig_pie
