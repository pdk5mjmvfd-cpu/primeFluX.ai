"""
PrimeFlux Triplets — three universal PF triplets.

- Presence triplet: (0, 1, √2)
- Trig triplet: (1, 2, 3)
- Combinatorics triplet: (p, p, q)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from typing import Optional


class TripletType(Enum):
    """Type of PF triplet."""
    PRESENCE = "presence"
    TRIG = "trig"
    COMBINATORICS = "combinatorics"
    UNKNOWN = "unknown"


@dataclass
class Triplet:
    """A PrimeFlux triplet."""
    a: float
    b: float
    c: float
    triplet_type: TripletType = TripletType.UNKNOWN

    def __post_init__(self) -> None:
        """Auto-detect triplet type if not set."""
        if self.triplet_type == TripletType.UNKNOWN:
            self.triplet_type = detect_triplet_type(self)


def make_triplets(tokens: list[str]) -> list[Triplet]:
    """
    Create triplets from tokens.
    
    Generates presence, trig, and combinatorics triplets based on
    token characteristics and relationships.

    Args:
        tokens: List of input tokens

    Returns:
        List of triplets
    """
    triplets = []
    
    if not tokens:
        return triplets
    
    sqrt2 = math.sqrt(2.0)
    
    # Process tokens in groups for triplet formation
    for i in range(0, len(tokens), 3):
        group = tokens[i:i+3]
        
        if len(group) == 3:
            # Convert tokens to numeric values using hash
            # Normalize to [0, 1] range
            hash_vals = [abs(hash(t)) % 10000 for t in group]
            max_hash = max(hash_vals) if hash_vals else 1.0
            values = [v / max_hash if max_hash > 0 else 0.0 for v in hash_vals]
            
            a, b, c = values[0], values[1], values[2]
            
            # Determine triplet type
            # Check for presence triplet: closeness to (0, 1, √2)
            dist_to_presence = (
                abs(a - 0.0) + abs(b - 1.0) + abs(c - sqrt2)
            )
            
            # Check for trig triplet: closeness to (1, 2, 3) normalized
            trig_normalized = [1.0/3.0, 2.0/3.0, 1.0]
            dist_to_trig = sum(abs(values[i] - trig_normalized[i]) for i in range(3))
            
            # Check for combinatorics: (p, p, q) pattern
            combinatorics_match = abs(a - b) < 0.1 and abs(c - a) > 0.1
            
            # Select type based on best match
            if dist_to_presence < 0.5:
                # Create presence triplet
                triplets.append(Triplet(
                    a=0.0,
                    b=1.0,
                    c=sqrt2,
                    triplet_type=TripletType.PRESENCE
                ))
            elif dist_to_trig < 0.3:
                # Create trig triplet (normalized to 1, 2, 3)
                triplets.append(Triplet(
                    a=1.0,
                    b=2.0,
                    c=3.0,
                    triplet_type=TripletType.TRIG
                ))
            elif combinatorics_match:
                # Create combinatorics triplet
                p = int(a * 100) if a > 0 else 2  # Ensure prime-like
                q = int(c * 100) if c > 0 else 3
                # Ensure p is prime-like (simplified)
                if p < 2:
                    p = 2
                triplets.append(Triplet(
                    a=float(p),
                    b=float(p),
                    c=float(q),
                    triplet_type=TripletType.COMBINATORICS
                ))
            else:
                # Default to presence triplet
                triplets.append(Triplet(
                    a=0.0,
                    b=1.0,
                    c=sqrt2,
                    triplet_type=TripletType.PRESENCE
                ))
        elif len(group) == 2:
            # Create presence triplet with two tokens
            hash_vals = [abs(hash(t)) % 10000 for t in group]
            val = (hash_vals[0] / 10000.0) if hash_vals else 0.5
            triplets.append(Triplet(
                a=0.0,
                b=val,
                c=sqrt2,
                triplet_type=TripletType.PRESENCE
            ))
        elif len(group) == 1:
            # Create presence triplet with single token
            hash_val = abs(hash(group[0])) % 10000
            val = hash_val / 10000.0
            triplets.append(Triplet(
                a=0.0,
                b=val,
                c=sqrt2,
                triplet_type=TripletType.PRESENCE
            ))
    
    return triplets


def detect_triplet_type(triplet: Triplet) -> TripletType:
    """
    Detect the type of a triplet based on its values.

    TODO: Implement full detection logic with PF math.

    Args:
        triplet: Triplet to classify

    Returns:
        Detected triplet type
    """
    # TODO: Implement full detection logic
    # Placeholder heuristics
    a, b, c = triplet.a, triplet.b, triplet.c
    
    # Check for presence triplet (0, 1, √2)
    if abs(a - 0.0) < 0.001 and abs(b - 1.0) < 0.001 and abs(c - math.sqrt(2.0)) < 0.001:
        return TripletType.PRESENCE
    
    # Check for trig triplet (1, 2, 3)
    if abs(a - 1.0) < 0.001 and abs(b - 2.0) < 0.001 and abs(c - 3.0) < 0.001:
        return TripletType.TRIG
    
    # Check for combinatorics pattern (p, p, q)
    if abs(a - b) < 0.001 and abs(c - a) > 0.001:
        return TripletType.COMBINATORICS
    
    return TripletType.UNKNOWN


def triplet_entropy(triplet: Triplet) -> float:
    """
    Compute entropy measure for a triplet.
    
    Entropy based on value distribution and triplet type.

    Args:
        triplet: Triplet to analyze

    Returns:
        Entropy value
    """
    a, b, c = abs(triplet.a), abs(triplet.b), abs(triplet.c)
    
    # Normalize values
    total = a + b + c
    if total == 0:
        return 0.0
    
    p_a = a / total
    p_b = b / total
    p_c = c / total
    
    # Compute entropy: H = -Σ p_i log p_i
    entropy = 0.0
    for p in [p_a, p_b, p_c]:
        if p > 0:
            entropy -= p * math.log2(p)
    
    # Adjust based on triplet type
    if triplet.triplet_type == TripletType.PRESENCE:
        # Presence triplets have higher entropy (superposition)
        entropy *= 1.2
    elif triplet.triplet_type == TripletType.TRIG:
        # Trig triplets have moderate entropy
        entropy *= 1.0
    elif triplet.triplet_type == TripletType.COMBINATORICS:
        # Combinatorics triplets have lower entropy (structure)
        entropy *= 0.8
    
    return entropy

