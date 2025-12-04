"""
Flux Operators.

F(x) = tanh(α·tan(β·x))
where α = √2, β = π/3

Fθ(x) = θ₀ sin(θ₁ x) + θ₂ tan(θ₃ x)
"""

from __future__ import annotations

import math
from typing import Tuple

SQRT2 = math.sqrt(2)
PI = math.pi


def flux_basic(x: float) -> float:
    """
    Basic flux operator: F(x) = tanh(α·tan(β·x)).
    
    Where α = √2, β = π/3.
    
    Args:
        x: Input value
        
    Returns:
        Flux value
    """
    alpha = SQRT2
    beta = PI / 3.0
    
    return math.tanh(alpha * math.tan(beta * x))


def flux_general(
    x: float,
    theta: Tuple[float, float, float, float] | None = None
) -> float:
    """
    General flux operator: Fθ(x) = θ₀ sin(θ₁ x) + θ₂ tan(θ₃ x).
    
    Args:
        x: Input value
        theta: Optional parameters (θ₀, θ₁, θ₂, θ₃)
               Default: (1.0, 1.0, 1.0, 1.0)
        
    Returns:
        Flux value
    """
    if theta is None:
        theta = (1.0, 1.0, 1.0, 1.0)
    
    theta0, theta1, theta2, theta3 = theta
    
    sin_term = theta0 * math.sin(theta1 * x)
    
    tan_val = math.tan(theta3 * x)
    if abs(tan_val) > 1e10:
        tan_val = math.copysign(1e10, tan_val)
    
    tan_term = theta2 * tan_val
    
    return sin_term + tan_term


def flux_propagate(x: float, curvature: float) -> float:
    """
    Propagate flux with curvature modulation.
    
    Args:
        x: Input value
        curvature: Curvature value
        
    Returns:
        Propagated flux
    """
    base_flux = flux_basic(x)
    
    # Curvature modulation
    curvature_factor = 1.0 + curvature * 0.2
    
    return base_flux * curvature_factor

