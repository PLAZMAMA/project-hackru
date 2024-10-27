import dash
from dash import html, dash_table, dcc
import kagglehub
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objs as go

# Download latest version
path = kagglehub.dataset_download("ruchi798/analyzing-screen-time")
csv_path = os.path.join(path, "Screentime - Overall Usage.csv")
df = pd.read_csv(csv_path)

xy_graph = go.Figure(data = [go.Scatter(x = df['Date '], y = df['Unlocks'])])


# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Phone screen time data set"),  # Display "Hello, World!" on the page
    html.Div(children = [dcc.Graph(figure=xy_graph)]),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],  # Create columns for each DataFrame column
        data=df.to_dict('records'),  # Convert DataFrame to a dictionary for Dash
        style_table={'overflowX': 'auto'},  # Style to make table scrollable if too wide
        page_size=10  # Optional: Limit rows per page
    ),
])
files = os.listdir(path)
# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
