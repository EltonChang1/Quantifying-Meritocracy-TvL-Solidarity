"""
Visualization utilities for simulation results
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict, List, Optional
import os


class SimulationVisualizer:
    """Create visualizations of simulation results"""
    
    def __init__(self, figsize: tuple = (12, 8), dpi: int = 100):
        """Initialize visualizer with default figure settings"""
        self.figsize = figsize
        self.dpi = dpi
    
    def plot_gini_evolution(
        self,
        results_dict: Dict,
        title: str = "Gini Coefficient Evolution",
        save_path: Optional[str] = None
    ):
        """Plot Gini coefficient over simulation iterations"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for label, results in results_dict.items():
            ax.plot(results['gini_history'], label=label, linewidth=2)
        
        ax.set_xlabel('Iteration', fontsize=12)
        ax.set_ylabel('Gini Coefficient', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1])
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig, ax
    
    def plot_wealth_distribution(
        self,
        results_dict: Dict,
        iteration: int = -1,
        title: str = "Final Wealth Distribution",
        save_path: Optional[str] = None
    ):
        """Plot wealth distribution at specified iteration"""
        n_results = len(results_dict)
        fig, axes = plt.subplots(1, n_results, figsize=(15, 5), dpi=self.dpi)
        
        if n_results == 1:
            axes = [axes]
        
        for ax, (label, results) in zip(axes, results_dict.items()):
            wealth_dist = results['wealth_distributions'][iteration]
            ax.hist(wealth_dist, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
            ax.set_xlabel('Wealth', fontsize=10)
            ax.set_ylabel('Frequency', fontsize=10)
            ax.set_title(f"{label}\n(Gini: {results['final_gini']:.3f})", fontsize=11)
            ax.grid(True, alpha=0.3, axis='y')
        
        fig.suptitle(title, fontsize=14, fontweight='bold')
        fig.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig, axes
    
    def plot_concentration_ratios(
        self,
        concentration_dict: Dict,
        title: str = "Wealth Concentration Ratios",
        save_path: Optional[str] = None
    ):
        """Plot wealth concentration by percentile"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        metrics = ['top_1_percent', 'top_5_percent', 'top_10_percent', 'top_25_percent']
        x_labels = ['Top 1%', 'Top 5%', 'Top 10%', 'Top 25%']
        
        x = np.arange(len(metrics))
        width = 0.15
        
        for i, (label, data) in enumerate(concentration_dict.items()):
            values = [data.get(m, 0) for m in metrics]
            ax.bar(x + i*width, values, width, label=label, alpha=0.8)
        
        ax.set_ylabel('Share of Total Wealth', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xticks(x + width * (len(concentration_dict) - 1) / 2)
        ax.set_xticklabels(x_labels)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim([0, 1])
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig, ax
    
    def plot_mobility_comparison(
        self,
        mobility_dict: Dict,
        title: str = "Upward Mobility Rates",
        save_path: Optional[str] = None
    ):
        """Compare upward mobility rates across scenarios"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        labels = list(mobility_dict.keys())
        values = [mobility_dict[label]['upward_mobility_rate'] for label in labels]
        colors = plt.cm.viridis(np.linspace(0, 1, len(labels)))
        
        bars = ax.bar(labels, values, color=colors, edgecolor='black', alpha=0.8)
        ax.set_ylabel('Upward Mobility Rate', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylim([0, 1])
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1%}', ha='center', va='bottom', fontsize=10)
        
        plt.xticks(rotation=45, ha='right')
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig, ax
    
    def plot_talent_wealth_relationship(
        self,
        results_dict: Dict,
        title: str = "Talent vs. Final Wealth",
        save_path: Optional[str] = None
    ):
        """Plot relationship between talent and final wealth"""
        n_results = len(results_dict)
        fig, axes = plt.subplots(1, n_results, figsize=(15, 5), dpi=self.dpi)
        
        if n_results == 1:
            axes = [axes]
        
        for ax, (label, results) in zip(axes, results_dict.items()):
            talents = results['agent_talents']
            final_wealths = [m['final_wealth'] for m in results['mobility_data']]
            
            ax.scatter(talents, final_wealths, alpha=0.5, s=20)
            
            # Fit line
            z = np.polyfit(talents, final_wealths, 1)
            p = np.poly1d(z)
            x_line = np.linspace(min(talents), max(talents), 100)
            ax.plot(x_line, p(x_line), "r--", linewidth=2, label=f'Correlation: {np.corrcoef(talents, final_wealths)[0,1]:.3f}')
            
            ax.set_xlabel('Initial Talent', fontsize=10)
            ax.set_ylabel('Final Wealth', fontsize=10)
            ax.set_title(f"{label}\n(Solidarity: {results['solidarity_rate']:.1%})", fontsize=11)
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        fig.suptitle(title, fontsize=14, fontweight='bold')
        fig.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig, axes
    
    def plot_comprehensive_comparison(
        self,
        results_dict: Dict,
        save_dir: Optional[str] = None
    ):
        """Create a comprehensive multi-panel comparison"""
        fig = plt.figure(figsize=(16, 12), dpi=self.dpi)
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
        
        labels = list(results_dict.keys())
        colors = plt.cm.Set2(np.linspace(0, 1, len(labels)))
        
        # 1. Gini Evolution
        ax1 = fig.add_subplot(gs[0, :2])
        for (label, results), color in zip(results_dict.items(), colors):
            ax1.plot(results['gini_history'], label=label, linewidth=2, color=color)
        ax1.set_ylabel('Gini Coefficient', fontsize=11)
        ax1.set_title('Gini Coefficient Evolution', fontsize=12, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # 2. Final Gini Comparison
        ax2 = fig.add_subplot(gs[0, 2])
        final_ginis = [results_dict[l]['final_gini'] for l in labels]
        ax2.bar(range(len(labels)), final_ginis, color=colors, edgecolor='black')
        ax2.set_ylabel('Final Gini', fontsize=11)
        ax2.set_title('Final Inequality', fontsize=12, fontweight='bold')
        ax2.set_xticks(range(len(labels)))
        ax2.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Mean Wealth Comparison
        ax3 = fig.add_subplot(gs[1, 0])
        mean_wealths = [results_dict[l]['final_wealth_mean'] for l in labels]
        ax3.bar(range(len(labels)), mean_wealths, color=colors, edgecolor='black')
        ax3.set_ylabel('Mean Wealth', fontsize=11)
        ax3.set_title('Average Wealth', fontsize=12, fontweight='bold')
        ax3.set_xticks(range(len(labels)))
        ax3.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Upward Mobility Comparison
        ax4 = fig.add_subplot(gs[1, 1])
        mobility_rates = [results_dict[l]['upward_mobility_rate'] for l in labels]
        ax4.bar(range(len(labels)), mobility_rates, color=colors, edgecolor='black')
        ax4.set_ylabel('Upward Mobility Rate', fontsize=11)
        ax4.set_title('Social Mobility', fontsize=12, fontweight='bold')
        ax4.set_xticks(range(len(labels)))
        ax4.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax4.set_ylim([0, 1])
        ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Top 10% Wealth Share
        ax5 = fig.add_subplot(gs[1, 2])
        top10_shares = [results_dict[l]['wealth_concentration_top10'] for l in labels]
        ax5.bar(range(len(labels)), top10_shares, color=colors, edgecolor='black')
        ax5.set_ylabel('Wealth Share', fontsize=11)
        ax5.set_title('Top 10% Wealth Share', fontsize=12, fontweight='bold')
        ax5.set_xticks(range(len(labels)))
        ax5.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax5.set_ylim([0, 1])
        ax5.grid(True, alpha=0.3, axis='y')
        
        # 6-8. Wealth Distributions
        for i, (label, results) in enumerate(results_dict.items()):
            ax = fig.add_subplot(gs[2, i])
            wealth_dist = results['wealth_distributions'][-1]
            ax.hist(wealth_dist, bins=40, color=colors[i], edgecolor='black', alpha=0.7)
            ax.set_xlabel('Wealth', fontsize=10)
            ax.set_ylabel('Frequency', fontsize=10)
            ax.set_title(f"{label}\n(Gini: {results['final_gini']:.3f})", fontsize=11)
            ax.grid(True, alpha=0.3, axis='y')
        
        fig.suptitle('Comprehensive Simulation Comparison', fontsize=16, fontweight='bold', y=0.995)
        
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            plt.savefig(os.path.join(save_dir, 'comprehensive_comparison.png'), 
                       dpi=self.dpi, bbox_inches='tight')
        
        return fig
