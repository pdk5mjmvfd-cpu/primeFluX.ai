"""
Flux reinforcement.

Adjusts embeddings according to PF flux state.
"""

from __future__ import annotations

from ApopToSiS.core.numpy_fallback import np
from typing import Any


class FluxReinforcement:
    """
    Adjusts embeddings according to PF flux state.
    
    Flux states modulate embedding vectors to reflect
    cognitive intensity and information flow.
    """

    def __init__(self) -> None:
        """Initialize flux reinforcement."""
        self.flux_multipliers = {
            "low_flux": 0.9,
            "mid_flux": 1.1,
            "high_flux": 1.3,
        }

    def adjust(
        self,
        vec: np.ndarray,
        flux_state: str
    ) -> np.ndarray:
        """
        Adjust embedding vector based on flux state.
        
        Args:
            vec: Input embedding vector
            flux_state: Current flux state
            
        Returns:
            Adjusted embedding vector
        """
        multiplier = self.flux_multipliers.get(flux_state, 1.0)
        adjusted = vec * multiplier
        
        # Renormalize
        norm = np.linalg.norm(adjusted)
        if norm > 0:
            adjusted = adjusted / norm
        
        return adjusted

    def get_flux_strength(self, flux_state: str) -> float:
        """
        Get flux strength multiplier.
        
        Args:
            flux_state: Flux state string
            
        Returns:
            Multiplier value
        """
        return self.flux_multipliers.get(flux_state, 1.0)

