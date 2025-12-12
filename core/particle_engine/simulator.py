"""
ParticleSimulator - PrimeFlux particle simulation.

Refactored from particle_simulator.py
"""

from __future__ import annotations

import math
from typing import List, Dict, Any, Optional, Callable
import numpy as np
from .particle import PFParticle
from .engine import ParticleEngine
from .geometry import BoundaryMapper
from ..math.path_integrals import Path, path_probability, path_integral, most_probable_path, superposition_of_paths


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
    
    def simulate_sde(self, drift: Callable[[float, float], float], 
                     diffusion: Callable[[float, float], float],
                     initial_value: float = 0.0,
                     dt: float = 0.01,
                     steps: int = 1000,
                     random_seed: Optional[int] = None) -> List[float]:
        """
        Simulate stochastic differential equation (SDE).
        
        Flux Evolution: dΦ(t) = μ(Φ, t)dt + σ(Φ, t)dW(t)
        Where:
        - μ = drift (toward attractor)
        - σ = diffusion (probabilistic spread)
        - dW = Wiener process (Brownian motion)
        
        Args:
            drift: Drift function μ(Φ, t)
            diffusion: Diffusion function σ(Φ, t)
            initial_value: Initial flux value
            dt: Time step
            steps: Number of steps
            random_seed: Optional random seed
            
        Returns:
            List of flux values over time
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        flux_values = [initial_value]
        current_flux = initial_value
        current_time = 0.0
        
        for step in range(steps):
            # Drift term
            mu = drift(current_flux, current_time)
            
            # Diffusion term (Wiener process)
            dW = np.random.normal(0.0, math.sqrt(dt))  # Brownian motion increment
            sigma = diffusion(current_flux, current_time)
            
            # SDE step: dΦ = μdt + σdW
            dphi = mu * dt + sigma * dW
            current_flux += dphi
            current_time += dt
            
            flux_values.append(current_flux)
        
        return flux_values
    
    def compute_path_integral(self, attractor_value: float, paths: List[Path],
                             lagrangian: Optional[Callable] = None) -> float:
        """
        Compute path integral to attractor.
        
        Args:
            attractor_value: Value of target attractor
            paths: List of paths to integrate over
            lagrangian: Optional Lagrangian function
            
        Returns:
            Path integral value
        """
        from ..math.attractors import Attractor, AttractorType
        from ..math.attractors import get_attractor_registry
        
        # Create temporary attractor
        registry = get_attractor_registry()
        temp_attractor = Attractor(
            name="temp",
            attractor_type=AttractorType.SPECIAL_IRRATIONAL,
            prime_id=999999,  # Temporary ID
            value=attractor_value
        )
        
        return path_integral(paths, temp_attractor, lagrangian)
    
    def add_stochastic_path(self, probability_distribution: Callable[[float], float],
                           t_start: float = 0.0, t_end: float = 1.0) -> Path:
        """
        Add stochastic path with given probability distribution.
        
        Args:
            probability_distribution: Probability density function P(t)
            t_start: Start time
            t_end: End time
            
        Returns:
            Path object
        """
        # Create path from probability distribution
        # Path trajectory is cumulative of probability
        def trajectory(t: float) -> float:
            # Integrate probability up to time t
            n_points = 100
            dt = (t - t_start) / n_points if t > t_start else 0.0
            integral = 0.0
            for i in range(n_points):
                s = t_start + i * dt
                integral += probability_distribution(s) * dt
            return integral
        
        return Path(trajectory, t_start, t_end)
