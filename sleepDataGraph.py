import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

sleep_data = pd.read_csv('./data/sleepdata_2.csv', sep=';')

df_clean = sleep_data[['Start', 'Sleep Quality', 'Steps']]
def sleepDataGraph():
    return (
        dcc.Graph(
        id='scatter plot',
        figure={
            'data': [
                # Line 1
                go.Scatter(
                    x = df_clean['Start'],
                    y = df_clean['Sleep Quality'],
                    mode = 'markers',
                    name='Sleep Quality',
                    yaxis = 'y',
                ),
                go.Scatter(
                    x = df_clean['Start'],
                    y = df_clean['Steps'],
                    mode = 'markers',
                    name = 'Steps per day',
                    marker=dict(color='orange'),
                    yaxis = 'y2'

                )
            ],
            'layout': go.Layout(
                title='Sleep Quality vs Steps in a day',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Sleep Quality'},
                yaxis2 = {
                    'title': 'Steps',
                    'overlaying': 'y',  # Overlay on the primary y-axis
                    'side': 'right',  # Steps on the right side
                    'titlefont': {'color': 'orange'},
                    'tickfont': {'color': 'orange'},
                    'showgrid': False  # Optional: Hide gridlines for clarity
                    },
            )
        }
    )
    ) 