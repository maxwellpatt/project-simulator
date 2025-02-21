from dataclasses import dataclass
from typing import List

from .tree import Tree


@dataclass
class Forest:
    site_factor: float
    region: str
    soil_type: str
    elevation: float
    mean_annual_temp: float
    mean_annual_rainfall: float

    def __init__(
        self,
        site_factor: float,
        region: str,
        soil_type: str,
        elevation: float,
        mean_annual_temp: float,
        mean_annual_rainfall: float,
    ):
        self.trees: List[Tree] = []
        self.site_factor = site_factor
        self.region = region
        self.soil_type = soil_type
        self.elevation = elevation
        self.mean_annual_temp = mean_annual_temp
        self.mean_annual_rainfall = mean_annual_rainfall
        self.history = []

    def add_tree(self, tree: Tree):
        self.trees.append(tree)
        self.history.append(
            {
                "action": "plant",
                "year": tree.year_planted,
                "species": tree.species,
                "x": tree.x,
                "y": tree.y,
            }
        )
