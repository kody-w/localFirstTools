"""
BasicAgent - Base class for all agents in the local-first agent system.

Agents must define:
- self.name (str): Unique identifier for the agent
- self.metadata (dict): Description, parameters, and configuration
- perform(**kwargs): Execute the agent's primary behavior
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BasicAgent(ABC):
    """
    Base class for all agents.

    Agents must define:
    - self.name (str)
    - self.metadata (dict)
    - perform(**kwargs) method
    """

    name: str
    metadata: dict

    def __init__(self):
        if not hasattr(self, "name"):
            raise ValueError("Agent must define a `name` attribute")

        if not hasattr(self, "metadata"):
            raise ValueError("Agent must define a `metadata` attribute")

    @abstractmethod
    def perform(self, **kwargs) -> Any:
        """
        Execute the agent's primary behavior.

        Args:
            **kwargs: Parameters defined in metadata['parameters']

        Returns:
            Result of the agent's execution (typically str or dict)
        """
        raise NotImplementedError("Agents must implement perform()")

    def describe(self) -> Dict:
        """
        Return agent metadata for registry or UI use.
        """
        return {
            "name": self.name,
            "metadata": self.metadata,
        }

    def validate_params(self, **kwargs) -> bool:
        """
        Validate that required parameters are provided.
        """
        required = self.metadata.get("parameters", {}).get("required", [])
        for param in required:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")
        return True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
