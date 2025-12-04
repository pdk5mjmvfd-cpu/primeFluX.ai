"""
Superposition Logic.

Quantum-like amplitude logic:
ψ = a|0⟩ + b|1⟩
|ψ| = √( |a|² + |b|² )
"""

from __future__ import annotations

import math
from .shells import Shell


def amplitude(a: float, b: float) -> float:
    """
    Compute superposition amplitude.
    
    |ψ| = √( |a|² + |b|² )
    
    Args:
        a: Coefficient for |0⟩
        b: Coefficient for |1⟩
        
    Returns:
        Amplitude
    """
    return math.sqrt(a**2 + b**2)


def magnitude(a: float, b: float) -> float:
    """
    Compute superposition magnitude (same as amplitude).
    
    Args:
        a: Coefficient for |0⟩
        b: Coefficient for |1⟩
        
    Returns:
        Magnitude
    """
    return amplitude(a, b)


def shell_from_superposition(psi: float) -> Shell:
    """
    Map superposition magnitude to shell.
    
    if |ψ| < 0.5 → shell 0
    if |ψ| < 0.8 → shell 2
    if |ψ| < 1.2 → shell 3
    else → shell 4
    
    Args:
        psi: Superposition magnitude
        
    Returns:
        Shell
    """
    if psi < 0.5:
        return Shell.PRESENCE
    elif psi < 0.8:
        return Shell.MEASUREMENT
    elif psi < 1.2:
        return Shell.CURVATURE
    else:
        return Shell.COLLAPSE
