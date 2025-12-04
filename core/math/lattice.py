"""
Prime Lattice (6k ± 1).

Dual-rail prime geometry:
- Rail A: p % 6 == 5 (6k - 1)
- Rail B: p % 6 == 1 (6k + 1)

Rules:
- Same rail = low flux
- Different rails = high flux
"""

from __future__ import annotations

from enum import Enum
import math


class PrimeRail(Enum):
    """Prime rail enumeration."""
    RAIL_A = "A"  # 6k - 1
    RAIL_B = "B"  # 6k + 1
    SPECIAL = "S"  # 2, 3 (special primes)


def prime_rail(p: int) -> PrimeRail:
    """
    Determine which rail a prime belongs to.
    
    Rail A: p % 6 == 5
    Rail B: p % 6 == 1
    Special: 2, 3
    
    Args:
        p: Prime number
        
    Returns:
        Prime rail
    """
    if p == 2 or p == 3:
        return PrimeRail.SPECIAL
    
    if p % 6 == 5:
        return PrimeRail.RAIL_A
    
    if p % 6 == 1:
        return PrimeRail.RAIL_B
    
    return PrimeRail.SPECIAL


def rail_interaction(p: int, q: int) -> float:
    """
    Compute rail interaction between primes.
    
    Same rail = low interaction
    Different rails = high interaction
    
    Args:
        p: First prime
        q: Second prime
        
    Returns:
        Interaction value (0.0 to 1.0)
    """
    rail_p = prime_rail(p)
    rail_q = prime_rail(q)
    
    if rail_p == PrimeRail.SPECIAL or rail_q == PrimeRail.SPECIAL:
        return 0.0
    
    if rail_p == rail_q:
        return 0.2  # Low interaction
    else:
        return 1.0  # High interaction


def flux_multiplier(p: int, q: int) -> float:
    """
    Compute flux multiplier based on rail interaction.
    
    Same rail = low flux (multiplier < 1.0)
    Different rails = high flux (multiplier > 1.0)
    
    Args:
        p: First prime
        q: Second prime
        
    Returns:
        Flux multiplier
    """
    interaction = rail_interaction(p, q)
    
    if interaction > 0.5:
        # High interaction → high flux
        return 1.5 + math.log(p * q) / 10.0
    else:
        # Low interaction → low flux
        return 0.5 + math.log(p * q) / 20.0
