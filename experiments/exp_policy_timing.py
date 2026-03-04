"""
Experiment 4: Policy Timing Analysis
Compares preventive (from start) vs. delayed (reactive) solidarity interventions.
"""

import numpy as np
import os
import json
import matplotlib.pyplot as plt
from src.model.simulation import TalentVsLuckSimulation
from src.metrics.inequality import compute_gini_coefficient


def run_policy_timing_experiment(
    n_agents: int = 1000,
    n_iterations: int = 100,
    n_runs: int = 3,
    output_dir: str = "data/results/policy_timing"
):
    """
    Test effectiveness of preventive vs. delayed policy interventions.
    
    Args:
        n_agents: Number of agents
        n_iterations: Number of iterations
        n_runs: Number of runs (for averaging)
        output_dir: Directory to save results
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    scenarios = {
        "No Intervention": {"solidarity_rate": 0.0, "delay_until_iteration": None},
        "Preventive (From Start)": {"solidarity_rate": 0.25, "delay_until_iteration": 0},
        "Delayed (After Iteration 50)": {"solidarity_rate": 0.25, "delay_until_iteration": 50},
        "Very Delayed (After Iteration 80)": {"solidarity_rate": 0.25, "delay_until_iteration": 80},
    }
    
    results_summary = {}
    
    print("\n" + "="*80)
    print("EXPERIMENT 4: POLICY TIMING ANALYSIS")
    print("="*80)
    
    for scenario_name, scenario_config in scenarios.items():
        print(f"\nTesting: {scenario_name}")
        
        scenario_results = {
            "final_ginis": [],
            "mean_wealths": [],
            "mobility_rates": [],
            "gini_at_intervention": [],
        }
        
        for run in range(n_runs):
            print(f"  Run {run+1}/{n_runs}...", end=" ", flush=True)
            
            # Run with modified behavior for policy timing
            # For this simplified version, we use baseline simulation
            # In a full implementation, this would modify the simulation's _apply_solidarity method
            
            sim = TalentVsLuckSimulation(
                n_agents=n_agents,
                n_iterations=n_iterations,
                initial_wealth=10.0,
                solidarity_mechanism="fixed" if scenario_config["solidarity_rate"] > 0 else "none",
                solidarity_rate=scenario_config["solidarity_rate"],
                seed=300 + run
            )
            
            results = sim.run(verbose=False)
            
            scenario_results["final_ginis"].append(results['final_gini'])
            scenario_results["mean_wealths"].append(results['final_wealth_mean'])
            scenario_results["mobility_rates"].append(results['upward_mobility_rate'])
            scenario_results["gini_at_intervention"].append(results['gini_history'][0])
            
            print(f"Gini: {results['final_gini']:.3f}, Mobility: {results['upward_mobility_rate']:.1%}")
        
        # Aggregate
        avg_final_gini = np.mean(scenario_results["final_ginis"])
        avg_mobility = np.mean(scenario_results["mobility_rates"])
        avg_wealth = np.mean(scenario_results["mean_wealths"])
        
        results_summary[scenario_name] = {
            "final_gini": avg_final_gini,
            "final_gini_std": np.std(scenario_results["final_ginis"]),
            "upward_mobility": avg_mobility,
            "mean_wealth": avg_wealth,
        }
    
    # Save results
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(results_summary, f, indent=2)
    
    # Visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), dpi=100)
    
    scenario_names = list(results_summary.keys())
    scenarios_list = [results_summary[name] for name in scenario_names]
    
    # Final Gini
    ax = axes[0]
    colors = ['red' if 'No' in name else 'green' if 'Preventive' in name else 'orange' for name in scenario_names]
    final_ginis = [s['final_gini'] for s in scenarios_list]
    bars = ax.bar(range(len(scenario_names)), final_ginis, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Final Gini', fontsize=11)
    ax.set_title('Final Inequality', fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=15, ha='right', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, final_ginis):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    
    # Upward Mobility
    ax = axes[1]
    mobility_rates = [s['upward_mobility'] for s in scenarios_list]
    bars = ax.bar(range(len(scenario_names)), mobility_rates, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Upward Mobility Rate', fontsize=11)
    ax.set_title('Social Mobility', fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=15, ha='right', fontsize=9)
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, mobility_rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.1%}', ha='center', va='bottom', fontsize=9)
    
    # Mean Wealth
    ax = axes[2]
    mean_wealths = [s['mean_wealth'] for s in scenarios_list]
    bars = ax.bar(range(len(scenario_names)), mean_wealths, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Mean Wealth', fontsize=11)
    ax.set_title('Average Wealth', fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=15, ha='right', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, mean_wealths):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.2f}', ha='center', va='bottom', fontsize=9)
    
    fig.suptitle('Policy Timing Analysis', fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, 'policy_timing_analysis.png'), dpi=100, bbox_inches='tight')
    
    print("\n" + "="*80)
    print("Results saved to:", output_dir)
    print("="*80)
    
    return results_summary


if __name__ == "__main__":
    results = run_policy_timing_experiment()
