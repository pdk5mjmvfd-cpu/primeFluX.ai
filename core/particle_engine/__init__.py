"""
Particle Engine - PrimeFlux particle physics simulation.

Integrates particle dynamics with trig modes and presence operator.
"""

from .particle import PFParticle, OrbitalChild, OrbitalShell
from .engine import ParticleEngine
from .geometry import BoundaryMapper
from .simulator import ParticleSimulator
from .evolution import PFEvolution
from .analysis import analyze_results, plot_particle_cloud
from .orbitals import compute_orbital_suite, pf_atomic_orbitals, QuarkColor
from .periodic_table import PeriodicTable
from .utils import *

__all__ = [
    'PFParticle',
    'OrbitalChild',
    'OrbitalShell',
    'ParticleEngine',
    'BoundaryMapper',
    'ParticleSimulator',
    'PFEvolution',
    'analyze_results',
    'plot_particle_cloud',
    'compute_orbital_suite',
    'pf_atomic_orbitals',
    'QuarkColor',
    'PeriodicTable'
]
