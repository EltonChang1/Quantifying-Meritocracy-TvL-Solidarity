"""
Agent class for the Talent vs. Luck simulation
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class Agent:
    """
    Represents an economic agent in the simulation.
    
    Attributes:
        agent_id: Unique identifier for the agent
        talent: Agent's innate ability (normally distributed, mean=0, std=1)
        wealth: Current accumulated wealth
        initial_wealth: Starting wealth (for reference)
        tax_avoidance_tendency: Behavior parameter for tax avoidance (0.0 to 1.0)
        history: List tracking wealth over time
        fortune_events: Number of positive luck events experienced
        misfortune_events: Number of negative luck events experienced
    """
    
    agent_id: int
    talent: float
    wealth: float = 0.0
    initial_wealth: float = 0.0
    tax_avoidance_tendency: float = 0.0
    history: List[float] = field(default_factory=list)
    fortune_events: int = 0
    misfortune_events: int = 0
    educational_subsidy_received: bool = False
    
    def __post_init__(self):
        """Initialize agent with starting wealth and history"""
        self.initial_wealth = self.wealth
        self.history = [self.wealth]
    
    def attempt_opportunity(
        self, 
        luck_factor: float,
        opportunity_value: float = 1.0
    ) -> bool:
        """
        Agent attempts an economic opportunity.
        Success probability is weighted by talent and luck.
        
        Args:
            luck_factor: Random number [0, 1] representing fortune
            opportunity_value: Value of the opportunity if successful
            
        Returns:
            bool: True if opportunity was successful
        """
        # Success probability combines talent and luck
        # Talent has minimal influence; luck is dominant (Pluchino et al. 2018 model)
        success_threshold = 0.5 + (self.talent * 0.02)  # Luck >> Talent
        
        if luck_factor < success_threshold:
            self.wealth += opportunity_value
            self.fortune_events += 1
            return True
        else:
            # Small penalty for failed opportunity
            self.wealth *= 0.95
            self.misfortune_events += 1
            return False
    
    def apply_solidarity_tax(self, tax_rate: float) -> float:
        """
        Apply solidarity/progressive tax to agent's wealth.
        High-wealth agents pay based on actual wealth.
        Low-wealth agents are exempt.
        
        Args:
            tax_rate: Percentage of wealth to tax (0.0 to 1.0)
            
        Returns:
            float: Amount of wealth taxed
        """
        # Strategic tax avoidance behavior
        if np.random.random() < self.tax_avoidance_tendency:
            # Agent reduces reported wealth by hiding some
            taxable_wealth = self.wealth * (1 - self.tax_avoidance_tendency * 0.5)
        else:
            taxable_wealth = self.wealth
        
        tax_amount = taxable_wealth * tax_rate
        self.wealth = max(0, self.wealth - tax_amount)
        return tax_amount
    
    def receive_redistribution(self, amount: float):
        """
        Receive redistributed wealth from solidarity measures.
        
        Args:
            amount: Amount to add to wealth
        """
        self.wealth += amount
    
    def receive_educational_subsidy(self, subsidy_amount: float):
        """
        Receive targeted educational subsidy.
        Improves future opportunity success rate.
        
        Args:
            subsidy_amount: Subsidy amount
        """
        self.wealth += subsidy_amount
        self.educational_subsidy_received = True
        # Educational subsidy can provide slight talent boost for future opportunities
        self.talent += 0.1
    
    def record_wealth(self):
        """Record current wealth in history"""
        self.history.append(self.wealth)
    
    def get_wealth_change(self) -> float:
        """Calculate total wealth change from initial"""
        return self.wealth - self.initial_wealth
    
    def get_upward_mobility(self) -> bool:
        """
        Determine if agent achieved upward mobility.
        Defined as wealth increase > 50% of initial or reaching top quartile.
        
        Returns:
            bool: True if agent showed upward mobility
        """
        if self.initial_wealth == 0:
            return self.wealth > 1.0
        return self.get_wealth_change() / self.initial_wealth > 0.5
    
    def reset_for_iteration(self):
        """Reset event counters for new iteration"""
        self.fortune_events = 0
        self.misfortune_events = 0
    
    def __repr__(self) -> str:
        return (f"Agent({self.agent_id}, talent={self.talent:.2f}, "
                f"wealth={self.wealth:.2f}, upward_mobility={self.get_upward_mobility()})")
