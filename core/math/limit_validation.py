"""
Limit Alignment Validation - All Math Must Respect Limits

Principle: All math must align with limits. Paths don't matter (multiple paths
to same limit), only limit value matters (interface contract).

Validates that all operations respect limit constraints and that attractor
convergence matches limit convergence.
"""

from __future__ import annotations

import math
from typing import List, Optional, Callable, Tuple, Any
from enum import Enum
from .attractors import get_attractor_registry, Attractor


class LimitType(Enum):
    """Types of limits."""
    CONVERGENT = "convergent"  # lim(n→∞) a_n = L (implements Attractor interface)
    DIVERGENT = "divergent"    # lim(n→∞) a_n = ±∞ (breaks interface contract)
    OSCILLATING = "oscillating"  # No limit (violates convergence, needs attractor)
    UNKNOWN = "unknown"        # Limit not yet determined


class Limit:
    """
    Limit representation.
    
    Limits are real objects that implement the Attractor interface.
    Path independence: multiple paths → same limit.
    """
    
    def __init__(self, sequence: Callable[[int], float], limit_type: LimitType = LimitType.UNKNOWN):
        """
        Initialize limit.
        
        Args:
            sequence: Function a(n) that generates sequence
            limit_type: Type of limit
        """
        self.sequence = sequence
        self.limit_type = limit_type
        self._cached_value: Optional[float] = None
        self._attractor_registry = get_attractor_registry()
    
    def compute_limit(self, max_iterations: int = 1000, tolerance: float = 1e-10) -> Optional[float]:
        """
        Compute limit value.
        
        Args:
            max_iterations: Maximum iterations to try
            tolerance: Convergence tolerance
            
        Returns:
            Limit value if convergent, None otherwise
        """
        if self._cached_value is not None:
            return self._cached_value
        
        if self.limit_type == LimitType.DIVERGENT:
            return None
        
        # Try to compute limit
        prev_value = self.sequence(1)
        for n in range(2, max_iterations + 1):
            current_value = self.sequence(n)
            
            # Check convergence
            if abs(current_value - prev_value) < tolerance:
                self._cached_value = current_value
                self.limit_type = LimitType.CONVERGENT
                return current_value
            
            # Check divergence
            if abs(current_value) > 1e10:
                self.limit_type = LimitType.DIVERGENT
                return None
            
            prev_value = current_value
        
        # If we get here, limit not determined
        self.limit_type = LimitType.UNKNOWN
        return None
    
    def check_path_independence(self, paths: List[List[float]]) -> bool:
        """
        Verify path independence: multiple paths → same limit.
        
        Args:
            paths: List of different paths (sequences)
            
        Returns:
            True if all paths converge to same limit
        """
        if not paths:
            return True
        
        limits = []
        for path in paths:
            if not path:
                continue
            # Limit is last value (assuming convergence)
            limit = path[-1]
            limits.append(limit)
        
        if not limits:
            return True
        
        # Check if all limits are approximately equal
        first_limit = limits[0]
        tolerance = 1e-10
        return all(abs(limit - first_limit) < tolerance for limit in limits)
    
    def get_attractor(self) -> Optional[Attractor]:
        """
        Get associated attractor if limit converges to one.
        
        Returns:
            Attractor if limit matches an attractor value, None otherwise
        """
        limit_value = self.compute_limit()
        if limit_value is None:
            return None
        
        # Check if limit value matches any attractor
        for attractor in self._attractor_registry._attractors.values():
            if attractor.value is not None:
                if abs(limit_value - attractor.value) < 1e-10:
                    return attractor
        
        return None
    
    def __repr__(self) -> str:
        limit_val = self.compute_limit()
        return f"Limit(type={self.limit_type.value}, value={limit_val})"


def validate_limit_alignment(operation: Callable, limit: Limit, *args, **kwargs) -> Tuple[bool, Optional[str]]:
    """
    Validate that operation respects limit constraints.
    
    Ensures all computations respect limit constraints.
    
    Args:
        operation: Operation to validate
        limit: Limit constraint
        *args, **kwargs: Arguments for operation
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Compute limit value
    limit_value = limit.compute_limit()
    
    if limit_value is None and limit.limit_type == LimitType.DIVERGENT:
        # Divergent limits break interface contract
        return (False, "Operation violates limit: limit is divergent")
    
    # Try to execute operation
    try:
        result = operation(*args, **kwargs)
        
        # Check if result respects limit
        if isinstance(result, (int, float)):
            if limit_value is not None:
                # Check if result is consistent with limit
                if abs(result - limit_value) > 1e-6:
                    return (False, f"Operation result {result} does not align with limit {limit_value}")
        
        return (True, None)
    except Exception as e:
        return (False, f"Operation failed: {str(e)}")


def validate_attractor_convergence(sequence: Callable[[int], float], attractor: Attractor, 
                                   max_iterations: int = 1000, tolerance: float = 1e-10) -> Tuple[bool, Optional[float]]:
    """
    Validate that sequence converges to attractor.
    
    Ensures attractor convergence matches limit convergence.
    
    Args:
        sequence: Sequence function a(n)
        attractor: Target attractor
        max_iterations: Maximum iterations
        tolerance: Convergence tolerance
        
    Returns:
        Tuple of (converges, limit_value)
    """
    if attractor.value is None:
        return (False, None)
    
    # Create limit from sequence
    limit = Limit(sequence)
    limit_value = limit.compute_limit(max_iterations, tolerance)
    
    if limit_value is None:
        return (False, None)
    
    # Check if limit matches attractor value
    if abs(limit_value - attractor.value) < tolerance:
        return (True, limit_value)
    
    return (False, limit_value)


def check_path_independence_multiple_paths(paths: List[List[float]], tolerance: float = 1e-10) -> bool:
    """
    Check path independence for multiple paths.
    
    Verifies that multiple paths converge to same limit.
    
    Args:
        paths: List of different paths (sequences)
        tolerance: Convergence tolerance
        
    Returns:
        True if all paths converge to same limit
    """
    if not paths:
        return True
    
    limits = []
    for path in paths:
        if not path:
            continue
        # Limit is last value (assuming convergence)
        limit = path[-1]
        limits.append(limit)
    
    if not limits:
        return True
    
    # Check if all limits are approximately equal
    first_limit = limits[0]
    return all(abs(limit - first_limit) < tolerance for limit in limits)


__all__ = [
    'Limit',
    'LimitType',
    'validate_limit_alignment',
    'validate_attractor_convergence',
    'check_path_independence_multiple_paths',
]

