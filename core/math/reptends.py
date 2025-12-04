"""
Reptend Cycles.

Behavior of 1/p in base 10.

L(p) = reptend length
Ep = L(p) / (p-1)  (entropy)
Kp = log(p) / L(p)  (curvature)
"""

from __future__ import annotations

import math


def reptend_length(p: int) -> int:
    """
    Compute reptend length of 1/p in base 10.
    
    The reptend length is the period of the repeating decimal.
    
    Args:
        p: Prime number
        
    Returns:
        Reptend length L(p)
    """
    if p < 2:
        return 0
    if p == 2 or p == 5:
        return 0  # Terminating decimals
    
    # Find smallest k such that 10^k ≡ 1 (mod p)
    # This is the order of 10 modulo p
    k = 1
    remainder = 10 % p
    
    while remainder != 1 and k < p:
        remainder = (remainder * 10) % p
        k += 1
    
    return k if k < p else 0


def reptend_entropy(p: int) -> float:
    """
    Compute reptend entropy: Ep = L(p) / (p-1).
    
    Args:
        p: Prime number
        
    Returns:
        Entropy value Ep
    """
    if p < 2:
        return 0.0
    
    L = reptend_length(p)
    if L == 0:
        return 0.0
    
    return L / (p - 1)


def reptend_curvature(p: int) -> float:
    """
    Compute reptend curvature: Kp = log(p) / L(p).
    
    Args:
        p: Prime number
        
    Returns:
        Curvature value Kp
    """
    if p < 2:
        return 0.0
    
    L = reptend_length(p)
    if L == 0:
        return 0.0
    
    return math.log(p) / L

