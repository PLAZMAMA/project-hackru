import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import dashboards
from dashboards.eye_tracking import EyeTrackingDashboard

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = [
    html.H1("CSV Data Display"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=eye_tracking_df.to_dict('records'),
        page_size=10,  # Adjust page size as needed
        style_table={'overflowX': 'auto'},  # Ensure horizontal scroll for wide tables
    )
]

# Function to read CSV file
def read_eye_tracking_csv(file_path = './data/eye_tracking_data.csv'):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convert timestamp to datetime
    return df

# Load the CSV data
eye_tracking_df = read_eye_tracking_csv()

# Define the layout of the app

# Check for an error
if dataframe.empty:
    layout_children.append(html.Div("Error reading the CSV file.", style={'color': 'red'}))
else:
    # Import dashboards
    dashboards = [
        EyeTrackingDashboard(dataframe)
    ]

    # Render the graphs in each dashboard to the layout
    for dashboard in dashboards:
        rendered_graphs = dashboard.render()
        for rendered_graph in rendered_graphs:
            layout_children.append(dcc.Graph(figure=rendered_graph))
    


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
