from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SimulationParameters:
    # Initial planting strategy
    initial_stocking_density: int
    overstocking_percentage: float
    species_mix: Dict[str, float]

    # Beating up parameters
    beating_up_threshold: int
    beating_up_years: List[int]
    max_beating_up_age: int

    # Financial parameters
    initial_planting_cost: float
    beating_up_cost_base: float
    beating_up_cost_increase: float
    grant_rate_per_hectare: float
    carbon_price_per_tonne: float
    discount_rate: float

    # Environmental parameters
    drought_probability: float
    flood_probability: float
    windthrow_probability: float
    disease_probability: float

    # Regional growth modifiers
    regional_growth_rate: Dict[str, Dict[str, float]]

    # Strategy parameters
    overstocking_strategy: Dict[str, float]
    beating_up_strategy: Dict[str, any]
    early_year_risks: Dict[str, float]
