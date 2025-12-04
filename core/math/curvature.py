"""
Curvature Functions.

Irrational + trig curvature dynamics.
"""

from __future__ import annotations

import math
from typing import Any
from .shells import Shell, shell_curvature
from .triplets import Triplet
from .reptends import reptend_curvature

SQRT2 = math.sqrt(2)
SQRT3 = math.sqrt(3)
SQRT5 = math.sqrt(5)
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi


def presence_curvature(x: float) -> float:
    """
    Compute presence curvature.
    
    Uses √2 - 1 constant.
    
    Args:
        x: Input value
        
    Returns:
        Presence curvature
    """
    kappa0 = SQRT2 - 1.0
    return kappa0 * abs(x)


def measurement_curvature(x: float) -> float:
    """
    Compute measurement curvature.
    
    Uses √2 scaling.
    
    Args:
        x: Input value
        
    Returns:
        Measurement curvature
    """
    kappa2 = SQRT2
    return kappa2 * abs(x)


def trig_curvature(x: float) -> float:
    """
    Compute trig curvature.
    
    Uses sin(x), cos(x), tan(x).
    
    Args:
        x: Input value
        
    Returns:
        Trig curvature
    """
    sin_val = math.sin(x)
    cos_val = math.cos(x)
    tan_val = math.tan(x)
    
    # Handle tan singularity
    if abs(tan_val) > 1e10:
        tan_val = math.copysign(1e10, tan_val)
    
    return abs(sin_val) + abs(cos_val) + abs(tan_val) / 3.0


def irrational_curvature(x: float) -> float:
    """
    Compute irrational curvature.
    
    Uses √2, √3, √5 contributions and φ scaling.
    
    Args:
        x: Input value
        
    Returns:
        Irrational curvature
    """
    sqrt2_contrib = SQRT2 * abs(x)
    sqrt3_contrib = SQRT3 * abs(x) * 0.5
    sqrt5_contrib = SQRT5 * abs(x) * 0.3
    
    phi_scaling = PHI * abs(x)
    
    return sqrt2_contrib + sqrt3_contrib + sqrt5_contrib + phi_scaling


def combined_curvature(
    x: float,
    triplet: Triplet | None = None,
    shell: Shell = Shell.PRESENCE
) -> float:
    """
    Compute combined curvature from all sources.
    
    Uses sin(x), cos(x), tan(x), √2, √3, √5, φ, π/φ, and reptend-modulated curvature.
    
    Args:
        x: Input value
        triplet: Optional triplet
        shell: Current shell
        
    Returns:
        Combined curvature
    """
    # Base shell curvature
    kappa_shell = shell_curvature(shell)
    
    # Trig contribution
    trig_contrib = trig_curvature(x)
    
    # Irrational contribution
    irr_contrib = irrational_curvature(x) * 0.1
    
    # Triplet contribution
    triplet_contrib = 0.0
    if triplet:
        triplet_contrib = triplet.curvature() * 0.2
    
    # Reptend contribution (if we have a prime)
    reptend_contrib = 0.0
    if triplet and triplet.triplet_type.value == "combinatoric":
        p = int(triplet.a)
        reptend_contrib = reptend_curvature(p) * 0.15
    
    # Combined
    total = (
        kappa_shell +
        trig_contrib * 0.3 +
        irr_contrib +
        triplet_contrib +
        reptend_contrib
    )
    
    return total

