"""
PrimeFlux Shells.

Shell transitions, shell curvature constants.

PF sequence: Presence (0) → Measurement (2) → Curvature (3) → Collapse (4)
"""

from __future__ import annotations

from enum import IntEnum
import math

SQRT2 = math.sqrt(2)
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio ≈ 1.618
PI = math.pi


class Shell(IntEnum):
    """PrimeFlux shell enumeration."""
    PRESENCE = 0
    MEASUREMENT = 2
    CURVATURE = 3
    COLLAPSE = 4


def shell_curvature(shell: Shell) -> float:
    """
    Get curvature value for a shell.
    
    κ₀ = 0
    κ₂ = √2
    κ₃ = π / φ
    κ₄ = φ²
    
    Args:
        shell: PF shell
        
    Returns:
        Curvature value
    """
    if shell == Shell.PRESENCE:
        return 0.0
    elif shell == Shell.MEASUREMENT:
        return SQRT2
    elif shell == Shell.CURVATURE:
        return PI / PHI
    elif shell == Shell.COLLAPSE:
        return PHI ** 2
    else:
        return 0.0


def next_shell(shell: Shell, curvature: float, entropy: float) -> Shell:
    """
    Determine next shell based on curvature and entropy.
    
    Transition rules:
    - presence → measurement: driven by √2 - 1
    - measurement → curvature: trig triplet
    - curvature → collapse: φ² potential well
    
    Args:
        shell: Current shell
        curvature: Current curvature
        entropy: Current entropy
        
    Returns:
        Next shell
    """
    if shell == Shell.PRESENCE:
        # Presence → measurement: driven by √2 - 1
        threshold = SQRT2 - 1.0
        if curvature >= threshold or entropy < 1.5:
            return Shell.MEASUREMENT
        return Shell.PRESENCE
    
    elif shell == Shell.MEASUREMENT:
        # Measurement → curvature: trig triplet
        if curvature >= SQRT2 * 0.8 or entropy < 1.2:
            return Shell.CURVATURE
        return Shell.MEASUREMENT
    
    elif shell == Shell.CURVATURE:
        # Curvature → collapse: φ² potential well
        if curvature >= PHI ** 2 * 0.9 or entropy < 0.6:
            return Shell.COLLAPSE
        return Shell.CURVATURE
    
    elif shell == Shell.COLLAPSE:
        # Collapse → presence (reset)
        return Shell.PRESENCE
    
    return Shell.PRESENCE


def shell_from_value(x: float) -> Shell:
    """
    Map a value to a shell based on magnitude.
    
    Args:
        x: Input value
        
    Returns:
        Shell
    """
    abs_x = abs(x)
    
    if abs_x < 0.5:
        return Shell.PRESENCE
    elif abs_x < SQRT2:
        return Shell.MEASUREMENT
    elif abs_x < PI / PHI:
        return Shell.CURVATURE
    else:
        return Shell.COLLAPSE


def shell_transition_probability(shell: Shell, curvature: float) -> float:
    """
    Compute probability of shell transition.
    
    Args:
        shell: Current shell
        curvature: Current curvature
        
    Returns:
        Transition probability (0.0 to 1.0)
    """
    kappa = shell_curvature(shell)
    
    if kappa == 0:
        return 0.0
    
    # Probability based on curvature ratio
    ratio = curvature / kappa
    
    # Sigmoid function for smooth transition
    import math
    return 1.0 / (1.0 + math.exp(-5.0 * (ratio - 0.8)))

