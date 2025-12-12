"""
ASCII–Flux Shell — PrimeFlux-Compatible Text Coordinate Mapping

Maps any input string as a PF-coordinate in a universal prompt manifold.

NOTE: This module now delegates to core/prime_ascii.py for prime mapping.
Maintains backward compatibility while using the new Prime ASCI system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any
import math
from .prime_ascii import get_prime_ascii

# Delegate to Prime ASCI system
_prime_ascii = get_prime_ascii()


def _nearest_prime(n: int) -> int:
    """
    Return prime for ASCII code n.
    
    Now delegates to Prime ASCI system for proper mapping.
    Maintains backward compatibility.
    """
    # Try to map ASCII code as character
    char = chr(n) if 0 <= n < 128 else None
    if char:
        prime_id = _prime_ascii.encode_char(char)
        if prime_id is not None:
            return prime_id
    
    # Fallback: find nearest prime (legacy behavior)
    # This should rarely be needed with full Prime ASCI mapping
    if n <= 2:
        return 2
    # Simple nearest prime search (legacy)
    _SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    best = _SMALL_PRIMES[0]
    best_diff = abs(best - n)
    for p in _SMALL_PRIMES[1:]:
        d = abs(p - n)
        if d < best_diff:
            best = p
            best_diff = d
    return best


@dataclass
class AsciiFluxPoint:
    """Single character ASCII-Flux point."""
    char: str
    ascii_code: int
    prime_code: int
    exp2: int
    exp5: int


@dataclass
class AsciiFluxSummary:
    """ASCII-Flux summary for a text string."""
    points: List[AsciiFluxPoint]
    entropy: float
    curvature: float
    dual_rail_ratio: float
    diversity: float


class AsciiFluxShell:
    """
    ASCII–Flux Shell

    Maps text → ASCII codes → (2,5)-salted prime coordinates and computes
    small PF-inspired metrics:

    - ascii_code: raw ord(c)
    - prime_code: nearest small prime (placeholder for PF 6k±1 mapping)
    - exp2, exp5: exponents of 2 and 5 in ascii_code's factorization
    - entropy: Shannon entropy over ascii codes
    - curvature: mean absolute difference between consecutive ascii codes
    - dual_rail_ratio: fraction of codes 'near' 6k±1 primes (heuristic)
    - diversity: unique character ratio

    This is a tiny reasoning substrate for Apop: a universal manifold of prompts.
    """

    def factor_2_5(self, n: int) -> tuple[int, int]:
        """Return exponents of 2 and 5 in n."""
        e2 = 0
        e5 = 0
        x = n
        while x > 0 and x % 2 == 0:
            e2 += 1
            x //= 2
        while x > 0 and x % 5 == 0:
            e5 += 1
            x //= 5
        return e2, e5

    def encode_text(self, text: str) -> AsciiFluxSummary:
        """
        Encode text into ASCII-Flux summary.
        
        Args:
            text: Input text string
            
        Returns:
            AsciiFluxSummary with metrics
        """
        if not text:
            return AsciiFluxSummary(
                points=[],
                entropy=0.0,
                curvature=0.0,
                dual_rail_ratio=0.0,
                diversity=0.0
            )

        points: List[AsciiFluxPoint] = []
        ascii_codes: List[int] = []

        for ch in text:
            code = ord(ch)
            ascii_codes.append(code)
            prime_code = _nearest_prime(code)
            exp2, exp5 = self.factor_2_5(code)
            points.append(
                AsciiFluxPoint(
                    char=ch,
                    ascii_code=code,
                    prime_code=prime_code,
                    exp2=exp2,
                    exp5=exp5,
                )
            )

        # entropy over ascii distribution
        freq: Dict[int, int] = {}
        for c in ascii_codes:
            freq[c] = freq.get(c, 0) + 1
        total = len(ascii_codes)
        entropy = 0.0
        for count in freq.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        # curvature: mean abs difference between consecutive ascii codes
        if len(ascii_codes) > 1:
            diffs = [abs(ascii_codes[i+1] - ascii_codes[i]) for i in range(len(ascii_codes) - 1)]
            curvature = sum(diffs) / len(diffs)
        else:
            curvature = 0.0

        # dual-rail ratio: heuristic "near 6k±1" check on prime_code
        def _is_six_k_pm_one(p: int) -> bool:
            if p < 5:
                return False
            k = (p - 1) // 6
            return p == 6 * k + 1 or p == 6 * k - 1

        near_dual_rail = sum(1 for pt in points if _is_six_k_pm_one(pt.prime_code))
        dual_rail_ratio = near_dual_rail / len(points) if points else 0.0

        # diversity: unique character fraction
        diversity = len(freq) / len(ascii_codes) if ascii_codes else 0.0

        return AsciiFluxSummary(
            points=points,
            entropy=entropy,
            curvature=curvature,
            dual_rail_ratio=dual_rail_ratio,
            diversity=diversity,
        )

    def to_dict(self, summary: AsciiFluxSummary) -> Dict[str, Any]:
        """Convert summary to a JSON-serializable dict for capsules."""
        return {
            "entropy": summary.entropy,
            "curvature": summary.curvature,
            "dual_rail_ratio": summary.dual_rail_ratio,
            "diversity": summary.diversity,
            "points": [
                {
                    "char": p.char,
                    "ascii": p.ascii_code,
                    "prime": p.prime_code,
                    "exp2": p.exp2,
                    "exp5": p.exp5,
                }
                for p in summary.points
            ],
        }

