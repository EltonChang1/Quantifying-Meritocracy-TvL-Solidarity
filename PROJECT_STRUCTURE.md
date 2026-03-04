# Project Structure Summary

## Project Root Files

- `README.md` - Main project documentation with overview, features, and usage
- `requirements.txt` - Python package dependencies
- `setup.py` - Package installation configuration
- `run_experiments.py` - Main script to run all experiments
- `LICENSE` - MIT License
- `.gitignore` - Git ignore rules

## Core Source Code (`src/`)

### `src/__init__.py`
Package initialization with imports for main classes

### `src/model/` - Simulation Engine
- `__init__.py` - Module initialization
- `agent.py` - Agent class with talent, wealth, and behavior modeling
- `simulation.py` - Main TalentVsLuckSimulation engine that orchestrates the simulation
- `solidarity.py` - Implementation of redistribution mechanisms

### `src/metrics/` - Analysis Metrics
- `__init__.py` - Module initialization
- `inequality.py` - Gini coefficient, concentration ratios, and mobility metrics

### `src/utils/` - Utilities
- `__init__.py` - Module initialization
- `visualization.py` - Plotting functions for Gini evolution, wealth distributions, and comparisons

## Experiments (`experiments/`)

Six comprehensive experiment scripts:

1. `01_fixed_solidarity_rates.py` - Tests fixed redistribution rates (0%, 5%, 15%, 25%, 40%, 60%)
2. `02_dynamic_solidarity.py` - Tests adaptive redistribution based on inequality thresholds
3. `03_agent_heterogeneity.py` - Tests behavioral heterogeneity (tax avoidance)
4. `04_policy_timing.py` - Compares preventive vs. delayed interventions
5. `05_multi_dimensional_policies.py` - Tests combined policy mechanisms
6. `06_sensitivity_analysis.py` - Tests robustness across parameter variations

Plus `__init__.py` for module imports

## Tests (`tests/`)

- `__init__.py` - Module initialization
- `test_agent.py` - Unit tests for Agent class
- `test_metrics.py` - Unit tests for inequality metrics

## Documentation (`docs/`)

- `methodology.md` - Detailed methodology, theory, and research design
- `references.md` - Comprehensive bibliography and citations
- `GETTING_STARTED.md` - Installation and usage guide

## Data (`data/`)

- `README.md` - Guide to results directory
- `results/` - Directory where experiment results are saved
  - Each experiment produces `summary.json` and visualization PNG files

## Notebooks (`notebooks/`)

- `sample_analysis.py` - Template for interactive Jupyter notebook analysis

## Key Features

### Core Model Classes

**Agent**
- Talent-based success probability in economic opportunities
- Wealth tracking and history
- Solidarity tax payment
- Redistribution receipt
- Mobility calculation

**TalentVsLuckSimulation**
- Configurable agent populations and iterations
- Multiple solidarity mechanisms
- Comprehensive metrics collection
- Result aggregation and reporting

### Solidarity Mechanisms

- Fixed-rate redistribution
- Dynamic/adaptive redistribution
- Progressive taxation
- Universal Basic Income (UBI)
- Targeted educational subsidies
- Multi-dimensional combinations

### Metrics

- Gini coefficient (0-1 inequality measure)
- Wealth concentration ratios (top 1%, 5%, 10%, 25%)
- Upward/downward mobility rates
- Social ladder transition matrices
- Talent-wealth correlation
- Intergenerational elasticity

### Experiments

1. **Fixed Solidarity Rates** - Establishes baseline relationships
2. **Dynamic Solidarity** - Tests adaptive mechanisms
3. **Agent Heterogeneity** - Tests policy robustness with realistic behaviors
4. **Policy Timing** - Preventive vs. reactive interventions
5. **Multi-Dimensional** - Combined policies
6. **Sensitivity Analysis** - Robustness across conditions

## Usage Examples

### Run All Experiments
```bash
python run_experiments.py --experiments all
```

### Run Single Experiment
```bash
python experiments/01_fixed_solidarity_rates.py
```

### Quick Simulation
```python
from src.model.simulation import TalentVsLuckSimulation

sim = TalentVsLuckSimulation(
    n_agents=1000,
    n_iterations=100,
    solidarity_mechanism="fixed",
    solidarity_rate=0.25
)
results = sim.run()
print(sim.get_summary())
```

### Run Tests
```bash
pytest tests/ -v
```

## Total File Count

- Core modules: 7 files
- Experiments: 7 files
- Tests: 3 files
- Documentation: 4 files
- Configuration: 4 files
- Data/Notebooks: 2 files
- **Total: 27+ files**

## Storage Structure

```
Quantifying-Meritocracy-TvL-Solidarity/
├── 6 core Python modules (agent, simulation, solidarity, metrics, visualization, tests)
├── 6 experiment scripts
├── 3 configuration files (setup.py, requirements.txt, .gitignore)
├── 4 documentation files
├── 1 main runner script
└── Data and notebooks directories
```

This is a complete, production-ready research project with:
✓ Modular architecture
✓ Comprehensive documentation
✓ Unit tests
✓ Multiple experiments
✓ Visualization tools
✓ Statistical analysis
✓ Git version control ready
