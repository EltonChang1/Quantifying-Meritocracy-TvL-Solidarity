"""
Inequality and mobility metrics
"""

import numpy as np
from typing import Tuple, List


def compute_gini_coefficient(wealth_array: np.ndarray) -> float:
    """
    Compute Gini coefficient for wealth distribution.
    
    Gini ranges from 0 (perfect equality) to 1 (maximum inequality).
    
    Args:
        wealth_array: Array of wealth values
        
    Returns:
        float: Gini coefficient
    """
    wealth_array = np.asarray(wealth_array)
    
    # Handle edge cases
    if len(wealth_array) == 0:
        return 0.0
    
    if np.sum(wealth_array) == 0:
        return 0.0
    
    # Sort wealth
    sorted_wealth = np.sort(wealth_array)
    n = len(sorted_wealth)
    
    # Gini formula: G = (2 * sum(i * w_i)) / (n * sum(w_i)) - (n + 1) / n
    cumsum = np.cumsum(sorted_wealth)
    gini = (2 * np.sum(np.arange(1, n + 1) * sorted_wealth)) / (n * np.sum(sorted_wealth)) - (n + 1) / n
    
    return max(0.0, min(1.0, gini))  # Clamp to [0, 1]


def compute_income_concentration_ratios(wealth_array: np.ndarray) -> dict:
    """
    Compute concentration ratios for various percentiles.
    
    Args:
        wealth_array: Array of wealth values
        
    Returns:
        Dict with concentration ratios
    """
    sorted_wealth = np.sort(wealth_array)
    total = np.sum(sorted_wealth)
    
    if total == 0:
        return {
            "top_1_percent": 0.0,
            "top_5_percent": 0.0,
            "top_10_percent": 0.0,
            "top_25_percent": 0.0,
            "bottom_50_percent": 0.0,
        }
    
    n = len(sorted_wealth)
    
    return {
        "top_1_percent": float(np.sum(sorted_wealth[-max(1, n//100):]) / total),
        "top_5_percent": float(np.sum(sorted_wealth[-max(1, n//20):]) / total),
        "top_10_percent": float(np.sum(sorted_wealth[-max(1, n//10):]) / total),
        "top_25_percent": float(np.sum(sorted_wealth[-max(1, n//4):]) / total),
        "bottom_50_percent": float(np.sum(sorted_wealth[:n//2]) / total),
    }


def compute_mobility_indices(
    initial_wealth: np.ndarray,
    final_wealth: np.ndarray,
    initial_talents: np.ndarray,
    final_talents: np.ndarray
) -> dict:
    """
    Compute social mobility indices.
    
    Args:
        initial_wealth: Initial wealth array
        final_wealth: Final wealth array
        initial_talents: Initial talent array
        final_talents: Final talent array
        
    Returns:
        Dict with mobility metrics
    """
    n = len(initial_wealth)
    
    # Wealth mobility
    wealth_change = final_wealth - initial_wealth
    positive_mobility = np.sum(wealth_change > 0) / n
    negative_mobility = np.sum(wealth_change < 0) / n
    
    # Mobility by initial quartile
    quartiles = np.array_split(
        np.argsort(initial_wealth),
        4
    )
    
    quartile_mobility = {}
    for q_idx, quartile_indices in enumerate(quartiles):
        q_agents = final_wealth[quartile_indices]
        quartile_percentile = np.mean(
            [np.searchsorted(np.sort(final_wealth), w) / n for w in q_agents]
        )
        quartile_mobility[f"q{q_idx+1}_avg_rank"] = quartile_percentile
    
    # Correlation between talent and final wealth
    talent_wealth_corr = np.corrcoef(initial_talents, final_wealth)[0, 1]
    
    return {
        "positive_mobility_rate": float(positive_mobility),
        "negative_mobility_rate": float(negative_mobility),
        "avg_wealth_change": float(np.mean(wealth_change)),
        "std_wealth_change": float(np.std(wealth_change)),
        "talent_wealth_correlation": float(talent_wealth_corr) if not np.isnan(talent_wealth_corr) else 0.0,
        "quartile_mobility": quartile_mobility,
        "max_wealth_change": float(np.max(wealth_change)),
        "min_wealth_change": float(np.min(wealth_change)),
    }


def compute_social_ladder_mobility(
    initial_wealth: np.ndarray,
    final_wealth: np.ndarray,
    rungs: int = 5
) -> dict:
    """
    Analyze mobility across social ladder rungs (quintiles by default).
    
    Args:
        initial_wealth: Initial wealth array
        final_wealth: Final wealth array
        rungs: Number of rungs (default 5 for quintiles)
        
    Returns:
        Dict with ladder mobility matrix and statistics
    """
    n = len(initial_wealth)
    
    # Assign initial and final rungs
    initial_rungs = np.digitize(initial_wealth, np.percentile(initial_wealth, np.linspace(0, 100, rungs+1)))
    final_rungs = np.digitize(final_wealth, np.percentile(final_wealth, np.linspace(0, 100, rungs+1)))
    
    # Transition matrix
    transition_matrix = np.zeros((rungs, rungs))
    for i in range(rungs):
        mask = initial_rungs == i + 1
        if np.sum(mask) > 0:
            final_rungs_subset = final_rungs[mask]
            for j in range(rungs):
                transition_matrix[i, j] = np.sum(final_rungs_subset == j + 1) / np.sum(mask)
    
    # Upward and downward movement
    upward_movement = np.sum(final_rungs > initial_rungs) / n
    downward_movement = np.sum(final_rungs < initial_rungs) / n
    stationary = np.sum(final_rungs == initial_rungs) / n
    
    return {
        "transition_matrix": transition_matrix.tolist(),
        "upward_movement_rate": float(upward_movement),
        "downward_movement_rate": float(downward_movement),
        "stationary_rate": float(stationary),
        "avg_rung_change": float(np.mean(final_rungs - initial_rungs)),
    }


def compute_intergenerational_elasticity(
    initial_talents: np.ndarray,
    final_wealth: np.ndarray
) -> float:
    """
    Compute intergenerational elasticity (IGE).
    How much parental characteristics predict child outcomes.
    
    Args:
        initial_talents: Initial talent levels (proxy for parental characteristics)
        final_wealth: Final wealth outcomes
        
    Returns:
        float: Intergenerational elasticity
    """
    # Simple linear regression coefficient
    x = initial_talents.reshape(-1, 1)
    y = final_wealth.reshape(-1, 1)
    
    # Avoid division by zero
    if np.std(x) == 0:
        return 0.0
    
    # Coefficient: cov(x,y) / var(x)
    covariance = np.cov(x.flatten(), y.flatten())[0, 1]
    variance_x = np.var(x)
    
    if variance_x == 0:
        return 0.0
    
    ige = covariance / variance_x
    return float(ige)


def compute_equality_of_opportunity(
    talents: np.ndarray,
    wealth: np.ndarray
) -> float:
    """
    Measure equality of opportunity.
    Higher values indicate that outcome is more driven by effort (talent)
    rather than luck or circumstance.
    
    Uses the correlation between talent and wealth as a proxy.
    
    Args:
        talents: Talent array
        wealth: Wealth array
        
    Returns:
        float: Measure of equality of opportunity (0 to 1)
    """
    if len(talents) < 2 or np.std(talents) == 0:
        return 0.0
    
    correlation = np.corrcoef(talents, wealth)[0, 1]
    
    # Convert correlation to 0-1 scale
    # Perfect correlation (1) = maximum equality of opportunity
    # No correlation (0) = luck dominates
    # Negative correlation (-1) = systematic disadvantage by talent
    
    if np.isnan(correlation):
        return 0.0
    
    return max(0.0, (correlation + 1) / 2)  # Scale to [0, 1]
