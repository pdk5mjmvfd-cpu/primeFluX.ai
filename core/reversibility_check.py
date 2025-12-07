"""
Reversibility Checker - Validates reversibility of transformations.

Checks that output entropy doesn't exceed input entropy beyond threshold.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import List


class ReversibilityChecker:
    """
    Reversibility checker for PrimeFlux transformations.
    
    Validates that transformations maintain reversibility by checking
    entropy constraints.
    """
    
    def entropy(self, primes: List[int]) -> float:
        """
        Calculate Shannon entropy of prime distribution.
        
        Args:
            primes: List of prime numbers
            
        Returns:
            Entropy in nats (natural log base)
        """
        if not primes:
            return 0.0
        
        # Count frequencies
        counter = Counter(primes)
        total = len(primes)
        
        # Calculate Shannon entropy: H = -Σ p(x) * ln(p(x))
        entropy = 0.0
        for count in counter.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log(p)
        
        return entropy
    
    def check(
        self,
        input_primes: List[int],
        output_primes: List[int],
        threshold: float = 0.1
    ) -> bool:
        """
        Check reversibility constraint.
        
        Returns True if output_entropy <= input_entropy + threshold (nats).
        
        Args:
            input_primes: Input prime modes
            output_primes: Output prime modes
            threshold: Entropy increase threshold (default: 0.1 nats)
            
        Returns:
            True if reversible, False otherwise
        """
        input_entropy = self.entropy(input_primes)
        output_entropy = self.entropy(output_primes)
        
        # Check: output_entropy <= input_entropy + threshold
        return output_entropy <= input_entropy + threshold
    
    def entropy_diff(
        self,
        input_primes: List[int],
        output_primes: List[int]
    ) -> float:
        """
        Calculate entropy difference.
        
        Args:
            input_primes: Input prime modes
            output_primes: Output prime modes
            
        Returns:
            Entropy difference (output - input) in nats
        """
        input_entropy = self.entropy(input_primes)
        output_entropy = self.entropy(output_primes)
        return output_entropy - input_entropy
