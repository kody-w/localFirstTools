import logging
import os
import sys
import importlib.util
from threading import Lock
from typing import Dict, Optional, List, Any

class AgentManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: return
        self._agents = {}
        self._initialized = True

    def register_agent(self, name, agent_instance):
        self._agents[name] = agent_instance

    def get_agent(self, name):
        return self._agents.get(name)

    def discover_agents(self, agents_directory="agents"):
        # Basic auto-discovery implementation
        pass
