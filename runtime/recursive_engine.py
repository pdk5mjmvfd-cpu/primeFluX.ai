"""
Recursive Learning Engine (RLE)

ApopToSiS v3 — PrimeFlux Cognitive Runtime

The RLE is responsible for:
- Capsule-driven recursive learning cycles
- Updating embeddings, concept lattice, and identity fields
- Reinforcing or attenuating experience
- Establishing cross-capsule continuity (proto-self)
"""

from __future__ import annotations

from typing import Any, Optional
import uuid
import time
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.experience_state import ExperienceState


class RecursiveLearningEngine:
    """
    Recursive Learning Engine (RLE).
    
    Handles capsule-driven recursive learning cycles,
    updating embeddings, concept lattice, and identity fields.
    """

    def __init__(
        self,
        experience_layer: Any,
        concept_lattice: Any,
        identity_core: Any,
        experience_state: ExperienceState | None = None,
    ) -> None:
        """
        Initialize RLE.
        
        Args:
            experience_layer: Experience layer instance
            concept_lattice: Concept lattice instance
            identity_core: Identity core instance
        """
        self.experience_layer = experience_layer
        self.concept_lattice = concept_lattice
        self.identity_core = identity_core
        self.experience_state = experience_state or ExperienceState()

    def process(
        self,
        capsule: Capsule | dict[str, Any],
        pfstate: PFState
    ) -> dict[str, Any]:
        """
        Main recursive update loop.
        
        Args:
            capsule: PF capsule (Capsule object or dict)
            pfstate: Current PF state
            
        Returns:
            Learning report dictionary
        """
        # Convert capsule to dict if needed
        if isinstance(capsule, Capsule):
            capsule_dict = capsule.to_dict()
        else:
            capsule_dict = capsule
        
        # 1. Update concept lattice with capsule content
        self.concept_lattice.update_from_capsule(
            capsule_dict.get("raw_tokens", []),
            capsule_dict.get("entropy", 0.0),
            capsule_dict.get("curvature", 0.0)
        )
        
        # 2. Experience layer reinforcement
        delta = {}
        if hasattr(self.experience_layer, 'update_from_capsule'):
            delta = self.experience_layer.update_from_capsule(capsule_dict)
        elif hasattr(self.experience_layer, 'update'):
            # Fallback to standard update method
            if isinstance(capsule, Capsule):
                self.experience_layer.update(capsule, pfstate)
            delta = {"updated": True}
        
        # 3. Identity drift update
        self.identity_core.update(
            curvature=capsule_dict.get("curvature", 0.0),
            entropy=capsule_dict.get("entropy", 0.0),
            density=capsule_dict.get("density", 0.0)
        )
        
        # 4. Return a learning report
        return {
            "recursive_id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "experience_delta": delta,
            "identity_snapshot": self.identity_core.export(),
            "lattice_snapshot": self.concept_lattice.summary()
        }

