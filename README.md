# Quantifying Meritocracy: Extending "Talent vs. Luck" Model to Incorporate Solidarity

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Research](https://img.shields.io/badge/Research-Computational%20Economics-orange.svg)](https://github.com/EltonChang1/Quantifying-Meritocracy-TvL-Solidarity)

## 📊 [**View Complete Results & Analysis →**](RESULTS.md)

---

## Overview

This project consists of **two parts**:

### Part 1: Recreation of "Talent vs. Luck" Model (Pluchino et al., 2018)

A computational validation of the landmark paper ["Talent vs Luck: The Role of Randomness in Success and Failure"](https://www.worldscientific.com/doi/epdf/10.1142/S0219525918500145) by A. Pluchino, A. E. Biondo, and A. Rapisarda.

**Core Finding Reproduced**: The paper demonstrated that the most successful individuals are rarely the most talented. Instead, success is largely determined by lucky events. Our implementation validates this counter-intuitive result through agent-based simulation where 1,000 agents with normally distributed talent navigate random economic opportunities over 40 years of career simulation.

### Part 2: Extension with Solidarity Mechanisms

**Original Research**: Extends the validated TvL model to test whether solidarity-based redistribution policies can correct meritocracy's inherent randomness. Through 6 comprehensive experiments, I demonstrate that:

- **15-25% wealth redistribution reduces inequality by 90%** (Gini: 0.39 → 0.03)
- **Perfect social mobility (100%) becomes achievable** with moderate redistribution
- **Preventive policies dramatically outperform reactive interventions**
- **Results hold even with 60% tax avoidance**, demonstrating real-world applicability

---

## Why This Matters to You

### If you're starting your career...
You might believe your success depends primarily on your talent and hard work. The TvL model shows **the most successful people are rarely the most talented**—instead, they were often in the right place at the right time. Understanding this helps you:
- **Make better career decisions** by seeking luck-rich environments (networking, high-opportunity fields)
- **Reduce self-blame** when setbacks occur—often it's not about your ability
- **Support redistribution policies** that give everyone multiple chances at success

### If you're already successful...
You might attribute your wealth to superior talent. The model reveals **random lucky events account for most extreme success**. This suggests:
- **Moderate taxation (15-25%) is justified** since your wealth resulted partly from chance
- **Redistribution doesn't harm productivity**—simulations show 100% mobility with 25% taxes
- **Supporting solidarity benefits everyone** by creating a resilient economic system

### If you're struggling financially...
You might blame yourself for lacking talent or effort. The evidence shows **talented people often fail due to bad luck**. Solidarity mechanisms:
- **Give you second chances** when random setbacks occur
- **Reduce inequality by 90%** while maintaining economic growth
- **Achieve 100% upward mobility** for those starting with less

---

## Key Features

### Part 1: TvL Model Recreation
- **Agent-Based Simulation**: 1,000 agents with normally distributed talent (μ=0, σ=1)
- **40-Year Career Simulation**: Each iteration represents 6 months of working life
- **Random Lucky/Unlucky Events**: Agents encounter opportunities that amplify or diminish wealth
- **Talent Modulation**: Success probability influenced by talent level (more talent = better exploitation of luck)
- **Validation Metrics**: Reproduces original paper's finding that most successful ≠ most talented

### Part 2: Solidarity Extension
- **Multiple Redistribution Strategies**:
  - Fixed redistribution rates (5%, 15%, 25%, 40%, 60%)
  - Dynamic/adaptive redistribution (responding to inequality thresholds)
  - Progressive taxation
  -Universal Basic Income (UBI)
  - Targeted educational subsidies
- **Comprehensive Metrics**: Gini coefficient, upward mobility rates, wealth concentration
- **Real-World Scenarios**:
  - Tax avoidance behavior (0-60% of agents)
  - Policy timing (preventive vs. reactive)
  - Parameter sensitivity (talent variability, opportunity values)

---

## Project Structure

```
├── src/
│   ├── model/               # Core simulation engine
│   │   ├── agent.py        # Agent class with talent & wealth
│   │   ├── simulation.py    # TvL simulation runner
│   │   └── solidarity.py    # Redistribution mechanisms
│   ├── metrics/             # Analysis metrics
│   │   └── inequality.py    # Gini, mobility calculations
│   └── utils/               # Utilities
│       └── visualization.py # Plotting and visualization
├── experiments/             # 6 solidarity experiments
│   ├── exp_fixed_solidarity_rates.py      # Optimal redistribution rate
│   ├── exp_dynamic_solidarity.py          # Adaptive policies
│   ├── exp_agent_heterogeneity.py         # Tax avoidance
│   ├── exp_policy_timing.py               # Preventive vs. reactive
│   ├── exp_multi_dimensional_policies.py  # Combined mechanisms
│   └── exp_sensitivity_analysis.py        # Parameter robustness
├── tests/                   # Unit tests
├── data/                    # Results and outputs
│   └── results/
├── notebooks/               # Jupyter notebooks for analysis
└── docs/                    # Documentation
```

---

## Key Results: What the Data Reveals

### Finding 1: Luck Dominates Success More Than You Think

![Fixed Solidarity Analysis](data/results/fixed_solidarity/fixed_solidarity_analysis.png)

**What this means for you**: Without redistribution, the system generates massive inequality (Gini: 0.393)—comparable to modern America—even though everyone starts equal and talent is normally distributed. The top 1% holds 7.36% of all wealth. **Your financial outcome depends more on random luck than your abilities.**

**The solution**: Just 15-25% redistribution collapses inequality by 92% (Gini drops to 0.031) while achieving 100% upward mobility. This means:
- If you're talented but unlucky, you get second chances
- If you're lucky, you still thrive while contributing to others' opportunities
- Society wastes less talent due to random setbacks

### Finding 2: Smart Policies Respond to Real-Time Conditions

![Dynamic Solidarity Analysis](data/results/dynamic_solidarity/dynamic_solidarity_analysis.png)

**What this means for you**: Fixed 25% redistribution works well, but **adaptive policies that respond when inequality exceeds thresholds (Gini > 0.50) work 13.5% better**. Think of it like:
- **Interest rates**: Central banks adjust based on inflation data
- **Your savings**: You might save more during uncertain times
- **Solidarity**: Ramp up when inequality spikes, ease when equality improves

**Practical implication**: Vote for politicians who support data-driven, responsive fiscal policies—not rigid ideological positions.

### Finding 3: Redistribution Works Even When People Cheat

![Heterogeneity Analysis](data/results/heterogeneity/heterogeneity_analysis.png)

**What this means for you**: The common objection "rich people will just avoid taxes" is empirically weak. **Even with 60% of agents avoiding taxes, 25% redistribution still achieves 90% inequality reduction** (Gini: 0.036 vs. 0.037 with full compliance).

**Why this matters**: Don't let perfect be the enemy of good. Imperfect enforcement still creates:
- Massively more equal societies
- 100% upward mobility for the disadvantaged
- Economic resilience

### Finding 4: Act Early or Pay the Price

The simulations show **preventive redistribution prevents 50-80 iterations (years) of extreme inequality** compared to reactive policies. Both eventually reach the same final Gini, but waiting means:
- A generation grows up in poverty unnecessarily
- Talent is wasted during high-inequality periods
- Social trust erodes

**Your action**: Support early intervention in your community—universal pre-K, progressive taxation from day one, not crisis-response welfare.

### Finding 5: Simple Beats Complex

Testing progressive taxation, UBI, educational subsidies, and combinations reveals: **Simple flat-rate redistribution (25%) outperforms all sophisticated alternatives**. This is counter-intuitive but important:
- Complex policies create loopholes
- Administrative overhead wastes resources
- Behavioral responses are unpredictable

**Lesson**: Support straightforward wealth transfers over Byzantine tax codes.

---

### Complete Experimental Analysis

See **[RESULTS.md](RESULTS.md)** for:
- Detailed methodology for each experiment
- Full data tables and statistics
- Policy recommendations grounded in evidence
- Theoretical connections to economics and justice literature

---

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

## Quick Results Summary

| Redistribution Rate | Gini Coefficient | Upward Mobility | Mean Wealth | Top 1% Share |
|---------------------|------------------|-----------------|-------------|--------------|
| **0% (No Policy)**  | 0.393 ⚠️        | 64.5%          | 24.73       | 7.36%        |
| **5%**              | 0.125            | 99.0%          | 21.28       | 2.77%        |
| **15%** ⭐          | **0.031** ✅    | **100.0%** ✅  | 20.09       | **1.20%** ✅ |
| **25%** ⭐          | **0.037** ✅    | **100.0%** ✅  | 20.06       | **1.11%** ✅ |
| **40%**             | 0.057            | 100.0%         | 20.16       | 1.20%        |
| **60%**             | 0.088            | 100.0%         | 19.60       | 1.34%        |

**Optimal Zone**: 15-25% redistribution achieves 90%+ inequality reduction while maintaining perfect mobility and stable wealth.

### Key Findings Across All Experiments

✅ **Pure meritocracy generates extreme inequality** (Gini: 0.39) despite equal starting conditions  
✅ **Moderate redistribution is highly effective**: 15-25% achieves near-perfect equality (Gini: 0.03)  
✅ **Preventive policies dominate**: Early intervention prevents 50-80 periods of unnecessary inequality  
✅ **Results are robust**: Findings hold across talent variability, compliance rates, and economic parameters  
✅ **Simple policies work best**: Fixed-rate redistribution outperforms complex multi-mechanism approaches  

📊 **[See Complete Analysis in RESULTS.md →](RESULTS.md)**

## Theoretical Foundation

### Part 1: Based on Validated Science
This project begins by computationally replicating:

**Pluchino, A., Biondo, A. E., & Rapisarda, A. (2018).** ["Talent vs Luck: The Role of Randomness in Success and Failure."](https://www.worldscientific.com/doi/epdf/10.1142/S0219525918500145) *Advances in Complex Systems*, 21(03n04), 1850014.

**Key insight from the original paper**: The most successful individuals are rarely the most talented. Success depends more on the random sequence of lucky/unlucky events encountered during a career than on initial talent levels.

### Part 2: Extends with Justice Theory
The solidarity mechanisms draw from:
- **Michael Sandel** - *The Tyranny of Merit* (2020): Critique of meritocratic hubris
- **John Rawls** - *A Theory of Justice* (1971): Difference principle justifying redistribution
- **Thomas Piketty** - *Capital in the Twenty-First Century* (2013): Empirical inequality dynamics
- **Robert Frank** - *Success and Luck* (2016): Role of contingency in achievement

---

## Author

Elton Chang

## Citation

```bibtex
@software{chang_2026,
  author = {Chang, Elton},
  title = {Quantifying Meritocracy: Extending {T}alent vs. {L}uck Model to Incorporate Solidarity},
  year = {2026},
  url = {https://github.com/EltonChang1/Quantifying-Meritocracy-TvL-Solidarity}
}
```

## References

See [docs/references.md](docs/references.md) for full bibliography.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please follow PEP 8 style guidelines and include tests for new features.

## Contact

For questions or collaboration: [GitHub Issues](https://github.com/EltonChang1/Quantifying-Meritocracy-TvL-Solidarity/issues)
