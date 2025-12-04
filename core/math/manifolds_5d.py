"""
PF 5D Manifold Embedding.

5D PF coordinate space: [x, κ, ρ, ψ, H]

Where:
- x = state value
- κ = curvature
- ρ = distinction density
- ψ = superposition magnitude
- H = Hamiltonian
"""

from __future__ import annotations

from typing import Tuple
import math
from .hamiltonians import hamiltonian
from .superposition import magnitude
from .density import distinction_density


def embed_to_5d(
    x: float,
    curvature: float,
    density: float,
    a: float = 0.0,
    b: float = 1.0
) -> Tuple[float, float, float, float, float]:
    """
    Embed state to 5D PF coordinate space.
    
    [x, κ, ρ, ψ, H]
    
    Args:
        x: State value
        curvature: Curvature value
        density: Distinction density
        a: Superposition coefficient a
        b: Superposition coefficient b
        
    Returns:
        5D coordinates (x, κ, ρ, ψ, H)
    """
    psi = magnitude(a, b)
    H = hamiltonian(x)
    
    return (x, curvature, density, psi, H)


def curvature_5d(state: Tuple[float, float, float, float, float]) -> float:
    """
    Extract curvature from 5D state.
    
    Args:
        state: 5D coordinates (x, κ, ρ, ψ, H)
        
    Returns:
        Curvature value
    """
    return state[1]  # κ is second element


def projection_3d(
    state: Tuple[float, float, float, float, float]
) -> Tuple[float, float, float]:
    """
    Project 5D state to 3D.
    
    Projects to (x, κ, H).
    
    Args:
        state: 5D coordinates
        
    Returns:
        3D projection (x, κ, H)
    """
    x, kappa, _, _, H = state
    return (x, kappa, H)

