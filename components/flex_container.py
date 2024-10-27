from __future__ import annotations
from typing import List
from dash import html
from dash.dcc.Graph import Graph
from plotly.graph_objs._figure import Figure

"""Flex container that houses graphs"""


class FlexContainer:
    def __init__(self, name: str, graphs: List[Graph], className: str):
        self.id = name
        self.graphs = graphs
        self.className = className  # flex-row or flex-col, @see assets/styles.css

    def html(self):
        return html.Div(
            self.graphs,
            className=self.className,
        )
