"""
PrimeFlux v3 Mathematics Core.

Complete mathematical implementation of PrimeFlux principles.
"""

from .shells import Shell, shell_curvature, next_shell, shell_from_value, shell_transition_probability
from .triplets import (
    TripletType,
    Triplet,
    make_presence_triplet,
    make_trig_triplet,
    make_combinatoric_triplet,
    triplet_entropy,
    triplet_curvature,
    detect_triplet_type,
    trig_triplet_mapping,
)
from .curvature import (
    presence_curvature,
    measurement_curvature,
    trig_curvature,
    irrational_curvature,
    combined_curvature,
)
from .reptends import (
    reptend_length,
    reptend_entropy,
    reptend_curvature,
)
from .lattice import (
    PrimeRail,
    prime_rail,
    rail_interaction,
    flux_multiplier,
)
from .flux_ops import (
    flux_basic,
    flux_general,
    flux_propagate,
)
from .hamiltonians import (
    hamiltonian,
    curvature_well,
    collapse_energy,
)
from .density import (
    distinction_density,
    curvature_density,
    density_gradient,
)
from .superposition import (
    amplitude,
    magnitude,
    shell_from_superposition,
)
from .duality import (
    duality_state,
    measurement_duality,
    error_curvature_duality,
)
from .combinatorics import (
    combinatoric_flux,
    combinatoric_entropy,
    combinatoric_curvature,
)
from .quanta_math import (
    compression_ratio,
    quanta_hash,
    quanta_mint,
)
from .manifolds_5d import (
    embed_to_5d,
    curvature_5d,
    projection_3d,
)

__all__ = [
    # Shells
    "Shell",
    "shell_curvature",
    "next_shell",
    "shell_from_value",
    "shell_transition_probability",
    # Triplets
    "TripletType",
    "Triplet",
    "make_presence_triplet",
    "make_trig_triplet",
    "make_combinatoric_triplet",
    "triplet_entropy",
    "triplet_curvature",
    "detect_triplet_type",
    "trig_triplet_mapping",
    # Curvature
    "presence_curvature",
    "measurement_curvature",
    "trig_curvature",
    "irrational_curvature",
    "combined_curvature",
    # Reptends
    "reptend_length",
    "reptend_entropy",
    "reptend_curvature",
    # Lattice
    "PrimeRail",
    "prime_rail",
    "rail_interaction",
    "flux_multiplier",
    # Flux
    "flux_basic",
    "flux_general",
    "flux_propagate",
    # Hamiltonian
    "hamiltonian",
    "curvature_well",
    "collapse_energy",
    # Density
    "distinction_density",
    "curvature_density",
    "density_gradient",
    # Superposition
    "amplitude",
    "magnitude",
    "shell_from_superposition",
    # Duality
    "duality_state",
    "measurement_duality",
    "error_curvature_duality",
    # Combinatorics
    "combinatoric_flux",
    "combinatoric_entropy",
    "combinatoric_curvature",
    # Quanta
    "compression_ratio",
    "quanta_hash",
    "quanta_mint",
    # Manifolds
    "embed_to_5d",
    "curvature_5d",
    "projection_3d",
]
