"""
Agent Creation API — allows users (or Apop itself) to generate new agents at runtime.

Agents become first-class PF operators.
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.agents.registry.registry import AgentRegistry
from ApopToSiS.agents.base.base_agent import PFBaseAgent


class AgentCreationAPI:
    """
    Agent Creation API.
    
    Allows users (or Apop itself) to generate new agents at runtime.
    Agents become first-class PF operators.
    """

    def __init__(self, registry: AgentRegistry | None = None) -> None:
        """
        Initialize Agent Creation API.

        Args:
            registry: Optional AgentRegistry instance
        """
        self.registry = registry or AgentRegistry()

    def create_agent(self, name: str, config: dict[str, Any]) -> PFBaseAgent:
        """
        Create a new PFBaseAgent subclass dynamically.
        
        Fields new agents must define:
        - triplet preferences
        - curvature tendencies
        - entropy signature
        - flux signature
        - shell bias

        Args:
            name: Agent name
            config: Agent configuration

        Returns:
            Created agent instance
        """
        # Create agent class dynamically
        agent_class = type(
            name,
            (PFBaseAgent,),
            {
                "__init__": lambda self, n=name, c=config: self._init_agent(n, c),
                "_init_agent": lambda self, n, c: setattr(self, 'name', n) or setattr(self, 'config', c),
                "analyze": lambda self, capsule, state: config.get("analyze", lambda c, s: {})(capsule, state),
                "transform": lambda self, capsule: config.get("transform", lambda c: c)(capsule),
                "flux_signature": lambda self: config.get("flux_signature", {}),
                "entropy_signature": lambda self: config.get("entropy_signature", {}),
            }
        )
        
        # Create instance
        agent = agent_class()
        agent.name = name
        agent.config = config
        
        # Register agent
        self.registry.register(name, agent)
        
        return agent

    def delete_agent(self, name: str) -> bool:
        """
        Delete an agent.

        Args:
            name: Agent name

        Returns:
            True if deleted, False if not found
        """
        if self.registry.get(name):
            self.registry.unregister(name)
            return True
        return False

    def list_agents(self) -> list[str]:
        """
        List all registered agents.

        Returns:
            List of agent names
        """
        return self.registry.list()

    def get_agent(self, name: str) -> PFBaseAgent | None:
        """
        Get an agent by name.

        Args:
            name: Agent name

        Returns:
            Agent instance or None
        """
        return self.registry.get(name)

