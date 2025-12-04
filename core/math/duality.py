"""
Presence-Measurement Duality.

Measurement/presence duality equations.
"""

from __future__ import annotations

import math

SQRT2 = math.sqrt(2)


def duality_state(x: float) -> float:
    """
    Compute duality state.
    
    Duality = distance from presence (0) to measurement (√2).
    
    Args:
        x: Input value
        
    Returns:
        Duality value (0.0 to 1.0)
    """
    # Normalize to [0, √2] range
    normalized = abs(x) / SQRT2
    
    # Duality = how far from pure presence
    return min(1.0, normalized)


def measurement_duality(x: float) -> float:
    """
    Compute measurement duality.
    
    Measurement creates duality (error).
    
    Args:
        x: Input value
        
    Returns:
        Measurement duality
    """
    # Duality distance from presence
    presence_dist = abs(x - 0.0)
    measurement_dist = abs(x - SQRT2)
    
    # Duality = ratio of distances
    total = presence_dist + measurement_dist
    if total == 0:
        return 0.0
    
    return measurement_dist / total


def error_curvature_duality(error: float) -> float:
    """
    Compute error-curvature duality.
    
    Error creates curvature, curvature creates distinction.
    
    Args:
        error: Measurement error
        
    Returns:
        Curvature from error
    """
    # Error drives curvature
    # Duality = error * √2 (measurement constant)
    return error * SQRT2

