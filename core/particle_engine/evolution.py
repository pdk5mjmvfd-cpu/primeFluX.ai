"""
PFEvolution - PrimeFlux evolution dynamics.

Refactored from pf_evolution.py
"""

from __future__ import annotations

from typing import List, Dict, Any
from .particle import PFParticle
from .engine import ParticleEngine


class PFEvolution:
    """
    PrimeFlux evolution dynamics.
    
    Tracks evolution of particle systems over time.
    """
    
    def __init__(self):
        """Initialize evolution tracker."""
        self.generations: List[Dict[str, Any]] = []
    
    def evolve(
        self,
        engine: ParticleEngine,
        generations: int,
        dt: float = 0.01
    ) -> List[Dict[str, Any]]:
        """
        Evolve particle system over generations.
        
        Args:
            engine: Particle engine
            generations: Number of generations
            dt: Time step per generation
            
        Returns:
            Evolution history
        """
        for gen in range(generations):
            # Step engine
            engine.step(dt, curvature=1.0)
            
            # Record generation
            gen_data = {
                "generation": gen,
                "time": engine.time,
                "particle_count": len(engine.particles),
                "total_energy": engine.get_total_energy(),
                "particles": [p.to_dict() for p in engine.particles]
            }
            self.generations.append(gen_data)
        
        return self.generations
    
    def get_generation(self, gen: int) -> Dict[str, Any]:
        """Get generation data."""
        if 0 <= gen < len(self.generations):
            return self.generations[gen]
        return {}
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """Get evolution summary."""
        if not self.generations:
            return {}
        
        return {
            "total_generations": len(self.generations),
            "final_energy": self.generations[-1].get("total_energy", 0.0),
            "initial_energy": self.generations[0].get("total_energy", 0.0),
            "energy_change": (
                self.generations[-1].get("total_energy", 0.0) -
                self.generations[0].get("total_energy", 0.0)
            )
        }
