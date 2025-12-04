"""
Core PrimeFlux modules: PF operators, triplets, shells, flux, ICM, LCM, and quanta.
"""

from .pf_core import (
    PFState,
    PFOperator,
    PFShell,
    PFTriplet,
    PFFlux,
    PFManifoldState,
    apply_operator,
    transition_shell,
    compute_curvature,
    compute_entropy,
    triplet_decomposition,
    validate_flux,
    next_shell,
)
from .ascii_flux import AsciiFluxShell

__all__ = [
    "PFState",
    "PFOperator",
    "PFShell",
    "PFTriplet",
    "PFFlux",
    "PFManifoldState",
    "apply_operator",
    "transition_shell",
    "compute_curvature",
    "compute_entropy",
    "triplet_decomposition",
    "validate_flux",
    "next_shell",
    "AsciiFluxShell",
]

