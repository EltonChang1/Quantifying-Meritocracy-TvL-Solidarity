"""
Experiment 2: Dynamic Solidarity Mechanisms
Tests adaptive redistribution that adjusts based on real-time inequality.
"""

import numpy as np
import os
import json
import matplotlib.pyplot as plt
from src.model.simulation import TalentVsLuckSimulation
from src.metrics.inequality import compute_income_concentration_ratios


def run_dynamic_solidarity_experiment(
    n_agents: int = 1000,
    n_iterations: int = 100,
    n_runs: int = 3,
    output_dir: str = "data/results/dynamic_solidarity"
):
    """
    Run simulations with dynamic redistribution.
    
    Args:
        n_agents: Number of agents
        n_iterations: Number of iterations
        n_runs: Number of runs (for averaging)
        output_dir: Directory to save results
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    scenarios = {
        "No Solidarity": {"mechanism": "none", "rate": 0.0},
        "Fixed 25%": {"mechanism": "fixed", "rate": 0.25},
        "Dynamic (Threshold 0.50)": {"mechanism": "dynamic", "rate": 0.25},
    }
    
    results_summary = {}
    
    print("\n" + "="*80)
    print("EXPERIMENT 2: DYNAMIC SOLIDARITY MECHANISMS")
    print("="*80)
    
    for scenario_name, scenario_config in scenarios.items():
        print(f"\nTesting: {scenario_name}")
        
        scenario_results = {
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
                solidarity_mechanism=scenario_config["mechanism"],
                solidarity_rate=scenario_config["rate"],
                seed=100 + run
            )
            
            results = sim.run(verbose=False)
            
            scenario_results["gini_histories"].append(results['gini_history'])
            scenario_results["final_ginis"].append(results['final_gini'])
            scenario_results["mean_wealths"].append(results['final_wealth_mean'])
            scenario_results["mobility_rates"].append(results['upward_mobility_rate'])
            
            print(f"Gini: {results['final_gini']:.3f}, Mobility: {results['upward_mobility_rate']:.1%}")
        
        # Aggregate
        avg_final_gini = np.mean(scenario_results["final_ginis"])
        avg_mean_gini = np.mean([np.mean(h) for h in scenario_results["gini_histories"]])
        std_gini = np.std([np.mean(h) for h in scenario_results["gini_histories"]])
        avg_mobility = np.mean(scenario_results["mobility_rates"])
        
        results_summary[scenario_name] = {
            "final_gini": avg_final_gini,
            "mean_gini": avg_mean_gini,
            "std_gini": std_gini,
            "upward_mobility": avg_mobility,
            "gini_histories": [h.tolist() if isinstance(h, np.ndarray) else h for h in scenario_results["gini_histories"]],
        }
    
    # Save results
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(results_summary, f, indent=2)
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=100)
    
    # Gini evolution comparison
    ax = axes[0]
    for scenario_name, results in results_summary.items():
        # Use first run's history as representative
        gini_history = results['gini_histories'][0]
        ax.plot(gini_history, label=scenario_name, linewidth=2)
    
    ax.set_xlabel('Iteration', fontsize=11)
    ax.set_ylabel('Gini Coefficient', fontsize=11)
    ax.set_title('Gini Coefficient Evolution', fontsize=12, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Final Gini comparison
    ax = axes[1]
    scenario_names = list(results_summary.keys())
    final_ginis = [results_summary[name]['final_gini'] for name in scenario_names]
    mobility_rates = [results_summary[name]['upward_mobility'] for name in scenario_names]
    
    x = np.arange(len(scenario_names))
    width = 0.35
    
    ax.bar(x - width/2, final_ginis, width, label='Final Gini', color='steelblue')
    ax.bar(x + width/2, mobility_rates, width, label='Upward Mobility', color='orange')
    
    ax.set_ylabel('Value', fontsize=11)
    ax.set_title('Inequality and Mobility Comparison', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('Dynamic Solidarity Analysis', fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dynamic_solidarity_analysis.png'), dpi=100, bbox_inches='tight')
    
    print("\n" + "="*80)
    print("Results saved to:", output_dir)
    print("="*80)
    
    return results_summary


if __name__ == "__main__":
    results = run_dynamic_solidarity_experiment()
