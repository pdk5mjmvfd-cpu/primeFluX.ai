"""
Eidos Agent — expansion / superposition (√2).

High entropy, broadening meaning, generating possibilities.

Role: Divergence, expansion, increase entropy
Shell Influence: Moves 0→2 and 2→3
PF Band: High-entropy curvature / oscillating rails
"""

from __future__ import annotations

from ApopToSiS.agents.base.base_agent import PFBaseAgent
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.user_safety_risk import UserSafetyRisk
from typing import Any
import math
from ApopToSiS.core.math.triplets import make_presence_triplet, make_trig_triplet, make_combinatoric_triplet
from ApopToSiS.core.math.superposition import magnitude, shell_from_superposition
from ApopToSiS.core.math.curvature import trig_curvature
from ApopToSiS.core.math.quanta_math import quanta_mint


class EidosAgent(PFBaseAgent):
    """
    Eidos Agent — expansion and superposition.
    
    Generates possibilities, frames, orientations.
    High entropy, broadening meaning.
    
    EIDOS BEHAVIOR:
    - Adds new possible distinctions
    - Creates combinatoric branches
    - Adds new triplets (presence, trig, combinatoric)
    - Boosts superposition (|ψ| decreases toward 0.7)
    - Adds future curvature possibilities
    - Increases QuantaCoin minting (more entropy to compress)
    """

    def __init__(self) -> None:
        """Initialize Eidos agent with safety risk assessor."""
        super().__init__(name="Eidos")
        self.safety_risk = UserSafetyRisk()

    def analyze(self, capsule: Capsule, state: PFState) -> dict[str, Any]:
        """
        Analyze capsule for expansion opportunities.
        
        Expand search radius, increase entropy, generate alternatives,
        identify combinatoric branching points.

        Args:
            capsule: Input capsule
            state: Current PF state

        Returns:
            Analysis with expansion possibilities
        """
        # Assess safety before expansion
        safety_result = self.safety_risk.assess_capsule_safety(capsule)
        
        # Expansion potential
        expansion_potential = state.entropy * math.sqrt(2.0)
        
        # Combinatoric branching points
        combinatoric_branches = len([t for t in capsule.triplets if isinstance(t, dict) and t.get("type") == "combinatoric"])
        
        return {
            "expansion_potential": expansion_potential,
            "possibility_count": len(capsule.raw_tokens) * 2,
            "superposition_strength": state.psi,
            "combinatoric_branches": combinatoric_branches,
            "safety_risk": safety_result.risk_score,
        }

    def transform(self, capsule: Capsule) -> Capsule:
        """
        Transform capsule through expansion.
        
        Eidos checks User Safety Risk (USR):
        - Explores safer creative space
        - Probes risk boundaries
        - Expands within safety constraints

        Args:
            capsule: Input capsule

        Returns:
            Expanded capsule
        """
        # Assess safety before expansion
        safety_result = self.safety_risk.assess_capsule_safety(capsule)
        
        # Expand within safety constraints
        if safety_result.agent_action == "block":
            # Don't expand unsafe directions
            new_metadata = {**capsule.metadata, "expansion_limited": True, "safety_risk_score": safety_result.risk_score}
            expansion_factor = 1.0  # No expansion
        elif safety_result.agent_action == "reframe":
            # Explore safer alternatives
            new_metadata = {**capsule.metadata, "safer_expansion": True, "safety_risk_score": safety_result.risk_score}
            expansion_factor = 1.2  # Moderate expansion
        else:
            new_metadata = capsule.metadata.copy()
            expansion_factor = 1.5  # Full expansion
        
        # Increase entropy (expansion)
        new_entropy = capsule.entropy * expansion_factor
        
        # Expand triplet summary
        new_summary = capsule.triplet_summary.copy()
        new_summary["expanded"] = True
        new_summary["expansion_factor"] = math.sqrt(2.0)
        
        # Add new triplets (presence, trig, combinatoric)
        new_triplets = capsule.triplets.copy()
        # Add presence triplet
        new_triplets.append({"a": 0.0, "b": 1.0, "c": math.sqrt(2.0), "type": "presence"})
        # Add trig triplet
        new_triplets.append({"a": 1.0, "b": 2.0, "c": 3.0, "type": "trig"})
        
        # Boost superposition (|ψ| decreases toward 0.7)
        new_psi = max(0.5, capsule.psi * 0.9)  # Decrease toward 0.7
        
        # Increase curvature slightly (future possibilities)
        new_curvature = capsule.curvature * 1.1
        
        # Create new capsule
        transformed = Capsule(
            triplet_summary=new_summary,
            shell_state=capsule.shell_state,
            entropy_snapshot=new_entropy,
            curvature_snapshot=new_curvature,
            timestamp=capsule.timestamp,
            raw_tokens=capsule.raw_tokens.copy(),
            pf_signature=capsule.pf_signature,
            compression_hash=capsule.compression_hash,
            metadata={**new_metadata, "agent": "eidos"},
            triplets=new_triplets,
            entropy=new_entropy,
            curvature=new_curvature,
            shell=capsule.shell,
            density=capsule.density,
            psi=new_psi,
            hamiltonian=capsule.hamiltonian,
        )
        
        return transformed

    def flux_signature(self) -> dict[str, Any]:
        """
        Get Eidos flux signature.
        
        High-frequency oscillatory flux.

        Returns:
            Flux signature dictionary
        """
        return {
            "amplitude": math.sqrt(2.0),
            "direction": "expansion",
            "shell_preference": 2,  # Measurement
            "type": "eidos",
            "curvature_bias": +0.2,
            "oscillation": "high",
            "density_shift": +0.1,
            "rail_interference": "divergent",
        }

    def entropy_signature(self) -> dict[str, Any]:
        """
        Get Eidos entropy signature.

        Returns:
            Entropy signature dictionary
        """
        return {
            "base_entropy": 1.0,
            "entropy_range": (0.5, 2.0),
            "tendency": "increase",
            "type": "eidos",
            "entropy_change": +0.3,
            "reptend_growth": +0.15,
        }
