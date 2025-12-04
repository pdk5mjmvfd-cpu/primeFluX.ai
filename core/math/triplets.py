"""
PrimeFlux Triplets.

Three fundamental triplets:
- Presence: (0, 1, √2)
- Trig: (1, 2, 3) with mapping to sin/cos/tan
- Combinatoric: (p, p, q)
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import Tuple
import math

SQRT2 = math.sqrt(2)


class TripletType(Enum):
    """Triplet type enumeration."""
    PRESENCE = "presence"
    TRIG = "trig"
    COMBINATORIC = "combinatoric"


@dataclass
class Triplet:
    """Base triplet class."""
    a: float
    b: float
    c: float
    triplet_type: TripletType
    
    def curvature(self) -> float:
        """
        Triplet curvature = product of triplet elements.
        
        Returns:
            Curvature value
        """
        return self.a * self.b * self.c
    
    def entropy(self) -> float:
        """
        Triplet entropy = sum of logs of elements.
        
        Returns:
            Entropy value
        """
        elements = [abs(self.a), abs(self.b), abs(self.c)]
        return sum(math.log(max(e, 0.001)) for e in elements)


def make_presence_triplet() -> Triplet:
    """
    Create presence triplet (0, 1, √2).
    
    Returns:
        Presence triplet
    """
    return Triplet(0.0, 1.0, SQRT2, TripletType.PRESENCE)


def make_trig_triplet() -> Triplet:
    """
    Create trig triplet (1, 2, 3).
    
    Returns:
        Trig triplet
    """
    return Triplet(1.0, 2.0, 3.0, TripletType.TRIG)


def make_combinatoric_triplet(p: int, q: int) -> Triplet:
    """
    Create combinatoric triplet (p, p, q).
    
    Args:
        p: First prime
        q: Second prime
        
    Returns:
        Combinatoric triplet
    """
    if not _is_prime(p) or not _is_prime(q):
        raise ValueError("p and q must be prime")
    
    return Triplet(float(p), float(p), float(q), TripletType.COMBINATORIC)


def triplet_entropy(triplet: Triplet) -> float:
    """
    Compute triplet entropy.
    
    Entropy = sum of logs of elements.
    
    Args:
        triplet: Triplet
        
    Returns:
        Entropy value
    """
    return triplet.entropy()


def triplet_curvature(triplet: Triplet) -> float:
    """
    Compute triplet curvature.
    
    Curvature = product of triplet elements.
    
    Args:
        triplet: Triplet
        
    Returns:
        Curvature value
    """
    return triplet.curvature()


def detect_triplet_type(tokens: list[float]) -> TripletType | None:
    """
    Detect triplet type from tokens.
    
    Args:
        tokens: List of token values
        
    Returns:
        Triplet type or None
    """
    if len(tokens) < 3:
        return None
    
    # Check for presence triplet (0, 1, √2)
    a, b, c = tokens[0], tokens[1], tokens[2]
    if abs(a - 0.0) < 0.1 and abs(b - 1.0) < 0.1 and abs(c - SQRT2) < 0.1:
        return TripletType.PRESENCE
    
    # Check for trig triplet (1, 2, 3)
    if abs(a - 1.0) < 0.1 and abs(b - 2.0) < 0.1 and abs(c - 3.0) < 0.1:
        return TripletType.TRIG
    
    # Check for combinatoric (p, p, q) where p, q are primes
    if _is_prime(int(a)) and abs(a - b) < 0.1 and _is_prime(int(c)):
        return TripletType.COMBINATORIC
    
    return None


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


def trig_triplet_mapping(theta: float) -> Tuple[float, float, float]:
    """
    Map trig triplet (1, 2, 3) to sin/cos/tan.
    
    Args:
        theta: Angle in radians
        
    Returns:
        Tuple of (sin, cos, tan)
    """
    return (math.sin(theta), math.cos(theta), math.tan(theta))
