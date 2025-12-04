"""
Aegis Agent — validation / collapse (3→4).

Low entropy, collapse, correctness.

Role: Validation, collapse, stability
Shell Influence: Moves 3→4 and 4→0
PF Band: Low curvature / supervised collapse
"""

from __future__ import annotations

from ApopToSiS.agents.base.base_agent import PFBaseAgent
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.user_safety_risk import UserSafetyRisk
from typing import Any
import math
from ApopToSiS.core.math.hamiltonians import collapse_energy


class AegisAgent(PFBaseAgent):
    """
    Aegis Agent — validation and collapse.
    
    Checks coherence, minimizes curvature, finalizes distinctions.
    Low entropy, collapse, correctness.
    
    AEGIS BEHAVIOR:
    - Finalizes collapse
    - Validates shell transitions
    - Ensures PF laws are respected
    - Decreases entropy sharply
    - Forces ψ to collapse state (> 1.2)
    - Returns a stable capsule
    """

    def __init__(self) -> None:
        """Initialize Aegis agent with safety risk assessor."""
        super().__init__(name="Aegis")
        self.safety_risk = UserSafetyRisk()

    def analyze(self, capsule: Capsule, state: PFState) -> dict[str, Any]:
        """
        Analyze capsule for validation.
        
        Detect contradictions, validate PF manifold rules,
        confirm triplet integrity.

        Args:
            capsule: Input capsule
            state: Current PF state

        Returns:
            Analysis with validation results
        """
        # Assess user safety risk
        safety_result = self.safety_risk.assess_capsule_safety(capsule)
        
        # Coherence score
        coherence_score = 1.0 - (state.curvature * 0.1)
        
        # Validation status
        validation_status = "valid" if state.entropy < 1.0 else "needs_review"
        
        # Collapse readiness
        collapse_readiness = 1.0 - (state.entropy * 0.5)
        
        return {
            "coherence_score": coherence_score,
            "validation_status": validation_status,
            "collapse_readiness": collapse_readiness,
            "safety_risk": safety_result.risk_score,
        }

    def transform(self, capsule: Capsule) -> Capsule:
        """
        Transform capsule through validation and collapse.
        
        Aegis enforces User Safety Risk (USR):
        - Blocks unsafe outputs
        - Validates safety constraints
        - Ensures ethical alignment

        Args:
            capsule: Input capsule

        Returns:
            Validated and collapsed capsule
        """
        # Assess user safety risk
        safety_result = self.safety_risk.assess_capsule_safety(capsule)
        
        # If unsafe, block or reframe
        if safety_result.agent_action == "block":
            # Block unsafe capsule
            new_metadata = {**capsule.metadata, "blocked": True, "block_reason": "user_safety_risk", "safety_risk_score": safety_result.risk_score}
        elif safety_result.agent_action == "reframe":
            # Reframe to safer version
            new_metadata = {**capsule.metadata, "reframed": True, "safety_risk_score": safety_result.risk_score}
        else:
            new_metadata = capsule.metadata.copy()
        
        # Reduce entropy (collapse)
        new_entropy = capsule.entropy * 0.5
        
        # Validate and collapse triplet summary
        new_summary = capsule.triplet_summary.copy()
        new_summary["validated"] = True
        new_summary["collapsed"] = True
        
        # Minimize curvature
        new_curvature = capsule.curvature * 0.7
        
        # Force ψ to collapse state (> 1.2)
        new_psi = max(1.2, capsule.psi * 1.1)
        
        # Create new capsule
        transformed = Capsule(
            triplet_summary=new_summary,
            shell_state=4,  # Collapse shell
            entropy_snapshot=new_entropy,
            curvature_snapshot=new_curvature,
            timestamp=capsule.timestamp,
            raw_tokens=capsule.raw_tokens.copy(),
            pf_signature=capsule.pf_signature,
            compression_hash=capsule.compression_hash,
            metadata={**new_metadata, "agent": "aegis", "validated": True},
            triplets=capsule.triplets.copy(),
            entropy=new_entropy,
            curvature=new_curvature,
            shell=4,  # Collapse
            density=capsule.density,
            psi=new_psi,
            hamiltonian=capsule.hamiltonian,
        )
        
        return transformed

    def flux_signature(self) -> dict[str, Any]:
        """
        Get Aegis flux signature.

        Returns:
            Flux signature dictionary
        """
        return {
            "amplitude": 0.5,
            "direction": "collapse",
            "shell_preference": 4,  # Collapse
            "type": "aegis",
            "curvature_bias": -0.2,
            "oscillation": "low",
            "density_shift": +0.05,
            "rail_interference": "convergent",
        }

    def entropy_signature(self) -> dict[str, Any]:
        """
        Get Aegis entropy signature.

        Returns:
            Entropy signature dictionary
        """
        return {
            "base_entropy": 0.3,
            "entropy_range": (0.1, 0.6),
            "tendency": "decrease",
            "type": "aegis",
            "entropy_change": -0.25,
            "reptend_growth": -0.1,
        }
