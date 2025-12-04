"""
PrimeFlux Shells — shell transition logic.

Shells:
- 0 = presence (unmeasured context)
- 2 = measurement (duality creation - NOT limiting)
- 3 = flux/curvature (error-driven flow)
- 4 = collapse (only after stabilization, not measurement)

PF Measurement Principle:
Measurement is NOT a limiting step.
Measurement is the gateway from Shell 0 → Shell 2,
where the system gains a new degree of freedom (error),
not loses one.

Measurement creates duality.
Duality creates error.
Error creates curvature.
Curvature creates flow.
Flow creates identity continuation.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional
import math


class Shell(Enum):
    """PrimeFlux shell enumeration."""
    PRESENCE = 0
    MEASUREMENT = 2
    FLUX = 3
    COLLAPSE = 4


# Transition rules: (from_shell, to_shell) -> allowed
transition_rules: dict[tuple[Shell, Shell], bool] = {
    (Shell.PRESENCE, Shell.MEASUREMENT): True,
    (Shell.MEASUREMENT, Shell.FLUX): True,
    (Shell.FLUX, Shell.COLLAPSE): True,
    (Shell.COLLAPSE, Shell.PRESENCE): True,
    # Disallow backwards transitions
    (Shell.MEASUREMENT, Shell.PRESENCE): False,
    (Shell.FLUX, Shell.MEASUREMENT): False,
    (Shell.COLLAPSE, Shell.FLUX): False,
    (Shell.PRESENCE, Shell.COLLAPSE): False,
    # Same shell transitions allowed
    (Shell.PRESENCE, Shell.PRESENCE): True,
    (Shell.MEASUREMENT, Shell.MEASUREMENT): True,
    (Shell.FLUX, Shell.FLUX): True,
    (Shell.COLLAPSE, Shell.COLLAPSE): True,
}


def validate_transition(prev: Shell, next_shell: Shell) -> bool:
    """
    Validate that a shell transition is allowed.

    Args:
        prev: Previous shell
        next_shell: Next shell

    Returns:
        True if transition is valid, False otherwise
    """
    return transition_rules.get((prev, next_shell), False)


def shell_of_value(x: float) -> Shell:
    """
    Determine which shell a value belongs to.
    
    Uses magnitude thresholds from PF math:
    - Irrational thresholds (√2, φ, π)
    - Curvature thresholds
    - Distinction density

    Args:
        x: Input value

    Returns:
        Shell assignment
    """
    abs_x = abs(x)
    sqrt2 = math.sqrt(2.0)
    phi = (1.0 + math.sqrt(5.0)) / 2.0  # Golden ratio
    pi = math.pi
    
    # Shell 0: Presence (indistinct)
    # Values close to 0 or very small
    if abs_x < 0.001:
        return Shell.PRESENCE
    
    # Shell 2: Measurement (duality)
    # Values in range [0, √2) or around 1
    if abs_x < sqrt2 or (abs(abs_x - 1.0) < 0.1):
        return Shell.MEASUREMENT
    
    # Shell 3: Flux/Curvature
    # Values in range [√2, φ) or around π/2
    if sqrt2 <= abs_x < phi or (abs(abs_x - pi/2) < 0.5):
        return Shell.FLUX
    
    # Shell 4: Collapse (commit)
    # Values >= φ or large values
    if abs_x >= phi:
        return Shell.COLLAPSE
    
    # Default to measurement for intermediate values
    return Shell.MEASUREMENT

