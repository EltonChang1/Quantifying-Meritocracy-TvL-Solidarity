"""
Tests for metrics
"""

import pytest
import numpy as np
from src.metrics.inequality import (
    compute_gini_coefficient,
    compute_income_concentration_ratios,
    compute_mobility_indices,
)


class TestMetrics:
    """Test inequality metrics"""
    
    def test_gini_perfect_equality(self):
        """Test Gini for perfect equality"""
        wealth = np.array([10.0, 10.0, 10.0, 10.0])
        gini = compute_gini_coefficient(wealth)
        
        assert gini == pytest.approx(0.0, abs=0.001)
    
    def test_gini_perfect_inequality(self):
        """Test Gini for maximum inequality"""
        wealth = np.array([0.0, 0.0, 0.0, 100.0])
        gini = compute_gini_coefficient(wealth)
        
        assert gini > 0.9
    
    def test_gini_normal_distribution(self):
        """Test Gini for normal wealth distribution"""
        np.random.seed(42)
        wealth = np.random.exponential(10.0, 1000)
        gini = compute_gini_coefficient(wealth)
        
        # Should be between 0 and 1
        assert 0 <= gini <= 1
    
    def test_concentration_ratios(self):
        """Test concentration ratio calculation"""
        wealth = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0])
        ratios = compute_income_concentration_ratios(wealth)
        
        # Top 1% should be highest
        assert ratios['top_1_percent'] >= ratios['top_5_percent']
        assert ratios['top_5_percent'] >= ratios['top_10_percent']
        
        # All should be in [0, 1]
        for key, value in ratios.items():
            assert 0 <= value <= 1
    
    def test_mobility_indices(self):
        """Test mobility indices calculation"""
        initial_wealth = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        final_wealth = np.array([15.0, 25.0, 28.0, 35.0, 60.0])
        talents = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
        final_talents = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
        
        mobility = compute_mobility_indices(initial_wealth, final_wealth, talents, final_talents)
        
        # Some agents experienced positive mobility
        assert mobility['positive_mobility_rate'] > 0
        
        # Rates should sum to approximately 1.0
        assert mobility['positive_mobility_rate'] + mobility['negative_mobility_rate'] <= 1.0
    
    def test_mobility_with_all_gains(self):
        """Test mobility when all agents gain"""
        initial_wealth = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        final_wealth = np.array([20.0, 30.0, 40.0, 50.0, 60.0])
        talents = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
        final_talents = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
        
        mobility = compute_mobility_indices(initial_wealth, final_wealth, talents, final_talents)
        
        assert mobility['positive_mobility_rate'] == 1.0
        assert mobility['negative_mobility_rate'] == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
