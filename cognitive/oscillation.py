"""
Oscillation dynamics.

Determines flux states based on:
- entropy
- curvature
- density
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.core.numpy_fallback import np


class OscillationDynamics:
    """
    Oscillation dynamics.
    
    Determines flux states based on:
    - entropy
    - curvature
    - density
    
    Flux states represent cognitive intensity and information flow.
    """

    def __init__(self) -> None:
        """Initialize oscillation dynamics."""
        self.entropy_threshold_low = 0.3
        self.entropy_threshold_high = 0.7
        self.curvature_threshold_low = 1.0
        self.curvature_threshold_high = 2.0
        self.last_flux = 0.0

    def compute_state(
        self,
        capsule: Capsule,
        vec: np.ndarray
    ) -> str:
        """
        Determine flux state based on capsule and embedding.
        
        Args:
            capsule: PF capsule
            vec: Embedding vector
            
        Returns:
            Flux state string ("low_flux", "mid_flux", "high_flux")
        """
        entropy = capsule.entropy
        curvature = capsule.curvature
        density = capsule.density
        
        # Oscillation smoothing to prevent runaway flux swings
        smoothed_curvature = (self.last_flux * 0.6) + (curvature * 0.4)
        self.last_flux = smoothed_curvature
        curvature = smoothed_curvature
        
        # Compute combined flux indicator
        flux_score = 0.0
        
        # Entropy contribution
        if entropy < self.entropy_threshold_low:
            flux_score += 0.0
        elif entropy < self.entropy_threshold_high:
            flux_score += 0.5
        else:
            flux_score += 1.0
        
        # Curvature contribution
        if curvature < self.curvature_threshold_low:
            flux_score += 0.0
        elif curvature < self.curvature_threshold_high:
            flux_score += 0.3
        else:
            flux_score += 0.7
        
        # Density contribution
        flux_score += min(density * 0.2, 0.3)
        
        # Determine state
        if flux_score < 0.5:
            return "low_flux"
        elif flux_score < 1.2:
            return "mid_flux"
        else:
            return "high_flux"

    def get_oscillation_frequency(self, capsule: Capsule) -> float:
        """
        Compute oscillation frequency from capsule.
        
        Args:
            capsule: PF capsule
            
        Returns:
            Frequency value
        """
        # Frequency based on entropy and curvature interaction
        return (capsule.entropy * capsule.curvature) / (capsule.density + 0.1)

