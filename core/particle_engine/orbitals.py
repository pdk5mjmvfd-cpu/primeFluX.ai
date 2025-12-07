"""
Orbitals - PrimeFlux atomic orbital calculations.

Merged from compute_orbital_suite.py and pf_atomic_orbitals.py
"""

from __future__ import annotations

import math
from typing import List, Dict, Any, Tuple
from .particle import PFParticle


def compute_orbital_suite(
    prime: int,
    n_max: int = 3
) -> Dict[str, Any]:
    """
    Compute orbital suite for given prime.
    
    Args:
        prime: Prime number
        n_max: Maximum principal quantum number
        
    Returns:
        Orbital suite dictionary
    """
    orbitals = []
    
    for n in range(1, n_max + 1):
        for l in range(n):
            for m in range(-l, l + 1):
                # Calculate orbital energy
                energy = -1.0 / (n * n)  # Simplified hydrogen-like
                
                # Calculate orbital radius
                radius = n * n * prime / 100.0  # Scaled by prime
                
                orbitals.append({
                    "n": n,
                    "l": l,
                    "m": m,
                    "energy": energy,
                    "radius": radius,
                    "prime": prime
                })
    
    return {
        "prime": prime,
        "orbital_count": len(orbitals),
        "orbitals": orbitals
    }


def pf_atomic_orbitals(
    prime: int,
    num_electrons: int = None
) -> List[Dict[str, Any]]:
    """
    Calculate PrimeFlux atomic orbitals.
    
    Args:
        prime: Prime number
        num_electrons: Number of electrons (default: prime)
        
    Returns:
        List of orbital dictionaries
    """
    if num_electrons is None:
        num_electrons = prime
    
    orbitals = []
    
    # Fill orbitals following Aufbau principle
    n = 1
    electron_count = 0
    
    while electron_count < num_electrons:
        for l in range(n):
            max_electrons = 2 * (2 * l + 1)  # 2(2l+1) electrons per subshell
            
            for m in range(-l, l + 1):
                if electron_count >= num_electrons:
                    break
                
                orbital = {
                    "n": n,
                    "l": l,
                    "m": m,
                    "energy": -1.0 / (n * n),
                    "occupied": True,
                    "prime": prime
                }
                orbitals.append(orbital)
                electron_count += 1
        
        n += 1
    
    return orbitals


def orbital_to_particle(orbital: Dict[str, Any]) -> PFParticle:
    """
    Convert orbital to particle representation.
    
    Args:
        orbital: Orbital dictionary
        
    Returns:
        PFParticle
    """
    n = orbital["n"]
    l = orbital["l"]
    m = orbital["m"]
    prime = orbital.get("prime", 2)
    
    # Spherical coordinates
    r = n * n * prime / 100.0
    theta = math.acos(m / (l + 1)) if l > 0 else 0.0
    phi = 2 * math.pi * prime / 100.0
    
    # Convert to Cartesian
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    
    # Momentum from quantum numbers
    px = l * math.cos(phi)
    py = l * math.sin(phi)
    pz = m
    
    return PFParticle(
        position=(x, y, z),
        momentum=(px, py, pz),
        prime=prime,
        energy=orbital.get("energy", 0.0)
    )
