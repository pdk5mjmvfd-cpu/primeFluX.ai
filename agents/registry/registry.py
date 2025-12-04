"""
Agent Registry — dynamic agent registration and management.
"""

from __future__ import annotations

from typing import Any, Optional
import json
from ApopToSiS.agents.base.base_agent import PFBaseAgent


class AgentRegistry:
    """
    Registry for managing agents dynamically.
    """

    def __init__(self) -> None:
        """Initialize registry."""
        self._agents: dict[str, PFBaseAgent] = {}

    def register(self, name: str, agent: PFBaseAgent) -> None:
        """
        Register an agent.

        Args:
            name: Agent name
            agent: Agent instance
        """
        self._agents[name] = agent

    def unregister(self, name: str) -> bool:
        """
        Unregister an agent.

        Args:
            name: Agent name

        Returns:
            True if agent was removed, False if not found
        """
        if name in self._agents:
            del self._agents[name]
            return True
        return False

    def list(self) -> list[str]:
        """
        List all registered agent names.

        Returns:
            List of agent names
        """
        return list(self._agents.keys())

    def get(self, name: str) -> Optional[PFBaseAgent]:
        """
        Get an agent by name.

        Args:
            name: Agent name

        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(name)

    def instantiate(self, name: str, agent_class: type[PFBaseAgent], *args: Any, **kwargs: Any) -> PFBaseAgent:
        """
        Instantiate and register an agent.

        Args:
            name: Agent name
            agent_class: Agent class
            *args: Positional arguments for agent constructor
            **kwargs: Keyword arguments for agent constructor

        Returns:
            Instantiated agent
        """
        agent = agent_class(*args, **kwargs)
        self.register(name, agent)
        return agent

    def load_from_file(self, filepath: str) -> None:
        """
        Load agent configurations from file.

        TODO: Implement full file loading logic.

        Args:
            filepath: Path to configuration file
        """
        # TODO: Implement file loading
        pass

    def save_to_file(self, filepath: str) -> None:
        """
        Save agent configurations to file.

        TODO: Implement full file saving logic.

        Args:
            filepath: Path to save configuration
        """
        # TODO: Implement file saving
        config = {
            "agents": list(self._agents.keys()),
        }
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)

