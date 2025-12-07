"""
PeriodicTable - PrimeFlux periodic table.

Refactored from periodic_table.py
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional


class PeriodicTable:
    """
    PrimeFlux periodic table.
    
    Maps primes to element-like properties.
    """
    
    def __init__(self):
        """Initialize periodic table."""
        self.elements: Dict[int, Dict[str, Any]] = {}
        self._initialize_elements()
    
    def _initialize_elements(self):
        """Initialize element data for primes."""
        # First few primes as elements
        prime_elements = {
            2: {"name": "Helium-Prime", "symbol": "He₂", "group": 0},
            3: {"name": "Lithium-Prime", "symbol": "Li₃", "group": 1},
            5: {"name": "Boron-Prime", "symbol": "B₅", "group": 13},
            7: {"name": "Nitrogen-Prime", "symbol": "N₇", "group": 15},
            11: {"name": "Sodium-Prime", "symbol": "Na₁₁", "group": 1},
            13: {"name": "Aluminum-Prime", "symbol": "Al₁₃", "group": 13},
            17: {"name": "Chlorine-Prime", "symbol": "Cl₁₇", "group": 17},
            19: {"name": "Potassium-Prime", "symbol": "K₁₉", "group": 1},
            23: {"name": "Vanadium-Prime", "symbol": "V₂₃", "group": 5},
            29: {"name": "Copper-Prime", "symbol": "Cu₂₉", "group": 11}
        }
        
        self.elements = prime_elements
    
    def get_element(self, prime: int) -> Optional[Dict[str, Any]]:
        """
        Get element data for prime.
        
        Args:
            prime: Prime number
            
        Returns:
            Element dictionary or None
        """
        if prime in self.elements:
            element = self.elements[prime].copy()
            element["prime"] = prime
            return element
        
        # Generate default for unknown prime
        return {
            "prime": prime,
            "name": f"Prime-{prime}",
            "symbol": f"P{prime}",
            "group": prime % 18
        }
    
    def get_all_elements(self) -> List[Dict[str, Any]]:
        """Get all elements."""
        return [
            self.get_element(prime)
            for prime in sorted(self.elements.keys())
        ]
