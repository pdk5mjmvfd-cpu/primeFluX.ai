"""
Orbitals - PrimeFlux atomic orbital calculations.

Merged from compute_orbital_suite.py and pf_atomic_orbitals.py
"""

from __future__ import annotations

import math
import random
from enum import Enum
from typing import List, Dict, Any, Tuple, Optional
from .particle import PFParticle, OrbitalChild, OrbitalShell


class QuarkColor(Enum):
    """Quark color phases for orbital children."""
    RED = 0.0
    GREEN = 2 * math.pi / 3
    BLUE = 4 * math.pi / 3
    
    @property
    def phase(self) -> float:
        """Get phase value."""
        return self.value
    
    @property
    def color_idx(self) -> int:
        """Get color index (0=RED, 1=GREEN, 2=BLUE)."""
        if self == QuarkColor.RED:
            return 0
        elif self == QuarkColor.GREEN:
            return 1
        else:  # BLUE
            return 2


def compute_orbital_suite(
    prime: int,
    n_max: int = 3,
    presence_on: bool = True
) -> Dict[str, Any]:
    """
    Compute orbital suite for given prime.
    
    Args:
        prime: Prime number
        n_max: Maximum principal quantum number
        presence_on: Whether event spaces are active
        
    Returns:
        Orbital suite dictionary
    """
    if not presence_on:
        return {
            "prime": prime,
            "orbital_count": 0,
            "orbitals": [],
            "status": "Static knot - atom as pure event space"
        }
    
    orbitals = []
    max_layer = n_max
    
    for n in range(1, n_max + 1):
        for l in range(n):
            for m in range(-l, l + 1):
                # Calculate orbital energy
                energy = -1.0 / (n * n)  # Simplified hydrogen-like
                
                # Calculate orbital radius
                radius = n * n * prime / 100.0  # Scaled by prime
                
                # Determine behavior: outer drives, inner constrains
                layer = n  # Layer number
                behavior = "drive" if layer > max_layer / 2 else "constrain"
                
                orbitals.append({
                    "n": n,
                    "l": l,
                    "m": m,
                    "energy": energy,
                    "radius": radius,
                    "prime": prime,
                    "layer": layer,
                    "behavior": behavior
                })
    
    return {
        "prime": prime,
        "orbital_count": len(orbitals),
        "orbitals": orbitals,
        "max_layer": max_layer
    }


def pf_atomic_orbitals(
    prime: int,
    num_electrons: int = None,
    presence_on: bool = True,
    nucleus_time_prob: float = 0.1
) -> List[Dict[str, Any]]:
    """
    Calculate PrimeFlux atomic orbitals with quark colors.
    
    Args:
        prime: Prime number
        num_electrons: Number of electrons (default: prime)
        presence_on: Whether event spaces are active
        nucleus_time_prob: Probability of electron dipping into nucleus
        
    Returns:
        List of orbital dictionaries with quark color phases
    """
    if num_electrons is None:
        num_electrons = prime
    
    orbitals = []
    quark_colors = [QuarkColor.RED, QuarkColor.GREEN, QuarkColor.BLUE]
    
    # Nucleus quark phases (one per color)
    nucleus_quark_phase = {
        QuarkColor.RED: random.uniform(0, 2 * math.pi),
        QuarkColor.GREEN: random.uniform(0, 2 * math.pi),
        QuarkColor.BLUE: random.uniform(0, 2 * math.pi)
    }
    
    # Fill orbitals following Aufbau principle
    n = 1
    electron_count = 0
    max_layer = 0
    
    while electron_count < num_electrons:
        for l in range(n):
            max_electrons = 2 * (2 * l + 1)  # 2(2l+1) electrons per subshell
            
            for m in range(-l, l + 1):
                if electron_count >= num_electrons:
                    break
                
                # Assign quark color (cycle through RED, GREEN, BLUE)
                color = quark_colors[electron_count % 3]
                
                # Electron phase: nucleus.quark_phase[color] + nucleus_time_prob * random
                electron_phase = (
                    nucleus_quark_phase[color] +
                    nucleus_time_prob * random.uniform(-0.1, 0.1)
                )
                
                # Determine behavior: outer drives, inner constrains
                layer = n
                if layer > max_layer:
                    max_layer = layer
                
                # For children: behavior = "drive" if layer > max_layer / 2 else "constrain"
                behavior = "drive" if layer > max_layer / 2 else "constrain"
                
                orbital = {
                    "n": n,
                    "l": l,
                    "m": m,
                    "energy": -1.0 / (n * n),
                    "occupied": True,
                    "prime": prime,
                    "quark_color": color.name,
                    "quark_phase": electron_phase,
                    "color_idx": color.color_idx,
                    "active": presence_on,  # Event space toggle
                    "layer": layer,
                    "behavior": behavior
                }
                orbitals.append(orbital)
                electron_count += 1
        
        n += 1
    
    # Update behavior based on final max_layer
    for orbital in orbitals:
        if orbital["layer"] > max_layer / 2:
            orbital["behavior"] = "drive"
        else:
            orbital["behavior"] = "constrain"
    
    if not presence_on:
        # Return static knot message
        return [{"status": "Static knot - atom as pure event space"}]
    
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
