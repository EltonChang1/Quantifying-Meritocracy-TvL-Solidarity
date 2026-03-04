"""
Experiment 1: Fixed Solidarity Rates
Tests how different fixed redistribution rates affect inequality and mobility.
"""

import numpy as np
import os
from src.model.simulation import TalentVsLuckSimulation
from src.utils.visualization import SimulationVisualizer
from src.metrics.inequality import (
    compute_gini_coefficient,
    compute_income_concentration_ratios,
    compute_mobility_indices
)


def run_fixed_solidarity_experiment(
    redistribution_rates: list = [0.0, 0.05, 0.15, 0.25, 0.40, 0.60],
    n_agents: int = 1000,
    n_iterations: int = 100,
    n_runs: int = 3,
    output_dir: str = "data/results/fixed_solidarity"
):
    """
    Run simulations with fixed redistribution rates.
    
    Args:
        redistribution_rates: List of rates to test
        n_agents: Number of agents
        n_iterations: Number of iterations
        n_runs: Number of runs per rate (for averaging)
        output_dir: Directory to save results
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    results_summary = {
        "redistribution_rates": [],
        "final_gini": [],
        "mean_gini": [],
        "std_gini": [],
        "mean_wealth": [],
        "upward_mobility": [],
        "wealth_concentration_top10": [],
        "top_1_percent": [],
        "top_5_percent": [],
        "top_10_percent": [],
        "top_25_percent": [],
        "bottom_50_percent": [],
    }
    
    print("\n" + "="*80)
    print("EXPERIMENT 1: FIXED SOLIDARITY RATES")
    print("="*80)
    
    for rate in redistribution_rates:
        print(f"\nTesting solidarity rate: {rate:.1%}")
        
        rate_results = {
            "gini_histories": [],
            "final_ginis": [],
            "mean_wealths": [],
            "mobility_rates": [],
        }
        
        for run in range(n_runs):
            print(f"  Run {run+1}/{n_runs}...", end=" ", flush=True)
            
            sim = TalentVsLuckSimulation(
                n_agents=n_agents,
                n_iterations=n_iterations,
                initial_wealth=10.0,
                solidarity_mechanism="fixed",
                solidarity_rate=rate,
                seed=42 + rate*100 + run  # Reproducible but varied seeds
            )
            
            results = sim.run(verbose=False)
            
            rate_results["gini_histories"].append(results['gini_history'])
            rate_results["final_ginis"].append(results['final_gini'])
            rate_results["mean_wealths"].append(results['final_wealth_mean'])
            rate_results["mobility_rates"].append(results['upward_mobility_rate'])
            
            print(f"Gini: {results['final_gini']:.3f}, Mobility: {results['upward_mobility_rate']:.1%}")
        
        # Aggregate results
        avg_final_gini = np.mean(rate_results["final_ginis"])
        avg_mean_gini = np.mean([np.mean(h) for h in rate_results["gini_histories"]])
        std_gini = np.std([np.mean(h) for h in rate_results["gini_histories"]])
        avg_mean_wealth = np.mean(rate_results["mean_wealths"])
        avg_mobility = np.mean(rate_results["mobility_rates"])
        
        # Re-run once more for concentration analysis
        sim_final = TalentVsLuckSimulation(
            n_agents=n_agents,
            n_iterations=n_iterations,
            initial_wealth=10.0,
            solidarity_mechanism="fixed",
            solidarity_rate=rate,
            seed=42
        )
        results_final = sim_final.run(verbose=False)
        
        concentration = compute_income_concentration_ratios(
            results_final['wealth_distributions'][-1]
        )
        
        # Store results
        results_summary["redistribution_rates"].append(rate)
        results_summary["final_gini"].append(avg_final_gini)
        results_summary["mean_gini"].append(avg_mean_gini)
        results_summary["std_gini"].append(std_gini)
        results_summary["mean_wealth"].append(avg_mean_wealth)
        results_summary["upward_mobility"].append(avg_mobility)
        results_summary["wealth_concentration_top10"].append(results_final['wealth_concentration_top10'])
        results_summary["top_1_percent"].append(concentration['top_1_percent'])
        results_summary["top_5_percent"].append(concentration['top_5_percent'])
        results_summary["top_10_percent"].append(concentration['top_10_percent'])
        results_summary["top_25_percent"].append(concentration['top_25_percent'])
        results_summary["bottom_50_percent"].append(concentration['bottom_50_percent'])
        
        print(f"  Average final Gini: {avg_final_gini:.3f}")
        print(f"  Average upward mobility: {avg_mobility:.1%}")
    
    # Save results
    import json
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(results_summary, f, indent=2)
    
    print("\n" + "="*80)
    print("Results saved to:", output_dir)
    print("="*80)
    
    # Create visualizations
    visualizer = SimulationVisualizer()
    
    # Plot: Gini vs Redistribution Rate
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=100)
    
    rates = results_summary["redistribution_rates"]
    
    # Gini
    ax = axes[0, 0]
    ax.plot(rates, results_summary["final_gini"], 'o-', linewidth=2, markersize=8, color='red')
    ax.fill_between(rates,
                     np.array(results_summary["mean_gini"]) - np.array(results_summary["std_gini"]),
                     np.array(results_summary["mean_gini"]) + np.array(results_summary["std_gini"]),
                     alpha=0.3, color='red')
    ax.set_xlabel('Redistribution Rate', fontsize=11)
    ax.set_ylabel('Gini Coefficient', fontsize=11)
    ax.set_title('Inequality vs. Redistribution Rate', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Mean Wealth
    ax = axes[0, 1]
    ax.plot(rates, results_summary["mean_wealth"], 'o-', linewidth=2, markersize=8, color='green')
    ax.set_xlabel('Redistribution Rate', fontsize=11)
    ax.set_ylabel('Mean Wealth', fontsize=11)
    ax.set_title('Average Wealth vs. Redistribution Rate', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Upward Mobility
    ax = axes[1, 0]
    ax.plot(rates, results_summary["upward_mobility"], 'o-', linewidth=2, markersize=8, color='blue')
    ax.set_xlabel('Redistribution Rate', fontsize=11)
    ax.set_ylabel('Upward Mobility Rate', fontsize=11)
    ax.set_title('Social Mobility vs. Redistribution Rate', fontsize=12, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3)
    
    # Wealth Concentration
    ax = axes[1, 1]
    ax.plot(rates, results_summary["top_10_percent"], 'o-', linewidth=2, markersize=8, label='Top 10%', color='purple')
    ax.plot(rates, results_summary["top_25_percent"], 's-', linewidth=2, markersize=8, label='Top 25%', color='orange')
    ax.plot(rates, results_summary["bottom_50_percent"], '^-', linewidth=2, markersize=8, label='Bottom 50%', color='brown')
    ax.set_xlabel('Redistribution Rate', fontsize=11)
    ax.set_ylabel('Wealth Share', fontsize=11)
    ax.set_title('Wealth Distribution vs. Redistribution Rate', fontsize=12, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    fig.suptitle('Fixed Solidarity Rates Analysis', fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fixed_solidarity_analysis.png'), dpi=100, bbox_inches='tight')
    print("\nVisualization saved to:", os.path.join(output_dir, 'fixed_solidarity_analysis.png'))
    
    return results_summary


if __name__ == "__main__":
    results = run_fixed_solidarity_experiment(
        redistribution_rates=[0.0, 0.05, 0.15, 0.25, 0.40, 0.60],
        n_agents=1000,
        n_iterations=100,
        n_runs=3
    )
