# Getting Started Guide

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Navigate to Project

```bash
cd Quantifying-Meritocracy-TvL-Solidarity
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "from src.model.simulation import TalentVsLuckSimulation; print('✓ Installation successful!')"
```

## Quick Start

### Run a Single Simulation

```python
from src.model.simulation import TalentVsLuckSimulation

# Create simulation
sim = TalentVsLuckSimulation(
    n_agents=1000,
    n_iterations=100,
    solidarity_mechanism="fixed",
    solidarity_rate=0.25  # 25% redistribution
)

# Run simulation
results = sim.run()

# View results
print(sim.get_summary())
```

### Run All Experiments

```bash
# Full run (takes 5-10 minutes)
python run_experiments.py --experiments all

# Quick run (takes 1-2 minutes)
python run_experiments.py --experiments all --quick

# Specific experiment
python run_experiments.py --experiments fixed dynamic
```

### Run Individual Experiments

```bash
# Experiment 1: Fixed Solidarity Rates
python experiments/01_fixed_solidarity_rates.py

# Experiment 2: Dynamic Solidarity
python experiments/02_dynamic_solidarity.py

# Experiment 3: Agent Heterogeneity
python experiments/03_agent_heterogeneity.py

# Experiment 4: Policy Timing
python experiments/04_policy_timing.py

# Experiment 5: Multi-Dimensional Policies
python experiments/05_multi_dimensional_policies.py

# Experiment 6: Sensitivity Analysis
python experiments/06_sensitivity_analysis.py
```

## Project Structure

```
Quantifying-Meritocracy-TvL-Solidarity/
├── README.md                  # Project overview
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── run_experiments.py         # Main experiment runner
├── src/                       # Source code
│   ├── model/                # Core simulation modules
│   │   ├── agent.py         # Agent class
│   │   ├── simulation.py     # Main simulation engine
│   │   └── solidarity.py     # Redistribution mechanisms
│   ├── metrics/             # Measurement and analysis
│   │   └── inequality.py    # Inequality metrics
│   └── utils/               # Utilities
│       └── visualization.py # Plotting functions
├── experiments/             # Individual experiment scripts
│   ├── 01_fixed_solidarity_rates.py
│   ├── 02_dynamic_solidarity.py
│   ├── 03_agent_heterogeneity.py
│   ├── 04_policy_timing.py
│   ├── 05_multi_dimensional_policies.py
│   └── 06_sensitivity_analysis.py
├── tests/                   # Unit tests
│   ├── test_agent.py
│   └── test_metrics.py
├── data/                    # Results and outputs
│   └── results/
└── docs/                    # Documentation
    ├── methodology.md
    └── references.md
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agent.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Interpreting Results

### Output Files

Each experiment produces:
- `summary.json`: Numerical results
- `{experiment_name}_analysis.png`: Visualization

### Key Metrics

**Gini Coefficient**
- Range: 0 to 1
- 0 = perfect equality
- 1 = maximum inequality
- < 0.30 = very equal
- 0.30-0.40 = relatively equal
- 0.40-0.50 = moderate
- > 0.50 = very unequal

**Upward Mobility**
- Percentage of agents improving their wealth
- Higher = better social mobility
- Target: > 60%

**Wealth Concentration**
- What percentage of total wealth top X% hold
- Top 10% should hold < 50% in equal societies
- Bottom 50% should hold > 20%

## Common Tasks

### Visualize Experiment Results

```python
from src.utils.visualization import SimulationVisualizer
from src.model.simulation import TalentVsLuckSimulation
import json

# Load results
with open('data/results/fixed/summary.json') as f:
    results = json.load(f)

# Create visualizer
viz = SimulationVisualizer(figsize=(14, 8))

# Plot comparisons
results_dict = {
    "No Solidarity": {"gini_history": results['gini_history'][0]},
    "25% Redistribution": {"gini_history": results['gini_history'][5]},
}
viz.plot_gini_evolution(results_dict)
```

### Compare Two Scenarios

```python
from src.model.simulation import TalentVsLuckSimulation

# Scenario 1: No redistribution
sim1 = TalentVsLuckSimulation(
    solidarity_mechanism="none",
    solidarity_rate=0.0
)
results1 = sim1.run()

# Scenario 2: 25% redistribution
sim2 = TalentVsLuckSimulation(
    solidarity_mechanism="fixed",
    solidarity_rate=0.25
)
results2 = sim2.run()

# Compare
print(sim1.compare_with(sim2))
```

### Export Results to CSV

```python
import pandas as pd
import json

# Load results
with open('data/results/multi_dimensional/summary.json') as f:
    results = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(results)
df.to_csv('results_export.csv', index=False)
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError: No module named 'src'`:

```bash
# Make sure you're running from project root
cd /path/to/Quantifying-Meritocracy-TvL-Solidarity

# Activate virtual environment
source venv/bin/activate
```

### Memory Issues

For large simulations, reduce parameters:

```python
sim = TalentVsLuckSimulation(
    n_agents=500,        # Reduce from 1000
    n_iterations=50,     # Reduce from 100
)
```

### Slow Performance

- Reduce `n_agents` or `n_iterations`
- Use `--quick` flag for experiments
- Run individual experiments instead of all

## Next Steps

1. **Explore Results**: Check `data/results/` for experiment outputs
2. **Read Documentation**: See `docs/methodology.md` for detailed theory
3. **Modify Simulations**: Edit simulations to test new hypotheses
4. **Contribute**: Add new experiment designs or features

## Support

For questions or issues:
- Check the main `README.md`
- Review documentation in `docs/`
- Examine test files for usage examples
- Run experiments with `--quick` flag to test functionality

Happy researching!
