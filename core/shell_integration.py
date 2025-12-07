"""
Shell Integration - Connects first shell logic to full PrimeFlux runtime.

Integrates CLI, distinction packets, shell transitions, and PrimeFlux principles.
"""

from __future__ import annotations

from typing import Dict, Any, Optional
from core.first_shell import (
    parse_distinction_packet,
    check_reversibility,
    process_first_shell,
    apply_data_freedom
)
from core.math.shells import Shell, shell_curvature, next_shell
from runtime.state.state import PFState


class ShellIntegration:
    """
    Integrates first shell logic with full PrimeFlux runtime.
    
    Connects:
    - Distinction packets → Shell transitions
    - Trig modes → Agent routing
    - Presence operator → Event spaces
    - Reversibility → Quanta minting
    - Data freedom → Transform operations
    """
    
    def __init__(self):
        """Initialize shell integration."""
        self.current_shell = Shell.PRESENCE
        self.shell_history: list[Dict[str, Any]] = []
    
    def process_with_shells(
        self,
        input_text: str,
        mode: str = 'refinement',
        presence_on: bool = True,
        agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process input through full shell system.
        
        Args:
            input_text: User input
            mode: Mode (research/refinement/relations)
            presence_on: Whether presence operator is enabled
            agent: Optional agent override
            
        Returns:
            Complete processing result with shell transitions
        """
        # Process through first shell
        first_shell_result = process_first_shell(input_text, mode, presence_on, agent)
        
        if first_shell_result["status"] == "presence_off":
            return first_shell_result
        
        packet = first_shell_result["packet"]
        shell_info = first_shell_result["shell"]
        
        # Update current shell
        self.current_shell = Shell(packet["next_shell"])
        
        # Record shell transition
        transition = {
            "from": Shell(packet["current_shell"]).name,
            "to": Shell(packet["next_shell"]).name,
            "curvature": packet["curvature"],
            "entropy": packet["entropy"],
            "phase": packet["phase"],
            "timestamp": packet["timestamp"]
        }
        self.shell_history.append(transition)
        
        return {
            **first_shell_result,
            "shell_transition": transition,
            "shell_history": self.shell_history.copy()
        }
    
    def get_shell_state(self) -> Dict[str, Any]:
        """Get current shell state."""
        return {
            "current_shell": self.current_shell.name,
            "shell_value": self.current_shell.value,
            "curvature": shell_curvature(self.current_shell),
            "transition_count": len(self.shell_history)
        }
    
    def reset_to_first_shell(self):
        """Reset to first shell (PRESENCE)."""
        self.current_shell = Shell.PRESENCE
        self.shell_history = []
