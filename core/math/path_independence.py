"""
Path Independence Validation - Multiple Paths → Same Attractor

Verifies that multiple paths (reptends, continued fractions, Machin series)
all converge to the same attractor. This proves path independence:
all paths to same attractor are equivalent (interface contract).
"""

from __future__ import annotations

import math
from typing import List, Callable, Tuple, Optional
from .attractors import get_attractor_registry, Attractor
from .path_integrals import Path, verify_path_independence
from .limit_validation import Limit, LimitType, check_path_independence_multiple_paths


def compute_reptend_path(prime: int, iterations: int = 100) -> List[float]:
    """
    Compute reptend path for prime p.
    
    Reptend: 1/p has repeating decimal period.
    Path: sequence of digits in reptend cycle.
    
    Args:
        prime: Prime number p
        iterations: Number of iterations
        
    Returns:
        List of values in reptend path
    """
    path = []
    remainder = 1
    seen = {}  # Track remainders to detect cycle
    
    for i in range(iterations):
        if remainder in seen:
            # Cycle detected, repeat from here
            cycle_start = seen[remainder]
            cycle = path[cycle_start:]
            # Extend path with cycle
            remaining = iterations - len(path)
            path.extend(cycle * (remaining // len(cycle) + 1))
            break
        
        seen[remainder] = len(path)
        digit = (remainder * 10) // prime
        path.append(digit / 10.0)  # Normalize to [0, 1)
        remainder = (remainder * 10) % prime
        
        if remainder == 0:
            # Terminating decimal
            break
    
    return path[:iterations]


def compute_continued_fraction_path(value: float, iterations: int = 100) -> List[float]:
    """
    Compute continued fraction path.
    
    Continued fraction: [a0; a1, a2, ...] = a0 + 1/(a1 + 1/(a2 + ...))
    Path: sequence of convergents.
    
    Args:
        value: Value to approximate
        iterations: Number of iterations
        
    Returns:
        List of convergent values
    """
    path = []
    x = value
    
    for i in range(iterations):
        a = int(x)
        path.append(a)
        
        if x - a < 1e-10:
            break
        
        x = 1.0 / (x - a)
    
    # Convert to actual convergents
    convergents = []
    if path:
        p_prev, p_curr = 0, 1
        q_prev, q_curr = 1, 0
        
        for a in path:
            p_next = a * p_curr + p_prev
            q_next = a * q_curr + q_prev
            convergents.append(p_next / q_next if q_next > 0 else 0.0)
            p_prev, p_curr = p_curr, p_next
            q_prev, q_curr = q_curr, q_next
    
    return convergents


def compute_machin_series_path(iterations: int = 100) -> List[float]:
    """
    Compute Machin's formula path for π.
    
    Machin's formula: π/4 = 4 arctan(1/5) - arctan(1/239)
    Path: sequence of partial sums.
    
    Args:
        iterations: Number of iterations
        
    Returns:
        List of partial sum values
    """
    path = []
    pi_approx = 0.0
    
    for n in range(iterations):
        # Taylor series for arctan: arctan(x) = x - x³/3 + x⁵/5 - ...
        term1 = 0.0
        term2 = 0.0
        
        for k in range(n + 1):
            sign = (-1)**k
            term1 += sign * (1/5)**(2*k+1) / (2*k+1)
            term2 += sign * (1/239)**(2*k+1) / (2*k+1)
        
        pi_approx = 4 * (4 * term1 - term2)
        path.append(pi_approx)
    
    return path


def verify_multiple_paths_to_attractor(attractor: Attractor, 
                                       paths: List[List[float]],
                                       tolerance: float = 1e-6) -> Tuple[bool, Dict[str, any]]:
    """
    Verify that multiple paths converge to same attractor.
    
    Tests path independence: all paths → same limit (interface contract).
    
    Args:
        attractor: Target attractor
        paths: List of different paths (reptends, continued fractions, Machin, etc.)
        tolerance: Convergence tolerance
        
    Returns:
        Tuple of (is_valid, details_dict)
    """
    if attractor.value is None:
        return (False, {"error": "Attractor has no value"})
    
    if not paths:
        return (False, {"error": "No paths provided"})
    
    # Check if all paths converge to attractor
    convergences = []
    for i, path in enumerate(paths):
        if not path:
            continue
        
        final_value = path[-1]
        distance = abs(final_value - attractor.value)
        convergences.append({
            "path_index": i,
            "final_value": final_value,
            "distance": distance,
            "converges": distance < tolerance
        })
    
    all_converge = all(c["converges"] for c in convergences)
    
    # Check path independence (all paths → same limit)
    path_independence = check_path_independence_multiple_paths(paths, tolerance)
    
    return (all_converge and path_independence, {
        "all_converge": all_converge,
        "path_independence": path_independence,
        "convergences": convergences,
        "attractor_value": attractor.value,
        "tolerance": tolerance
    })


def test_pi_path_independence() -> Tuple[bool, Dict[str, any]]:
    """
    Test path independence for π using multiple computational paths.
    
    Tests: reptends, continued fractions, Machin series all → π
    
    Returns:
        Tuple of (is_valid, details_dict)
    """
    registry = get_attractor_registry()
    pi_attractor = registry.get_by_name("pi")
    
    if not pi_attractor or pi_attractor.value is None:
        return (False, {"error": "π attractor not found"})
    
    # Generate multiple paths to π
    paths = []
    
    # Path 1: Reptend (using prime near π, e.g., 3)
    reptend_path = compute_reptend_path(3, 100)
    # Scale to approximate π (simplified)
    reptend_scaled = [v * 10 for v in reptend_path[:50]]
    paths.append(reptend_scaled)
    
    # Path 2: Continued fraction
    cf_path = compute_continued_fraction_path(math.pi, 50)
    paths.append(cf_path)
    
    # Path 3: Machin series
    machin_path = compute_machin_series_path(50)
    paths.append(machin_path)
    
    # Verify all paths converge to π
    return verify_multiple_paths_to_attractor(pi_attractor, paths)


__all__ = [
    'compute_reptend_path',
    'compute_continued_fraction_path',
    'compute_machin_series_path',
    'verify_multiple_paths_to_attractor',
    'test_pi_path_independence',
]

