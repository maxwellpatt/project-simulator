from src.models.simulation_parameters import SimulationParameters
from src.simulation.monte_carlo import ForestSimulation
import logging


def main():
    logging.info("Initializing forest simulation")
    # Define simulation parameters
    params = SimulationParameters(
        # Initial planting strategy
        initial_stocking_density=2500,  # trees per hectare
        overstocking_percentage=0.2,  # 20% extra trees
        species_mix={"scots_pine": 0.7, "birch": 0.3},
        # Beating up parameters
        beating_up_threshold=2000,  # minimum acceptable trees/ha
        beating_up_years=[2, 3, 4],  # years to perform beating up
        max_beating_up_age=5,
        # Financial parameters
        initial_planting_cost=1.50,  # £ per tree
        beating_up_cost_base=2.00,  # £ per tree
        beating_up_cost_increase=0.15,  # 15% increase per year
        grant_rate_per_hectare=350.00,  # £ per hectare
        carbon_price_per_tonne=20.00,  # £ per tonne CO2
        discount_rate=0.035,  # 3.5%
        # Environmental parameters
        drought_probability=0.1,
        flood_probability=0.05,
        windthrow_probability=0.08,
        disease_probability=0.03,
        # Regional growth modifiers
        regional_growth_rate={
            "Scotland": {"highland": 0.7, "lowland": 0.85, "beating_up_window": 3},
            "SouthEngland": {"lowland": 1.2, "beating_up_window": 1},
        },
        # Strategy parameters
        overstocking_strategy={
            "enabled": True,
            "initial_surplus": 0.2,
            "expected_mortality": 0.15,
            "competition_factor": 0.1,
        },
        beating_up_strategy={
            "timing": "early",
            "max_age_difference": 2,
            "competition_threshold": 0.8,
            "cost_increase_per_year": 0.15,
        },
        early_year_risks={
            "drought_mortality_multiplier": 1.5,
            "flood_mortality_multiplier": 1.3,
            "disease_spread_rate": 0.1,
            "density_resilience_factor": 0.2,
        },
    )

    # Define simulation size first
    site_area = 1  # hectares
    logging.info(f"Creating simulation instance for {site_area} hectares")
    simulation = ForestSimulation(params, site_area)

    # Define simulation duration
    num_iterations = 5
    simulation_years = 30
    logging.info(f"Running simulation: {num_iterations} iterations for {simulation_years} years")
    results = simulation.run_simulation(num_iterations, simulation_years)

    logging.info("Processing final results")
    # Print some basic statistics
    print("\nSimulation Results:")
    print("-" * 50)

    # Calculate averages across all iterations for the final year
    final_year_stats = {
        key: sum(iter_result[key][-1] for iter_result in results) / num_iterations
        for key in results[0].keys()
    }

    print(
        f"After {simulation_years} years (averaged over {num_iterations} iterations):"
    )
    print(
        f"Final stocking density: {final_year_stats['stocking_density']:.0f} trees/ha"
    )
    print(f"Mean tree height: {final_year_stats['mean_height']:.1f} m")
    print(f"Survival rate: {final_year_stats['survival_rate']:.1%}")
    print(f"Total beating up costs: £{final_year_stats['beating_up_costs']:.2f}/ha")
    print(
        f"Carbon sequestered: {final_year_stats['carbon_sequestration']:.1f} tCO2e/ha"
    )


if __name__ == "__main__":
    main()
