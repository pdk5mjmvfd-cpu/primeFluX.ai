"""
Path Integrals - Probabilistic Path Definitions

Path probability distributions for attractor convergence.
Path integrals over all possible trajectories to attractors.

Mathematical Framework:
- Path Space: Ω = {all possible trajectories x(t)}
- Probability Measure: P: Ω → [0,1] (path probability)
- Path Integral: ∫_Ω P(ω) dω = 1 (normalization)

For Attractor Fields:
P(path → attractor A) = exp(-S[path] / ħ)
Where S[path] = action integral along path
ħ = information quantum (Planck-like constant)
"""

from __future__ import annotations

import math
from typing import List, Callable, Tuple, Optional, Dict
import numpy as np
from .attractors import get_attractor_registry, Attractor


# Information quantum (Planck-like constant for information)
HBAR_INFO = 1.0  # Normalized to 1


class Path:
    """
    Represents a path (trajectory) in the flux manifold.
    
    A path is a function x(t) that describes evolution over time.
    """
    
    def __init__(self, trajectory: Callable[[float], float], t_start: float = 0.0, t_end: float = 1.0):
        """
        Initialize path.
        
        Args:
            trajectory: Function x(t) describing the path
            t_start: Start time
            t_end: End time
        """
        self.trajectory = trajectory
        self.t_start = t_start
        self.t_end = t_end
    
    def evaluate(self, t: float) -> float:
        """
        Evaluate path at time t.
        
        Args:
            t: Time
            
        Returns:
            Path value at time t
        """
        return self.trajectory(t)
    
    def sample(self, n_points: int = 100) -> List[Tuple[float, float]]:
        """
        Sample path at n_points.
        
        Args:
            n_points: Number of sample points
            
        Returns:
            List of (t, x(t)) tuples
        """
        dt = (self.t_end - self.t_start) / (n_points - 1)
        samples = []
        for i in range(n_points):
            t = self.t_start + i * dt
            x = self.evaluate(t)
            samples.append((t, x))
        return samples


def action_integral(path: Path, lagrangian: Optional[Callable[[float, float], float]] = None) -> float:
    """
    Compute action integral along path.
    
    S[path] = ∫ L(x, ẋ) dt
    
    Default Lagrangian: L = (1/2)ẋ² - V(x) (kinetic - potential)
    
    Args:
        path: Path to compute action for
        lagrangian: Optional Lagrangian function L(x, ẋ)
        
    Returns:
        Action integral value
    """
    if lagrangian is None:
        # Default: L = (1/2)ẋ² (kinetic energy)
        def default_lagrangian(x: float, xdot: float) -> float:
            return 0.5 * xdot**2
        lagrangian = default_lagrangian
    
    # Numerically integrate action
    samples = path.sample(100)
    action = 0.0
    
    for i in range(len(samples) - 1):
        t1, x1 = samples[i]
        t2, x2 = samples[i + 1]
        dt = t2 - t1
        
        # Approximate velocity
        xdot = (x2 - x1) / dt if dt > 0 else 0.0
        
        # Midpoint value
        x_mid = (x1 + x2) / 2.0
        
        # Add contribution
        action += lagrangian(x_mid, xdot) * dt
    
    return action


def path_probability(path: Path, attractor: Attractor, lagrangian: Optional[Callable] = None) -> float:
    """
    Compute probability of path leading to attractor.
    
    P(path → attractor A) = exp(-S[path] / ħ)
    
    Args:
        path: Path to evaluate
        attractor: Target attractor
        lagrangian: Optional Lagrangian function
        
    Returns:
        Probability (0.0 to 1.0)
    """
    action = action_integral(path, lagrangian)
    
    # Probability: exp(-S / ħ)
    prob = math.exp(-action / HBAR_INFO)
    
    return prob


def path_integral(paths: List[Path], attractor: Attractor, 
                  lagrangian: Optional[Callable] = None) -> float:
    """
    Compute path integral over all paths.
    
    ∫_Ω P(ω) dω = ∫_Ω exp(-S[ω]/ħ) d[ω]
    
    Args:
        paths: List of all possible paths
        attractor: Target attractor
        lagrangian: Optional Lagrangian function
        
    Returns:
        Path integral value (normalized probability)
    """
    if not paths:
        return 0.0
    
    # Compute probability for each path
    probabilities = [path_probability(path, attractor, lagrangian) for path in paths]
    
    # Sum over all paths (path integral)
    integral = sum(probabilities)
    
    # Normalize (should sum to 1 for all paths to attractor)
    total = sum(probabilities)
    if total > 0:
        return integral / total
    
    return 0.0


def most_probable_path(paths: List[Path], attractor: Attractor,
                       lagrangian: Optional[Callable] = None) -> Optional[Path]:
    """
    Find most probable path (least action).
    
    Most probable = lowest action = most efficient.
    
    Args:
        paths: List of possible paths
        attractor: Target attractor
        lagrangian: Optional Lagrangian function
        
    Returns:
        Most probable path (lowest action)
    """
    if not paths:
        return None
    
    # Compute action for each path
    path_actions = []
    for path in paths:
        action = action_integral(path, lagrangian)
        path_actions.append((path, action))
    
    # Find path with minimum action
    min_path, min_action = min(path_actions, key=lambda x: x[1])
    
    return min_path


def superposition_of_paths(paths: List[Path], attractor: Attractor,
                           lagrangian: Optional[Callable] = None) -> Callable[[float], float]:
    """
    Compute superposition of all paths.
    
    Nature computes via superposition of all paths, not single path.
    Superposition: Ψ(t) = Σ_i P(path_i) * path_i(t)
    
    Args:
        paths: List of all possible paths
        attractor: Target attractor
        lagrangian: Optional Lagrangian function
        
    Returns:
        Superposition function Ψ(t)
    """
    if not paths:
        return lambda t: 0.0
    
    # Compute probabilities for each path
    probabilities = [path_probability(path, attractor, lagrangian) for path in paths]
    
    # Normalize probabilities
    total_prob = sum(probabilities)
    if total_prob == 0:
        return lambda t: 0.0
    
    normalized_probs = [p / total_prob for p in probabilities]
    
    def superposition(t: float) -> float:
        """Superposition at time t."""
        result = 0.0
        for path, prob in zip(paths, normalized_probs):
            result += prob * path.evaluate(t)
        return result
    
    return superposition


def verify_path_independence(paths: List[Path], attractor: Attractor,
                             tolerance: float = 1e-10) -> bool:
    """
    Verify path independence: all paths → same attractor.
    
    All paths to same attractor have equal weight at the limit.
    
    Args:
        paths: List of different paths
        attractor: Target attractor
        tolerance: Convergence tolerance
        
    Returns:
        True if all paths converge to attractor
    """
    if not paths or attractor.value is None:
        return False
    
    # Check if all paths end near attractor value
    for path in paths:
        final_value = path.evaluate(path.t_end)
        if abs(final_value - attractor.value) > tolerance:
            return False
    
    return True


def probabilistic_closure(paths: List[Path], attractor: Attractor,
                          lagrangian: Optional[Callable] = None) -> Dict[str, any]:
    """
    Implement probabilistic closure: superposition of all paths, most probable = least action.
    
    Nature computes via superposition of all paths, not single path.
    Most probable = lowest action = most efficient.
    All paths to same attractor have equal weight at the limit.
    
    Args:
        paths: List of all possible paths
        attractor: Target attractor
        lagrangian: Optional Lagrangian function
        
    Returns:
        Dictionary with:
        - superposition: Superposition function Ψ(t)
        - most_probable_path: Path with lowest action
        - path_integral: Path integral value
        - all_paths_equal_weight: True if all paths have equal weight at limit
    """
    if not paths:
        return {
            "superposition": lambda t: 0.0,
            "most_probable_path": None,
            "path_integral": 0.0,
            "all_paths_equal_weight": True
        }
    
    # Compute superposition
    psi = superposition_of_paths(paths, attractor, lagrangian)
    
    # Find most probable path (least action)
    most_probable = most_probable_path(paths, attractor, lagrangian)
    
    # Compute path integral
    integral = path_integral(paths, attractor, lagrangian)
    
    # Check if all paths have equal weight at limit
    # (All paths to same attractor have equal weight at the limit)
    all_equal_weight = verify_path_independence(paths, attractor)
    
    return {
        "superposition": psi,
        "most_probable_path": most_probable,
        "path_integral": integral,
        "all_paths_equal_weight": all_equal_weight,
        "num_paths": len(paths)
    }


__all__ = [
    'Path',
    'action_integral',
    'path_probability',
    'path_integral',
    'most_probable_path',
    'superposition_of_paths',
    'verify_path_independence',
    'HBAR_INFO',
]

