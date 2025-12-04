"""
Language Curvature Manifold (LCM) — Apop's "brain".

Full PF-driven state transitions, distinction chains, and capsule generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional
import math
import time
from ApopToSiS.core.icm import ICM, ICMState
from ApopToSiS.core.math.shells import Shell, shell_curvature, next_shell, shell_transition_probability
import random

from ApopToSiS.core.math.triplets import (
    Triplet,
    TripletType,
    make_presence_triplet,
    make_trig_triplet,
    make_combinatoric_triplet,
    triplet_entropy,
    triplet_curvature,
    detect_triplet_type,
)
from ApopToSiS.core.math.curvature import combined_curvature
from ApopToSiS.core.math.reptends import reptend_entropy
from ApopToSiS.core.math.lattice import rail_interaction, flux_multiplier
from ApopToSiS.core.math.flux_ops import flux_basic, flux_propagate
from ApopToSiS.core.math.hamiltonians import hamiltonian, collapse_energy
from ApopToSiS.core.math.density import distinction_density
from ApopToSiS.core.math.superposition import magnitude, shell_from_superposition
from ApopToSiS.core.math.duality import measurement_duality, error_curvature_duality
from ApopToSiS.core.math.combinatorics import combinatoric_curvature, combinatoric_entropy
from ApopToSiS.combinatoric.interpreter import CombinatoricInterpreter, CombinatoricDistinctionPacket
from ApopToSiS.core.ascii_flux import AsciiFluxShell


@dataclass
class LCMState:
    """LCM internal state."""
    tokens: list[str] = field(default_factory=list)
    triplets: list[Triplet] = field(default_factory=list)
    current_shell: Shell = Shell.PRESENCE
    shell_history: list[Shell] = field(default_factory=list)
    distinction_chain: list[dict[str, Any]] = field(default_factory=list)
    entropy_history: list[float] = field(default_factory=list)
    curvature_history: list[float] = field(default_factory=list)
    distinction_counts: list[int] = field(default_factory=list)


class LCM:
    """
    Language Curvature Manifold — Apop's cognitive processing engine.
    
    Uses full PF math for:
    - Triplet computation
    - Shell transitions
    - Curvature accumulation
    - Entropy computation
    - Distinction chain building
    - Capsule generation
    """

    def __init__(self, icm: Optional[ICM] = None, experience_manager: Any = None) -> None:
        """
        Initialize LCM.

        Args:
            icm: Optional ICM instance
            experience_manager: Optional ExperienceManager instance
        """
        self.state = LCMState()
        self.icm = icm or ICM()
        self.combinatoric_interpreter = CombinatoricInterpreter()
        self.experience_manager = experience_manager
        self.ascii_flux_shell = AsciiFluxShell()
        self._last_input_tokens: list[str] = []
        self._last_triplets: list[Triplet] = []
        self._last_user_text: str = ""

    def process_tokens(self, tokens: list[str]) -> None:
        """
        Process tokens and update LCM state.

        Args:
            tokens: List of tokens to process
        """
        tokens = tokens or []
        self._last_input_tokens = list(tokens)
        self._last_user_text = " ".join(tokens)
        self.state.tokens.extend(tokens)
        
        # Compute triplets
        triplets = self.compute_triplets(tokens)
        self._last_triplets = triplets
        self.state.triplets.extend(triplets)
        
        # Update ICM
        self.icm.update_curvature(tokens, triplets)
        self.icm.update_entropy(tokens, triplets)
        self.icm.update_shell()
        self.icm.update_flux()
        
        # Update LCM state from ICM
        icm_state = self.icm.to_lcm_state()
        entropy = icm_state["entropy"]
        curvature = icm_state["curvature"]
        shell_value = int(icm_state["shell"])

        # --- Flux damping ---
        entropy *= 0.92
        curvature *= 0.88

        # --- Measurement noise (stochastic realism) ---
        measurement_noise = random.uniform(-0.015, 0.015)
        entropy = max(0.0, entropy + measurement_noise)

        # --- Shell integrity enforcement ---
        if hasattr(self, "_last_shell_value"):
            if abs(shell_value - self._last_shell_value) > 1 and shell_value != Shell.COLLAPSE.value:
                shell_value = self._last_shell_value + (1 if shell_value > self._last_shell_value else -1)
        self._last_shell_value = shell_value

        # Persist adjustments back into ICM state
        self.icm.state.curvature = curvature
        self.icm.state.entropy = entropy
        self.icm.state.shell = Shell(shell_value)
        if self.icm.state.curvature_history:
            self.icm.state.curvature_history[-1] = curvature
        if self.icm.state.entropy_history:
            self.icm.state.entropy_history[-1] = entropy

        self.state.current_shell = Shell(shell_value)
        self.state.curvature_history.append(curvature)
        self.state.entropy_history.append(entropy)

    def compute_triplets(self, tokens: list[str]) -> list[Triplet]:
        """
        Compute triplets from tokens.
        
        Detects and creates:
        - Presence triplets (0, 1, √2)
        - Trig triplets (1, 2, 3)
        - Combinatoric triplets (p, p, q)
        
        Args:
            tokens: List of tokens
            
        Returns:
            List of triplets
        """
        triplets = []
        
        # Convert tokens to numeric values (hash-based)
        token_values = [float(hash(t) % 100) / 100.0 for t in tokens]
        
        # Detect triplets in sequence
        for i in range(len(token_values) - 2):
            triplet_vals = token_values[i:i+3]
            triplet_type = detect_triplet_type(triplet_vals)
            
            if triplet_type == TripletType.PRESENCE:
                triplets.append(make_presence_triplet())
            elif triplet_type == TripletType.TRIG:
                triplets.append(make_trig_triplet())
            elif triplet_type == TripletType.COMBINATORIC:
                # Extract primes (simplified)
                p = max(2, int(abs(triplet_vals[0]) * 100))
                q = max(2, int(abs(triplet_vals[2]) * 100))
                # Ensure primes
                p = _next_prime(p)
                q = _next_prime(q)
                try:
                    triplets.append(make_combinatoric_triplet(p, q))
                except ValueError:
                    pass
        
        return triplets

    def shell_transition(self, target_shell: Shell) -> bool:
        """
        Attempt to transition to target shell.
        
        Args:
            target_shell: Target shell
            
        Returns:
            True if transition successful
        """
        prob = shell_transition_probability(self.state.current_shell, self.icm.state.curvature)
        
        if prob > 0.5:
            self.state.shell_history.append(self.state.current_shell)
            self.state.current_shell = target_shell
            return True
        
        return False

    def build_distinction_chain(
        self,
        state: dict[str, Any],
        capsule: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """
        Build distinction chain from state and capsule.
        
        Args:
            state: Current state
            capsule: Current capsule
            
        Returns:
            List of distinction events
        """
        event = {
            "shell_before": self.state.shell_history[-1].value if self.state.shell_history else Shell.PRESENCE.value,
            "shell_after": self.state.current_shell.value,
            "curvature_before": self.state.curvature_history[-2] if len(self.state.curvature_history) >= 2 else 0.0,
            "curvature_after": self.state.curvature_history[-1] if self.state.curvature_history else 0.0,
            "entropy": self.state.entropy_history[-1] if self.state.entropy_history else 0.0,
            "flux": capsule.get("flux", 0.0),
            "density": capsule.get("density", 0.0),
            "timestamp": capsule.get("timestamp", 0.0),
        }
        
        self.state.distinction_chain.append(event)
        return self.state.distinction_chain

    def compute_entropy(
        self,
        tokens: list[str] | None = None,
        triplets: list[Triplet] | None = None
    ) -> float:
        """
        Compute entropy from tokens and triplets.
        
        Uses:
        - Triplet entropy
        - Reptend entropy
        - Combinatoric entropy
        
        Args:
            tokens: Optional tokens (uses state if None)
            triplets: Optional triplets (uses state if None)
            
        Returns:
            Entropy value
        """
        if tokens is None:
            tokens = self.state.tokens
        if triplets is None:
            triplets = self.state.triplets
        
        # Base entropy from tokens
        token_entropy = math.log(len(tokens) + 1) if tokens else 0.0
        
        # Triplet entropy
        triplet_ent = sum(triplet.entropy() for triplet in triplets)
        
        # Reptend entropy
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
        
        return total_entropy

    def compute_curvature(
        self,
        tokens: list[str] | None = None,
        triplets: list[Triplet] | None = None
    ) -> float:
        """
        Compute curvature from tokens and triplets.
        
        Uses combined curvature from PF math.
        
        Args:
            tokens: Optional tokens (uses state if None)
            triplets: Optional triplets (uses state if None)
            
        Returns:
            Curvature value
        """
        if tokens is None:
            tokens = self.state.tokens
        if triplets is None:
            triplets = self.state.triplets
        
        # Get curvature from ICM
        return self.icm.state.curvature

    def generate_capsule(
        self,
        state: dict[str, Any] | None = None,
        tokens: list[str] | None = None,
        triplets: list[Triplet] | None = None,
        user_text: str | None = None
    ) -> dict[str, Any]:
        """
        Generate JSON-Flux capsule.
        
        Args:
            state: Optional state (uses current state if None)
            tokens: Optional tokens (uses state if None)
            triplets: Optional triplets (uses state if None)
            
        Returns:
            Capsule dictionary
        """
        if tokens is None:
            tokens = self._last_input_tokens
        if triplets is None:
            triplets = self._last_triplets
        user_text = user_text if user_text is not None else self._last_user_text
        user_tokens = list(tokens or [])
        triplets = triplets or []
        
        # Get ICM state
        icm_state = self.icm.to_lcm_state()
        
        # Compute values
        entropy = self.compute_entropy(user_tokens, triplets)
        curvature = self.compute_curvature(user_tokens, triplets)
        
        # Distinction density
        distinction_counts = [1] * len(user_tokens)
        density = distinction_density(distinction_counts, window=5)
        density_val = density[-1] if isinstance(density, list) and density else (density if isinstance(density, float) else 0.0)
        
        # Superposition
        psi = magnitude(0.5, 0.5)
        
        # Hamiltonian
        H = hamiltonian(curvature)
        
        # Reptend entropy (from combinatoric triplets)
        reptend_ent = 0.0
        for triplet in triplets:
            if triplet.triplet_type.value == "combinatoric":
                p = int(triplet.a)
                reptend_ent += reptend_entropy(p)
        
        # Rail interference (from combinatoric triplets)
        rail_interf = 0.0
        for triplet in triplets:
            if triplet.triplet_type.value == "combinatoric":
                p = int(triplet.a)
                q = int(triplet.c)
                rail_interf += rail_interaction(p, q)
        
        # Quanta hash
        from .math.quanta_math import quanta_hash
        capsule_data = {
            "tokens": user_tokens,
            "triplets": [{"a": t.a, "b": t.b, "c": t.c, "type": t.triplet_type.value} for t in triplets],
            "entropy": entropy,
            "curvature": curvature,
        }
        quanta_hash_val = quanta_hash(capsule_data)
        
        # Compute ASCII-Flux metrics
        text_for_ascii = user_text or " ".join(user_tokens)
        ascii_summary = self.ascii_flux_shell.encode_text(text_for_ascii)
        ascii_flux_dict = self.ascii_flux_shell.to_dict(ascii_summary)

        flux_value = icm_state.get("flux", 0.0)
        flux_label = self._determine_flux_label(flux_value)
        raw_tokens = self._build_raw_tokens(user_tokens, flux_label)
        
        # Build capsule
        capsule = {
            "raw_tokens": raw_tokens,
            "triplets": [{"a": t.a, "b": t.b, "c": t.c, "type": t.triplet_type.value} for t in triplets],
            "entropy": entropy,
            "curvature": curvature,
            "shell": self.state.current_shell.value,
            "density": density_val,
            "psi": psi,
            "hamiltonian": H,
            "reptend_entropy": reptend_ent,
            "rail_interference": rail_interf,
            "flux": icm_state["flux"],
            "timestamp": time.time(),
            "quanta_hash": quanta_hash_val,
            "ascii_flux": ascii_flux_dict,
            "metadata": {
                "flux_label": flux_label,
            },
        }
        
        return capsule

    def _determine_flux_label(self, flux_value: float | None) -> str:
        """
        Bucket flux value into low/mid/high bands.
        """
        if flux_value is None:
            return "mid_flux"
        if flux_value < 0.33:
            return "low_flux"
        if flux_value < 0.66:
            return "mid_flux"
        return "high_flux"

    def _build_raw_tokens(self, user_tokens: list[str], flux_label: str) -> list[str]:
        """
        Build raw token list with a tiny internal prefix plus current user tokens.
        """
        shell_tag = {
            "high_flux": "shell_collapse",
            "low_flux": "shell_presence",
        }.get(flux_label, "shell_curvature")
        internal_prefix = ["...", "internal", "flux", shell_tag]
        return internal_prefix + list(user_tokens or [])

    def integrate_capsule(self, capsule: dict[str, Any], state: dict[str, Any] | None = None) -> None:
        """
        Integrate capsule into LCM state.
        
        Args:
            capsule: Capsule to integrate
            state: Optional state
        """
        # Update tokens
        if "raw_tokens" in capsule:
            self.state.tokens.extend(capsule["raw_tokens"])
        
        # Update triplets
        if "triplets" in capsule:
            for t_data in capsule["triplets"]:
                if t_data["type"] == "presence":
                    self.state.triplets.append(make_presence_triplet())
                elif t_data["type"] == "trig":
                    self.state.triplets.append(make_trig_triplet())
                elif t_data["type"] == "combinatoric":
                    # Reconstruct combinatoric triplet
                    p = int(t_data["a"])
                    q = int(t_data["c"])
                    try:
                        self.state.triplets.append(make_combinatoric_triplet(p, q))
                    except ValueError:
                        pass
        
        # Update shell
        if "shell" in capsule:
            self.state.current_shell = Shell(capsule["shell"])
        
        # Update history
        if "entropy" in capsule:
            self.state.entropy_history.append(capsule["entropy"])
        if "curvature" in capsule:
            self.state.curvature_history.append(capsule["curvature"])
        
        # Build distinction chain
        self.build_distinction_chain(state or {}, capsule)

    def integrate_llm_feedback(
        self,
        capsule: dict[str, Any] | None = None,
        pf_meta: dict[str, Any] | None = None,
        curvature_hint: float | None = None,
        flux_hint: str | None = None,
        entropy_hint: float | None = None
    ) -> None:
        """
        Integrate LLM feedback into LCM.
        
        Allowed to influence, not override.
        
        Args:
            capsule: Optional capsule dictionary with LLM feedback
            pf_meta: Optional PF metadata
            curvature_hint: Optional curvature hint
            flux_hint: Optional flux hint
            entropy_hint: Optional entropy hint
        """
        # Allowed to influence, not override
        return None

    def interpret(self, text: str) -> CombinatoricDistinctionPacket:
        """
        Interpret text through combinatoric interpreter.
        
        Args:
            text: Input text
            
        Returns:
            CombinatoricDistinctionPacket
        """
        return self.combinatoric_interpreter.interpret(text)

    def update_from_combinatorics(self, packet: CombinatoricDistinctionPacket) -> dict[str, Any]:
        """
        Update LCM from combinatoric packet.
        
        Args:
            packet: CombinatoricDistinctionPacket
            
        Returns:
            Generated capsule
        """
        # Process tokens
        self.process_tokens(packet.tokens)
        
        # Generate capsule
        return self.generate_capsule()

    def integrate_llm_feedback(
        self,
        capsule: dict[str, Any] | None = None,
        pf_meta: dict[str, Any] | None = None,
        curvature_hint: list[float] | None = None,
        flux_hint: dict[str, Any] | None = None,
        entropy_hint: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Combine LLM-provided hybrid-mode metadata with local PF capsule.
        
        This does NOT replace local curvature/entropy.
        It influences but does not dominate (PF rules).
        
        Args:
            capsule: Local PF capsule dictionary
            pf_meta: PF metadata from LLM
            curvature_hint: Curvature trajectory hints from LLM
            flux_hint: Flux interpretation from LLM
            entropy_hint: Entropy alignment hints from LLM
            
        Returns:
            Updated capsule with LLM feedback integrated (or empty dict if capsule is None)
        """
        # Handle None capsule
        if capsule is None:
            return {}
        
        # Initialize defaults
        if pf_meta is None:
            pf_meta = {}
        if curvature_hint is None:
            curvature_hint = []
        if flux_hint is None:
            flux_hint = {}
        if entropy_hint is None:
            entropy_hint = {}
        
        # Store LLM metadata in capsule
        capsule["pf_signature"] = pf_meta
        capsule["curvature_hint"] = curvature_hint
        capsule["flux_hint"] = flux_hint
        capsule["entropy_hint"] = entropy_hint
        
        # Light influence on local PF values (PF rules dominate)
        # Entropy amplifier (small influence)
        entropy_amplifier = entropy_hint.get("amplifier", 0.0) if isinstance(entropy_hint, dict) else 0.0
        if isinstance(entropy_amplifier, (int, float)):
            # Clamp amplifier to reasonable range
            entropy_amplifier = max(-0.5, min(0.5, float(entropy_amplifier)))
            capsule["entropy"] = capsule.get("entropy", 0.0) * (1.0 + entropy_amplifier)
        
        # Curvature hint (very light influence)
        if curvature_hint and isinstance(curvature_hint, list) and len(curvature_hint) > 0:
            # Use average of curvature hints, scaled down
            avg_curvature_hint = sum(curvature_hint) / len(curvature_hint)
            capsule["curvature"] = capsule.get("curvature", 0.0) + (avg_curvature_hint * 0.01)
        
        # Flux hint stored but not directly applied (informational only)
        if flux_hint:
            capsule["flux_interpretation"] = flux_hint
        
        return capsule


def _next_prime(n: int) -> int:
    """Find next prime >= n."""
    if n < 2:
        return 2
    if n == 2:
        return 2
    
    candidate = n
    while True:
        if _is_prime(candidate):
            return candidate
        candidate += 1


def _is_prime(n: int) -> bool:
    """Check if n is prime."""
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
