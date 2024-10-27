from __future__ import annotations
import dash
from dash import html, dcc, dash_table
import pandas as pd
from pandas import DataFrame

from datetime import datetime
from util.dates import format_date

# Import dashboards
from graphs import render_eye_tracking_pie, render_daily_summary_timeline, render_productivity_bar_char
from components.flex_container import FlexContainer


def read_eye_tracking_csv(file_path="./data/eye_tracking_data_v2.csv"):
    """Reads CSV file and returns a Pandas DataFrame"""

    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert timestamp to datetime
    return df


def read_app_usage_csv(file_path="./data/app_usage.csv"):
    """Reads CSV file and returns a Pandas DataFrame"""

    df = pd.read_csv(file_path)

    df["start_time"] = pd.to_datetime(df["start_time"])  # Convert timestamp to datetime
    df["end_time"] = pd.to_datetime(df["end_time"])  # Convert timestamp to datetime
    df["timedelta"] = pd.to_timedelta(df["timedelta"])

    return df


# Load the CSV data and check for an error
EYE_TRACKING_DF = read_eye_tracking_csv()
APP_USAGE_DF = read_app_usage_csv()

# Initialize the Dash app
APP = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap"
    ],
)


def preprocess(app_usage_df) -> None:

    # Preprocessing: Filter by today's date
    app_usage_df["start_time"] = pd.to_datetime(app_usage_df["start_time"])
    app_usage_df["end_time"] = pd.to_datetime(app_usage_df["end_time"])

    app_usage_df = app_usage_df[
        (app_usage_df["start_time"].dt.date == datetime(2022, 7, 26).date())
    ]


def render(app, eye_tracking_df: DataFrame, app_usage_df: DataFrame) -> None:
    """
    Renders the app layout in the given app.

    Parameters:
        dfs: A dictionary of dataframes in the following format:
        {
            "dataframe_name": dataframe,
            ...
        }

        The current expected dataframes are:
        {
            "eye_tracking_df": sliced_eye_tracking_df,
            "app_usage_df": sliced_app_usage_df
        }
    """

    app.layout = []  # Started empty for to avoid type hinting feakouts by the LSP

    # Check dataframe date ranges match each other
    dfs_date_ranges = {
        (
            app_usage_df["start_time"].min().date(),
            app_usage_df["end_time"].max().date()
        ),
        (
            eye_tracking_df["timestamp"].min().date(),
            eye_tracking_df["timestamp"].max().date(),
        ),
    }

    # Check all dataframes have the same date
    if len(dfs_date_ranges) != 1:
        # raise ValueError(
        #     f"Dataframes date ranges are missmatched: {dfs_date_ranges = }"
        # )
        # TODO: For now only print this future error, uncomment the raised error
        # above when the dataframes are passed to this function pre sliced.

        print(f"Error: Dataframes date ranges are missmatched: {dfs_date_ranges = }")

    # Header for daily summary
    placeholder_display_date = app_usage_df["start_time"].min().date()
    app.layout.append(html.H1(format_date(placeholder_display_date)))
    
    app.layout.append(html.H3("Daily Summary"))

    # Import dashboards
    DASHBOARDS = [
        FlexContainer(
            "daily-summary",
            [
                dcc.Graph(
                    figure=render_daily_summary_timeline(app_usage_df),
                    style={"width": "100%"},
                ),
            ],
            "flex-row",
        ),
        FlexContainer(
            "daily-breakdown",
            [
                dcc.Graph(figure=render_productivity_bar_char(eye_tracking_df, app_usage_df)),
                dcc.Graph(figure=render_eye_tracking_pie(eye_tracking_df)),
            ],
            "flex-row",
        ),
    ]

    # Render the graphs in each dashboard to the layout
    for container in DASHBOARDS:
        app.layout.append(container.html())


# Run the app
if __name__ == "__main__":
    preprocess(APP_USAGE_DF)
    render(APP, eye_tracking_df=EYE_TRACKING_DF, app_usage_df=APP_USAGE_DF)
    APP.run_server(debug=True)
