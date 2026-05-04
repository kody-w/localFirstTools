"""
Local-First Agent System

A simple, local-first agent framework for creating and managing AI agents.
No cloud dependencies - everything runs locally.
"""

from .basic_agent import BasicAgent
from .agent_generator import AgentGenerator

__all__ = ["BasicAgent", "AgentGenerator"]
