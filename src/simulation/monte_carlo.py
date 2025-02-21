import random
from typing import List
import logging
import numpy as np

from src.models.forest import Forest
from src.models.tree import Tree
from src.models.simulation_parameters import SimulationParameters

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ForestSimulation:
    def __init__(self, params: SimulationParameters, site_area_hectares: float):
        self.params = params
        self.site_area = site_area_hectares

    def run_simulation(self, num_iterations: int, years: int) -> List[dict]:
        logging.info(f"Starting simulation with {num_iterations} iterations over {years} years")
        results = []

        for i in range(num_iterations):
            if i % 10 == 0:  # Log every 10th iteration
                logging.info(f"Running iteration {i}/{num_iterations}")
            forest = self._initialize_forest()
            yearly_results = self._simulate_years(forest, years)
            results.append(yearly_results)

        logging.info("Simulation completed successfully")
        return results

    def _initialize_forest(self) -> Forest:
        forest = Forest(
            site_factor=random.uniform(0.8, 1.0),
            region="Scotland",  # Could be parameterized
            soil_type="brown_earth",
            elevation=200,
            mean_annual_temp=8.5,
            mean_annual_rainfall=1000,
        )

        # Calculate initial number of trees based on stocking density and overstocking
        base_trees = self.site_area * self.params.initial_stocking_density
        total_trees = base_trees * (1 + self.params.overstocking_percentage)

        # Plant initial trees
        for _ in range(int(total_trees)):
            x = random.uniform(0, self.site_area * 100)  # Convert to meters
            y = random.uniform(0, self.site_area * 100)

            # Select species based on species mix
            species = random.choices(
                list(self.params.species_mix.keys()),
                weights=list(self.params.species_mix.values()),
            )[0]

            tree = Tree(species=species, x=x, y=y, year_planted=0)
            forest.add_tree(tree)

        return forest

    def _simulate_years(self, forest: Forest, years: int) -> dict:
        logging.info(f"Starting yearly simulation for forest with {len(forest.trees)} trees")
        yearly_data = {
            "stocking_density": [],
            "mean_height": [],
            "survival_rate": [],
            "beating_up_costs": [],
            "carbon_sequestration": [],
        }

        for year in range(years):
            if year % 5 == 0:  # Log every 5th year
                logging.info(f"Simulating year {year}/{years}")
                living_trees = len([t for t in forest.trees if t.is_alive])
                logging.debug(f"Current living trees: {living_trees}")

            # Apply environmental risks
            self._apply_environmental_risks(forest, year)
            
            # Grow trees
            self._grow_trees(forest)
            
            # Perform beating up if necessary
            if year in self.params.beating_up_years:
                logging.info(f"Performing beating up in year {year}")
                self._perform_beating_up(forest, year)
            
            # Record yearly statistics
            self._record_statistics(forest, yearly_data)

        return yearly_data

    def _apply_environmental_risks(self, forest: Forest, year: int):
        """Apply environmental risks like drought, flood, windthrow and disease"""
        for tree in forest.trees:
            if not tree.is_alive:
                continue
            
            # Check each environmental risk
            if random.random() < self.params.drought_probability:
                mortality_chance = self.params.early_year_risks["drought_mortality_multiplier"] if year < 5 else 1.0
                if random.random() < (0.3 * mortality_chance):
                    tree.is_alive = False
                
            if random.random() < self.params.flood_probability:
                mortality_chance = self.params.early_year_risks["flood_mortality_multiplier"] if year < 5 else 1.0
                if random.random() < (0.2 * mortality_chance):
                    tree.is_alive = False
                
            if random.random() < self.params.windthrow_probability:
                # Reduce windthrow risk based on stocking density
                density_factor = len([t for t in forest.trees if t.is_alive]) / (self.site_area * self.params.initial_stocking_density)
                resistance = self.params.early_year_risks["density_resilience_factor"] * density_factor
                if random.random() < (0.15 * (1 - resistance)):
                    tree.is_alive = False

    def _grow_trees(self, forest: Forest):
        """Simulate tree growth with competition effects"""
        for tree in forest.trees:
            if not tree.is_alive:
                continue
            
            # Calculate competition from neighboring trees
            neighbors = self._count_neighbors(tree, forest)
            competition_factor = min(0.8, neighbors * self.params.overstocking_strategy["competition_factor"])
            
            # Get regional growth rate
            growth_rate = self.params.regional_growth_rate["Scotland"]["highland"]  # Simplified for now
            
            # Grow the tree
            tree.grow(growth_rate, competition_factor)

    def _count_neighbors(self, tree: Tree, forest: Forest, radius: float = 2.0) -> int:
        """Count number of living trees within radius meters"""
        return sum(
            1 for other in forest.trees
            if other.is_alive 
            and other != tree
            and ((other.x - tree.x)**2 + (other.y - tree.y)**2)**0.5 < radius
        )

    def _perform_beating_up(self, forest: Forest, year: int):
        living_trees = len([t for t in forest.trees if t.is_alive])
        required_trees = self.site_area * self.params.beating_up_threshold
        
        if living_trees < required_trees:
            trees_to_add = int(required_trees - living_trees)
            logging.info(f"Beating up required: adding {trees_to_add} trees in year {year}")
            for _ in range(trees_to_add):
                x = random.uniform(0, self.site_area * 100)
                y = random.uniform(0, self.site_area * 100)
                species = random.choices(
                    list(self.params.species_mix.keys()),
                    weights=list(self.params.species_mix.values())
                )[0]
                new_tree = Tree(species=species, x=x, y=y, year_planted=year)
                new_tree.is_beaten_up = True
                forest.add_tree(new_tree)
            logging.debug(f"Beating up completed. New total: {len(forest.trees)} trees")

    def _record_statistics(self, forest: Forest, yearly_data: dict):
        """Record yearly forest statistics"""
        living_trees = [t for t in forest.trees if t.is_alive]
        
        if not living_trees:  # Avoid division by zero
            yearly_data["stocking_density"].append(0)
            yearly_data["mean_height"].append(0)
            yearly_data["survival_rate"].append(0)
            yearly_data["carbon_sequestration"].append(0)
        else:
            yearly_data["stocking_density"].append(len(living_trees) / self.site_area)
            yearly_data["mean_height"].append(sum(t.height for t in living_trees) / len(living_trees))
            yearly_data["survival_rate"].append(len(living_trees) / len(forest.trees))
            # Simplified carbon calculation
            carbon = sum((t.height * t.diameter * 0.5) for t in living_trees)  # Very basic estimate
            yearly_data["carbon_sequestration"].append(carbon)
        
        # Calculate beating up costs for this year
        beaten_up_trees = len([t for t in living_trees if t.is_beaten_up])
        yearly_data["beating_up_costs"].append(beaten_up_trees * self.params.beating_up_cost_base)
