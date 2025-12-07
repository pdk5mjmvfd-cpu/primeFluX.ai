"""
ParticleEngine - PrimeFlux particle dynamics engine.

Refactored from pf_particle_engine.py
Integrates with trig modes and presence operator.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple
from .particle import PFParticle


class ParticleEngine:
    """
    PrimeFlux particle dynamics engine.
    
    Integrates trig modes: force = g_PF * curvature
    Uses math.sin/cos/tan based on mode.
    """
    
    def __init__(self, mode: str = 'refinement', presence_on: bool = True):
        """
        Initialize particle engine.
        
        Args:
            mode: Mode (research/refinement/relations)
            presence_on: Whether presence operator is enabled
        """
        self.particles: List[PFParticle] = []
        self.mode = mode
        self.presence_on = presence_on
        self.time = 0.0
    
    def presence_operator(self, phase: float) -> float:
        """
        Presence operator: g_PF(phase, mode) = trig(mode) if presence_on else 0.
        
        Args:
            phase: Phase value
            
        Returns:
            Presence value
        """
        if not self.presence_on:
            return 0.0
        
        if self.mode == 'research':
            return math.sin(phase)
        elif self.mode == 'refinement':
            return math.cos(phase)
        elif self.mode == 'relations':
            return math.tan(phase)
        else:
            return math.cos(phase)  # Default
    
    def calculate_force(
        self,
        particle: PFParticle,
        curvature: float,
        phase: float
    ) -> Tuple[float, float, float]:
        """
        Calculate force on particle.
        
        Force = g_PF * curvature
        
        Args:
            particle: Particle to calculate force for
            curvature: Curvature value
            phase: Phase value
            
        Returns:
            Force vector (fx, fy, fz)
        """
        g_pf = self.presence_operator(phase)
        
        # Force = g_PF * curvature
        force_magnitude = g_pf * curvature
        
        # Direction based on particle position (radial)
        x, y, z = particle.position
        r = math.sqrt(x**2 + y**2 + z**2)
        
        if r > 0:
            # Radial force
            fx = (x / r) * force_magnitude
            fy = (y / r) * force_magnitude
            fz = (z / r) * force_magnitude
        else:
            fx, fy, fz = 0.0, 0.0, 0.0
        
        return (fx, fy, fz)
    
    def add_particle(self, particle: PFParticle):
        """Add particle to engine."""
        self.particles.append(particle)
    
    def step(self, dt: float, curvature: float = 1.0):
        """
        Advance simulation by one step.
        
        Args:
            dt: Time step
            curvature: Curvature value
        """
        # Calculate phase from time
        phase = self.time % (2 * math.pi)
        
        # Update each particle
        for particle in self.particles:
            # Calculate force
            force = self.calculate_force(particle, curvature, phase)
            
            # Update momentum
            particle.update_momentum(force, dt)
            
            # Update position
            particle.update_position(dt)
        
        # Advance time
        self.time += dt
    
    def get_total_energy(self) -> float:
        """Get total energy of all particles."""
        return sum(p.energy for p in self.particles)
    
    def get_particles(self) -> List[PFParticle]:
        """Get all particles."""
        return self.particles.copy()
