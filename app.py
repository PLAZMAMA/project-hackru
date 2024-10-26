import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to read CSV file
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convert timestamp to datetime
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return pd.DataFrame(columns=["Error"])  # Return an empty DataFrame with an Error column

# Load the CSV data
csv_file_path = './eye_tracking_data.csv'  # Replace with your CSV file path
dataframe = read_csv(csv_file_path)

# Define the layout of the app
layout_children = [
    html.H1("CSV Data Display"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_size=10,  # Adjust page size as needed
        style_table={'overflowX': 'auto'},  # Ensure horizontal scroll for wide tables
    )
]

# Check for an error
if dataframe.empty:
    layout_children.append(html.Div("Error reading the CSV file.", style={'color': 'red'}))
else:
    # Create a count of states over time
    state_columns = ['looking_right', 'looking_left', 'looking_center', 'looking_up', 'looking_down']
    states_counts = dataframe[state_columns].sum().reset_index()
    states_counts.columns = ['State', 'Count']

    # Filter out zero counts
    states_counts = states_counts[states_counts['Count'] > 0]

    # Create a pie chart for the states
    fig_pie = px.pie(
        states_counts,
        title='Counts of Looking States',
        names='State',
        values='Count'
    )

    # Define positions for each looking state
    positions = {
        'looking_left': (-1, 0),
        'looking_right': (1, 0),
        'looking_up': (0, 1),
        'looking_down': (0, -1),
        'looking_center': (0, 0)
    }

    # Prepare data for circular plot
    circle_data = []
    for state in state_columns:
        # Check if the state exists in states_counts
        if state in states_counts['State'].values:
            count = states_counts.loc[states_counts['State'] == state, 'Count'].values[0]
        else:
            count = 0  # Set count to 0 if state is not found

        coords = positions[state]
        circle_data.append({
            'x': coords[0],
            'y': coords[1],
            'state': state,
            'count': count  # Added count for each state
        })

    # Create a scatter plot for looking states
    fig_circle = go.Figure()

    for point in circle_data:
        fig_circle.add_trace(go.Scatter(
            x=[point['x']],
            y=[point['y']],
            mode='markers+text',
            text=point['state'],
            textposition='top center',
            marker=dict(size=point['count'] * 5, line=dict(width=2)),  # Adjust size based on count
            name=point['state']
        ))

    # Set layout for circular plot
    fig_circle.update_layout(
        title='Looking States on Circle',
        xaxis=dict(range=[-1.5, 1.5], title='X Coordinate', zeroline=True, scaleanchor="y"),  # Link x and y axes
        yaxis=dict(range=[-1.5, 1.5], title='Y Coordinate', zeroline=True),
        showlegend=False,
        shapes=[
            dict(type='circle', xref='x', yref='y', x0=-1.2, x1=1.2, y0=-1.2, y1=1.2, line=dict(color='LightSkyBlue', width=2))
        ],
        height=600,  # Optional: Adjust the height if needed
        width=600    # Optional: Adjust the width if needed
    )

    # Add the graphs to the layout
    layout_children.append(dcc.Graph(figure=fig_pie))
    layout_children.append(dcc.Graph(figure=fig_circle))

app.layout = html.Div(children=layout_children)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
