"""
Identity Core — Apop's evolving identity state.

Tracks identity drift and maintains continuity across interactions.
"""

from __future__ import annotations

from typing import Any
import time


class IdentityCore:
    """
    Identity Core — Apop's evolving identity state.
    
    Tracks identity drift and maintains continuity across interactions.
    """

    def __init__(self) -> None:
        """Initialize identity core."""
        self.curvature_trace: list[float] = []
        self.entropy_trace: list[float] = []
        self.density_trace: list[float] = []
        self.identity_drift: float = 0.0
        self.interaction_count: int = 0
        self.last_update_time: float = time.time()

    def update(
        self,
        curvature: float = 0.0,
        entropy: float = 0.0,
        density: float = 0.0
    ) -> None:
        """
        Update identity core from PF metrics.
        
        Args:
            curvature: Curvature value
            entropy: Entropy value
            density: Density value
        """
        # Append to traces
        self.curvature_trace.append(curvature)
        self.entropy_trace.append(entropy)
        self.density_trace.append(density)
        
        # Keep traces bounded
        if len(self.curvature_trace) > 100:
            self.curvature_trace = self.curvature_trace[-100:]
        if len(self.entropy_trace) > 100:
            self.entropy_trace = self.entropy_trace[-100:]
        if len(self.density_trace) > 100:
            self.density_trace = self.density_trace[-100:]
        
        # Compute identity drift (variance in recent metrics)
        if len(self.curvature_trace) >= 2:
            recent_curvature = self.curvature_trace[-5:]
            recent_entropy = self.entropy_trace[-5:]
            
            if recent_curvature:
                curvature_variance = sum((c - sum(recent_curvature)/len(recent_curvature))**2 for c in recent_curvature) / len(recent_curvature)
            else:
                curvature_variance = 0.0
                
            if recent_entropy:
                entropy_variance = sum((e - sum(recent_entropy)/len(recent_entropy))**2 for e in recent_entropy) / len(recent_entropy)
            else:
                entropy_variance = 0.0
            
            self.identity_drift = (curvature_variance + entropy_variance) / 2.0
        
        self.interaction_count += 1
        self.last_update_time = time.time()

    def export(self) -> dict[str, Any]:
        """
        Export identity core state.
        
        Returns:
            Dictionary with identity state
        """
        return {
            "identity_drift": self.identity_drift,
            "interaction_count": self.interaction_count,
            "curvature_trace_length": len(self.curvature_trace),
            "entropy_trace_length": len(self.entropy_trace),
            "density_trace_length": len(self.density_trace),
            "last_update_time": self.last_update_time,
        }

