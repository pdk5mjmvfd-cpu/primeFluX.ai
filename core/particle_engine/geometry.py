"""
BoundaryMapper - PrimeFlux boundary geometry.

Refactored from boundary_mapper.py
"""

from __future__ import annotations

import math
from typing import Tuple, List
from .particle import PFParticle


class BoundaryMapper:
    """
    Maps particles to boundary geometry.
    
    Handles periodic boundaries and geometric constraints.
    """
    
    def __init__(self, bounds: Tuple[float, float, float] = (10.0, 10.0, 10.0)):
        """
        Initialize boundary mapper.
        
        Args:
            bounds: Boundary box (x_max, y_max, z_max)
        """
        self.bounds = bounds
    
    def apply_boundary(self, particle: PFParticle) -> PFParticle:
        """
        Apply periodic boundary conditions.
        
        Args:
            particle: Particle to apply boundary to
            
        Returns:
            Particle with boundary applied
        """
        x, y, z = particle.position
        x_max, y_max, z_max = self.bounds
        
        # Periodic boundaries
        x = x % (2 * x_max) - x_max
        y = y % (2 * y_max) - y_max
        z = z % (2 * z_max) - z_max
        
        # Create new particle with updated position
        new_particle = PFParticle(
            position=(x, y, z),
            momentum=particle.momentum,
            prime=particle.prime,
            mass=particle.mass,
            charge=particle.charge
        )
        
        return new_particle
    
    def is_inside(self, particle: PFParticle) -> bool:
        """Check if particle is inside boundaries."""
        x, y, z = particle.position
        x_max, y_max, z_max = self.bounds
        
        return (
            -x_max <= x <= x_max and
            -y_max <= y <= y_max and
            -z_max <= z <= z_max
        )
    
    def map_particles(self, particles: List[PFParticle]) -> List[PFParticle]:
        """Map all particles to boundaries."""
        return [self.apply_boundary(p) for p in particles]
