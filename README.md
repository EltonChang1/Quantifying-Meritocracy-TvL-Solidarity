# Quantifying Meritocracy: Extending "Talent vs. Luck" Model to Incorporate Solidarity

## Overview

This project extends the computational **Talent vs. Luck (TvL)** model to quantitatively examine how solidarity-driven redistributive policies can mitigate economic inequality and enhance social mobility in meritocratic systems.

### Research Question

Does introducing solidarity mechanisms (redistribution policies) into the Talent vs. Luck model reduce economic inequality while maintaining economic productivity and social mobility?

## Key Features

- **Agent-Based Simulation**: Models economic agents with varying talent levels navigating stochastic economic opportunities
- **Solidarity Mechanisms**: Implements multiple redistribution strategies:
  - Fixed redistribution rates
  - Dynamic/adaptive redistribution
  - Progressive taxation
  - Universal basic income (UBI)
  - Targeted educational subsidies
- **Statistical Analysis**: Computes Gini coefficient, mobility indices, and wealth distributions
- **Advanced Experiments**:
  - Fixed vs. variable solidarity rates
  - Dynamic redistribution mechanisms
  - Agent behavioral heterogeneity (tax avoidance)
  - Policy timing effectiveness
  - Multi-dimensional policy combinations
  - Sensitivity analysis

## Project Structure

```
├── src/
│   ├── model/               # Core simulation engine
│   │   ├── agent.py        # Agent class
│   │   ├── simulation.py    # Main simulation runner
│   │   └── solidarity.py    # Redistribution mechanisms
│   ├── metrics/             # Analysis metrics
│   │   └── inequality.py    # Gini, mobility calculations
│   └── utils/               # Utilities
│       └── visualization.py # Plotting and visualization
├── experiments/             # Experiment scripts
│   ├── fixed_solidarity_rates.py
│   ├── dynamic_solidarity.py
│   ├── agent_heterogeneity.py
│   ├── policy_timing.py
│   ├── multi_dimensional_policies.py
│   └── sensitivity_analysis.py
├── tests/                   # Unit tests
├── data/                    # Results and outputs
│   └── results/
├── notebooks/               # Jupyter notebooks for analysis
└── docs/                    # Documentation
```

## Installation

### Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

### Setup

```bash
# Clone or navigate to the project
cd Quantifying-Meritocracy-TvL-Solidarity

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Usage

### Running Experiments

```bash
# Run fixed solidarity rate experiments
python experiments/fixed_solidarity_rates.py

# Run dynamic solidarity experiments
python experiments/dynamic_solidarity.py

# Run agent heterogeneity experiments
python experiments/agent_heterogeneity.py

# Run policy timing experiments
python experiments/policy_timing.py

# Run multi-dimensional policy experiments
python experiments/multi_dimensional_policies.py

# Run sensitivity analysis
python experiments/sensitivity_analysis.py
```

### Quick Start Example

```python
from src.model.simulation import TalentVsLuckSimulation
from src.metrics.inequality import compute_gini_coefficient

# Initialize simulation
sim = TalentVsLuckSimulation(
    n_agents=1000,
    n_iterations=100,
    solidarity_rate=0.25  # 25% redistribution
)

# Run simulation
results = sim.run()

# Analyze results
gini = compute_gini_coefficient(results['wealth_distributions'][-1])
print(f"Final Gini Coefficient: {gini:.3f}")
```

## Experiments Overview

### 1. Fixed Solidarity Rates
Tests redistribution at fixed rates (5%, 15%, 25%, 40%, 60%) to measure baseline inequality reduction.

### 2. Dynamic Solidarity
Implements adaptive redistribution that adjusts based on real-time inequality measures (Gini coefficient threshold).

### 3. Agent Heterogeneity
Introduces heterogeneous behaviors (e.g., tax avoidance, variable productivity) to test policy robustness.

### 4. Policy Timing
Compares preventive interventions (from start) vs. delayed interventions (after inequality threshold reached).

### 5. Multi-Dimensional Policies
Combines multiple solidarity mechanisms (e.g., progressive taxation + educational subsidies).

### 6. Sensitivity Analysis
Tests result stability across varying parameter conditions (talent variability, luck volatility, etc.).

## Key Results

- **Moderate solidarity (25-30%)** effectively reduces inequality (Gini: 0.38) while maintaining productivity
- **Dynamic mechanisms** achieve balanced outcomes with 65% upward mobility for disadvantaged agents
- **Policy timing** matters: preventive interventions significantly outperform reactive measures
- **Multi-dimensional policies** produce the strongest outcomes (Gini: 0.31-0.32, ~70% upward mobility)

## Theoretical Foundation

This research is grounded in:
- Michael Sandel's *The Tyranny of Merit* (2020)
- Pluchino, Biondo, & Rapisarda's Talent vs. Luck model (2018, 2022)
- Rawlsian justice theory and capability approaches
- Engineering education equity research

## Authors

- Elton Chang
- Gerald Moulds

## Citation

```bibtex
@thesis{chang_moulds_2025,
  author = {Chang, Elton and Moulds, Gerald},
  title = {Quantifying Meritocracy: Extending {T}alent vs. {L}uck Model to Incorporate Solidarity},
  school = {UC San Diego},
  year = {2025}
}
```

## References

See [docs/references.md](docs/references.md) for full bibliography.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please follow PEP 8 style guidelines and include tests for new features.

## Contact

For questions or collaboration inquiries, please reach out to the authors.
