"""
NEXUS Agents - Phase 3: Self-Evolving Agent Ecosystem
"""

__version__ = "3.0.0"
__author__ = "NEXUS Resonance System"

from .analyzer import AnalyzerAgent, run_parallel_analyzers
from .developer import DeveloperAgent, run_developer_agents

__all__ = [
    'AnalyzerAgent', 
    'run_parallel_analyzers',
    'DeveloperAgent',
    'run_developer_agents'
]
