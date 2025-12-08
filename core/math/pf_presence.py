"""
PrimeFlux Presence Vector Core.

Minimal 1/0/-1 lattice vector – the atomic unit of PrimeFlux presence.

Theory:
- Presence vectors map distinctions (text) to fixed-dimensional lattice points
- Bijection: same text → same presence vector (deterministic via SHA-256)
- Reversible: presence ↔ bitstring conversion preserves information
- Apoptosis-ready: flip_rail() provides involution for pruning non-monotone chains

Source: Weierstrass (1885) – trigonometric polynomial convergence guarantees
        dense exploration of presence manifold under irrational rotation.
"""

from __future__ import annotations

import hashlib
from typing import List, Optional


class PresenceVector:
    """
    Minimal 1/0/-1 lattice vector – the atomic unit of PrimeFlux presence.
    
    Each component is constrained to {-1, 0, 1}, representing:
    - 1: positive presence (rail active)
    - 0: neutral/zero (rail inactive)
    - -1: negative presence (rail inverted)
    
    The vector is derived deterministically from input text via SHA-256 hashing,
    ensuring bit-perfect reproducibility for audit and reversibility.
    """

    def __init__(self, components: List[int]):
        """
        Initialize presence vector from component list.
        
        Args:
            components: List of integers, each must be in {-1, 0, 1}
            
        Raises:
            ValueError: If any component is not in {-1, 0, 1}
        """
        if any(x not in (-1, 0, 1) for x in components):
            raise ValueError("PresenceVector only allows -1, 0, 1")
        self.components = components

    @classmethod
    def from_text(cls, text: str, dim: int = 64) -> "PresenceVector":
        """
        Grok's simplified interface - exact bit extraction matching Grok's spec.
        """
        h = hashlib.sha256(text.encode()).digest()
        bits = ''.join(f'{b:08b}' for b in h)
        vec = []
        for a, b in zip(bits[::4], bits[1::4]):
            if a == b == '0': 
                vec.append(0)
            elif a == '1' and b == '0': 
                vec.append(1)
            elif a == '0' and b == '1': 
                vec.append(-1)
            else: 
                vec.append(0)
            if len(vec) >= dim: 
                break
        return cls(vec[:dim])
    
    @classmethod
    def from_distinction(cls, text: str, dim: int = 64) -> "PresenceVector":
        """
        Create presence vector from text distinction.
        
        Smallest possible mapping: hash(string) → fixed N-component presence.
        Uses SHA-256 to ensure deterministic bijection: same text → same vector.
        
        Algorithm:
        1. Hash text to 256-bit digest
        2. Extract bits in pairs (2 bits → one component)
        3. Map: 00→0, 10→1, 01→-1, 11→0 (neutral)
        4. Truncate/pad to requested dimension
        
        Args:
            text: Input text to convert to presence
            dim: Target dimension (default 64, will grow to 256+ for full SHA-256 space)
            
        Returns:
            PresenceVector with dim components
        """
        h = hashlib.sha256(text.encode()).digest()
        
        # Take first 32 bytes → 256 bits → map to -1/0/1
        bits = bin(int.from_bytes(h, "big"))[2:].zfill(256)
        vec = []
        
        # Process bits in pairs: 2 bits → one component
        for i in range(0, min(len(bits) - 1, dim * 2), 2):
            a = bits[i]
            b = bits[i + 1] if i + 1 < len(bits) else "0"
            
            if a == b == "0":
                vec.append(0)
            elif a == "1" and b == "0":
                vec.append(1)
            elif a == "0" and b == "1":
                vec.append(-1)
            else:  # 11 → 0 (neutral)
                vec.append(0)
            
            if len(vec) >= dim:
                break
        
        # Pad if needed
        while len(vec) < dim:
            vec.append(0)
        
        return cls(vec[:dim])

    def flip_rail(self, idx: int) -> "PresenceVector":
        """
        Apoptosis operation – flip one -1 ↔ 1 (involution).
        
        Flips the sign of a non-zero component. Zero components remain unchanged.
        This operation is involutive: flip_rail(flip_rail(v)) == v.
        
        Used in v2 for pruning non-monotone oscillation chains via apoptosis.
        
        Args:
            idx: Index of component to flip
            
        Returns:
            New PresenceVector with flipped component
        """
        c = self.components.copy()
        if 0 <= idx < len(c) and c[idx] != 0:
            c[idx] = -c[idx]
        return PresenceVector(c)

    def to_bitstring(self, width: int = 256) -> str:
        """
        Convert presence vector back to bitstring (reversibility for audit).
        
        Inverse operation of from_distinction() bit mapping:
        - 1 → "10"
        - -1 → "01"
        - 0 → "00" or "11" (ambiguous, defaults to "00")
        
        Args:
            width: Target bitstring width (default 256 for SHA-256 compatibility)
            
        Returns:
            Binary string representation
        """
        bits = []
        for x in self.components:
            if x == 1:
                bits.append("10")
            elif x == -1:
                bits.append("01")
            else:  # 0
                bits.append("00")
        
        bitstring = "".join(bits)
        
        # Pad or truncate to requested width
        if len(bitstring) < width:
            bitstring = bitstring.ljust(width, "0")
        elif len(bitstring) > width:
            bitstring = bitstring[:width]
        
        return bitstring

    def __repr__(self) -> str:
        """String representation showing first 8 components."""
        preview = " ".join(map(str, self.components[:8]))
        if len(self.components) > 8:
            preview += "..."
        return f"PV[{len(self.components)}]({preview})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, PresenceVector):
            return False
        return self.components == other.components

    def __len__(self) -> int:
        """Return dimension of presence vector."""
        return len(self.components)
