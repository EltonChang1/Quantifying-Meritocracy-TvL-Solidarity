"""
Experiment 6: Sensitivity Analysis
Tests robustness of results across varying parameter conditions.
"""

import numpy as np
import os
import json
import matplotlib.pyplot as plt
from src.model.simulation import TalentVsLuckSimulation


def run_sensitivity_analysis(
    n_agents: int = 1000,
    n_iterations: int = 100,
    n_runs: int = 2,
    output_dir: str = "data/results/sensitivity_analysis"
):
    """
    Test sensitivity of results to parameter variations.
    
    Args:
        n_agents: Number of agents
        n_iterations: Number of iterations
        n_runs: Number of runs (for averaging)
        output_dir: Directory to save results
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    base_config = {
        "talent_std": 1.0,
        "opportunity_value": 1.0,
        "opportunities_per_iteration": 5,
    }
    
    # Parameter variations
    variations = {
        "Low Talent Variability": {"talent_std": 0.5},
        "High Talent Variability": {"talent_std": 2.0},
        "Low Opportunity Value": {"opportunity_value": 0.5},
        "High Opportunity Value": {"opportunity_value": 2.0},
    }
    
    results_summary = {}
    
    print("\n" + "="*80)
    print("EXPERIMENT 6: SENSITIVITY ANALYSIS")
    print("="*80)
    
    for variation_name, variation_params in variations.items():
        print(f"\nTesting: {variation_name}")
        
        # Run with no solidarity and with solidarity for comparison
        configs = {
            "No Solidarity": {"solidarity_mechanism": "none", "solidarity_rate": 0.0},
            "Fixed 25%": {"solidarity_mechanism": "fixed", "solidarity_rate": 0.25},
        }
        
        variation_results = {}
        
        for config_name, config in configs.items():
            final_ginis = []
            mobility_rates = []
            
            for run in range(n_runs):
                sim_config = {
                    "n_agents": n_agents,
                    "n_iterations": n_iterations,
                    "initial_wealth": 10.0,
                    "talent_std": variation_params.get("talent_std", base_config["talent_std"]),
                    "opportunity_value": variation_params.get("opportunity_value", base_config["opportunity_value"]),
                    "opportunities_per_iteration": variation_params.get("opportunities_per_iteration", base_config["opportunities_per_iteration"]),
                    "solidarity_mechanism": config["solidarity_mechanism"],
                    "solidarity_rate": config["solidarity_rate"],
                    "seed": 500 + run,
                }
                
                sim = TalentVsLuckSimulation(**sim_config)
                results = sim.run(verbose=False)
                
                final_ginis.append(results['final_gini'])
                mobility_rates.append(results['upward_mobility_rate'])
            
            variation_results[config_name] = {
                "final_gini": np.mean(final_ginis),
                "upward_mobility": np.mean(mobility_rates),
            }
        
        results_summary[variation_name] = variation_results
    
    # Save results
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(results_summary, f, indent=2)
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=100)
    
    variation_names = list(results_summary.keys())
    
    # Gini sensitivity
    ax = axes[0]
    no_solidarity_ginis = [results_summary[var]['No Solidarity']['final_gini'] for var in variation_names]
    with_solidarity_ginis = [results_summary[var]['Fixed 25%']['final_gini'] for var in variation_names]
    
    x = np.arange(len(variation_names))
    width = 0.35
    
    ax.bar(x - width/2, no_solidarity_ginis, width, label='No Solidarity', color='red', alpha=0.7)
    ax.bar(x + width/2, with_solidarity_ginis, width, label='Fixed 25%', color='green', alpha=0.7)
    
    ax.set_ylabel('Final Gini', fontsize=11)
    ax.set_title('Gini Coefficient Sensitivity', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(variation_names, rotation=15, ha='right', fontsize=9)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Mobility sensitivity
    ax = axes[1]
    no_solidarity_mob = [results_summary[var]['No Solidarity']['upward_mobility'] for var in variation_names]
    with_solidarity_mob = [results_summary[var]['Fixed 25%']['upward_mobility'] for var in variation_names]
    
    ax.bar(x - width/2, no_solidarity_mob, width, label='No Solidarity', color='red', alpha=0.7)
    ax.bar(x + width/2, with_solidarity_mob, width, label='Fixed 25%', color='green', alpha=0.7)
    
    ax.set_ylabel('Upward Mobility Rate', fontsize=11)
    ax.set_title('Mobility Sensitivity', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(variation_names, rotation=15, ha='right', fontsize=9)
    ax.set_ylim([0, 1])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('Sensitivity Analysis', fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sensitivity_analysis.png'), dpi=100, bbox_inches='tight')
    
    print("\n" + "="*80)
    print("Results saved to:", output_dir)
    print("="*80)
    
    return results_summary


if __name__ == "__main__":
    results = run_sensitivity_analysis()
