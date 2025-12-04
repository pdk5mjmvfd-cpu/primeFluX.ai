"""
Dynamic Agent API — user and Apop can create agents.

Agents must have:
- triplet preferences
- flux signatures
- entropy patterns
- shell transition tendencies
"""

from __future__ import annotations

from typing import Any, Optional
from ApopToSiS.agents.base.base_agent import PFBaseAgent
from ApopToSiS.agents.registry.registry import AgentRegistry
from ApopToSiS.runtime.capsules import Capsule


class DynamicAgentConfig:
    """
    Configuration for creating a dynamic agent.
    
    Agents MUST declare:
    - triplet influence
    - flux signature
    - entropy signature
    - shell-weight vector
    - curvature influence
    - combinatoric bias
    
    These values determine how the supervisor routes them.
    """

    def __init__(
        self,
        name: str,
        triplet_preferences: dict[str, Any],
        flux_signature: dict[str, Any],
        entropy_pattern: dict[str, Any],
        shell_transition_tendencies: dict[int, float],
        triplet_influence: dict[str, float] | None = None,
        shell_weight_vector: dict[int, float] | None = None,
        curvature_influence: float = 1.0,
        combinatoric_bias: float = 0.0,
    ) -> None:
        """
        Initialize agent configuration.

        Args:
            name: Agent name
            triplet_preferences: Triplet type preferences
            flux_signature: Flux signature (must include amplitude, direction, shell_preference)
            entropy_pattern: Entropy pattern (must include base_entropy, entropy_range, tendency)
            shell_transition_tendencies: Shell transition probabilities
            triplet_influence: Influence weights for each triplet type
            shell_weight_vector: Weight vector for each shell (0, 2, 3, 4)
            curvature_influence: How much curvature affects this agent (0.0 to 1.0)
            combinatoric_bias: Bias toward combinatorics triplets (-1.0 to 1.0)
        """
        self.name = name
        self.triplet_preferences = triplet_preferences
        self.flux_signature = flux_signature
        self.entropy_pattern = entropy_pattern
        self.shell_transition_tendencies = shell_transition_tendencies
        self.triplet_influence = triplet_influence or {
            "presence": 1.0,
            "trig": 1.0,
            "combinatorics": 1.0,
        }
        self.shell_weight_vector = shell_weight_vector or {
            0: 1.0,  # PRESENCE
            2: 1.0,  # MEASUREMENT
            3: 1.0,  # FLUX
            4: 1.0,  # COLLAPSE
        }
        self.curvature_influence = curvature_influence
        self.combinatoric_bias = combinatoric_bias


class DynamicAgent(PFBaseAgent):
    """A dynamically created agent."""

    def __init__(self, config: DynamicAgentConfig) -> None:
        """
        Initialize dynamic agent.

        Args:
            config: Agent configuration
        """
        self.config = config

    def analyze(self, capsule: Capsule) -> dict[str, Any]:
        """
        Analyze capsule using agent configuration.
        
        Uses all PF factors:
        - triplet influence
        - flux signature
        - entropy pattern
        - shell-weight vector
        - curvature influence
        - combinatoric bias

        Args:
            capsule: Input capsule

        Returns:
            Analysis dictionary
        """
        # Compute triplet match
        triplet_match = self._match_triplets(capsule.triplet_summary)
        
        # Compute shell match
        shell_match = self.config.shell_weight_vector.get(capsule.shell_state, 0.0)
        
        # Compute curvature influence
        curvature_score = capsule.curvature_snapshot * self.config.curvature_influence
        
        return {
            "agent_name": self.config.name,
            "flux_amplitude": self.config.flux_signature.get("amplitude", 0.0),
            "entropy_match": self._match_entropy(capsule.entropy_snapshot),
            "triplet_match": triplet_match,
            "shell_match": shell_match,
            "curvature_score": curvature_score,
            "combinatoric_bias": self.config.combinatoric_bias,
        }
    
    def _match_triplets(self, triplet_summary: dict[str, Any]) -> float:
        """
        Compute how well triplets match agent's triplet influence.
        
        Args:
            triplet_summary: Triplet summary from capsule
            
        Returns:
            Match score
        """
        if "types" not in triplet_summary:
            return 0.0
        
        types = triplet_summary.get("types", [])
        if not types:
            return 0.0
        
        # Count triplet types
        type_counts = {}
        for ttype in types:
            type_counts[ttype] = type_counts.get(ttype, 0) + 1
        
        # Compute weighted match
        total = len(types)
        match_score = 0.0
        
        for ttype, count in type_counts.items():
            influence = self.config.triplet_influence.get(ttype, 0.0)
            match_score += (count / total) * influence
        
        return match_score

    def transform(self, capsule: Capsule) -> Capsule:
        """
        Transform capsule using agent configuration.

        Args:
            capsule: Input capsule

        Returns:
            Transformed capsule
        """
        # Apply flux signature
        flux_amp = self.config.flux_signature.get("amplitude", 1.0)
        new_entropy = capsule.entropy_snapshot * flux_amp
        
        # Update triplet summary
        new_summary = capsule.triplet_summary.copy()
        new_summary["agent"] = self.config.name
        
        # Create transformed capsule
        transformed = Capsule(
            triplet_summary=new_summary,
            shell_state=capsule.shell_state,
            entropy_snapshot=new_entropy,
            curvature_snapshot=capsule.curvature_snapshot,
            timestamp=capsule.timestamp,
            raw_tokens=capsule.raw_tokens.copy(),
            pf_signature=capsule.pf_signature,
            compression_hash=capsule.compression_hash,
            metadata={**capsule.metadata, "dynamic_agent": self.config.name},
        )
        
        return transformed

    def flux_signature(self) -> dict[str, Any]:
        """
        Get flux signature from configuration.

        Returns:
            Flux signature dictionary
        """
        return self.config.flux_signature.copy()

    def entropy_signature(self) -> dict[str, Any]:
        """
        Get entropy signature from configuration.

        Returns:
            Entropy signature dictionary
        """
        return self.config.entropy_pattern.copy()

    def _match_entropy(self, entropy: float) -> float:
        """
        Compute how well entropy matches agent pattern.

        Args:
            entropy: Input entropy

        Returns:
            Match score
        """
        pattern = self.config.entropy_pattern
        base = pattern.get("base_entropy", 0.5)
        return 1.0 - abs(entropy - base)


class DynamicAgentAPI:
    """API for creating and managing dynamic agents."""

    def __init__(self, registry: Optional[AgentRegistry] = None) -> None:
        """
        Initialize API.

        Args:
            registry: Optional agent registry
        """
        self.registry = registry or AgentRegistry()

    def create_agent(self, config: DynamicAgentConfig) -> DynamicAgent:
        """
        Create a new dynamic agent.

        Args:
            config: Agent configuration

        Returns:
            Created agent
        """
        agent = DynamicAgent(config)
        self.registry.register(config.name, agent)
        return agent

    def delete_agent(self, name: str) -> bool:
        """
        Delete an agent.

        Args:
            name: Agent name

        Returns:
            True if deleted, False if not found
        """
        return self.registry.unregister(name)

    def list_agents(self) -> list[str]:
        """
        List all agents.

        Returns:
            List of agent names
        """
        return self.registry.list()

    def save_agent(self, agent: PFBaseAgent, name: str) -> None:
        """
        Save an agent to registry.

        Args:
            agent: Agent instance
            name: Agent name
        """
        self.registry.register(name, agent)

    def load_agent(self, agent_name: str) -> Optional[PFBaseAgent]:
        """
        Load an agent from registry.

        Args:
            agent_name: Agent name

        Returns:
            Agent instance or None if not found
        """
        return self.registry.get(agent_name)

