"""
Solidarity and redistribution mechanisms
"""

import numpy as np
from typing import List, Tuple, Dict
from src.model.agent import Agent


class SolidarityMechanism:
    """
    Implements various solidarity/redistribution mechanisms.
    """
    
    @staticmethod
    def fixed_redistribution(
        agents: List[Agent],
        redistribution_rate: float,
        threshold_percentile: float = 25.0
    ) -> Dict[str, float]:
        """
        Fixed-rate wealth redistribution.
        Takes percentage of wealth from high earners, distributes to low earners.
        
        Args:
            agents: List of agents
            redistribution_rate: Percentage of wealth to redistribute (0.0 to 1.0)
            threshold_percentile: Percentile for low earners (default 25th percentile)
            
        Returns:
            Dict with statistics about redistribution
        """
        wealths = np.array([a.wealth for a in agents])
        threshold = np.percentile(wealths, threshold_percentile)
        
        # Collect taxes from high earners
        total_tax = 0
        for agent in agents:
            if agent.wealth > threshold:
                tax = agent.apply_solidarity_tax(redistribution_rate)
                total_tax += tax
        
        # Redistribute to low earners
        low_wealth_agents = [a for a in agents if a.wealth <= threshold]
        if low_wealth_agents and total_tax > 0:
            per_agent_distribution = total_tax / len(low_wealth_agents)
            for agent in low_wealth_agents:
                agent.receive_redistribution(per_agent_distribution)
        
        return {
            "total_tax_collected": total_tax,
            "agents_taxed": len([a for a in agents if a.wealth > threshold]),
            "agents_subsidized": len(low_wealth_agents),
            "avg_subsidy": total_tax / len(low_wealth_agents) if low_wealth_agents else 0,
        }
    
    @staticmethod
    def dynamic_redistribution(
        agents: List[Agent],
        current_gini: float,
        gini_threshold: float = 0.50,
        base_redistribution_rate: float = 0.15,
        max_redistribution_rate: float = 0.60
    ) -> Tuple[float, Dict[str, float]]:
        """
        Dynamic/adaptive redistribution based on inequality threshold.
        Increases redistribution when Gini exceeds threshold.
        
        Args:
            agents: List of agents
            current_gini: Current Gini coefficient
            gini_threshold: Gini threshold for triggering adjustment
            base_redistribution_rate: Base redistribution rate
            max_redistribution_rate: Maximum redistribution rate allowed
            
        Returns:
            Tuple of (actual_redistribution_rate, statistics)
        """
        # Adjust redistribution rate based on inequality
        if current_gini > gini_threshold:
            # Scale up from base to max as Gini exceeds threshold
            excess_gini = current_gini - gini_threshold
            max_excess = 1.0 - gini_threshold
            adjustment = (excess_gini / max_excess) * (max_redistribution_rate - base_redistribution_rate)
            actual_rate = base_redistribution_rate + adjustment
            actual_rate = min(actual_rate, max_redistribution_rate)
        else:
            actual_rate = base_redistribution_rate
        
        stats = SolidarityMechanism.fixed_redistribution(agents, actual_rate)
        stats["applied_rate"] = actual_rate
        stats["gini_threshold_exceeded"] = current_gini > gini_threshold
        
        return actual_rate, stats
    
    @staticmethod
    def progressive_taxation(
        agents: List[Agent],
        base_rate: float = 0.20
    ) -> Dict[str, float]:
        """
        Progressive taxation where tax rate increases with wealth.
        
        Args:
            agents: List of agents
            base_rate: Base tax rate for median income
            
        Returns:
            Dict with taxation statistics
        """
        wealths = np.array([a.wealth for a in agents])
        median_wealth = np.median(wealths)
        
        total_tax = 0
        progressive_agents = 0
        
        for agent in agents:
            if agent.wealth > 0:
                # Wealth ratio compared to median
                ratio = agent.wealth / (median_wealth + 1e-6)
                # Progressive tax: increases with wealth
                tax_rate = base_rate * ratio
                tax_rate = min(tax_rate, 0.70)  # Cap at 70%
                tax = agent.wealth * tax_rate
                agent.wealth -= tax
                total_tax += tax
                progressive_agents += 1
        
        # Distribute to low earners
        low_earners = [a for a in agents if a.wealth < median_wealth / 2]
        if low_earners and total_tax > 0:
            per_agent = total_tax / len(low_earners)
            for agent in low_earners:
                agent.receive_redistribution(per_agent)
        
        return {
            "total_tax_collected": total_tax,
            "avg_tax_rate": total_tax / sum(a.wealth for a in agents) if sum(a.wealth for a in agents) > 0 else 0,
            "progressive_agents": progressive_agents,
            "subsidized_agents": len(low_earners),
        }
    
    @staticmethod
    def universal_basic_income(
        agents: List[Agent],
        ubi_amount: float
    ) -> Dict[str, float]:
        """
        Implement universal basic income for all agents.
        
        Args:
            agents: List of agents
            ubi_amount: UBI amount per agent
            
        Returns:
            Dict with UBI statistics
        """
        total_ubi = ubi_amount * len(agents)
        
        # Collect from high earners
        wealths = np.array([a.wealth for a in agents])
        threshold = np.percentile(wealths, 75)  # Top 25%
        
        total_collected = 0
        for agent in agents:
            if agent.wealth > threshold:
                collection_rate = 0.25 + (agent.wealth - threshold) / (wealths.max() - threshold + 1e-6) * 0.25
                collection = agent.wealth * collection_rate
                agent.wealth -= collection
                total_collected += collection
        
        # Distribute UBI to all
        sufficient_funds = total_collected >= total_ubi
        actual_ubi = min(ubi_amount, total_collected / len(agents))
        
        for agent in agents:
            agent.receive_redistribution(actual_ubi)
        
        return {
            "ubi_amount_per_person": actual_ubi,
            "total_ubi_distributed": actual_ubi * len(agents),
            "total_collected": total_collected,
            "sufficient_funds": sufficient_funds,
        }
    
    @staticmethod
    def targeted_educational_subsidy(
        agents: List[Agent],
        subsidy_rate: float,
        target_percentile: float = 40.0
    ) -> Dict[str, float]:
        """
        Target educational subsidies to lower-talent or lower-wealth agents.
        
        Args:
            agents: List of agents
            subsidy_rate: Percentage of total wealth to allocate as subsidies
            target_percentile: Percentile to target (low talent/wealth)
            
        Returns:
            Dict with subsidy statistics
        """
        # Calculate total pool for subsidies
        total_wealth = sum(a.wealth for a in agents)
        total_subsidy_pool = total_wealth * subsidy_rate
        
        # Identify low-talent agents
        talents = np.array([a.talent for a in agents])
        talent_threshold = np.percentile(talents, target_percentile)
        
        eligible_agents = [a for a in agents if a.talent < talent_threshold]
        
        if eligible_agents:
            per_agent_subsidy = total_subsidy_pool / len(eligible_agents)
            for agent in eligible_agents:
                agent.receive_educational_subsidy(per_agent_subsidy)
        
        return {
            "total_subsidy_pool": total_subsidy_pool,
            "subsidy_per_agent": total_subsidy_pool / len(eligible_agents) if eligible_agents else 0,
            "agents_subsidized": len(eligible_agents),
            "target_talent_level": talent_threshold,
        }
    
    @staticmethod
    def multi_dimensional_solidarity(
        agents: List[Agent],
        progressive_tax_rate: float = 0.15,
        educational_subsidy_rate: float = 0.10
    ) -> Dict[str, Dict]:
        """
        Combine multiple solidarity mechanisms.
        
        Args:
            agents: List of agents
            progressive_tax_rate: Progressive taxation rate
            educational_subsidy_rate: Educational subsidy rate
            
        Returns:
            Dict with results from all mechanisms
        """
        results = {}
        
        # Apply progressive taxation
        results["progressive_taxation"] = SolidarityMechanism.progressive_taxation(
            agents, progressive_tax_rate
        )
        
        # Apply targeted educational subsidies
        results["educational_subsidy"] = SolidarityMechanism.targeted_educational_subsidy(
            agents, educational_subsidy_rate
        )
        
        return results
