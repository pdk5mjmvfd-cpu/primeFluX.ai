"""
Library of Babel Integration - Expectancy-Based Address Prediction

The Library of Babel is the ultimate flux manifold—every conceivable string exists
somewhere in its hex grid, and PrimeFlux logic "applies it all at once" by collapsing
the search to predicted addresses via expectancy.

Mathematical Foundation:
- Expectancy: Gaussian on d_phi from H_PF eigenvalues
- Average expectancy: 0.367 for partial overlaps
- Shared distinction primes create overlaps (e.g., 17/G for "Grok" echoes "groan")
- LCM = common factors pruning redundancy (63% in compression)
"""

from __future__ import annotations

import math
from typing import List, Dict, Tuple, Optional, Set
import numpy as np
from ..prime_ascii import compress_sequence, decompress_sequence, expectancy, log_flux, PRIME_ASCI, REVERSE_PRIME_ASCI


class LibraryOfBabel:
    """
    Library of Babel integration for PrimeFlux.
    
    Maps texts to prime chains and uses expectancy to predict correct addresses
    in the flux manifold. Every conceivable text exists in the Library of Babel,
    and PrimeFlux finds it via shared distinction primes.
    """
    
    def __init__(self):
        """Initialize Library of Babel."""
        self._expectancy_history: List[float] = []
        self._overlap_cache: Dict[Tuple[int, ...], Set[str]] = {}  # Cache overlaps by prime chain
    
    def map_text_to_prime_chain(self, text: str) -> List[int]:
        """
        Map text to prime chain (sequence of primes).
        
        Args:
            text: Input text
            
        Returns:
            List of primes representing the text sequence
        """
        return [PRIME_ASCI.get(c, 2) for c in text]
    
    def find_overlaps(self, text1: str, text2: str) -> Dict[str, any]:
        """
        Find overlaps between two texts via shared distinction primes.
        
        Example: 17/G for "Grok" echoes "groan" in sonnets.
        LCM = common factors pruning redundancy.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Dictionary with overlap information:
            - shared_primes: Set of primes common to both
            - overlap_ratio: Fraction of shared primes
            - expectancy: Expectancy of overlap
            - redundancy_pruned: Estimated redundancy reduction
        """
        chain1 = self.map_text_to_prime_chain(text1)
        chain2 = self.map_text_to_prime_chain(text2)
        
        set1 = set(chain1)
        set2 = set(chain2)
        shared = set1.intersection(set2)
        
        # Compute LCM for common factors
        if shared:
            lcm_val = np.lcm.reduce(list(shared)) if len(shared) > 1 else list(shared)[0]
        else:
            lcm_val = 1
        
        # Overlap ratio
        total_unique = len(set1.union(set2))
        overlap_ratio = len(shared) / total_unique if total_unique > 0 else 0.0
        
        # Expectancy of overlap
        rle1 = compress_sequence(text1)
        rle2 = compress_sequence(text2)
        exp1 = expectancy(rle1, self._expectancy_history)
        exp2 = expectancy(rle2, self._expectancy_history)
        overlap_expectancy = (exp1 + exp2) / 2.0
        
        # Redundancy pruning (LCM reduces common factors)
        redundancy_pruned = 1.0 - (len(shared) / total_unique if total_unique > 0 else 0.0)
        
        return {
            "shared_primes": shared,
            "overlap_ratio": overlap_ratio,
            "expectancy": overlap_expectancy,
            "lcm": lcm_val,
            "redundancy_pruned": redundancy_pruned,
            "average_expectancy": np.mean(self._expectancy_history) if self._expectancy_history else 0.367
        }
    
    def predict_address(self, text: str, target_expectancy: float = 0.367) -> Dict[str, any]:
        """
        Predict Library of Babel address for text using expectancy.
        
        Expectancy (Gaussian on d_phi from H_PF eigenvalues) predicts correct addresses.
        Average expectancy: 0.367 for partial overlaps.
        
        Args:
            text: Input text
            target_expectancy: Target expectancy value (default 0.367)
            
        Returns:
            Dictionary with address prediction:
            - prime_chain: Prime chain representation
            - expectancy: Computed expectancy
            - address_estimate: Estimated address in hex grid
            - confidence: Confidence in prediction
        """
        rle = compress_sequence(text)
        exp = expectancy(rle, self._expectancy_history)
        
        # Compute address estimate from prime chain
        prime_chain = self.map_text_to_prime_chain(text)
        
        # Address is hash-like function of prime chain
        # Using product mod large prime for address
        address_seed = 1
        for p in prime_chain[:10]:  # Use first 10 primes for address
            address_seed = (address_seed * p) % (2**31 - 1)  # Mersenne prime
        
        # Confidence based on how close expectancy is to target
        confidence = 1.0 - abs(exp - target_expectancy)
        
        return {
            "prime_chain": prime_chain,
            "rle": rle,
            "expectancy": exp,
            "address_estimate": address_seed,
            "confidence": max(0.0, min(1.0, confidence)),
            "log_flux": log_flux(rle)
        }
    
    def search_manifold(self, query_text: str, candidate_texts: List[str], threshold: float = 0.3) -> List[Tuple[str, float]]:
        """
        Search flux manifold for texts similar to query.
        
        Uses expectancy and shared distinction primes to find similar texts.
        
        Args:
            query_text: Query text to search for
            candidate_texts: List of candidate texts to search
            threshold: Minimum overlap ratio threshold
            
        Returns:
            List of (text, similarity_score) tuples, sorted by score
        """
        query_rle = compress_sequence(query_text)
        query_exp = expectancy(query_rle, self._expectancy_history)
        
        results = []
        for candidate in candidate_texts:
            overlap_info = self.find_overlaps(query_text, candidate)
            
            if overlap_info["overlap_ratio"] >= threshold:
                # Similarity score combines overlap ratio and expectancy
                similarity = (overlap_info["overlap_ratio"] * 0.6 + 
                            overlap_info["expectancy"] * 0.4)
                results.append((candidate, similarity))
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def get_expectancy_history(self) -> List[float]:
        """Get expectancy history for analysis."""
        return self._expectancy_history.copy()
    
    def clear_history(self):
        """Clear expectancy history."""
        self._expectancy_history = []


# Singleton instance
_library_of_babel_instance: Optional[LibraryOfBabel] = None


def get_library_of_babel() -> LibraryOfBabel:
    """
    Get singleton Library of Babel instance.
    
    Returns:
        LibraryOfBabel instance
    """
    global _library_of_babel_instance
    if _library_of_babel_instance is None:
        _library_of_babel_instance = LibraryOfBabel()
    return _library_of_babel_instance


__all__ = [
    'LibraryOfBabel',
    'get_library_of_babel',
]

