from typing import List
from plotly.graph_objs._figure import Figure

class Dashboard:
    # constructor
    def __init__(self, dataframe):
        self.dataframe = dataframe
    
    # any preparation of the dataframe here
    def prepare(self, dataframe) -> None:
        pass
    
    # return list of plotly figures to be rendered
    def render(self) -> List[Figure]:
        return []