"""
Sample Jupyter notebook for interactive exploration of simulation results.
This file is meant to be used as a template for Jupyter notebook analysis.

To use:
1. Create a new Jupyter notebook
2. Copy code cells from this file
3. Run cells interactively
"""

# %%
# Import required libraries
import numpy as np
import matplotlib.pyplot as plt
import json
from src.model.simulation import TalentVsLuckSimulation
from src.utils.visualization import SimulationVisualizer
from src.metrics.inequality import compute_gini_coefficient, compute_income_concentration_ratios

# %%
# Run a single simulation with visualization
print("Running single simulation...")
sim = TalentVsLuckSimulation(
    n_agents=1000,
    n_iterations=100,
    solidarity_mechanism="fixed",
    solidarity_rate=0.25,
    seed=42
)

results = sim.run()
print(sim.get_summary())

# %%
# Plot Gini evolution
plt.figure(figsize=(12, 5))
plt.plot(results['gini_history'], linewidth=2, color='steelblue')
plt.xlabel('Iteration', fontsize=12)
plt.ylabel('Gini Coefficient', fontsize=12)
plt.title('Gini Coefficient Evolution Over Time', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Plot wealth distribution
plt.figure(figsize=(12, 5))
wealth_dist = results['wealth_distributions'][-1]
plt.hist(wealth_dist, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
plt.xlabel('Wealth', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title(f'Final Wealth Distribution (Gini: {results["final_gini"]:.3f})', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# %%
# Compare different solidarity rates
print("Comparing different solidarity rates...")
scenarios = {
    "No Redistribution (0%)": {"mechanism": "fixed", "rate": 0.0},
    "Low Redistribution (15%)": {"mechanism": "fixed", "rate": 0.15},
    "Moderate Redistribution (25%)": {"mechanism": "fixed", "rate": 0.25},
    "High Redistribution (40%)": {"mechanism": "fixed", "rate": 0.40},
}

comparison_results = {}
for scenario_name, config in scenarios.items():
    sim = TalentVsLuckSimulation(
        n_agents=1000,
        n_iterations=100,
        solidarity_mechanism=config["mechanism"],
        solidarity_rate=config["rate"],
        seed=42
    )
    comparison_results[scenario_name] = sim.run()
    print(f"{scenario_name}: Gini = {comparison_results[scenario_name]['final_gini']:.3f}, "
          f"Mobility = {comparison_results[scenario_name]['upward_mobility_rate']:.1%}")

# %%
# Visualize comparison
fig, axes = plt.subplots(1, 3, figsize=(16, 4))

# Gini comparison
scenario_names = list(comparison_results.keys())
gini_values = [comparison_results[name]['final_gini'] for name in scenario_names]
mobility_values = [comparison_results[name]['upward_mobility_rate'] for name in scenario_names]
wealth_values = [comparison_results[name]['final_wealth_mean'] for name in scenario_names]

axes[0].bar(range(len(scenario_names)), gini_values, color='steelblue', alpha=0.7, edgecolor='black')
axes[0].set_ylabel('Final Gini', fontsize=11)
axes[0].set_title('Inequality', fontsize=12, fontweight='bold')
axes[0].set_xticks(range(len(scenario_names)))
axes[0].set_xticklabels(scenario_names, rotation=20, ha='right', fontsize=9)
axes[0].grid(True, alpha=0.3, axis='y')

axes[1].bar(range(len(scenario_names)), mobility_values, color='green', alpha=0.7, edgecolor='black')
axes[1].set_ylabel('Upward Mobility', fontsize=11)
axes[1].set_title('Social Mobility', fontsize=12, fontweight='bold')
axes[1].set_xticks(range(len(scenario_names)))
axes[1].set_xticklabels(scenario_names, rotation=20, ha='right', fontsize=9)
axes[1].set_ylim([0, 1])
axes[1].grid(True, alpha=0.3, axis='y')

axes[2].bar(range(len(scenario_names)), wealth_values, color='orange', alpha=0.7, edgecolor='black')
axes[2].set_ylabel('Mean Wealth', fontsize=11)
axes[2].set_title('Average Wealth', fontsize=12, fontweight='bold')
axes[2].set_xticks(range(len(scenario_names)))
axes[2].set_xticklabels(scenario_names, rotation=20, ha='right', fontsize=9)
axes[2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# %%
# Analyze individual agents
print("\nAnalyzing individual agent outcomes...")
mobility_data = comparison_results["Moderate Redistribution (25%)"]["mobility_data"]

# Sample some agents
print("\nSample agents (with 25% redistribution):")
for agent in mobility_data[:5]:
    print(f"  Agent {agent['agent_id']}: "
          f"Talent={agent['talent']:.2f}, "
          f"Initial={agent['initial_wealth']:.2f}, "
          f"Final={agent['final_wealth']:.2f}, "
          f"Upward Mobility: {agent['upward_mobility']}")

# %%
# Calculate concentration ratios
print("\nWealth concentration analysis...")
final_wealth_moderate = comparison_results["Moderate Redistribution (25%)"]["wealth_distributions"][-1]
final_wealth_none = comparison_results["No Redistribution (0%)"]["wealth_distributions"][-1]

conc_moderate = compute_income_concentration_ratios(final_wealth_moderate)
conc_none = compute_income_concentration_ratios(final_wealth_none)

print("\nWith 25% redistribution:")
for metric, value in conc_moderate.items():
    print(f"  {metric}: {value:.1%}")

print("\nWith no redistribution:")
for metric, value in conc_none.items():
    print(f"  {metric}: {value:.1%}")

# %%
# Save comparison results
import json

output = {
    scenario_name: {
        "final_gini": comparison_results[scenario_name]['final_gini'],
        "upward_mobility_rate": comparison_results[scenario_name]['upward_mobility_rate'],
        "final_wealth_mean": comparison_results[scenario_name]['final_wealth_mean'],
        "wealth_concentration_top10": comparison_results[scenario_name]['wealth_concentration_top10'],
    }
    for scenario_name in scenario_names
}

with open('sample_analysis_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Results saved to sample_analysis_results.json")

# %%
print("Analysis complete!")
