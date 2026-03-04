"""
Tests for Agent class
"""

import pytest
import numpy as np
from src.model.agent import Agent


class TestAgent:
    """Test Agent functionality"""
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = Agent(agent_id=0, talent=0.5, wealth=10.0, initial_wealth=10.0)
        
        assert agent.agent_id == 0
        assert agent.talent == 0.5
        assert agent.wealth == 10.0
        assert agent.initial_wealth == 10.0
        assert len(agent.history) == 1
        assert agent.history[0] == 10.0
    
    def test_attempt_opportunity_success(self):
        """Test successful opportunity"""
        agent = Agent(agent_id=0, talent=1.0, wealth=10.0, initial_wealth=10.0)
        
        # With high talent and low luck, should succeed
        initial_wealth = agent.wealth
        result = agent.attempt_opportunity(luck_factor=0.1, opportunity_value=5.0)
        
        assert result == True
        assert agent.wealth == initial_wealth + 5.0
        assert agent.fortune_events == 1
    
    def test_attempt_opportunity_failure(self):
        """Test failed opportunity"""
        agent = Agent(agent_id=0, talent=-1.0, wealth=10.0, initial_wealth=10.0)
        
        initial_wealth = agent.wealth
        result = agent.attempt_opportunity(luck_factor=0.9, opportunity_value=5.0)
        
        assert result == False
        assert agent.wealth < initial_wealth  # Should have penalty
        assert agent.misfortune_events == 1
    
    def test_solidarity_tax(self):
        """Test solidarity tax application"""
        agent = Agent(agent_id=0, talent=0.0, wealth=100.0, initial_wealth=10.0)
        
        tax_amount = agent.apply_solidarity_tax(0.25)
        
        assert tax_amount > 0
        assert agent.wealth < 100.0
        assert agent.wealth == 100.0 - tax_amount
    
    def test_receive_redistribution(self):
        """Test receiving redistribution"""
        agent = Agent(agent_id=0, talent=0.0, wealth=10.0, initial_wealth=10.0)
        
        agent.receive_redistribution(5.0)
        
        assert agent.wealth == 15.0
    
    def test_wealth_change(self):
        """Test wealth change calculation"""
        agent = Agent(agent_id=0, talent=0.0, wealth=20.0, initial_wealth=10.0)
        
        change = agent.get_wealth_change()
        
        assert change == 10.0
    
    def test_upward_mobility(self):
        """Test upward mobility determination"""
        agent = Agent(agent_id=0, talent=0.0, wealth=20.0, initial_wealth=10.0)
        
        assert agent.get_upward_mobility() == True
        
        agent.wealth = 5.0
        assert agent.get_upward_mobility() == False
    
    def test_record_wealth(self):
        """Test wealth history recording"""
        agent = Agent(agent_id=0, talent=0.0, wealth=10.0, initial_wealth=10.0)
        
        assert len(agent.history) == 1
        agent.wealth = 20.0
        agent.record_wealth()
        assert len(agent.history) == 2
        assert agent.history[1] == 20.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
