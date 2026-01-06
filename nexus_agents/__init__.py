"""
NEXUS Agents Module - Phase 3 Extended with Resonance
"""

__version__ = "3.1.0"
__author__ = "NEXUS Bot"

from .phase3.tester_agent import TesterAgent
from .phase3.optimizer_agent import OptimizerAgent
from .phase3.extended_evolution_loop import ExtendedEvolutionLoop
from .phase3.resonant_analyzer import ResonantAnalyzerAgent, ResonatorTools

__all__ = ['TesterAgent', 'OptimizerAgent', 'ExtendedEvolutionLoop',
           'ResonantAnalyzerAgent', 'ResonatorTools']
