"""
NEXUS Agents Module
Phase 3 - Self-evolving analyzer agents
"""

__version__ = "3.0.0"
__author__ = "NEXUS Bot"

# Phase 3 Extended agents
from .phase3.tester_agent import TesterAgent
from .phase3.optimizer_agent import OptimizerAgent
from .phase3.extended_evolution_loop import ExtendedEvolutionLoop

__all__ = ['TesterAgent', 'OptimizerAgent', 'ExtendedEvolutionLoop']
