"""
Distinction Chains.

Distinction events follow PF:
0 → 2  (measurement duality)
2 → 3  (flux curvature)
3 → 4  (collapse)
4 → 0  (reset)

Agent disagreement = flux amplitude (NOT an error).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from ApopToSiS.core.math.shells import Shell


@dataclass
class DistinctionEvent:
    """A single distinction event."""
    state_before: dict[str, Any]
    state_after: dict[str, Any]
    operator: str = ""
    shell_before: Shell = Shell.PRESENCE
    shell_after: Shell = Shell.PRESENCE
    curvature_before: float = 0.0
    curvature_after: float = 0.0
    flux_amplitude: float = 0.0
    timestamp: float = 0.0


class DistinctionChain:
    """Chain of distinction events."""
    
    def __init__(self) -> None:
        """Initialize distinction chain."""
        self.events: list[DistinctionEvent] = []
    
    def add_event(self, event: DistinctionEvent) -> None:
        """
        Add distinction event to chain.
        
        Args:
            event: Distinction event
        """
        self.events.append(event)
    
    def last_shell(self) -> Shell:
        """
        Get last shell from chain.
        
        Returns:
            Last shell
        """
        if not self.events:
            return Shell.PRESENCE
        return self.events[-1].shell_after
    
    def last_curvature(self) -> float:
        """
        Get last curvature from chain.
        
        Returns:
            Last curvature
        """
        if not self.events:
            return 0.0
        return self.events[-1].curvature_after
    
    def flux_amplitude(self) -> float:
        """
        Compute total flux amplitude from chain.
        
        Agent disagreement = flux amplitude (NOT an error).
        
        Returns:
            Total flux amplitude
        """
        if not self.events:
            return 0.0
        
        # Sum of flux amplitudes
        total_flux = sum(event.flux_amplitude for event in self.events)
        
        # Disagreement = flux (not error)
        return total_flux
    
    def validate_transition(self, from_shell: Shell, to_shell: Shell) -> bool:
        """
        Validate shell transition.
        
        Valid transitions:
        0 → 2  (measurement duality)
        2 → 3  (flux curvature)
        3 → 4  (collapse)
        4 → 0  (reset)
        
        Args:
            from_shell: Source shell
            to_shell: Target shell
            
        Returns:
            True if transition is valid
        """
        valid_transitions = {
            Shell.PRESENCE: [Shell.MEASUREMENT],
            Shell.MEASUREMENT: [Shell.CURVATURE],
            Shell.CURVATURE: [Shell.COLLAPSE],
            Shell.COLLAPSE: [Shell.PRESENCE],
        }
        
        return to_shell in valid_transitions.get(from_shell, [])
