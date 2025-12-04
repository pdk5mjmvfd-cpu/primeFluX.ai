"""
PFState — Runtime PrimeFlux state container.

Maintains PF metrics, history, and state across interactions.
"""

from __future__ import annotations

from typing import Any, Optional
from dataclasses import dataclass, field
from ApopToSiS.core.math.shells import Shell
from ApopToSiS.runtime.capsules import Capsule


@dataclass
class PFState:
    """
    PFState — Runtime PrimeFlux state container.
    
    Maintains PF metrics, history, and state across interactions.
    """

    # Core PF metrics
    shell: Shell = Shell.PRESENCE
    curvature: float = 0.0
    entropy: float = 0.0
    density: float = 0.0
    psi: float = 1.0  # Superposition magnitude
    hamiltonian: float = 0.0
    
    # History tracking
    shell_history: list[Shell] = field(default_factory=list)
    curvature_history: list[float] = field(default_factory=list)
    entropy_history: list[float] = field(default_factory=list)
    distinction_chain: list[dict[str, Any]] = field(default_factory=list)
    
    # State references
    experience_manager: Any = None
    current_shell: Shell = Shell.PRESENCE
    
    # Additional state
    last_cognitive_trace: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def update_from_capsule(self, capsule: Capsule) -> None:
        """
        Update state from capsule.
        
        Args:
            capsule: PF capsule
        """
        # Update core metrics
        self.curvature = capsule.curvature
        self.entropy = capsule.entropy
        self.density = capsule.density
        self.psi = capsule.psi
        self.hamiltonian = capsule.hamiltonian
        
        # Update shell
        shell_value = capsule.shell
        if shell_value == 0:
            self.shell = Shell.PRESENCE
            self.current_shell = Shell.PRESENCE
        elif shell_value == 2:
            self.shell = Shell.MEASUREMENT
            self.current_shell = Shell.MEASUREMENT
        elif shell_value == 3:
            self.shell = Shell.CURVATURE
            self.current_shell = Shell.CURVATURE
        elif shell_value == 4:
            self.shell = Shell.COLLAPSE
            self.current_shell = Shell.COLLAPSE
        else:
            # Default to presence
            self.shell = Shell.PRESENCE
            self.current_shell = Shell.PRESENCE
        
        # Update history
        self.shell_history.append(self.current_shell)
        self.curvature_history.append(self.curvature)
        self.entropy_history.append(self.entropy)
        
        # Keep history bounded
        if len(self.shell_history) > 100:
            self.shell_history = self.shell_history[-100:]
        if len(self.curvature_history) > 100:
            self.curvature_history = self.curvature_history[-100:]
        if len(self.entropy_history) > 100:
            self.entropy_history = self.entropy_history[-100:]
        
        # Add to history
        self.history.append({
            "curvature": self.curvature,
            "entropy": self.entropy,
            "shell": shell_value,
            "timestamp": capsule.timestamp,
        })
        
        # Keep history bounded
        if len(self.history) > 100:
            self.history = self.history[-100:]

    def update(self, data: dict[str, Any]) -> None:
        """
        Update state from dictionary.
        
        Args:
            data: State data dictionary
        """
        if "curvature" in data:
            self.curvature = data["curvature"]
        if "entropy" in data:
            self.entropy = data["entropy"]
        if "density" in data:
            self.density = data["density"]
        if "psi" in data:
            self.psi = data["psi"]
        if "hamiltonian" in data:
            self.hamiltonian = data["hamiltonian"]
        if "shell" in data:
            shell_value = data["shell"]
            if shell_value == 0:
                self.shell = Shell.PRESENCE
                self.current_shell = Shell.PRESENCE
            elif shell_value == 2:
                self.shell = Shell.MEASUREMENT
                self.current_shell = Shell.MEASUREMENT
            elif shell_value == 3:
                self.shell = Shell.FLUX
                self.current_shell = Shell.FLUX
            elif shell_value == 4:
                self.shell = Shell.COLLAPSE
                self.current_shell = Shell.COLLAPSE
        
        # Update history
        if "curvature" in data or "entropy" in data:
            self.curvature_history.append(self.curvature)
            self.entropy_history.append(self.entropy)
            
            # Keep history bounded
            if len(self.curvature_history) > 100:
                self.curvature_history = self.curvature_history[-100:]
            if len(self.entropy_history) > 100:
                self.entropy_history = self.entropy_history[-100:]

    def to_dict(self) -> dict[str, Any]:
        """
        Convert state to dictionary.
        
        Returns:
            State dictionary
        """
        return {
            "shell": self.current_shell.value if hasattr(self.current_shell, 'value') else int(self.current_shell),
            "curvature": self.curvature,
            "entropy": self.entropy,
            "density": self.density,
            "psi": self.psi,
            "hamiltonian": self.hamiltonian,
            "shell_history_length": len(self.shell_history),
            "curvature_history_length": len(self.curvature_history),
            "entropy_history_length": len(self.entropy_history),
            "distinction_chain_length": len(self.distinction_chain),
        }

