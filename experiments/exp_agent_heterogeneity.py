"""
Experiment 3: Agent Behavioral Heterogeneity
Tests how heterogeneous agent behaviors (e.g., tax avoidance) affect policy effectiveness.
"""

import numpy as np
import os
import json
import matplotlib.pyplot as plt
from src.model.simulation import TalentVsLuckSimulation


def run_heterogeneity_experiment(
    n_agents: int = 1000,
    n_iterations: int = 100,
    n_runs: int = 3,
    output_dir: str = "data/results/heterogeneity"
):
    """
    Test simulations with varying levels of agent behavioral heterogeneity.
    
    Args:
        n_agents: Number of agents
        n_iterations: Number of iterations
        n_runs: Number of runs (for averaging)
        output_dir: Directory to save results
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Different tax avoidance rates represent behavioral heterogeneity
    tax_avoidance_rates = [0.0, 0.20, 0.40, 0.60]
    solidarity_rates = [0.0, 0.25, 0.50]
    
    results_grid = {}
    
    print("\n" + "="*80)
    print("EXPERIMENT 3: AGENT BEHAVIORAL HETEROGENEITY")
    print("="*80)
    
    for solidarity_rate in solidarity_rates:
        print(f"\nSolidarity Rate: {solidarity_rate:.1%}")
        results_grid[solidarity_rate] = {}
        
        for avoidance_rate in tax_avoidance_rates:
            print(f"  Tax Avoidance Rate: {avoidance_rate:.1%}...", end=" ", flush=True)
            
            final_ginis = []
            mobility_rates = []
            mean_wealths = []
            
            for run in range(n_runs):
                sim = TalentVsLuckSimulation(
                    n_agents=n_agents,
                    n_iterations=n_iterations,
                    initial_wealth=10.0,
                    solidarity_mechanism="fixed",
                    solidarity_rate=solidarity_rate,
                    tax_avoidance_rate=avoidance_rate,
                    seed=200 + run
                )
                
                results = sim.run(verbose=False)
                final_ginis.append(results['final_gini'])
                mobility_rates.append(results['upward_mobility_rate'])
                mean_wealths.append(results['final_wealth_mean'])
            
            results_grid[solidarity_rate][avoidance_rate] = {
                "avg_gini": np.mean(final_ginis),
                "std_gini": np.std(final_ginis),
                "avg_mobility": np.mean(mobility_rates),
                "avg_wealth": np.mean(mean_wealths),
            }
            
            print(f"Gini: {np.mean(final_ginis):.3f}, Mobility: {np.mean(mobility_rates):.1%}")
    
    # Save results
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(results_grid, f, indent=2)
    
    # Visualization: Heatmap
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=100)
    
    for idx, metric in enumerate(['avg_gini', 'avg_mobility']):
        ax = axes[idx]
        
        # Build matrix
        matrix = np.zeros((len(solidarity_rates), len(tax_avoidance_rates)))
        for i, solidarity_rate in enumerate(solidarity_rates):
            for j, avoidance_rate in enumerate(tax_avoidance_rates):
                matrix[i, j] = results_grid[solidarity_rate][avoidance_rate][metric]
        
        im = ax.imshow(matrix, cmap='RdYlGn_r' if metric == 'avg_gini' else 'RdYlGn', aspect='auto')
        
        ax.set_xticks(range(len(tax_avoidance_rates)))
        ax.set_yticks(range(len(solidarity_rates)))
        ax.set_xticklabels([f'{r:.0%}' for r in tax_avoidance_rates])
        ax.set_yticklabels([f'{r:.0%}' for r in solidarity_rates])
        ax.set_xlabel('Tax Avoidance Rate', fontsize=11)
        ax.set_ylabel('Solidarity Rate', fontsize=11)
        
        title = 'Final Gini' if metric == 'avg_gini' else 'Upward Mobility'
        ax.set_title(title, fontsize=12, fontweight='bold')
        
        # Add text annotations
        for i in range(len(solidarity_rates)):
            for j in range(len(tax_avoidance_rates)):
                text = ax.text(j, i, f'{matrix[i, j]:.2f}',
                             ha="center", va="center", color="black", fontsize=10)
        
        plt.colorbar(im, ax=ax)
    
    fig.suptitle('Agent Heterogeneity Analysis', fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, 'heterogeneity_analysis.png'), dpi=100, bbox_inches='tight')
    
    print("\n" + "="*80)
    print("Results saved to:", output_dir)
    print("="*80)
    
    return results_grid


if __name__ == "__main__":
    results = run_heterogeneity_experiment()
