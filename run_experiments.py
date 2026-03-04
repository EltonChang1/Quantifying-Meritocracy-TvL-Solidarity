#!/usr/bin/env python3
"""
Main experiment runner script.
Run all experiments for Talent vs. Luck with Solidarity study.
"""

import os
import sys
import argparse
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments import (
    run_fixed_solidarity_experiment,
    run_dynamic_solidarity_experiment,
    run_heterogeneity_experiment,
    run_policy_timing_experiment,
    run_multi_dimensional_experiment,
    run_sensitivity_analysis,
)
import sys


def main():
    """Run all experiments"""
    
    parser = argparse.ArgumentParser(
        description="Run experiments for Talent vs. Luck with Solidarity study"
    )
    parser.add_argument(
        "--experiments",
        nargs="+",
        choices=["fixed", "dynamic", "heterogeneity", "timing", "multi", "sensitivity", "all"],
        default=["all"],
        help="Which experiments to run"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick version with fewer iterations and runs"
    )
    parser.add_argument(
        "--output-dir",
        default="data/results",
        help="Output directory for results"
    )
    
    args = parser.parse_args()
    
    # Configure for quick or full run
    if args.quick:
        config = {
            "n_agents": 500,
            "n_iterations": 50,
            "n_runs": 2,
        }
        print("Running in QUICK mode (fewer iterations and runs)")
    else:
        config = {
            "n_agents": 1000,
            "n_iterations": 100,
            "n_runs": 3,
        }
        print("Running in FULL mode")
    
    # Map experiment names to functions
    experiment_map = {
        "fixed": (run_fixed_solidarity_experiment, "Experiment 1: Fixed Solidarity Rates"),
        "dynamic": (run_dynamic_solidarity_experiment, "Experiment 2: Dynamic Solidarity"),
        "heterogeneity": (run_heterogeneity_experiment, "Experiment 3: Agent Heterogeneity"),
        "timing": (run_policy_timing_experiment, "Experiment 4: Policy Timing"),
        "multi": (run_multi_dimensional_experiment, "Experiment 5: Multi-Dimensional Policies"),
        "sensitivity": (run_sensitivity_analysis, "Experiment 6: Sensitivity Analysis"),
    }
    
    # Determine which experiments to run
    if "all" in args.experiments:
        experiments_to_run = list(experiment_map.keys())
    else:
        experiments_to_run = args.experiments
    
    print("\n" + "="*80)
    print("QUANTIFYING MERITOCRACY: TALENT VS. LUCK WITH SOLIDARITY")
    print("="*80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Configuration: {config}")
    print(f"Experiments to run: {', '.join(experiments_to_run)}")
    print("="*80 + "\n")
    
    results = {}
    start_time = time.time()
    
    for exp_key in experiments_to_run:
        if exp_key not in experiment_map:
            print(f"Unknown experiment: {exp_key}")
            continue
        
        exp_func, exp_name = experiment_map[exp_key]
        
        print(f"\n{'='*80}")
        print(f"Running: {exp_name}")
        print(f"{'='*80}\n")
        
        exp_start = time.time()
        
        try:
            exp_output_dir = os.path.join(args.output_dir, exp_key)
            
            if exp_key == "fixed":
                result = exp_func(
                    redistribution_rates=[0.0, 0.05, 0.15, 0.25, 0.40, 0.60],
                    **config,
                    output_dir=exp_output_dir
                )
            elif exp_key == "heterogeneity":
                result = exp_func(**config, output_dir=exp_output_dir)
            else:
                result = exp_func(**config, output_dir=exp_output_dir)
            
            results[exp_key] = "SUCCESS"
            
            exp_duration = time.time() - exp_start
            print(f"\n✓ {exp_name} completed in {exp_duration:.1f}s")
            
        except Exception as e:
            results[exp_key] = f"FAILED: {str(e)}"
            print(f"\n✗ {exp_name} failed: {str(e)}")
    
    # Summary
    total_duration = time.time() - start_time
    
    print("\n" + "="*80)
    print("EXPERIMENT SUMMARY")
    print("="*80)
    
    for exp_key, status in results.items():
        status_symbol = "✓" if status == "SUCCESS" else "✗"
        print(f"{status_symbol} {exp_key}: {status}")
    
    print(f"\nTotal duration: {total_duration:.1f}s")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nResults saved to: {args.output_dir}")
    print("="*80 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
