from typing import List
import plotly.express as px
from plotly.graph_objs._figure import Figure

class EyeTrackingDashboard:
    def __init__(self, dataframe) -> None:
        self.dataframe = dataframe

        self.prepare(dataframe)

    def prepare(self, dataframe) -> None:
        # Create a count of states over time
        self.state_columns = ['looking_right', 'looking_left', 'looking_center', 'looking_up', 'looking_down']
        self.states_counts = dataframe[self.state_columns].sum().reset_index()
        self.states_counts.columns = ['State', 'Count']

        # Filter out zero counts
        self.states_counts = self.states_counts[self.states_counts['Count'] > 0]
    
    def render_pie(self) -> Figure:
        # Create a pie chart for the states
        fig_pie = px.pie(
            self.states_counts,
            title='Counts of Looking States',
            names='State',
            values='Count'
        )

        return fig_pie

    def render(self) -> List[Figure]:
        graphs = []
        graphs.append(self.render_pie())
        return graphs