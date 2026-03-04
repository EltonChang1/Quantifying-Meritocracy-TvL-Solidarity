"""
Experiment 5: Multi-Dimensional Solidarity Mechanisms
Tests combinations of multiple solidarity policies.
"""

import numpy as np
import os
import json
import matplotlib.pyplot as plt
from src.model.simulation import TalentVsLuckSimulation


def run_multi_dimensional_experiment(
    n_agents: int = 1000,
    n_iterations: int = 100,
    n_runs: int = 3,
    output_dir: str = "data/results/multi_dimensional"
):
    """
    Test combined solidarity mechanisms.
    
    Args:
        n_agents: Number of agents
        n_iterations: Number of iterations
        n_runs: Number of runs (for averaging)
        output_dir: Directory to save results
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    scenarios = {
        "No Solidarity": {"mechanism": "none", "rate": 0.0},
        "Fixed Redistribution (25%)": {"mechanism": "fixed", "rate": 0.25},
        "Progressive Taxation": {"mechanism": "progressive", "rate": 0.25},
        "Universal Basic Income": {"mechanism": "ubi", "rate": 2.5},  # Fixed UBI amount
        "Multi-Dimensional": {"mechanism": "multi", "rate": 0.15},
    }
    
    results_summary = {}
    
    print("\n" + "="*80)
    print("EXPERIMENT 5: MULTI-DIMENSIONAL SOLIDARITY MECHANISMS")
    print("="*80)
    
    for scenario_name, scenario_config in scenarios.items():
        print(f"\nTesting: {scenario_name}")
        
        final_ginis = []
        mobility_rates = []
        mean_wealths = []
        top10_shares = []
        
        for run in range(n_runs):
            print(f"  Run {run+1}/{n_runs}...", end=" ", flush=True)
            
            sim = TalentVsLuckSimulation(
                n_agents=n_agents,
                n_iterations=n_iterations,
                initial_wealth=10.0,
                solidarity_mechanism=scenario_config["mechanism"],
                solidarity_rate=scenario_config["rate"],
                seed=400 + run
            )
            
            results = sim.run(verbose=False)
            
            final_ginis.append(results['final_gini'])
            mobility_rates.append(results['upward_mobility_rate'])
            mean_wealths.append(results['final_wealth_mean'])
            top10_shares.append(results['wealth_concentration_top10'])
            
            print(f"Gini: {results['final_gini']:.3f}, Mobility: {results['upward_mobility_rate']:.1%}")
        
        results_summary[scenario_name] = {
            "final_gini": np.mean(final_ginis),
            "final_gini_std": np.std(final_ginis),
            "upward_mobility": np.mean(mobility_rates),
            "upward_mobility_std": np.std(mobility_rates),
            "mean_wealth": np.mean(mean_wealths),
            "top10_share": np.mean(top10_shares),
        }
    
    # Save results
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(results_summary, f, indent=2)
    
    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=100)
    
    scenario_names = list(results_summary.keys())
    
    # Final Gini
    ax = axes[0, 0]
    final_ginis = [results_summary[name]['final_gini'] for name in scenario_names]
    stds = [results_summary[name]['final_gini_std'] for name in scenario_names]
    ax.bar(range(len(scenario_names)), final_ginis, color='steelblue', alpha=0.7, edgecolor='black')
    ax.errorbar(range(len(scenario_names)), final_ginis, yerr=stds, fmt='none', color='black', capsize=5)
    ax.set_ylabel('Final Gini', fontsize=11)
    ax.set_title('Final Inequality', fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=25, ha='right', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Upward Mobility
    ax = axes[0, 1]
    mobility_rates = [results_summary[name]['upward_mobility'] for name in scenario_names]
    mobility_stds = [results_summary[name]['upward_mobility_std'] for name in scenario_names]
    ax.bar(range(len(scenario_names)), mobility_rates, color='green', alpha=0.7, edgecolor='black')
    ax.errorbar(range(len(scenario_names)), mobility_rates, yerr=mobility_stds, fmt='none', color='black', capsize=5)
    ax.set_ylabel('Upward Mobility Rate', fontsize=11)
    ax.set_title('Social Mobility', fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=25, ha='right', fontsize=9)
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3, axis='y')
    
    # Mean Wealth
    ax = axes[1, 0]
    mean_wealths = [results_summary[name]['mean_wealth'] for name in scenario_names]
    ax.bar(range(len(scenario_names)), mean_wealths, color='orange', alpha=0.7, edgecolor='black')
    ax.set_ylabel('Mean Wealth', fontsize=11)
    ax.set_title('Average Wealth', fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=25, ha='right', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Top 10% Share
    ax = axes[1, 1]
    top10_shares = [results_summary[name]['top10_share'] for name in scenario_names]
    ax.bar(range(len(scenario_names)), top10_shares, color='purple', alpha=0.7, edgecolor='black')
    ax.set_ylabel('Wealth Share', fontsize=11)
    ax.set_title('Top 10% Wealth Share', fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=25, ha='right', fontsize=9)
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('Multi-Dimensional Solidarity Analysis', fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, 'multi_dimensional_analysis.png'), dpi=100, bbox_inches='tight')
    
    print("\n" + "="*80)
    print("Results saved to:", output_dir)
    print("="*80)
    
    return results_summary


if __name__ == "__main__":
    results = run_multi_dimensional_experiment()
