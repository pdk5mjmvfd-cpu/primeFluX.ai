"""
PrimeFlux Flux Operators — flux computation and propagation.

Implements:
- Flux operator: F_theta(x) = tanh(α tan(β x))
- Flux tensor (vector of partial derivatives)
- Flux amplitude computation

PF Flux-Error Principle:
Error becomes the driver of flux, not the "price" of flux.
flux_amplitude = f(error, curvature_gradient)

Meaning:
More error → more flux
More flux → more information
Thus flux never "dampens", it only stabilizes at Shell 4.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Any, Optional
import math
from .pf_core import PFState, PFManifoldState

# Optional FluxAI OperatorCore integration
try:
    from fluxai.operator_core.polyform_ops import ReversiblePolyformOps
    OPERATOR_CORE_AVAILABLE = True
except ImportError:
    OPERATOR_CORE_AVAILABLE = False
    ReversiblePolyformOps = None


@dataclass
class FluxOperator:
    """
    A PrimeFlux flux operator.
    
    F_theta(x) = tanh(α tan(β x))
    
    Where:
    - α = curvature scaling
    - β = frequency scaling
    - θ includes irrational constants (√2, π, φ, e)
    """
    name: str
    alpha: float = 1.0  # Curvature scaling
    beta: float = 1.0  # Frequency scaling
    sqrt2_factor: float = 1.0  # √2 influence
    pi_factor: float = 1.0  # π influence
    phi_factor: float = 1.0  # φ (golden ratio) influence
    e_factor: float = 1.0  # e influence
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __call__(self, x: float) -> float:
        """
        Apply flux operator: F_theta(x) = tanh(α tan(β x))
        
        Args:
            x: Input value
            
        Returns:
            Flux value
        """
        # Combine irrational constants
        theta = (
            self.sqrt2_factor * math.sqrt(2.0) +
            self.pi_factor * math.pi +
            self.phi_factor * ((1.0 + math.sqrt(5.0)) / 2.0) +
            self.e_factor * math.e
        ) / 4.0  # Normalize
        
        # Apply flux operator
        flux = math.tanh(self.alpha * math.tan(self.beta * x * theta))
        return flux


def apply_flux(state: PFState, operator: FluxOperator) -> PFState:
    """
    Apply a flux operator to a state.
    
    Flux = derivative of distinction.
    flux = (Δx / Δt) + curvature terms + error terms
    
    PF Principle: Error drives flux expansion, not reduction.

    Args:
        state: Current PF state
        operator: Flux operator to apply

    Returns:
        New state after flux application
    """
    # Compute flux value
    flux_value = operator(state.value)
    
    # Error contributes to flux (error = continuation)
    error_contribution = state.measurement_error * 0.2
    flux_value += error_contribution
    
    # Update state value with flux
    new_value = state.value + flux_value
    
    # Update curvature based on flux and error
    curvature_term = abs(flux_value) * 0.1
    error_curvature = state.measurement_error * 0.15  # Error creates curvature
    new_curvature = state.curvature + curvature_term + error_curvature
    
    # Update entropy based on flux amplitude (error expands entropy)
    flux_amp = abs(flux_value)
    entropy_change = flux_amp * 0.05
    error_entropy = state.measurement_error * 0.1  # Error expands information
    new_entropy = state.entropy + entropy_change + error_entropy
    
    # Update measurement error (error propagates, doesn't decay)
    new_error = state.measurement_error + abs(flux_value) * 0.1
    
    return PFState(
        shell=state.shell,
        value=new_value,
        curvature=new_curvature,
        entropy=new_entropy,
        measurement_error=new_error,
        triplet=state.triplet,
        combinatorics=state.combinatorics,
        lattice_position=state.lattice_position,
        metadata={**state.metadata, **operator.metadata, "flux_applied": True}
    )


def curvature_gradient(state: PFManifoldState) -> float:
    """
    Compute the curvature gradient for a manifold state.
    
    Gradient = vector of partial derivatives of curvature.

    Args:
        state: Manifold state

    Returns:
        Curvature gradient
    """
    if not state.triplets:
        return 0.0
    
    # Compute gradient from triplet variance
    all_values = []
    for triplet in state.triplets:
        all_values.extend([triplet.a, triplet.b, triplet.c])
    
    if len(all_values) < 2:
        return 0.0
    
    # Compute variance (proxy for gradient)
    mean_val = sum(all_values) / len(all_values)
    variance = sum((v - mean_val) ** 2 for v in all_values) / len(all_values)
    
    # Gradient is related to rate of change
    gradient = math.sqrt(variance) * state.curvature
    
    return gradient


def flux_amplitude(state: PFState, use_operator_core: bool = False, operator_core: Optional[ReversiblePolyformOps] = None) -> float:
    """
    Compute the flux amplitude for a state.
    
    PF Principle: Error drives flux, not limits it.
    |flux| = sqrt(dx^2 + curvature^2 + entropy^2 + error^2)
    
    More error → more flux → more information
    
    Args:
        state: PF state
        use_operator_core: If True, use reversible polyform operations
        operator_core: Optional ReversiblePolyformOps instance

    Returns:
        Flux amplitude (error-driven, not error-limited)
    """
    # Use polyform operations if enabled
    if use_operator_core and OPERATOR_CORE_AVAILABLE and operator_core is not None:
        # Encode state as polyform
        from fluxai.memory.polyform_int import PrimeFluxInt
        state_pfi = PrimeFluxInt(salt=int(state.value * 1000) % (2**32))
        state_pfi.encode({
            "value": state.value,
            "curvature": state.curvature,
            "entropy": state.entropy,
            "error": state.measurement_error
        }, salt=state_pfi.salt)
        
        # Use polyform flux amplitude
        return operator_core.flux_amplitude_polyform(state_pfi)
    
    # Standard computation
    # Compute components
    dx = abs(state.value)  # Value change component
    curvature_component = abs(state.curvature)
    entropy_component = abs(state.entropy)
    error_component = abs(state.measurement_error)  # Error drives flux
    
    # Flux amplitude - error contributes to flux, not reduces it
    amplitude = math.sqrt(
        dx**2 + 
        curvature_component**2 + 
        entropy_component**2 + 
        error_component**2
    )
    
    return amplitude


def flux_tensor(state: PFState) -> list[float]:
    """
    Compute flux tensor as vector of partial derivatives.
    
    Returns:
        List of flux components [dx, d_curvature, d_entropy]
    """
    return [
        state.value,  # dx component
        state.curvature,  # curvature component
        state.entropy,  # entropy component
    ]

