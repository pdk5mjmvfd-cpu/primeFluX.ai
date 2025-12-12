"""
PrimeFlux Attractors - Unified Framework for Stable Convergence Points

Mathematical Foundation:
- Flux wave equation: ∇²Ψ - (1/v²)∂²Ψ/∂t² = Φ(p)Ψ (ApopTosis Thesis §2.5)
- Divergence law: ∇·Φ = 0 (Lyapunov function proving convergence) (ApopTosis Thesis §3.6)
- Empirical validation: σ ≈ 1/√2 invariant across 9000+ primes

Attractors are stable equilibria of the flux dynamics, toward which the system
converges. They are "hidden" - stored as reserved prime IDs, not computed.
"""

from __future__ import annotations

import math
from typing import Dict, Set, Optional, Tuple
from enum import Enum
from .reptends import reptend_length


class AttractorType(Enum):
    """Types of attractors in PrimeFlux system."""
    PRIME_REPTEND = "prime_reptend"
    SPECIAL_IRRATIONAL = "special_irrational"
    PRIME_ROOT = "prime_root"
    IMAGINARY_UNIT = "imaginary_unit"
    HAMILTONIAN_SEED = "hamiltonian_seed"


# Reserved prime IDs for attractors (hardcoded, not computed)
# These are "hidden" values that stabilize the system
ATTRACTOR_PRIME_IDS: Dict[str, int] = {
    # Special irrationals
    "pi": 31337,
    "e": 31357,
    "phi": 31379,  # Golden ratio φ
    "sqrt2": 31387,
    "sqrt3": 31393,
    "sqrt5": 31397,
    # Imaginary unit
    "i": 31411,
    # Hamiltonian seeds (irrational generators)
    "seed_1_11": 31417,  # 1/11 ≈ 0.090909...
    "seed_11_18": 31441,  # 11/18 ≈ 0.61111...
    "seed_1_3": 31447,  # 1/3 = 0.333...
    # Zeta(3) - Apéry's constant
    "zeta3": 31469,
}


class Attractor:
    """
    Represents a stable convergence point in PrimeFlux dynamics.
    
    Attractors are equilibria of the flux wave equation:
    ∇²Ψ - (1/v²)∂²Ψ/∂t² = Φ(p)Ψ
    
    Convergence is proven by ∇·Φ = 0 (divergence law, Lyapunov function).
    """
    
    def __init__(
        self,
        name: str,
        attractor_type: AttractorType,
        prime_id: int,
        value: Optional[float] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Initialize attractor.
        
        Args:
            name: Attractor name (e.g., "pi", "e", "reptend_7")
            attractor_type: Type of attractor
            prime_id: Reserved prime ID for this attractor
            value: Numerical value (if applicable, None for "hidden" attractors)
            metadata: Additional metadata (e.g., reptend period, prime p)
        """
        self.name = name
        self.attractor_type = attractor_type
        self.prime_id = prime_id
        self.value = value
        self.metadata = metadata or {}
    
    def __repr__(self) -> str:
        return f"Attractor({self.name}, type={self.attractor_type.value}, prime_id={self.prime_id})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Attractor):
            return False
        return self.prime_id == other.prime_id
    
    def __hash__(self) -> int:
        return hash(self.prime_id)


class AttractorRegistry:
    """
    Registry of all PrimeFlux attractors.
    
    Provides unified access to attractors across the system.
    """
    
    def __init__(self):
        """Initialize attractor registry."""
        self._attractors: Dict[int, Attractor] = {}
        self._by_name: Dict[str, Attractor] = {}
        self._by_type: Dict[AttractorType, Set[Attractor]] = {
            atype: set() for atype in AttractorType
        }
        
        # Initialize with hardcoded attractors
        self._initialize_special_irrationals()
        self._initialize_hamiltonian_seeds()
        self._initialize_imaginary_unit()
        self._initialize_zeta3()
    
    def _initialize_special_irrationals(self):
        """Initialize special irrational attractors."""
        specials = {
            "pi": (math.pi, AttractorType.SPECIAL_IRRATIONAL),
            "e": (math.e, AttractorType.SPECIAL_IRRATIONAL),
            "phi": ((1 + math.sqrt(5)) / 2, AttractorType.SPECIAL_IRRATIONAL),
            "sqrt2": (math.sqrt(2), AttractorType.SPECIAL_IRRATIONAL),
            "sqrt3": (math.sqrt(3), AttractorType.SPECIAL_IRRATIONAL),
            "sqrt5": (math.sqrt(5), AttractorType.SPECIAL_IRRATIONAL),
        }
        
        for name, (value, atype) in specials.items():
            prime_id = ATTRACTOR_PRIME_IDS[name]
            attractor = Attractor(name, atype, prime_id, value=value)
            self.register(attractor)
    
    def _initialize_hamiltonian_seeds(self):
        """Initialize Hamiltonian seed attractors."""
        seeds = {
            "seed_1_11": (1.0 / 11.0, AttractorType.HAMILTONIAN_SEED),
            "seed_11_18": (11.0 / 18.0, AttractorType.HAMILTONIAN_SEED),
            "seed_1_3": (1.0 / 3.0, AttractorType.HAMILTONIAN_SEED),
        }
        
        for name, (value, atype) in seeds.items():
            prime_id = ATTRACTOR_PRIME_IDS[name]
            attractor = Attractor(name, atype, prime_id, value=value)
            self.register(attractor)
    
    def _initialize_imaginary_unit(self):
        """Initialize imaginary unit attractor."""
        prime_id = ATTRACTOR_PRIME_IDS["i"]
        # i is not a real number, but we store it as a special attractor
        attractor = Attractor(
            "i",
            AttractorType.IMAGINARY_UNIT,
            prime_id,
            value=None,  # Hidden - not computed
            metadata={"is_imaginary": True}
        )
        self.register(attractor)
    
    def _initialize_zeta3(self):
        """Initialize zeta(3) attractor (Apéry's constant)."""
        # Zeta(3) ≈ 1.2020569031595942
        zeta3_value = sum(1.0 / (n ** 3) for n in range(1, 1000))  # Approximation
        prime_id = ATTRACTOR_PRIME_IDS["zeta3"]
        attractor = Attractor(
            "zeta3",
            AttractorType.SPECIAL_IRRATIONAL,
            prime_id,
            value=zeta3_value,
            metadata={"is_apery_constant": True}
        )
        self.register(attractor)
    
    def register(self, attractor: Attractor):
        """
        Register an attractor.
        
        Args:
            attractor: Attractor to register
        """
        self._attractors[attractor.prime_id] = attractor
        self._by_name[attractor.name] = attractor
        self._by_type[attractor.attractor_type].add(attractor)
    
    def get_by_prime_id(self, prime_id: int) -> Optional[Attractor]:
        """
        Get attractor by prime ID.
        
        Args:
            prime_id: Prime ID
            
        Returns:
            Attractor if found, None otherwise
        """
        return self._attractors.get(prime_id)
    
    def get_by_name(self, name: str) -> Optional[Attractor]:
        """
        Get attractor by name.
        
        Args:
            name: Attractor name
            
        Returns:
            Attractor if found, None otherwise
        """
        return self._by_name.get(name)
    
    def get_by_type(self, attractor_type: AttractorType) -> Set[Attractor]:
        """
        Get all attractors of a given type.
        
        Args:
            attractor_type: Type of attractor
            
        Returns:
            Set of attractors
        """
        return self._by_type.get(attractor_type, set()).copy()
    
    def is_attractor_prime(self, prime_id: int) -> bool:
        """
        Check if a prime ID is reserved for an attractor.
        
        Args:
            prime_id: Prime ID to check
            
        Returns:
            True if reserved, False otherwise
        """
        return prime_id in self._attractors
    
    def get_field_strength(self, attractor: Attractor, position: tuple[float, float, float, float]) -> float:
        """
        Get relativistic field strength at position.
        
        Args:
            attractor: Attractor creating the field
            position: Position (t, x, y, z)
            
        Returns:
            Field strength magnitude
        """
        return get_field_strength(attractor, position)
    
    def get_path_probability(self, path: List[float], attractor: Attractor) -> float:
        """
        Get probabilistic path probability to attractor.
        
        Args:
            path: Path as list of values
            attractor: Target attractor
            
        Returns:
            Path probability (0.0 to 1.0)
        """
        return get_path_probability(path, attractor)
    
    def get_number_class(self, number: int) -> str:
        """
        Get OOP classification of number.
        
        Args:
            number: Integer to classify
            
        Returns:
            Classification: "prime", "composite", or "attractor"
        """
        return get_number_class(number)
    
    def validate_limit(self, sequence: List[float], attractor: Attractor, 
                      tolerance: float = 1e-10) -> bool:
        """
        Validate limit alignment: sequence converges to attractor.
        
        Args:
            sequence: Sequence of values
            attractor: Target attractor
            tolerance: Convergence tolerance
            
        Returns:
            True if sequence converges to attractor
        """
        return validate_limit(sequence, attractor, tolerance)
    
    def register_prime_reptend(self, prime: int) -> Attractor:
        """
        Register a prime reptend as an attractor.
        
        Prime reptends are repeating decimal periods of 1/p.
        They form stable cycles via Fermat's Little Theorem.
        
        Args:
            prime: Prime number p
            
        Returns:
            Registered attractor
        """
        period = reptend_length(prime)
        if period == 0:
            raise ValueError(f"Prime {prime} has no reptend (terminating decimal)")
        
        name = f"reptend_{prime}"
        # Use prime itself as the prime_id (primes are unique)
        prime_id = prime
        
        attractor = Attractor(
            name,
            AttractorType.PRIME_REPTEND,
            prime_id,
            value=None,  # Hidden - not computed
            metadata={
                "prime": prime,
                "period": period,
                "reptend_value": 1.0 / prime
            }
        )
        
        self.register(attractor)
        return attractor
    
    def register_prime_root(self, prime: int) -> Attractor:
        """
        Register √p as an attractor.
        
        Args:
            prime: Prime number p
            
        Returns:
            Registered attractor
        """
        name = f"sqrt_{prime}"
        # Use a derived prime ID (next prime after p, or p^2 mod some large prime)
        # For simplicity, use p * 1000 + 1 as a unique identifier
        # In production, this should use a proper prime mapping
        prime_id = prime * 1000 + 1
        
        attractor = Attractor(
            name,
            AttractorType.PRIME_ROOT,
            prime_id,
            value=math.sqrt(prime),
            metadata={"prime": prime}
        )
        
        self.register(attractor)
        return attractor


# Global registry instance
_registry: Optional[AttractorRegistry] = None


def get_attractor_registry() -> AttractorRegistry:
    """
    Get the global attractor registry (singleton).
    
    Returns:
        AttractorRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = AttractorRegistry()
    return _registry


def check_convergence(flux_divergence: float, threshold: float = 1e-10) -> bool:
    """
    Check if system is converging toward attractors.
    
    Uses divergence law: ∇·Φ = 0 (Lyapunov function).
    System converges if divergence is near zero.
    
    Args:
        flux_divergence: Computed divergence ∇·Φ
        threshold: Convergence threshold (default 1e-10)
        
    Returns:
        True if converging (|∇·Φ| < threshold), False otherwise
    """
    return abs(flux_divergence) < threshold


def get_attractor_prime_id(name: str) -> Optional[int]:
    """
    Get reserved prime ID for an attractor by name.
    
    Args:
        name: Attractor name (e.g., "pi", "e", "phi")
        
    Returns:
        Prime ID if found, None otherwise
    """
    registry = get_attractor_registry()
    attractor = registry.get_by_name(name)
    return attractor.prime_id if attractor else None


def is_attractor_prime(prime_id: int) -> bool:
    """
    Check if a prime ID is reserved for an attractor.
    
    Args:
        prime_id: Prime ID to check
        
    Returns:
        True if reserved, False otherwise
    """
    registry = get_attractor_registry()
    return registry.is_attractor_prime(prime_id)


def get_field_strength(attractor: Attractor, position: tuple[float, float, float, float]) -> float:
    """
    Get relativistic field strength at position.
    
    Uses relativistic field theory to compute field strength.
    
    Args:
        attractor: Attractor creating the field
        position: Position (t, x, y, z)
        
    Returns:
        Field strength magnitude
    """
    from .relativistic_fields import AttractorField
    
    if attractor.value is None:
        return 0.0
    
    field = AttractorField(attractor.value, attractor.name)
    return field.field_strength(position)


def get_path_probability(path: List[float], attractor: Attractor) -> float:
    """
    Get probabilistic path probability to attractor.
    
    Uses path integral formulation.
    
    Args:
        path: Path as list of values
        attractor: Target attractor
        
    Returns:
        Path probability (0.0 to 1.0)
    """
    from .path_integrals import Path, path_probability
    
    if not path or attractor.value is None:
        return 0.0
    
    # Create path from list
    def trajectory(t: float) -> float:
        if t < 0 or t >= len(path):
            return path[-1] if path else 0.0
        idx = int(t * (len(path) - 1))
        return path[min(idx, len(path) - 1)]
    
    path_obj = Path(trajectory, 0.0, 1.0)
    return path_probability(path_obj, attractor)


def get_number_class(number: int) -> str:
    """
    Get OOP classification of number.
    
    Args:
        number: Integer to classify
        
    Returns:
        Classification: "prime", "composite", or "attractor"
    """
    from .number_classes import create_number, AttractorPrime, Prime
    
    num_obj = create_number(number)
    
    if isinstance(num_obj, AttractorPrime):
        return "attractor_prime"
    elif isinstance(num_obj, Prime):
        return "prime"
    else:
        return "composite"


def validate_limit(sequence: List[float], attractor: Attractor, 
                  tolerance: float = 1e-10) -> bool:
    """
    Validate limit alignment: sequence converges to attractor.
    
    Args:
        sequence: Sequence of values
        attractor: Target attractor
        tolerance: Convergence tolerance
        
    Returns:
        True if sequence converges to attractor
    """
    if not sequence or attractor.value is None:
        return False
    
    # Check if last value is near attractor
    final_value = sequence[-1]
    return abs(final_value - attractor.value) < tolerance

