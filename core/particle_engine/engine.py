"""
ParticleEngine - PrimeFlux particle dynamics engine.

Refactored from pf_particle_engine.py
Integrates with trig modes and presence operator.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple
from .particle import PFParticle, OrbitalChild, OrbitalShell


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
        self.shells: List[OrbitalShell] = []
        self.nucleus: Optional[PFParticle] = None  # Nucleus particle (atom center)
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
    
    def update_particle(self, particle: PFParticle, curvature: float, phase: float, dt: float):
        """
        Update particle with force calculation.
        
        Handles OrbitalChild inheritance from parent shell.
        
        Args:
            particle: Particle to update
            curvature: Curvature value
            phase: Phase value
            dt: Time step
        """
        # Calculate base force
        force = self.calculate_force(particle, curvature, phase)
        
        # If OrbitalChild, inherit force from parent and handle flux dip
        if isinstance(particle, OrbitalChild) and particle.parent_shell is not None:
            # Flux dip: child.phase += flux_dip_prob * parent.phase
            # Electron "time in nucleus" - phase influenced by parent
            particle.phase += particle.flux_dip_prob * particle.parent_shell.phase
            
            # Inherit force: inherit_force = parent.curvature * (π - e)
            inherit_force_magnitude = particle.parent_shell.curvature * (math.pi - math.e)
            
            # Direction based on child position relative to nucleus
            if self.nucleus is not None:
                dx = particle.position[0] - self.nucleus.position[0]
                dy = particle.position[1] - self.nucleus.position[1]
                dz = particle.position[2] - self.nucleus.position[2]
                r = math.sqrt(dx**2 + dy**2 + dz**2)
                
                if r > 0:
                    inherit_force = (
                        (dx / r) * inherit_force_magnitude,
                        (dy / r) * inherit_force_magnitude,
                        (dz / r) * inherit_force_magnitude
                    )
                    # Add inherited force
                    force = (
                        force[0] + inherit_force[0],
                        force[1] + inherit_force[1],
                        force[2] + inherit_force[2]
                    )
            
            # Inner constrains: Cap force by parent curvature * (π - e)
            max_force = particle.parent_shell.curvature * (math.pi - math.e)
            force_magnitude = math.sqrt(force[0]**2 + force[1]**2 + force[2]**2)
            if force_magnitude > max_force:
                scale = max_force / force_magnitude
                force = (
                    force[0] * scale,
                    force[1] * scale,
                    force[2] * scale
                )
        
        # Update momentum
        particle.update_momentum(force, dt)
        
        # Update position
        particle.update_position(dt)
    
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
            self.update_particle(particle, curvature, phase, dt)
        
        # Atom movement: outer shells drive nucleus
        # Outer drives movement, inner constrains identity
        if self.nucleus is not None:
            # Calculate drag from outer shells only (outer drives)
            atom_velocity = [0.0, 0.0, 0.0]
            
            for shell in self.shells:
                for child in shell.children:
                    # Only outer children (drive behavior) contribute to movement
                    if child.behavior == "drive" and hasattr(child, 'drag'):
                        # Drag direction: from nucleus to child
                        dx = child.position[0] - self.nucleus.position[0]
                        dy = child.position[1] - self.nucleus.position[1]
                        dz = child.position[2] - self.nucleus.position[2]
                        r = math.sqrt(dx**2 + dy**2 + dz**2)
                        
                        if r > 0:
                            atom_velocity[0] += (dx / r) * child.drag
                            atom_velocity[1] += (dy / r) * child.drag
                            atom_velocity[2] += (dz / r) * child.drag
            
            # Update nucleus position: outer drives inner
            self.nucleus.position = (
                self.nucleus.position[0] + atom_velocity[0] * dt,
                self.nucleus.position[1] + atom_velocity[1] * dt,
                self.nucleus.position[2] + atom_velocity[2] * dt
            )
        
        # Advance time
        self.time += dt
    
    def get_total_energy(self) -> float:
        """Get total energy of all particles."""
        return sum(p.energy for p in self.particles)
    
    def get_particles(self) -> List[PFParticle]:
        """Get all particles."""
        return self.particles.copy()
