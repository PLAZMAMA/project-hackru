from __future__ import annotations
import dash
from dash import html, dcc, dash_table
import pandas as pd

from datetime import datetime
from util.dates import format_date

# Import dashboards
from graphs import (
    render_eye_tracking_pie, 
    render_daily_summary_timeline
)
from components.flex_container import FlexContainer

def read_eye_tracking_csv(file_path = './data/eye_tracking_data.csv'):
    """Reads CSV file and returns a Pandas DataFrame"""

    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convert timestamp to datetime
    return df

def read_app_usage_csv(file_path = './data/app_usage.csv'):
    """Reads CSV file and returns a Pandas DataFrame"""

    df = pd.read_csv(file_path)

    df['start_time'] = pd.to_datetime(df['start_time'])  # Convert timestamp to datetime
    df['end_time'] = pd.to_datetime(df['end_time'])  # Convert timestamp to datetime

    return df
    

# Load the CSV data and check for an error
EYE_TRACKING_DF = read_eye_tracking_csv()
APP_USAGE_DF = read_app_usage_csv()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap'
])

def render(app, **dfs) -> None:
    """
    Renders the app layout in the given app.

    Parameters:
        dfs: A dictionary of dataframes in the following format:
        {
            "dataframe_name": dataframe,
            ...
        }

        An example is:
        {
            "eye_tracking_df": sliced_eye_tracking_df,
            "app_usage_df": sliced_app_usage_df
        }
    """

    app.layout = [] # Started empty for to avoid type hinting feakouts by the LSP


    # Header for daily summary
    today = datetime.now()
    app.layout.append(html.H1(format_date(today)))
    app.layout.append(html.H3("Daily Summary"))

    # Import dashboards
    DASHBOARDS = [
        FlexContainer(
            "daily-summary",
            [
                dcc.Graph(figure=render_daily_summary_timeline(dfs["app_usage_df"]), style={'width': '100%'}),
            ],
            "flex-row"
        ),
        FlexContainer(
            "daily-breakdown",
            [
                dcc.Graph(figure=render_eye_tracking_pie(dfs["eye_tracking_df"])),
                dcc.Graph(figure=render_eye_tracking_pie(dfs["eye_tracking_df"]))
            ],
            "flex-row"
        ),
    ]

    # Render the graphs in each dashboard to the layout
    for container in DASHBOARDS:
        app.layout.append(container.html())

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
