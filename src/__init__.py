"""
Quantifying Meritocracy: Extending Talent vs. Luck Model to Incorporate Solidarity
"""

__version__ = "1.0.0"
__author__ = "Elton Chang"
__email__ = "contact@quantifyingmeritocracy.edu"

from src.model.agent import Agent
from src.model.simulation import TalentVsLuckSimulation
from src.metrics.inequality import compute_gini_coefficient, compute_mobility_indices

__all__ = [
    "Agent",
    "TalentVsLuckSimulation",
    "compute_gini_coefficient",
    "compute_mobility_indices",
]
