"""
Base Agent — abstract base class for all PF agents.

Agents are PF-manifold operators, not LLM prompts.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState


class PFBaseAgent(ABC):
    """
    Base class for all PrimeFlux agents.
    
    Agents interact with:
    - PF curvature
    - distinction density
    - reptend entropy
    - rail interference
    - Hamiltonian curvature
    - superposition magnitude ψ
    - triplet oscillation
    """

    def __init__(self, name: str = "") -> None:
        """
        Initialize agent.

        Args:
            name: Agent name
        """
        self.name = name

    @abstractmethod
    def analyze(self, capsule: Capsule, state: PFState) -> dict[str, Any]:
        """
        Inspect capsule and produce agent-specific metrics.

        Args:
            capsule: Input capsule
            state: Current PF state

        Returns:
            Analysis dictionary
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, capsule: Capsule) -> Capsule:
        """
        Modify capsule based on the agent's PF signature.

        Args:
            capsule: Input capsule

        Returns:
            Transformed capsule
        """
        raise NotImplementedError

    @abstractmethod
    def flux_signature(self) -> dict[str, Any]:
        """
        Return PF flux characteristics — curvature, density, oscillation.

        Returns:
            Flux signature dictionary
        """
        raise NotImplementedError

    @abstractmethod
    def entropy_signature(self) -> dict[str, Any]:
        """
        Return agent's entropy influence profile.

        Returns:
            Entropy signature dictionary
        """
        raise NotImplementedError
