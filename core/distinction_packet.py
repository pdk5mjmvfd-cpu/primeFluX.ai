"""
Distinction Packet - PrimeFlux distinction data structure.

Represents a distinction packet with prime modes, rail phase, and curvature.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

# Try to import sympy for prime factorization
try:
    from sympy.ntheory import factorint
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False
    # Fallback: simple prime factorization stub
    def factorint(n: int) -> dict:
        """Stub prime factorization."""
        if n < 2:
            return {}
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors


@dataclass
class DistinctionPacket:
    """
    Distinction packet with prime modes, rail phase, and curvature.
    
    Attributes:
        prime_modes: List of prime numbers (modes)
        rail_phase: Rail phase value in range [-1, 1]
        curvature_value: Curvature value (absolute value of phase)
        timestamp: Timestamp of packet creation
    """
    prime_modes: List[int]
    rail_phase: float  # Range: [-1, 1]
    curvature_value: float
    timestamp: datetime
    
    def __post_init__(self):
        """Validate and clamp values after initialization."""
        # Clamp rail_phase to [-1, 1]
        if self.rail_phase < -1.0:
            self.rail_phase = -1.0
        elif self.rail_phase > 1.0:
            self.rail_phase = 1.0
        
        # Ensure curvature is non-negative
        if self.curvature_value < 0.0:
            self.curvature_value = abs(self.rail_phase)
    
    @classmethod
    def from_input(cls, text: str) -> "DistinctionPacket":
        """
        Create distinction packet from input text.
        
        Parses primes via sympy.ntheory.factorint(len(text) or stub),
        phase = (hash(text) % 200 / 100.0) - 1,
        curvature = abs(phase).
        
        Args:
            text: Input text string
            
        Returns:
            DistinctionPacket instance
        """
        # Get text length for prime factorization
        text_len = len(text) if text else 1
        
        # Factorize length to get prime modes
        factors = factorint(text_len)
        prime_modes = list(factors.keys())
        
        # If no primes found, use default
        if not prime_modes:
            prime_modes = [2]  # Default prime
        
        # Calculate rail phase: (hash(text) % 200 / 100.0) - 1
        text_hash = hash(text) if text else 0
        phase_raw = (abs(text_hash) % 200) / 100.0
        rail_phase = phase_raw - 1.0  # Range: [-1, 1]
        
        # Curvature is absolute value of phase
        curvature_value = abs(rail_phase)
        
        # Create timestamp
        timestamp = datetime.now()
        
        return cls(
            prime_modes=prime_modes,
            rail_phase=rail_phase,
            curvature_value=curvature_value,
            timestamp=timestamp
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "prime_modes": self.prime_modes,
            "rail_phase": self.rail_phase,
            "curvature_value": self.curvature_value,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DistinctionPacket":
        """Create from dictionary."""
        from datetime import datetime
        
        return cls(
            prime_modes=data["prime_modes"],
            rail_phase=data["rail_phase"],
            curvature_value=data["curvature_value"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
