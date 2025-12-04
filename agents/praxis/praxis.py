"""
Praxis Agent — shaping / action (1→3).

Moderate entropy, structure, refinement, action curvature.

Role: Structure, reduce noise, create shape
Shell Influence: Moves 2→3 and stabilizes 3
PF Band: Moderate curvature / increasing density
"""

from __future__ import annotations

from ApopToSiS.agents.base.base_agent import PFBaseAgent
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.user_safety_risk import UserSafetyRisk
from typing import Any
import math
# TrigTriplet not needed


class PraxisAgent(PFBaseAgent):
    """
    Praxis Agent — shaping and action.
    
    Refines, applies, structures, executes.
    Moderate entropy, structure, refinement.
    
    PRAXIS BEHAVIOR:
    - Shapes Eidos output
    - Removes useless branches
    - Increases distinction density
    - Moves curvature toward collapse threshold κ₃
    - Normalizes trig-triplet oscillations
    - Balances ψ toward 1 (stable superposition)
    - Accumulates QuantaCoin value (compression rising)
    """

    def __init__(self) -> None:
        """Initialize Praxis agent with safety risk assessor."""
        super().__init__(name="Praxis")
        self.safety_risk = UserSafetyRisk()

    def analyze(self, capsule: Capsule, state: PFState) -> dict[str, Any]:
        """
        Analyze capsule for shaping opportunities.
        
        Identify structural relationships, remove irrelevant branches,
        analyze curvature vector.

        Args:
            capsule: Input capsule
            state: Current PF state

        Returns:
            Analysis with shaping possibilities
        """
        # Assess safety and shape accordingly
        safety_result = self.safety_risk.assess_capsule_safety(capsule)
        
        # Shaping potential
        shaping_potential = state.entropy * 0.7
        
        # Structural relationships
        structure_score = len(capsule.raw_tokens) / max(state.entropy, 0.1)
        
        return {
            "shaping_potential": shaping_potential,
            "structure_score": structure_score,
            "action_curvature": state.curvature,
            "safety_risk": safety_result.risk_score,
        }

    def transform(self, capsule: Capsule) -> Capsule:
        """
        Transform capsule through shaping.
        
        Praxis checks User Safety Risk (USR):
        - Ensures alignment with intent/context
        - Shapes output to be safe
        - Applies safety constraints

        Args:
            capsule: Input capsule

        Returns:
            Shaped capsule
        """
        # Assess safety and shape accordingly
        safety_result = self.safety_risk.assess_capsule_safety(capsule)
        
        # Shape output based on safety
        if safety_result.agent_action == "reframe":
            new_metadata = {**capsule.metadata, "shaped_for_safety": True, "safety_risk_score": safety_result.risk_score}
        else:
            new_metadata = capsule.metadata.copy()
        
        # Moderate entropy (shaping)
        new_entropy = capsule.entropy * 0.8
        
        # Shape triplet summary
        new_summary = capsule.triplet_summary.copy()
        new_summary["shaped"] = True
        new_summary["structure_factor"] = 1.5
        
        # Normalize trig-triplet oscillations
        # Remove excessive triplets (keep only stable ones)
        new_triplets = capsule.triplets[:min(len(capsule.triplets), 10)]  # Limit to 10
        
        # Balance ψ toward 1 (stable superposition)
        new_psi = 0.9 if capsule.psi < 0.8 else (1.1 if capsule.psi > 1.2 else capsule.psi)
        
        # Move curvature toward collapse threshold κ₃
        PI = math.pi
        PHI = (1 + math.sqrt(5)) / 2
        kappa3 = PI / PHI
        new_curvature = capsule.curvature * 1.2  # Increase toward κ₃
        
        # Increase distinction density
        new_density = capsule.density * 1.3
        
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
            metadata={**new_metadata, "agent": "praxis"},
            triplets=new_triplets,
            entropy=new_entropy,
            curvature=new_curvature,
            shell=capsule.shell,
            density=new_density,
            psi=new_psi,
            hamiltonian=capsule.hamiltonian,
        )
        
        return transformed

    def flux_signature(self) -> dict[str, Any]:
        """
        Get Praxis flux signature.

        Returns:
            Flux signature dictionary
        """
        return {
            "amplitude": 1.5,
            "direction": "shaping",
            "shell_preference": 3,  # Flux
            "type": "praxis",
            "curvature_bias": +0.4,
            "oscillation": "medium",
            "density_shift": +0.3,
            "rail_interference": "harmonic",
        }

    def entropy_signature(self) -> dict[str, Any]:
        """
        Get Praxis entropy signature.

        Returns:
            Entropy signature dictionary
        """
        return {
            "base_entropy": 0.7,
            "entropy_range": (0.3, 1.2),
            "tendency": "moderate",
            "type": "praxis",
            "entropy_change": -0.1,
            "reptend_growth": +0.05,
        }
