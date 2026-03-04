"""
Main simulation engine for Talent vs. Luck with Solidarity
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from tqdm import tqdm
from src.model.agent import Agent
from src.model.solidarity import SolidarityMechanism
from src.metrics.inequality import compute_gini_coefficient, compute_mobility_indices


class TalentVsLuckSimulation:
    """
    Agent-based simulation of economic success incorporating talent, luck, and solidarity.
    """
    
    def __init__(
        self,
        n_agents: int = 1000,
        n_iterations: int = 100,
        initial_wealth: float = 10.0,
        talent_mean: float = 0.0,
        talent_std: float = 1.0,
        opportunity_value: float = 1.0,
        opportunities_per_iteration: int = 5,
        solidarity_mechanism: str = "none",
        solidarity_rate: float = 0.0,
        tax_avoidance_rate: float = 0.0,
        seed: Optional[int] = None,
    ):
        """
        Initialize simulation.
        
        Args:
            n_agents: Number of agents in simulation
            n_iterations: Number of simulation iterations
            initial_wealth: Starting wealth for all agents
            talent_mean: Mean of talent distribution
            talent_std: Standard deviation of talent distribution
            opportunity_value: Value of each economic opportunity
            opportunities_per_iteration: Number of opportunities per iteration
            solidarity_mechanism: Type of redistribution ("none", "fixed", "dynamic", "progressive", "ubi")
            solidarity_rate: Rate of redistribution/taxation
            tax_avoidance_rate: Proportion of agents with tax avoidance tendency (0.0 to 1.0)
            seed: Random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
        
        self.n_agents = n_agents
        self.n_iterations = n_iterations
        self.initial_wealth = initial_wealth
        self.talent_mean = talent_mean
        self.talent_std = talent_std
        self.opportunity_value = opportunity_value
        self.opportunities_per_iteration = opportunities_per_iteration
        self.solidarity_mechanism = solidarity_mechanism
        self.solidarity_rate = solidarity_rate
        self.tax_avoidance_rate = tax_avoidance_rate
        
        # Initialize agents
        self.agents: List[Agent] = []
        self._initialize_agents()
        
        # Results tracking
        self.gini_history = []
        self.wealth_distributions = []
        self.mobility_indices = []
        self.results = {}
    
    def _initialize_agents(self):
        """Create and initialize agents"""
        self.agents = []
        for i in range(self.n_agents):
            talent = np.random.normal(self.talent_mean, self.talent_std)
            tax_avoidance = np.random.random() < self.tax_avoidance_rate
            agent_tax_avoidance = np.random.random() if tax_avoidance else 0.0
            
            agent = Agent(
                agent_id=i,
                talent=talent,
                wealth=self.initial_wealth,
                initial_wealth=self.initial_wealth,
                tax_avoidance_tendency=agent_tax_avoidance,
            )
            self.agents.append(agent)
    
    def _run_economic_round(self):
        """Run a round of economic opportunities for all agents"""
        for agent in self.agents:
            for _ in range(self.opportunities_per_iteration):
                luck = np.random.random()
                agent.attempt_opportunity(luck, self.opportunity_value)
            agent.record_wealth()
    
    def _apply_solidarity(self):
        """Apply configured solidarity mechanism"""
        if self.solidarity_mechanism == "none":
            return {"mechanism": "none"}
        elif self.solidarity_mechanism == "fixed":
            return SolidarityMechanism.fixed_redistribution(
                self.agents, self.solidarity_rate
            )
        elif self.solidarity_mechanism == "dynamic":
            current_gini = compute_gini_coefficient(
                np.array([a.wealth for a in self.agents])
            )
            rate, stats = SolidarityMechanism.dynamic_redistribution(
                self.agents, current_gini, gini_threshold=0.50
            )
            return stats
        elif self.solidarity_mechanism == "progressive":
            return SolidarityMechanism.progressive_taxation(
                self.agents, self.solidarity_rate
            )
        elif self.solidarity_mechanism == "ubi":
            return SolidarityMechanism.universal_basic_income(
                self.agents, self.solidarity_rate
            )
        elif self.solidarity_mechanism == "multi":
            return SolidarityMechanism.multi_dimensional_solidarity(
                self.agents,
                progressive_tax_rate=self.solidarity_rate,
                educational_subsidy_rate=self.solidarity_rate * 0.66  # 2/3 for education
            )
        else:
            raise ValueError(f"Unknown solidarity mechanism: {self.solidarity_mechanism}")
    
    def run(self, verbose: bool = True) -> Dict:
        """
        Run the simulation.
        
        Args:
            verbose: Whether to show progress bar
            
        Returns:
            Dict containing simulation results
        """
        iterator = tqdm(range(self.n_iterations), disable=not verbose)
        
        for iteration in iterator:
            # Economic opportunities
            self._run_economic_round()
            
            # Apply solidarity
            solidarity_stats = self._apply_solidarity()
            
            # Record metrics
            wealths = np.array([a.wealth for a in self.agents])
            gini = compute_gini_coefficient(wealths)
            self.gini_history.append(gini)
            self.wealth_distributions.append(wealths.copy())
            
            iterator.set_description(f"Gini: {gini:.3f}")
        
        # Calculate final metrics
        self._calculate_final_metrics()
        
        return self.results
    
    def _calculate_final_metrics(self):
        """Calculate final simulation metrics"""
        final_wealths = np.array([a.wealth for a in self.agents])
        
        # Mobility analysis
        mobility_data = []
        for agent in self.agents:
            mobility_data.append({
                "agent_id": agent.agent_id,
                "talent": agent.talent,
                "initial_wealth": agent.initial_wealth,
                "final_wealth": agent.wealth,
                "wealth_change": agent.get_wealth_change(),
                "upward_mobility": agent.get_upward_mobility(),
                "fortune_events": agent.fortune_events,
                "misfortune_events": agent.misfortune_events,
                "educational_subsidy_received": agent.educational_subsidy_received,
            })
        
        upward_mobility_count = sum(1 for m in mobility_data if m["upward_mobility"])
        upward_mobility_rate = upward_mobility_count / len(mobility_data)
        
        self.results = {
            "n_agents": self.n_agents,
            "n_iterations": self.n_iterations,
            "solidarity_mechanism": self.solidarity_mechanism,
            "solidarity_rate": self.solidarity_rate,
            "final_gini": self.gini_history[-1],
            "mean_gini": np.mean(self.gini_history),
            "std_gini": np.std(self.gini_history),
            "gini_history": self.gini_history,
            "wealth_distributions": self.wealth_distributions,
            "initial_wealth_mean": np.mean([a.initial_wealth for a in self.agents]),
            "final_wealth_mean": np.mean(final_wealths),
            "final_wealth_median": np.median(final_wealths),
            "final_wealth_std": np.std(final_wealths),
            "total_wealth": np.sum(final_wealths),
            "wealth_concentration_top10": np.sum(np.sort(final_wealths)[-int(self.n_agents*0.1):]) / np.sum(final_wealths),
            "wealth_concentration_top1": np.sum(np.sort(final_wealths)[-1:]) / np.sum(final_wealths),
            "upward_mobility_rate": upward_mobility_rate,
            "downward_mobility_rate": 1.0 - upward_mobility_rate,
            "mobility_data": mobility_data,
            "agent_talents": [a.talent for a in self.agents],
            "agent_fortunes": [a.fortune_events for a in self.agents],
            "agent_misfortunes": [a.misfortune_events for a in self.agents],
        }
    
    def get_summary(self) -> str:
        """Get human-readable summary of results"""
        if not self.results:
            return "Simulation not yet run. Call run() first."
        
        summary = f"""
{'='*60}
SIMULATION SUMMARY
{'='*60}
Configuration:
  - Agents: {self.results['n_agents']}
  - Iterations: {self.results['n_iterations']}
  - Solidarity Mechanism: {self.results['solidarity_mechanism']}
  - Solidarity Rate: {self.results['solidarity_rate']:.1%}

Results:
  - Final Gini Coefficient: {self.results['final_gini']:.3f}
  - Mean Gini Coefficient: {self.results['mean_gini']:.3f}
  - Total Wealth: {self.results['total_wealth']:.2f}
  - Mean Agent Wealth: {self.results['final_wealth_mean']:.2f}
  - Top 10% Wealth Concentration: {self.results['wealth_concentration_top10']:.1%}
  - Upward Mobility Rate: {self.results['upward_mobility_rate']:.1%}
{'='*60}
        """
        return summary
    
    def compare_with(self, other: 'TalentVsLuckSimulation') -> str:
        """
        Compare this simulation's results with another.
        
        Args:
            other: Another TalentVsLuckSimulation instance with results
            
        Returns:
            String with comparison
        """
        if not self.results or not other.results:
            return "Both simulations must be run before comparison."
        
        gini_diff = self.results['final_gini'] - other.results['final_gini']
        wealth_diff = self.results['final_wealth_mean'] - other.results['final_wealth_mean']
        mobility_diff = self.results['upward_mobility_rate'] - other.results['upward_mobility_rate']
        
        comparison = f"""
{'='*60}
SIMULATION COMPARISON
{'='*60}
Current:  {self.results['solidarity_mechanism']} ({self.results['solidarity_rate']:.1%})
Other:    {other.results['solidarity_mechanism']} ({other.results['solidarity_rate']:.1%})

Metric Differences (Current - Other):
  - Gini Coefficient: {gini_diff:+.3f} {'(better)' if gini_diff < 0 else '(worse)'}
  - Mean Wealth: {wealth_diff:+.2f}
  - Upward Mobility: {mobility_diff:+.1%}
{'='*60}
        """
        return comparison
