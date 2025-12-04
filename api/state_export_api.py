"""
State Export API — allows extraction of PF-state for:
- UI
- models
- visualization
- debugging
- future hardware integrations
- training external agents

This is Apop's full introspection layer.
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.experience.manager import ExperienceManager


class StateExportAPI:
    """
    State Export API.
    
    Allows extraction of PF-state for:
    - UI
    - models
    - visualization
    - debugging
    - future hardware integrations
    - training external agents
    
    This is Apop's full introspection layer.
    """

    def __init__(
        self,
        pf_state: PFState | None = None,
        context: Context | None = None,
        experience: ExperienceManager | None = None
    ) -> None:
        """
        Initialize State Export API.

        Args:
            pf_state: Optional PF state
            context: Optional context
            experience: Optional experience manager
        """
        self.state = pf_state or PFState()
        self.context = context or Context()
        self.experience = experience or ExperienceManager()

    def export_state(self) -> dict[str, Any]:
        """
        Export full PF state.
        
        Returns complete introspection data.

        Returns:
            Dictionary with full PF state
        """
        return {
            "shell": self.state.shell.value if hasattr(self.state.shell, 'value') else self.state.shell,
            "curvature": self.state.curvature,
            "entropy": self.state.entropy,
            "density": self.state.density,
            "psi": self.state.psi,
            "hamiltonian": self.state.hamiltonian,
            "reptend_entropy": getattr(self.state, 'reptend_entropy', 0.0),
            "rail_interference": getattr(self.state, 'rail_interference', 0.0),
            "distinction_chain": str(self.state.distinction_chain) if hasattr(self.state, 'distinction_chain') else [],
            "experience_summary": self.experience.summarize(),
            "context_window": [c.to_dict() if hasattr(c, 'to_dict') else str(c) for c in self.context.last_capsules(5)],
            "curvature_trend": self.context.curvature_trend(),
            "entropy_trend": self.context.entropy_trend(),
            "disagreement_level": self.context.disagreement_level(),
        }

    def export_minimal_state(self) -> dict[str, Any]:
        """
        Export minimal PF state (just core metrics).

        Returns:
            Dictionary with minimal state
        """
        return {
            "shell": self.state.shell.value if hasattr(self.state.shell, 'value') else self.state.shell,
            "curvature": self.state.curvature,
            "entropy": self.state.entropy,
            "density": self.state.density,
        }

    def export_experience(self) -> dict[str, Any]:
        """
        Export experience layer data.

        Returns:
            Dictionary with experience summary
        """
        return self.experience.summarize()

    def export_context(self) -> dict[str, Any]:
        """
        Export context data.

        Returns:
            Dictionary with context data
        """
        return {
            "last_capsules": [c.to_dict() if hasattr(c, 'to_dict') else str(c) for c in self.context.last_capsules(10)],
            "curvature_trend": self.context.curvature_trend(),
            "entropy_trend": self.context.entropy_trend(),
            "disagreement_level": self.context.disagreement_level(),
        }

