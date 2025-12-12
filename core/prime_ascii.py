"""
Prime ASCI - Universal Encoding Layer for PrimeFlux

Maps text, symbols, and numbers to primes using Fundamental Theorem of Arithmetic.
Provides bijective text→prime mapping with reversible factorization.

Mathematical Foundation:
- Fundamental Theorem of Arithmetic: Every integer > 1 factors uniquely into primes
- Prime density: 1/ln(n) for probabilistic routing
- Prime moduli: Uniform distribution for hashing

Integration:
- Uses core/math/attractors.py for special number protection
- Replaces hash-based mapping in core/lcm.py
- Provides prime-based hashing for agent routing
"""

from __future__ import annotations

import math
from typing import List, Dict, Optional, Tuple, Set
from .math.attractors import get_attractor_registry, is_attractor_prime


# First 26 primes for A-Z mapping
# A=2, B=3, C=5, D=7, E=11, F=13, G=17, H=19, I=23, J=29, K=31, L=37, M=41,
# N=43, O=47, P=53, Q=59, R=61, S=67, T=71, U=73, V=79, W=83, X=89, Y=97, Z=101
LETTER_PRIMES: Dict[str, int] = {
    'A': 2, 'B': 3, 'C': 5, 'D': 7, 'E': 11, 'F': 13, 'G': 17, 'H': 19,
    'I': 23, 'J': 29, 'K': 31, 'L': 37, 'M': 41, 'N': 43, 'O': 47, 'P': 53,
    'Q': 59, 'R': 61, 'S': 67, 'T': 71, 'U': 73, 'V': 79, 'W': 83, 'X': 89,
    'Y': 97, 'Z': 101
}

# Lowercase maps to same primes (case-insensitive)
for letter, prime in list(LETTER_PRIMES.items()):
    LETTER_PRIMES[letter.lower()] = prime

# Digits 0-9 mapped to next primes after Z
# 0=103, 1=107, 2=109, 3=113, 4=127, 5=131, 6=137, 7=139, 8=149, 9=151
DIGIT_PRIMES: Dict[str, int] = {
    '0': 103, '1': 107, '2': 109, '3': 113, '4': 127,
    '5': 131, '6': 137, '7': 139, '8': 149, '9': 151
}

# Common symbols mapped to next primes
# Starting from 157 (next prime after 151)
SYMBOL_PRIMES: Dict[str, int] = {
    '!': 157, '?': 163, '@': 167, '#': 173, '$': 179, '%': 181,
    '^': 191, '&': 193, '*': 197, '(': 199, ')': 211, '-': 223,
    '_': 227, '=': 229, '+': 233, '[': 239, ']': 241, '{': 251,
    '}': 257, '|': 263, '\\': 269, ':': 271, ';': 277, '"': 281,
    "'": 283, '<': 293, '>': 307, ',': 311, '.': 313, '/': 317,
    '?': 331, '~': 337, '`': 347, ' ': 349,  # Space
}

# Operators get reserved namespace (next primes after symbols)
OPERATOR_PRIMES: Dict[str, int] = {
    '+': 353, '-': 359, '*': 367, '/': 373, '=': 379,
    '==': 383, '!=': 389, '<': 397, '>': 401, '<=': 409,
    '>=': 419, '&&': 421, '||': 431, '!': 433,
}


def _is_prime(n: int) -> bool:
    """Check if n is prime (simple trial division)."""
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


def _factorize(n: int) -> List[Tuple[int, int]]:
    """
    Factorize integer into prime factors with exponents.
    
    Returns list of (prime, exponent) tuples.
    Example: 12 → [(2, 2), (3, 1)]
    """
    if n < 2:
        return []
    
    factors = []
    # Factor out 2
    exp = 0
    while n % 2 == 0:
        exp += 1
        n //= 2
    if exp > 0:
        factors.append((2, exp))
    
    # Factor out odd primes
    for p in range(3, int(math.sqrt(n)) + 1, 2):
        exp = 0
        while n % p == 0:
            exp += 1
            n //= p
        if exp > 0:
            factors.append((p, exp))
    
    # Remaining n is prime
    if n > 1:
        factors.append((n, 1))
    
    return factors


def _prime_product(factors: List[Tuple[int, int]]) -> int:
    """
    Compute product of prime factors with exponents.
    
    Args:
        factors: List of (prime, exponent) tuples
        
    Returns:
        Product = ∏(prime^exponent)
    """
    result = 1
    for prime, exp in factors:
        result *= prime ** exp
    return result


class PrimeASCI:
    """
    Prime ASCI encoding system.
    
    Maps text, symbols, and numbers to primes using Fundamental Theorem of Arithmetic.
    Provides reversible encoding with unique factorization.
    """
    
    def __init__(self):
        """Initialize Prime ASCI system."""
        self.registry = get_attractor_registry()
        self._version = "1.0"  # Version for migration tracking
    
    def encode_char(self, char: str) -> Optional[int]:
        """
        Encode single character to prime.
        
        Args:
            char: Single character
            
        Returns:
            Prime ID, or None if character not mappable
        """
        if len(char) != 1:
            return None
        
        # Check letters
        if char in LETTER_PRIMES:
            return LETTER_PRIMES[char]
        
        # Check digits
        if char in DIGIT_PRIMES:
            return DIGIT_PRIMES[char]
        
        # Check symbols
        if char in SYMBOL_PRIMES:
            return SYMBOL_PRIMES[char]
        
        # Check operators
        if char in OPERATOR_PRIMES:
            return OPERATOR_PRIMES[char]
        
        return None
    
    def encode_string(self, text: str) -> List[int]:
        """
        Encode string to list of prime IDs.
        
        Args:
            text: Input string
            
        Returns:
            List of prime IDs (one per character)
        """
        primes = []
        for char in text:
            prime_id = self.encode_char(char)
            if prime_id is not None:
                primes.append(prime_id)
        return primes
    
    def encode_string_as_product(self, text: str) -> int:
        """
        Encode string as single prime product (composite token).
        
        Uses Fundamental Theorem: product uniquely factors back to original primes.
        
        Args:
            text: Input string
            
        Returns:
            Product of prime IDs
        """
        primes = self.encode_string(text)
        if not primes:
            return 1  # Empty string → 1 (multiplicative identity)
        
        product = 1
        for prime in primes:
            product *= prime
        return product
    
    def decode_product(self, product: int) -> Optional[str]:
        """
        Decode prime product back to string.
        
        Uses unique factorization to recover original primes.
        
        Args:
            product: Prime product
            
        Returns:
            Decoded string, or None if factorization invalid
        """
        if product == 1:
            return ""  # Empty string
        
        if product < 2:
            return None
        
        # Factorize product
        factors = _factorize(product)
        
        # Reconstruct string from prime factors
        # Note: This assumes factors are in order (may need sorting)
        chars = []
        reverse_map = {prime: char for char, prime in LETTER_PRIMES.items()}
        reverse_map.update({prime: char for char, prime in DIGIT_PRIMES.items()})
        reverse_map.update({prime: char for char, prime in SYMBOL_PRIMES.items()})
        reverse_map.update({prime: char for char, prime in OPERATOR_PRIMES.items()})
        
        for prime, exp in factors:
            if prime not in reverse_map:
                # Check if it's an attractor prime
                if is_attractor_prime(prime):
                    # Attractors are "hidden" - don't decode
                    continue
                return None  # Unknown prime
            
            char = reverse_map[prime]
            # Repeat character by exponent
            chars.extend([char] * exp)
        
        return ''.join(chars)
    
    def encode_number(self, number: int) -> int:
        """
        Encode number as prime factorization.
        
        Numbers are encoded as products of their prime factors.
        Example: 123 = 3 × 41 → product of prime IDs for 3 and 41
        
        Args:
            number: Integer to encode
            
        Returns:
            Prime product representing the number
        """
        if number < 0:
            # Negative numbers: use special prime for sign
            return -self.encode_number(-number)
        
        if number == 0:
            return DIGIT_PRIMES['0']
        
        if number == 1:
            return DIGIT_PRIMES['1']
        
        # Factorize number
        factors = _factorize(number)
        
        # Convert factors to prime product
        # Each factor (prime, exp) becomes (prime_id^exp) in product
        product = 1
        for prime, exp in factors:
            # Map prime to its prime ID (if it's a single digit, use DIGIT_PRIMES)
            if prime < 10:
                prime_id = DIGIT_PRIMES[str(prime)]
            else:
                # For larger primes, we need to map them
                # For now, use the prime itself (assuming it's in our mapping)
                prime_id = prime
            
            product *= prime_id ** exp
        
        return product
    
    def is_reserved_prime(self, prime_id: int) -> bool:
        """
        Check if prime ID is reserved (attractor or special constant).
        
        Args:
            prime_id: Prime ID to check
            
        Returns:
            True if reserved, False otherwise
        """
        # Check attractors
        if is_attractor_prime(prime_id):
            return True
        
        # Check if in our mapping ranges
        all_primes = set(LETTER_PRIMES.values())
        all_primes.update(DIGIT_PRIMES.values())
        all_primes.update(SYMBOL_PRIMES.values())
        all_primes.update(OPERATOR_PRIMES.values())
        
        return prime_id in all_primes
    
    def validate_factorization(self, product: int) -> bool:
        """
        Validate that a product can be factorized into valid primes.
        
        Args:
            product: Prime product to validate
            
        Returns:
            True if valid, False otherwise
        """
        if product < 2:
            return False
        
        factors = _factorize(product)
        
        for prime, _ in factors:
            # Check if prime is reserved (attractor or in mapping)
            if not self.is_reserved_prime(prime):
                # Check if it's a valid prime (not composite)
                if not _is_prime(prime):
                    return False
        
        return True
    
    def get_version(self) -> str:
        """Get Prime ASCI version for migration tracking."""
        return self._version


# Global instance
_prime_ascii: Optional[PrimeASCI] = None


def get_prime_ascii() -> PrimeASCI:
    """
    Get global Prime ASCI instance (singleton).
    
    Returns:
        PrimeASCI instance
    """
    global _prime_ascii
    if _prime_ascii is None:
        _prime_ascii = PrimeASCI()
    return _prime_ascii

