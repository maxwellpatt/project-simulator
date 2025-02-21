from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Tree:
    species: str
    x: float
    y: float
    year_planted: int

    def __init__(self, species: str, x: float, y: float, year_planted: int):
        self.species = species
        self.x = x
        self.y = y
        self.year_planted = year_planted
        self.age = 0
        self.height = 0.3  # Initial seedling height in meters
        self.diameter = 0.01  # Initial diameter in meters
        self.is_alive = True
        self.is_beaten_up = False

    def grow(self, growth_rate: float, competition_factor: float):
        if not self.is_alive:
            return

        # Basic growth model
        self.age += 1
        self.height += 0.5 * growth_rate * (1 - competition_factor)
        self.diameter += 0.005 * growth_rate * (1 - competition_factor)
