"""
Combinatorics of Triplets.

(p, p, q) triplet math and combinatoric explosion.
"""

from __future__ import annotations

import math


def combinatoric_flux(p: int, q: int) -> float:
    """
    Compute combinatoric flux.
    
    Args:
        p: First prime
        q: Second prime
        
    Returns:
        Flux value
    """
    # Flux = log(p·q) with interaction
    return math.log(p * q)


def combinatoric_entropy(p: int, q: int) -> float:
    """
    Compute combinatoric entropy.
    
    Entropy = log(p) + log(q)
    
    Args:
        p: First prime
        q: Second prime
        
    Returns:
        Entropy value
    """
    return math.log(p) + math.log(q)


def combinatoric_curvature(p: int, q: int) -> float:
    """
    Compute combinatoric curvature.
    
    Curvature = log(p·q)
    
    Args:
        p: First prime
        q: Second prime
        
    Returns:
        Curvature value
    """
    return math.log(p * q)

