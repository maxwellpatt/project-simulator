# Forest Growth Simulation

A Monte Carlo simulation tool for modeling forest growth, survival, and carbon sequestration under various environmental conditions and management strategies.

## Overview

This project simulates the growth and development of mixed-species forests over time, taking into account various factors such as:
- Environmental risks (drought, flood, windthrow, disease)
- Competition between trees
- Regional growth variations
- Management interventions (beating up)
- Financial considerations

## User Guide

### Key Parameters to Consider

When running the simulation, you may want to adjust these key parameters in `main.py`. Below are the most important parameters grouped by category, with their default values and explanations.

#### 🌳 Site Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `site_area` | 1 | Area of forest in hectares |
| `simulation_years` | 30 | Duration of simulation |
| `num_iterations` | 5 | Number of Monte Carlo iterations (increase for more robust results) |

#### 🌱 Planting Strategy
| Parameter | Default | Description |
|-----------|---------|-------------|
| `initial_stocking_density` | 2500 | Trees per hectare |
| `species_mix` | `{"scots_pine": 0.7, "birch": 0.3}` | Proportion of each species |
| `overstocking_percentage` | 0.2 | Extra trees planted as buffer (20%) |

#### 🌪️ Environmental Risk Factors
| Parameter | Default | Description |
|-----------|---------|-------------|
| `drought_probability` | 0.1 | Annual chance of drought |
| `flood_probability` | 0.05 | Annual chance of flooding |
| `windthrow_probability` | 0.08 | Annual chance of windthrow |
| `disease_probability` | 0.03 | Annual chance of disease |

#### 👨‍🌾 Management Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `beating_up_threshold` | 2000 | Minimum acceptable trees/ha |
| `beating_up_years` | [2,3,4] | Years to perform replanting |
| `beating_up_cost_base` | £2.00 | Cost per replacement tree |
| `max_beating_up_age` | 5 | Maximum age for beating up operations |

#### 💰 Financial Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `initial_planting_cost` | £1.50 | Cost per tree |
| `grant_rate_per_hectare` | £350.00 | Government grant amount |
| `carbon_price_per_tonne` | £20.00 | Carbon credit value |
| `discount_rate` | 0.035 | Annual discount rate (3.5%) |

### Example Scenarios

#### Dry Site Conditions

## Key Features

### Forest Simulation
- Simulates individual tree growth and survival
- Handles multiple tree species (currently Scots Pine and Birch)
- Models competition between neighboring trees
- Tracks forest metrics over time

### Environmental Modeling
- Regional growth rate variations
- Environmental risk factors:
  - Drought
  - Flooding
  - Windthrow
  - Disease
- Early-year vulnerability adjustments

### Management Strategies
- Beating up (replanting) operations
- Overstocking strategies
- Density-dependent resilience
- Cost tracking and financial analysis

## Configuration

The simulation is highly configurable through the `SimulationParameters` class, allowing adjustment of:

- Initial planting strategy (density, species mix)
- Environmental risk probabilities
- Regional growth modifiers
- Management intervention parameters
- Financial parameters
- Early-year risk multipliers

## Usage

Basic usage example:
```python
python
from src.models.simulation_parameters import SimulationParameters
from src.simulation.monte_carlo import ForestSimulation
Configure simulation parameters
params = SimulationParameters(
initial_stocking_density=2500,
overstocking_percentage=0.2,
species_mix={"scots_pine": 0.7, "birch": 0.3},
# ... other parameters
)

# Create and run simulation
simulation = ForestSimulation(params, site_area=1)
results = simulation.run_simulation(num_iterations=1000, years=30)
```
## Output Metrics

The simulation provides detailed metrics including:
- Final stocking density (trees/ha)
- Mean tree height
- Survival rate
- Beating up costs
- Carbon sequestration (tCO2e/ha)

## Technical Details

The simulation uses:
- Monte Carlo methods for risk modeling
- Spatial competition modeling
- Growth rate adjustments based on local conditions
- Financial tracking including grants and carbon pricing

## Requirements

- Python 3.7+
- NumPy
- Logging module

## Future Enhancements

Potential areas for expansion:
- Additional tree species
- More sophisticated growth models
- Climate change scenarios
- Enhanced visualization tools
- Additional management interventions
