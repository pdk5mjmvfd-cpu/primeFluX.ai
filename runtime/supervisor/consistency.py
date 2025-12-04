"""
Self-Consistency Engine.

Tracks identity and PF metrics to maintain internal consistency.
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.capsules import Capsule


class ConsistencyEngine:
    """
    Self-Consistency Engine.
    
    Tracks identity and PF metrics to maintain internal consistency.
    """

    def __init__(self) -> None:
        """Initialize consistency engine."""
        self.memory: list[tuple[float, float]] = []
        self.bias_vector: float = 0.0

    def update(self, capsule: Capsule) -> dict[str, Any]:
        """
        Update consistency tracking from capsule.
        
        Args:
            capsule: PF capsule
            
        Returns:
            Dictionary with consistency metrics
        """
        # Track identity + PF metrics
        curvature = getattr(capsule, 'curvature_snapshot', capsule.curvature)
        entropy = getattr(capsule, 'entropy_snapshot', capsule.entropy)

        # Append memory
        self.memory.append((curvature, entropy))

        # Bias vector slowly moves toward stable curvature/entropy
        target = (curvature + entropy) / 2.0
        self.bias_vector = (self.bias_vector * 0.9) + (target * 0.1)

        # Keep memory bounded
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]

        return {
            "bias_vector": self.bias_vector,
            "memory_size": len(self.memory)
        }

