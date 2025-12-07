"""
ParticleSimulator - PrimeFlux particle simulation.

Refactored from particle_simulator.py
"""

from __future__ import annotations

import math
from typing import List, Dict, Any
from .particle import PFParticle
from .engine import ParticleEngine
from .geometry import BoundaryMapper


class ParticleSimulator:
    """
    Particle simulator for PrimeFlux dynamics.
    
    Runs simulations with prime-based particle systems.
    """
    
    def __init__(
        self,
        mode: str = 'refinement',
        presence_on: bool = True,
        bounds: tuple = (10.0, 10.0, 10.0)
    ):
        """
        Initialize simulator.
        
        Args:
            mode: Mode (research/refinement/relations)
            presence_on: Whether presence operator is enabled
            bounds: Boundary box
        """
        self.engine = ParticleEngine(mode=mode, presence_on=presence_on)
        self.boundary = BoundaryMapper(bounds=bounds)
        self.history: List[Dict[str, Any]] = []
    
    def add_particle(self, particle: PFParticle):
        """Add particle to simulation."""
        self.engine.add_particle(particle)
    
    def run_simulation(
        self,
        prime: int,
        steps: int,
        dt: float = 0.01,
        curvature: float = 1.0
    ) -> Dict[str, Any]:
        """
        Run simulation for given prime and steps.
        
        Args:
            prime: Prime number for simulation
            steps: Number of simulation steps
            dt: Time step
            curvature: Curvature value
            
        Returns:
            Simulation results
        """
        # Initialize particles if empty
        if not self.engine.particles:
            # Create particles based on prime
            for i in range(prime):
                particle = PFParticle(
                    position=(
                        math.cos(2 * math.pi * i / prime),
                        math.sin(2 * math.pi * i / prime),
                        0.0
                    ),
                    momentum=(0.0, 0.0, 0.0),
                    prime=prime
                )
                self.engine.add_particle(particle)
        
        # Run simulation
        initial_energy = self.engine.get_total_energy()
        
        for step in range(steps):
            # Step simulation
            self.engine.step(dt, curvature)
            
            # Apply boundaries
            self.engine.particles = self.boundary.map_particles(
                self.engine.particles
            )
            
            # Record state
            if step % 10 == 0:  # Record every 10 steps
                self.history.append({
                    "step": step,
                    "time": self.engine.time,
                    "energy": self.engine.get_total_energy(),
                    "particle_count": len(self.engine.particles)
                })
        
        final_energy = self.engine.get_total_energy()
        energy_conservation = abs(final_energy - initial_energy) / max(initial_energy, 1.0)
        
        return {
            "prime": prime,
            "steps": steps,
            "initial_energy": initial_energy,
            "final_energy": final_energy,
            "energy_conservation": energy_conservation,
            "particle_count": len(self.engine.particles),
            "history": self.history,
            "mode": self.engine.mode,
            "presence_on": self.engine.presence_on
        }
    
    def get_particles(self) -> List[PFParticle]:
        """Get current particles."""
        return self.engine.get_particles()
    
    def reset(self):
        """Reset simulator."""
        self.engine.particles = []
        self.history = []
        self.engine.time = 0.0
