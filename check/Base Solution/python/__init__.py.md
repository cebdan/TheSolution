"""
TheSolution - Base Solution Module

Базовые классы и системы координат для CAD системы TheSolution
"""

from .solution_coordinate import SolutionCoordinate
from .base_solution import Solution

__version__ = "1.0.0"
__author__ = "TheSolution Team"

__all__ = [
    "SolutionCoordinate",
    "Solution"
]
