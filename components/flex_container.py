from __future__ import annotations
from typing import List, Dict, Any
from plotly.graph_objs._figure import Figure

"""Flex container that houses graphs"""
class FlexContainer:
    def __init__(self, name: str, graphs: List[Figure], flex_properties: Dict[str, Any]):
        self.graphs = graphs
        # flex properties
        # set id to name

