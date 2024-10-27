from __future__ import annotations
from typing import List, Any
import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import dashboards
from graphs import render_eye_tracking_pie
from components.flex_container import FlexContainer

def read_eye_tracking_csv(file_path = './data/eye_tracking_data.csv'):
    """Reads CSV file and returns a Pandas DataFrame"""

    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convert timestamp to datetime
    return df

# Load the CSV data and check for an error
EYE_TRACKING_DF = read_eye_tracking_csv()
# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = [
    html.H1("CSV Data Display"),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in EYE_TRACKING_DF.columns],
    data=EYE_TRACKING_DF.to_dict('records'),
    page_size=10,  # Adjust page size as needed
    style_table={'overflowX': 'auto'},  # Ensure horizontal scroll for wide tables
    )
]


# Import dashboards
DASHBOARDS = [
    FlexContainer(
        "daily-breakdown",
        [
            render_eye_tracking_pie(EYE_TRACKING_DF)
        ],
        {}
    ),
]

# Render the graphs in each dashboard to the layout
for dashboard in DASHBOARDS:
    for rendered_graph in dashboard.graphs:
        app.layout.append(dcc.Graph(figure=rendered_graph))

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
