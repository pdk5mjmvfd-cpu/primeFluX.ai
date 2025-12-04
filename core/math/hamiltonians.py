"""
PrimeFlux Hamiltonian.

H(x) = κ₂ sin(x) + κ₃ tan(x) + log(|x| + 2)

Where:
- κ₂ = √2 (shell 2 curvature)
- κ₃ = π / φ (shell 3 curvature)

Collapse occurs when H(x) > φ²
"""

from __future__ import annotations

import math
from .shells import Shell, shell_curvature

SQRT2 = math.sqrt(2)
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi


def hamiltonian(x: float) -> float:
    """
    Compute PrimeFlux Hamiltonian.
    
    H(x) = κ₂ sin(x) + κ₃ tan(x) + log(|x| + 2)
    
    Args:
        x: Input value
        
    Returns:
        Hamiltonian value
    """
    kappa2 = SQRT2  # Shell 2 curvature
    kappa3 = PI / PHI  # Shell 3 curvature
    
    sin_term = kappa2 * math.sin(x)
    
    tan_val = math.tan(x)
    if abs(tan_val) > 1e10:
        tan_val = math.copysign(1e10, tan_val)
    
    tan_term = kappa3 * tan_val
    log_term = math.log(abs(x) + 2.0)
    
    return sin_term + tan_term + log_term


def curvature_well(x: float) -> float:
    """
    Compute curvature potential well.
    
    Args:
        x: Input value
        
    Returns:
        Potential well depth
    """
    H = hamiltonian(x)
    kappa4 = PHI ** 2  # Collapse threshold
    
    # Well depth = distance from collapse
    return kappa4 - H


def collapse_energy(x: float) -> float:
    """
    Compute collapse energy.
    
    Collapse occurs when H(x) > φ².
    
    Args:
        x: Input value
        
    Returns:
        Collapse energy (positive = collapsed)
    """
    H = hamiltonian(x)
    kappa4 = PHI ** 2  # Collapse threshold
    
    return H - kappa4

