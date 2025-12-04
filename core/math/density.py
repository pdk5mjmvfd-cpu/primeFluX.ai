"""
Distinction Density Fields.

ρ(t) = (# distinctions at t) / (window_size)
"""

from __future__ import annotations

from typing import Sequence
import math


def distinction_density(
    tokens: Sequence[int],
    window: int = 5,
    position: int | None = None
) -> float | list[float]:
    """
    Compute distinction density.
    
    ρ(t) = (# distinctions at t) / (window_size)
    
    Args:
        tokens: Sequence of distinction counts
        window: Window size
        position: Optional specific position, None for all positions
        
    Returns:
        Density value(s)
    """
    if len(tokens) == 0:
        return 0.0 if position is not None else []
    
    if position is not None:
        # Single position
        start = max(0, position - window // 2)
        end = min(len(tokens), position + window // 2 + 1)
        
        window_tokens = tokens[start:end]
        count = sum(window_tokens)
        
        return count / window
    else:
        # All positions
        return [
            distinction_density(tokens, window, i)
            for i in range(len(tokens))
        ]


def curvature_density(tokens: Sequence[int], window: int = 5) -> list[float]:
    """
    Compute curvature density field.
    
    Args:
        tokens: Sequence of distinction counts
        window: Window size
        
    Returns:
        List of curvature density values
    """
    densities = distinction_density(tokens, window)
    
    # Curvature density = density * curvature factor
    return [d * 1.5 for d in densities]


def density_gradient(tokens: Sequence[int], window: int = 5) -> list[float]:
    """
    Compute density gradient.
    
    Args:
        tokens: Sequence of distinction counts
        window: Window size
        
    Returns:
        List of gradient values
    """
    densities = distinction_density(tokens, window)
    
    if len(densities) < 2:
        return [0.0] * len(densities)
    
    # Gradient = difference between adjacent densities
    gradients = [densities[i+1] - densities[i] for i in range(len(densities) - 1)]
    gradients.append(0.0)  # Last position has no gradient
    
    return gradients

