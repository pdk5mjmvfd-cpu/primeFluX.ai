"""
Information Curvature Manifold (ICM).

PF geometric engine that accumulates:
- curvature gradients
- reptend-based entropy
- dual-rail interference
- flux amplitude
- distinction density
- Hamiltonian energy
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import math
from ApopToSiS.core.math.shells import Shell, shell_curvature, next_shell
from ApopToSiS.core.math.triplets import Triplet, make_presence_triplet, make_trig_triplet, make_combinatoric_triplet
from ApopToSiS.core.math.curvature import combined_curvature, trig_curvature, irrational_curvature
from ApopToSiS.core.math.reptends import reptend_entropy, reptend_curvature
from ApopToSiS.core.math.lattice import rail_interaction, flux_multiplier
from ApopToSiS.core.math.flux_ops import flux_basic, flux_propagate
from ApopToSiS.core.math.hamiltonians import hamiltonian, curvature_well
from ApopToSiS.core.math.density import distinction_density
from ApopToSiS.core.math.superposition import magnitude
from ApopToSiS.core.math.combinatorics import combinatoric_curvature, combinatoric_entropy


@dataclass
class ICMState:
    """ICM internal state."""
    curvature: float = 0.0
    entropy: float = 0.0
    shell: Shell = Shell.PRESENCE
    flux: float = 0.0
    density: float = 0.0
    psi_superposition: float = 0.0
    H_potential: float = 0.0
    curvature_history: list[float] = field(default_factory=list)
    entropy_history: list[float] = field(default_factory=list)
    shell_history: list[Shell] = field(default_factory=list)
    distinction_counts: list[int] = field(default_factory=list)


class ICM:
    """
    Information Curvature Manifold.
    
    PF geometric engine that processes tokens and triplets to produce
    curvature, entropy, shell, flux, density, superposition, and Hamiltonian.
    """

    def __init__(self) -> None:
        """Initialize ICM."""
        self.state = ICMState()

    def update_curvature(
        self,
        tokens: list[str],
        triplets: list[Triplet]
    ) -> None:
        """
        Update curvature from tokens and triplets.
        
        Uses:
        - irrational curvature
        - trig curvature
        - reptend curvature
        - PF Hamiltonian curvature
        - superposition curvature
        
        Args:
            tokens: List of tokens
            triplets: List of triplets
        """
        if not tokens:
            return
        
        # Compute distinction counts
        distinction_counts = [1] * len(tokens)  # Each token is a distinction
        self.state.distinction_counts.extend(distinction_counts)
        
        # Compute distinction density
        if len(self.state.distinction_counts) > 0:
            density = distinction_density(
                self.state.distinction_counts,
                window=5,
                position=len(self.state.distinction_counts) - 1
            )
            self.state.density = density if isinstance(density, float) else density[-1] if density else 0.0
        
        # Process triplets for curvature
        total_curvature = 0.0
        
        for triplet in triplets:
            # Combined curvature from triplet
            triplet_curv = combined_curvature(
                x=len(tokens),
                triplet=triplet,
                shell=self.state.shell
            )
            total_curvature += triplet_curv
        
        # Add irrational curvature
        irr_curv = irrational_curvature(len(tokens))
        total_curvature += irr_curv * 0.1
        
        # Add trig curvature
        trig_curv = trig_curvature(len(tokens))
        total_curvature += trig_curv * 0.2
        
        # Reptend curvature (if combinatoric triplets)
        for triplet in triplets:
            if triplet.triplet_type.value == "combinatoric":
                p = int(triplet.a)
                reptend_curv = reptend_curvature(p)
                total_curvature += reptend_curv * 0.15
        
        # Update state
        self.state.curvature = total_curvature
        self.state.curvature_history.append(total_curvature)

    def compute_curvature_derivative(self) -> float:
        """
        Compute curvature derivative.
        
        Returns:
            Curvature derivative
        """
        if len(self.state.curvature_history) < 2:
            return 0.0
        
        # Derivative = difference
        return self.state.curvature_history[-1] - self.state.curvature_history[-2]

    def temporal_coherence(self) -> float:
        """
        Compute temporal coherence.
        
        Returns:
            Temporal coherence value
        """
        if len(self.state.curvature_history) < 2:
            return 1.0
        
        # Coherence = inverse of variance
        import statistics
        if len(self.state.curvature_history) > 1:
            variance = statistics.variance(self.state.curvature_history[-10:])
            return 1.0 / (1.0 + variance)
        
        return 1.0

    def distinction_density(self) -> float:
        """
        Get current distinction density.
        
        Returns:
            Distinction density
        """
        return self.state.density

    def to_lcm_state(self) -> dict[str, Any]:
        """
        Convert ICM state to LCM-compatible state.
        
        Returns:
            Dictionary with:
            - curvature
            - entropy
            - shell
            - flux
            - density
            - psi_superposition
            - H_potential
        """
        # Compute flux
        flux = flux_basic(self.state.curvature)
        
        # Compute superposition
        psi = magnitude(0.5, 0.5)  # Default superposition
        
        # Compute Hamiltonian
        H = hamiltonian(self.state.curvature)
        
        return {
            "curvature": self.state.curvature,
            "entropy": self.state.entropy,
            "shell": self.state.shell.value,
            "flux": flux,
            "density": self.state.density,
            "psi_superposition": psi,
            "H_potential": H,
        }

    def update_entropy(
        self,
        tokens: list[str],
        triplets: list[Triplet]
    ) -> None:
        """
        Update entropy from tokens and triplets.
        
        Uses reptend-based entropy and combinatoric entropy.
        
        Args:
            tokens: List of tokens
            triplets: List of triplets
        """
        # Base entropy from tokens
        token_entropy = math.log(len(tokens) + 1)
        
        # Triplet entropy
        triplet_ent = 0.0
        for triplet in triplets:
            triplet_ent += triplet.entropy()
        
        # Reptend entropy (if combinatoric triplets)
        reptend_ent = 0.0
        for triplet in triplets:
            if triplet.triplet_type.value == "combinatoric":
                p = int(triplet.a)
                reptend_ent += reptend_entropy(p)
        
        # Combinatoric entropy
        combinatoric_ent = 0.0
        for triplet in triplets:
            if triplet.triplet_type.value == "combinatoric":
                p = int(triplet.a)
                q = int(triplet.c)
                combinatoric_ent += combinatoric_entropy(p, q)
        
        # Combined entropy
        total_entropy = (
            token_entropy * 0.3 +
            triplet_ent * 0.3 +
            reptend_ent * 0.2 +
            combinatoric_ent * 0.2
        )
        
        self.state.entropy = total_entropy
        self.state.entropy_history.append(total_entropy)

    def update_shell(self) -> None:
        """
        Update shell based on curvature and entropy.
        """
        new_shell = next_shell(
            self.state.shell,
            self.state.curvature,
            self.state.entropy
        )
        
        if new_shell != self.state.shell:
            self.state.shell_history.append(self.state.shell)
            self.state.shell = new_shell

    def update_flux(self) -> None:
        """
        Update flux amplitude.
        """
        self.state.flux = flux_propagate(
            self.state.curvature,
            self.state.curvature
        )
