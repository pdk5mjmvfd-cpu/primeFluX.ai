"""
Utils - Utility functions for particle engine.

Refactored from utils.py
"""

from __future__ import annotations

import math
from typing import List, Tuple
from .particle import PFParticle


def calculate_center_of_mass(particles: List[PFParticle]) -> Tuple[float, float, float]:
    """
    Calculate center of mass of particle system.
    
    Args:
        particles: List of particles
        
    Returns:
        Center of mass (x, y, z)
    """
    if not particles:
        return (0.0, 0.0, 0.0)
    
    total_mass = sum(p.mass for p in particles)
    if total_mass == 0:
        return (0.0, 0.0, 0.0)
    
    x_cm = sum(p.position[0] * p.mass for p in particles) / total_mass
    y_cm = sum(p.position[1] * p.mass for p in particles) / total_mass
    z_cm = sum(p.position[2] * p.mass for p in particles) / total_mass
    
    return (x_cm, y_cm, z_cm)


def calculate_total_momentum(particles: List[PFParticle]) -> Tuple[float, float, float]:
    """
    Calculate total momentum of particle system.
    
    Args:
        particles: List of particles
        
    Returns:
        Total momentum (px, py, pz)
    """
    px_total = sum(p.momentum[0] for p in particles)
    py_total = sum(p.momentum[1] for p in particles)
    pz_total = sum(p.momentum[2] for p in particles)
    
    return (px_total, py_total, pz_total)


def calculate_angular_momentum(particles: List[PFParticle]) -> Tuple[float, float, float]:
    """
    Calculate total angular momentum.
    
    Args:
        particles: List of particles
        
    Returns:
        Angular momentum (Lx, Ly, Lz)
    """
    cm = calculate_center_of_mass(particles)
    
    Lx, Ly, Lz = 0.0, 0.0, 0.0
    
    for p in particles:
        # Position relative to CM
        rx = p.position[0] - cm[0]
        ry = p.position[1] - cm[1]
        rz = p.position[2] - cm[2]
        
        # Momentum
        px, py, pz = p.momentum
        
        # Angular momentum: L = r × p
        Lx += ry * pz - rz * py
        Ly += rz * px - rx * pz
        Lz += rx * py - ry * px
    
    return (Lx, Ly, Lz)


def distance_matrix(particles: List[PFParticle]) -> List[List[float]]:
    """
    Calculate distance matrix between all particles.
    
    Args:
        particles: List of particles
        
    Returns:
        Distance matrix (symmetric)
    """
    n = len(particles)
    matrix = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = particles[i].distance_to(particles[j])
            matrix[i][j] = dist
            matrix[j][i] = dist
    
    return matrix
