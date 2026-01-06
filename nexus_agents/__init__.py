"""
NEXUS Agents - Phase 3: Self-Evolving Agent Ecosystem
Inspired by EvoAgentX architecture
"""

__version__ = "3.1.0"
__author__ = "NEXUS Resonance System"

# Legacy agents
from .analyzer import AnalyzerAgent, run_parallel_analyzers
from .developer import DeveloperAgent, run_developer_agents

# EvoAgentX-style agents
from .evo_core import (
    EvoAgent,
    AnalyzerAgent as EvoAnalyzer,
    DeveloperAgent as EvoDeveloper,
    EvolutionPipeline,
    AgentMemory
)

__all__ = [
    # Legacy
    'AnalyzerAgent',
    'run_parallel_analyzers',
    'DeveloperAgent', 
    'run_developer_agents',
    # EvoAgentX
    'EvoAgent',
    'EvoAnalyzer',
    'EvoDeveloper',
    'EvolutionPipeline',
    'AgentMemory'
]
