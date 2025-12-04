"""
PrimeFlux Core — mathematical backbone of PF.

This module provides the fundamental PrimeFlux operations:
- distinction
- flux
- shells
- curvature
- combinatorics

Implements full PrimeFlux mathematics based on distinction dynamics,
flux operators, triplet logic, and shell transitions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Any
from enum import Enum
import math
import collections


class PFShell(Enum):
    """PrimeFlux shell enumeration."""
    PRESENCE = 0
    MEASUREMENT = 2
    FLUX = 3
    COLLAPSE = 4


@dataclass
class PFState:
    """
    State of a PrimeFlux operation.
    
    A distinction state = a point x in the PF manifold.
    State includes:
    - shell σ ∈ {0,2,3,4}
    - triplet decomposition
    - curvature
    - entropy
    - lattice position
    - combinatorics (p,p,q)
    - measurement_error (PF Principle: error = continuation, not reduction)
    
    PF Measurement-Error Principle:
    Measurement does NOT reduce information.
    Instead, measurement creates a duality state (Shell 2)
    and produces an "error term" that encodes the distance
    from presence (Shell 0). That error becomes the seed for
    curvature evolution (Shell 3).
    
    Error = continuation, not reduction.
    """
    shell: PFShell = PFShell.PRESENCE
    value: float = 0.0
    curvature: float = 0.0
    entropy: float = 0.0
    measurement_error: float = 0.0  # Error = new degree of freedom, not limitation
    triplet: PFTriplet | None = None
    combinatorics: tuple[int, int, int] | None = None  # (p, p, q)
    lattice_position: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PFTriplet:
    """A PrimeFlux triplet (presence, trig, or combinatorics)."""
    a: float
    b: float
    c: float
    triplet_type: str = "unknown"


@dataclass
class PFFlux:
    """Flux representation."""
    amplitude: float = 0.0
    direction: str = "neutral"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PFManifoldState:
    """State of a PrimeFlux manifold."""
    curvature: float = 0.0
    entropy: float = 0.0
    triplets: list[PFTriplet] = field(default_factory=list)
    shell_history: list[PFShell] = field(default_factory=list)


class PFOperator(Protocol):
    """Protocol for PrimeFlux operators."""

    def __call__(self, state: PFState) -> PFState:
        """Apply the operator to a state."""
        ...


def apply_operator(state: PFState, operator: PFOperator) -> PFState:
    """
    Apply a PrimeFlux operator to a state.

    Args:
        state: Current PF state
        operator: Operator to apply

    Returns:
        New PF state after operator application
    """
    return operator(state)


def compute_measurement_error(state: PFState) -> float:
    """
    Compute measurement error as duality distance.
    
    PF Law: Measurement produces error, error produces distinction,
    distinction produces flux, flux produces information.
    
    Measurement does NOT reduce information - it creates duality.
    Error = the distance from presence (Shell 0) = new degree of freedom.
    
    Args:
        state: Current PF state
        
    Returns:
        Measurement error (informational potential, not loss)
    """
    if state.shell == PFShell.PRESENCE:
        # No error in presence - pure unmeasured context
        return 0.0
    
    # Error = duality distance from presence
    # This represents the informational potential created by measurement
    if state.shell == PFShell.MEASUREMENT:
        # Measurement creates duality - error is the distance
        error = abs(state.value - 0.0)  # Distance from presence
        return error
    
    # For flux and collapse, error accumulates
    base_error = abs(state.value)
    curvature_contribution = state.curvature * 0.1
    return base_error + curvature_contribution


def transition_shell(
    state: PFState,
    flux_amplitude: float | None = None,
    curvature_gradient: float | None = None,
    triplet_class: str | None = None,
    combinatorics_stable: bool = True
) -> PFState:
    """
    Transition to the next shell in the PF sequence.
    
    Shell transitions follow: 0 → 2 → 3 → 4 → 0
    Transition is computed by:
    - magnitude of flux
    - curvature gradient sign
    - triplet class
    - combinatorics stability

    Args:
        state: Current PF state
        flux_amplitude: Magnitude of flux (if None, uses default transition)
        curvature_gradient: Curvature gradient sign
        triplet_class: Triplet class identifier
        combinatorics_stable: Whether combinatorics structure is stable

    Returns:
        New state with updated shell
    """
    # If flux amplitude is provided, use it to determine transition
    if flux_amplitude is not None:
        # High flux amplitude (> threshold) forces transition
        flux_threshold = 0.5
        if flux_amplitude > flux_threshold:
            new_shell = next_shell(state.shell)
        else:
            # Low flux may stay in same shell
            new_shell = state.shell
    else:
        # Default sequential transition
        new_shell = next_shell(state.shell)
    
    # Curvature gradient sign can influence transition
    if curvature_gradient is not None:
        if curvature_gradient < 0:  # Negative gradient may delay transition
            # Stay in current shell if gradient is negative
            if state.shell != PFShell.COLLAPSE:
                pass  # Allow transition
        elif curvature_gradient > 1.0:  # Strong positive gradient forces transition
            new_shell = next_shell(state.shell)
    
    # Combinatorics stability check
    if not combinatorics_stable:
        # Unstable combinatorics may prevent transition
        if state.shell == PFShell.FLUX:
            # Stay in flux until stable
            new_shell = state.shell
    
    # Compute measurement error (error = continuation, not reduction)
    measurement_error = compute_measurement_error(state)
    
    return PFState(
        shell=new_shell,
        value=state.value,
        curvature=state.curvature,
        entropy=state.entropy,
        measurement_error=measurement_error,
        triplet=state.triplet,
        combinatorics=state.combinatorics,
        lattice_position=state.lattice_position,
        metadata=state.metadata
    )


def compute_curvature(state: PFManifoldState) -> float:
    """
    Compute curvature measure for a manifold state.
    
    Curvature = f(irrational constants, triplet oscillation, distinction-density)
    
    Uses:
    - √2 superposition section
    - π / φ / e curvature triplet section
    - reptend-cycle curvature patterns

    Args:
        state: Manifold state

    Returns:
        Curvature scalar
    """
    # Irrational constants
    sqrt2 = math.sqrt(2.0)
    pi = math.pi
    phi = (1.0 + math.sqrt(5.0)) / 2.0  # Golden ratio
    e = math.e
    
    # Base curvature from irrational constants
    base_curvature = (sqrt2 + pi / phi) / e
    
    # Triplet oscillation component
    triplet_oscillation = 0.0
    if state.triplets:
        # Compute variance in triplet values
        all_values = []
        for triplet in state.triplets:
            all_values.extend([triplet.a, triplet.b, triplet.c])
        
        if len(all_values) > 1:
            mean_val = sum(all_values) / len(all_values)
            variance = sum((v - mean_val) ** 2 for v in all_values) / len(all_values)
            triplet_oscillation = math.sqrt(variance)
    
    # Distinction density component
    distinction_density = len(state.triplets) / max(len(state.shell_history), 1)
    
    # Combine components
    curvature = base_curvature * (1.0 + triplet_oscillation) * (1.0 + distinction_density * 0.1)
    
    return curvature


def compute_entropy(state: PFManifoldState) -> float:
    """
    Compute entropy measure for a manifold state.
    
    Entropy = degree of distinction spread.
    H = -Σ p_i log p_i
    
    Where p_i comes from:
    - triplet frequencies
    - shell occupancy
    - combinatorics (p,p,q)
    - token dispersion

    Args:
        state: Manifold state

    Returns:
        Entropy scalar
    """
    entropy = 0.0
    
    # Triplet frequency entropy
    if state.triplets:
        triplet_types = [t.triplet_type for t in state.triplets]
        type_counts = collections.Counter(triplet_types)
        total = len(triplet_types)
        
        for count in type_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p) if p > 0 else 0.0
    
    # Shell occupancy entropy
    if state.shell_history:
        shell_counts = collections.Counter(state.shell_history)
        total_shells = len(state.shell_history)
        
        for count in shell_counts.values():
            if count > 0:
                p = count / total_shells
                entropy += 0.5 * (-p * math.log2(p) if p > 0 else 0.0)
    
    # Combinatorics entropy (from triplet values)
    if state.triplets:
        value_entropy = 0.0
        all_values = []
        for triplet in state.triplets:
            all_values.extend([abs(triplet.a), abs(triplet.b), abs(triplet.c)])
        
        if all_values:
            # Bin values into ranges for entropy computation
            if max(all_values) > 0:
                bins = collections.Counter(int(v * 10) for v in all_values)
                total_vals = len(all_values)
                for count in bins.values():
                    if count > 0:
                        p = count / total_vals
                        value_entropy -= p * math.log2(p) if p > 0 else 0.0
        
        entropy += 0.3 * value_entropy
    
    return max(entropy, 0.0)  # Ensure non-negative


def triplet_decomposition(tokens: list[str]) -> list[PFTriplet]:
    """
    Decompose tokens into PF triplets.
    
    Converts tokens into presence, trig, and combinatorics triplets
    based on token characteristics and relationships.

    Args:
        tokens: List of input tokens

    Returns:
        List of PF triplets
    """
    triplets = []
    
    if not tokens:
        return triplets
    
    # Process tokens in groups of 3 for triplet formation
    for i in range(0, len(tokens), 3):
        group = tokens[i:i+3]
        
        if len(group) == 3:
            # Convert tokens to numeric values (simplified: use hash/ord)
            values = [float(hash(t) % 100) / 100.0 for t in group]
            
            # Normalize values
            max_val = max(values) if values else 1.0
            if max_val > 0:
                values = [v / max_val for v in values]
            
            # Determine triplet type based on values
            a, b, c = values[0], values[1], values[2]
            
            # Check for presence triplet pattern (0, 1, √2)
            sqrt2 = math.sqrt(2.0)
            if abs(a) < 0.1 and abs(b - 1.0) < 0.1 and abs(c - sqrt2) < 0.1:
                triplet_type = "presence"
            # Check for trig triplet pattern (1, 2, 3)
            elif abs(a - 0.33) < 0.1 and abs(b - 0.67) < 0.1 and abs(c - 1.0) < 0.1:
                triplet_type = "trig"
            # Check for combinatorics pattern (p, p, q)
            elif abs(a - b) < 0.1 and abs(c - a) > 0.1:
                triplet_type = "combinatorics"
            else:
                triplet_type = "unknown"
            
            triplets.append(PFTriplet(a=a, b=b, c=c, triplet_type=triplet_type))
        elif len(group) == 2:
            # Create triplet with default third value
            values = [float(hash(t) % 100) / 100.0 for t in group]
            values.append(math.sqrt(2.0))  # Add √2 as third value
            triplets.append(PFTriplet(a=values[0], b=values[1], c=values[2], triplet_type="presence"))
        elif len(group) == 1:
            # Create presence triplet with single token
            val = float(hash(group[0]) % 100) / 100.0
            triplets.append(PFTriplet(a=0.0, b=val, c=math.sqrt(2.0), triplet_type="presence"))
    
    return triplets


def validate_flux(state: PFState) -> bool:
    """
    Validate that a flux state is well-formed.
    
    Validates:
    - Shell is in valid range {0, 2, 3, 4}
    - Curvature is finite
    - Entropy is non-negative
    - Triplet values are finite
    - Combinatorics structure is valid if present

    Args:
        state: PF state to validate

    Returns:
        True if valid, False otherwise
    """
    # Check shell validity
    if state.shell not in [PFShell.PRESENCE, PFShell.MEASUREMENT, PFShell.FLUX, PFShell.COLLAPSE]:
        return False
    
    # Check curvature is finite
    if not math.isfinite(state.curvature):
        return False
    
    # Check entropy is non-negative and finite
    if state.entropy < 0 or not math.isfinite(state.entropy):
        return False
    
    # Check triplet if present
    if state.triplet is not None:
        if not all(math.isfinite(v) for v in [state.triplet.a, state.triplet.b, state.triplet.c]):
            return False
    
    # Check combinatorics if present
    if state.combinatorics is not None:
        p1, p2, q = state.combinatorics
        if p1 <= 0 or p2 <= 0 or q <= 0:
            return False
        # Check that p1 == p2 (combinatorics requirement)
        if abs(p1 - p2) > 0.001:
            return False
    
    # Check lattice position is finite
    if not math.isfinite(state.lattice_position):
        return False
    
    return True


def next_shell(current_shell: PFShell) -> PFShell:
    """
    Get the next shell in the PF sequence.

    Sequence: PRESENCE (0) -> MEASUREMENT (2) -> FLUX (3) -> COLLAPSE (4) -> PRESENCE (0)

    Args:
        current_shell: Current shell

    Returns:
        Next shell in sequence
    """
    transitions = {
        PFShell.PRESENCE: PFShell.MEASUREMENT,
        PFShell.MEASUREMENT: PFShell.FLUX,
        PFShell.FLUX: PFShell.COLLAPSE,
        PFShell.COLLAPSE: PFShell.PRESENCE,
    }
    return transitions.get(current_shell, PFShell.PRESENCE)

