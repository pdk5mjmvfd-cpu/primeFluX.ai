"""
Number Classes as OOP Structures - PrimeFlux Number System

In PrimeFlux, numbers are not just values—they are computational structures:
- Primes = Classes (irreducible distinctions, fundamental types)
- Composites = Methods (structured operations, composed behaviors)
- Attractors = Interfaces (stable contracts, convergence points)

This transforms number theory into object-oriented computation where:
- Factorization = Class decomposition / code introspection
- Multiplication = Method composition / function pipelines
- Convergence = Interface implementation
- Path independence = All paths to same attractor are equivalent
"""

from __future__ import annotations

import math
from typing import List, Dict, Optional, Tuple, Set, Protocol
from abc import ABC, abstractmethod
from .attractors import get_attractor_registry, Attractor


class Fundamental(Protocol):
    """
    Fundamental interface that all numbers implement.
    
    Defines the contract for number operations.
    """
    
    def factorize(self) -> List[Tuple[int, int]]:
        """Class decomposition / code introspection."""
        ...
    
    def multiply(self, other: 'Number') -> 'Number':
        """Function composition / method chaining."""
        ...
    
    def converge(self) -> Optional[float]:
        """Interface check / path independence validation."""
        ...
    
    def get_attractor(self) -> Optional[Attractor]:
        """Interface lookup."""
        ...


class Number(ABC):
    """
    Base class for all PrimeFlux numbers.
    
    Implements Fundamental interface.
    """
    
    def __init__(self, value: int):
        """
        Initialize number.
        
        Args:
            value: Integer value
        """
        self.value = value
        self._attractor_registry = get_attractor_registry()
    
    @abstractmethod
    def factorize(self) -> List[Tuple[int, int]]:
        """
        Factorize number (class decomposition / code introspection).
        
        Returns:
            List of (prime, exponent) tuples
        """
        pass
    
    @abstractmethod
    def multiply(self, other: 'Number') -> 'Number':
        """
        Multiply with another number (function composition / method chaining).
        
        Args:
            other: Another number
            
        Returns:
            New number (composite)
        """
        pass
    
    def converge(self) -> Optional[float]:
        """
        Check convergence to attractor (interface check).
        
        Returns:
            Converged value if converges, None otherwise
        """
        # Check if this number is an attractor
        attractor = self.get_attractor()
        if attractor and attractor.value is not None:
            return attractor.value
        return None
    
    def get_attractor(self) -> Optional[Attractor]:
        """
        Get associated attractor (interface lookup).
        
        Returns:
            Attractor if this number is associated with one, None otherwise
        """
        # Check if value is an attractor prime
        if self._attractor_registry.is_attractor_prime(self.value):
            return self._attractor_registry.get_by_prime_id(self.value)
        return None
    
    def check_path_independence(self, paths: List[List[int]]) -> bool:
        """
        Verify path independence: all paths → same limit.
        
        Args:
            paths: List of different computational paths
            
        Returns:
            True if all paths converge to same value
        """
        if not paths:
            return True
        
        # Compute limit for each path
        limits = []
        for path in paths:
            # Simplified: sum path as limit approximation
            limit = sum(path) / len(path) if path else 0.0
            limits.append(limit)
        
        # Check if all limits are approximately equal
        if not limits:
            return True
        
        first_limit = limits[0]
        tolerance = 1e-10
        return all(abs(limit - first_limit) < tolerance for limit in limits)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"


class Prime(Number):
    """
    Prime number - irreducible class.
    
    Primes are fundamental types that cannot be decomposed further.
    """
    
    def factorize(self) -> List[Tuple[int, int]]:
        """
        Factorize prime (returns itself).
        
        Primes are irreducible - they are their own factorization.
        """
        return [(self.value, 1)]
    
    def multiply(self, other: Number) -> 'Composite':
        """
        Multiply with another number (create method pipeline).
        
        Args:
            other: Another number
            
        Returns:
            Composite (method composition)
        """
        # Create composite from multiplication
        result_value = self.value * other.value
        return ProductComposite(result_value, [self, other])
    
    def is_attractor_prime(self) -> bool:
        """Check if this prime is an attractor."""
        return self._attractor_registry.is_attractor_prime(self.value)


class AttractorPrime(Prime):
    """
    Attractor prime - interface implementation.
    
    Special primes that are attractors (e.g., π, e, φ).
    """
    
    def get_attractor(self) -> Optional[Attractor]:
        """Get the attractor associated with this prime."""
        return self._attractor_registry.get_by_prime_id(self.value)


class Composite(Number):
    """
    Composite number - method composition.
    
    Composites are structured operations, composed behaviors.
    Multiplication = function composition / method chaining.
    """
    
    def __init__(self, value: int, factors: Optional[List[Number]] = None):
        """
        Initialize composite.
        
        Args:
            value: Integer value
            factors: List of prime factors (for method decomposition)
        """
        super().__init__(value)
        self.factors = factors or []
    
    def factorize(self) -> List[Tuple[int, int]]:
        """
        Factorize composite (class decomposition / code introspection).
        
        Decomposes the composite into its prime factors.
        """
        if self.factors:
            # Use stored factors
            factor_dict: Dict[int, int] = {}
            for factor in self.factors:
                for p, exp in factor.factorize():
                    factor_dict[p] = factor_dict.get(p, 0) + exp
            return list(factor_dict.items())
        
        # Factorize from value
        factors = []
        n = self.value
        if n < 2:
            return []
        
        # Factor out 2
        exp = 0
        while n % 2 == 0:
            exp += 1
            n //= 2
        if exp > 0:
            factors.append((2, exp))
        
        # Factor out odd primes
        for p in range(3, int(math.sqrt(n)) + 1, 2):
            exp = 0
            while n % p == 0:
                exp += 1
                n //= p
            if exp > 0:
                factors.append((p, exp))
        
        if n > 1:
            factors.append((n, 1))
        
        return factors
    
    def multiply(self, other: Number) -> 'Composite':
        """
        Multiply with another number (method chaining).
        
        Args:
            other: Another number
            
        Returns:
            New composite (chained methods)
        """
        result_value = self.value * other.value
        new_factors = self.factors + [other]
        return ProductComposite(result_value, new_factors)


class PowerComposite(Composite):
    """
    Power composite - repeated method calls.
    
    Represents p^n (prime raised to power n).
    """
    
    def __init__(self, base: int, exponent: int):
        """
        Initialize power composite.
        
        Args:
            base: Base prime
            exponent: Exponent
        """
        value = base ** exponent
        factors = [Prime(base)] * exponent
        super().__init__(value, factors)
        self.base = base
        self.exponent = exponent


class ProductComposite(Composite):
    """
    Product composite - method chaining.
    
    Represents p·q (product of primes).
    """
    
    def __init__(self, value: int, factors: List[Number]):
        """
        Initialize product composite.
        
        Args:
            value: Product value
            factors: List of prime factors
        """
        super().__init__(value, factors)


class AttractorInterface:
    """
    Attractor interface contract.
    
    "All paths to me are equivalent" - path independence.
    """
    
    def __init__(self, attractor: Attractor):
        """
        Initialize attractor interface.
        
        Args:
            attractor: The attractor this interface represents
        """
        self.attractor = attractor
        self.name = attractor.name
    
    def check_path_equivalence(self, paths: List[List[float]]) -> bool:
        """
        Verify that all paths converge to same limit.
        
        Interface contract: all paths to attractor are equivalent.
        
        Args:
            paths: List of different paths (sequences of values)
            
        Returns:
            True if all paths converge to same limit
        """
        if not paths:
            return True
        
        # Compute limit for each path
        limits = []
        for path in paths:
            if not path:
                continue
            # Limit is last value (assuming convergence)
            limit = path[-1]
            limits.append(limit)
        
        if not limits:
            return True
        
        # Check if all limits are approximately equal to attractor value
        if self.attractor.value is None:
            # For hidden attractors, check if limits are approximately equal
            first_limit = limits[0]
            tolerance = 1e-10
            return all(abs(limit - first_limit) < tolerance for limit in limits)
        else:
            # Check if all limits converge to attractor value
            tolerance = 1e-10
            return all(abs(limit - self.attractor.value) < tolerance for limit in limits)
    
    def __repr__(self) -> str:
        return f"AttractorInterface({self.name})"


def create_number(value: int) -> Number:
    """
    Factory function to create appropriate number type.
    
    Args:
        value: Integer value
        
    Returns:
        Prime, AttractorPrime, or Composite as appropriate
    """
    registry = get_attractor_registry()
    
    # Check if prime
    if _is_prime(value):
        if registry.is_attractor_prime(value):
            return AttractorPrime(value)
        return Prime(value)
    
    # Otherwise composite
    return Composite(value)


def _is_prime(n: int) -> bool:
    """Check if n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


__all__ = [
    'Number',
    'Prime',
    'AttractorPrime',
    'Composite',
    'PowerComposite',
    'ProductComposite',
    'AttractorInterface',
    'create_number',
    'Fundamental',
]

