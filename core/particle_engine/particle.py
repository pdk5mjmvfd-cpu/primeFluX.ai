"""
PFParticle - PrimeFlux particle representation.

Refactored from pf_particle.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class PFParticle:
    """
    PrimeFlux particle with position, momentum, and prime properties.
    
    Particles represent distinctions in PrimeFlux geometry.
    """
    position: Tuple[float, float, float]  # (x, y, z)
    momentum: Tuple[float, float, float]  # (px, py, pz)
    prime: int  # Prime number associated with particle
    mass: float = 1.0
    charge: float = 0.0
    energy: float = 0.0
    
    def __post_init__(self):
        """Calculate energy from momentum."""
        if self.energy == 0.0:
            # Kinetic energy: E = p²/(2m)
            p_squared = sum(p**2 for p in self.momentum)
            self.energy = p_squared / (2.0 * self.mass)
    
    def update_position(self, dt: float):
        """Update position based on momentum."""
        x, y, z = self.position
        px, py, pz = self.momentum
        
        self.position = (
            x + (px / self.mass) * dt,
            y + (py / self.mass) * dt,
            z + (pz / self.mass) * dt
        )
    
    def update_momentum(self, force: Tuple[float, float, float], dt: float):
        """Update momentum based on force."""
        fx, fy, fz = force
        px, py, pz = self.momentum
        
        self.momentum = (
            px + fx * dt,
            py + fy * dt,
            pz + fz * dt
        )
        
        # Recalculate energy
        p_squared = sum(p**2 for p in self.momentum)
        self.energy = p_squared / (2.0 * self.mass)
    
    def distance_to(self, other: PFParticle) -> float:
        """Calculate distance to another particle."""
        dx = self.position[0] - other.position[0]
        dy = self.position[1] - other.position[1]
        dz = self.position[2] - other.position[2]
        return math.sqrt(dx**2 + dy**2 + dz**2)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "position": self.position,
            "momentum": self.momentum,
            "prime": self.prime,
            "mass": self.mass,
            "charge": self.charge,
            "energy": self.energy
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PFParticle":
        """Create from dictionary."""
        return cls(
            position=tuple(data["position"]),
            momentum=tuple(data["momentum"]),
            prime=data["prime"],
            mass=data.get("mass", 1.0),
            charge=data.get("charge", 0.0),
            energy=data.get("energy", 0.0)
        )
