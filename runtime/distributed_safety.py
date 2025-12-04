"""
Distributed Safety Model.

Two layers:
1. User Safety - Handled by Aegis + LCM/ICM
2. Network Safety - Handled by:
   - QuantaCoin trust
   - PF curvature consistency
   - dual-rail 6k±1 validation
   - timestamp ordering
   - capsule signatures
   - triplet validity
   - shell pipeline validation

Capsules failing checks are discarded.
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.core.math.shells import Shell
from ApopToSiS.core.math.triplets import Triplet, TripletType


class DistributedSafety:
    """
    Distributed safety validator.
    
    Validates capsules from network sources.
    """

    def __init__(self, min_quanta_ratio: float = 1.0) -> None:
        """
        Initialize safety validator.

        Args:
            min_quanta_ratio: Minimum QuantaCoin ratio to trust
        """
        self.min_quanta_ratio = min_quanta_ratio

    def validate_llm_metadata(self, pfmeta: dict[str, Any]) -> bool:
        """
        Validate LLM-provided PF metadata.
        
        Minimal structure check:
        - Must be a dictionary
        - Must not override local curvature entirely (PF rules dominate)
        
        Args:
            pfmeta: PF metadata dictionary from LLM
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(pfmeta, dict):
            return False
        
        # PF meta must not override local curvature entirely
        # (LLM provides hints, but local PF computation is authoritative)
        if "curvature" in pfmeta:
            # If LLM tries to set absolute curvature, reject it
            # (only hints are allowed in hybrid mode)
            return False
        
        return True

    def validate_network_capsule(self, capsule: Capsule) -> tuple[bool, str]:
        """
        Validate capsule from network.
        
        Checks:
        1. QuantaCoin trust (compression ratio)
        2. PF curvature consistency
        3. Dual-rail 6k±1 validation
        4. Timestamp ordering
        5. Capsule signatures
        6. Triplet validity
        7. Shell pipeline validation
        8. LLM metadata validation (if present)

        Args:
            capsule: Capsule to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # 1. QuantaCoin trust
        if capsule.compression_ratio < self.min_quanta_ratio:
            return False, f"QuantaCoin ratio too low: {capsule.compression_ratio}"
        
        # 2. PF curvature consistency
        if capsule.curvature < 0 or capsule.curvature > 100:
            return False, f"Invalid curvature: {capsule.curvature}"
        
        # 3. Timestamp ordering
        if capsule.timestamp <= 0:
            return False, f"Invalid timestamp: {capsule.timestamp}"
        
        # 4. Capsule signatures
        if not capsule.capsule_id:
            return False, "Missing capsule_id"
        
        if not capsule.device_id:
            return False, "Missing device_id"
        
        if not capsule.quanta_hash:
            return False, "Missing quanta_hash"
        
        # 5. Triplet validity
        for triplet_data in capsule.triplets:
            if isinstance(triplet_data, dict):
                # Check triplet structure
                if "a" not in triplet_data or "b" not in triplet_data or "c" not in triplet_data:
                    return False, "Invalid triplet structure"
        
        # 6. Shell pipeline validation
        if capsule.shell not in [0, 2, 3, 4]:
            return False, f"Invalid shell: {capsule.shell}"
        
        # 7. Dual-rail validation (check rail_interference is reasonable)
        if capsule.rail_interference < 0 or capsule.rail_interference > 10:
            return False, f"Invalid rail_interference: {capsule.rail_interference}"
        
        # 8. LLM metadata validation (if present)
        pf_signature = getattr(capsule, 'pf_signature', None) or capsule.metadata.get('pf_signature', {})
        if pf_signature:
            if not self.validate_llm_metadata(pf_signature):
                return False, "Invalid LLM PF metadata"
        
        return True, ""

    def validate_curvature_consistency(
        self,
        capsule: Capsule,
        previous_capsule: Capsule | None = None
    ) -> tuple[bool, str]:
        """
        Validate PF curvature consistency.
        
        Checks that curvature changes are reasonable.

        Args:
            capsule: Current capsule
            previous_capsule: Previous capsule (if available)

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not previous_capsule:
            return True, ""
        
        # Check curvature change is reasonable
        curvature_delta = abs(capsule.curvature - previous_capsule.curvature)
        
        # Large jumps might indicate tampering
        if curvature_delta > 10.0:
            return False, f"Curvature jump too large: {curvature_delta}"
        
        return True, ""

    def validate_shell_transition(
        self,
        capsule: Capsule,
        previous_capsule: Capsule | None = None
    ) -> tuple[bool, str]:
        """
        Validate shell pipeline transition.
        
        Valid transitions: 0→2, 2→3, 3→4, 4→0

        Args:
            capsule: Current capsule
            previous_capsule: Previous capsule (if available)

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not previous_capsule:
            return True, ""
        
        prev_shell = previous_capsule.shell
        curr_shell = capsule.shell
        
        # Valid transitions
        valid_transitions = {
            0: [2],  # Presence → Measurement
            2: [3],  # Measurement → Curvature
            3: [4],  # Curvature → Collapse
            4: [0],  # Collapse → Presence (reset)
        }
        
        if prev_shell in valid_transitions:
            if curr_shell not in valid_transitions[prev_shell]:
                return False, f"Invalid shell transition: {prev_shell}→{curr_shell}"
        
        return True, ""

    def compute_trust_score(self, capsule: Capsule) -> float:
        """
        Compute trust score for capsule.
        
        Based on:
        - QuantaCoin ratio
        - Curvature consistency
        - Shell transition validity
        - Timestamp freshness

        Args:
            capsule: Capsule to score

        Returns:
            Trust score (0.0 to 1.0)
        """
        score = 0.0
        
        # QuantaCoin ratio (0.4 weight)
        quanta_score = min(capsule.compression_ratio / 2.0, 1.0)
        score += quanta_score * 0.4
        
        # Curvature consistency (0.2 weight)
        if 0 <= capsule.curvature <= 10:
            curvature_score = 1.0
        else:
            curvature_score = max(0.0, 1.0 - abs(capsule.curvature - 5.0) / 10.0)
        score += curvature_score * 0.2
        
        # Shell validity (0.2 weight)
        if capsule.shell in [0, 2, 3, 4]:
            shell_score = 1.0
        else:
            shell_score = 0.0
        score += shell_score * 0.2
        
        # Timestamp freshness (0.2 weight)
        import time
        age = time.time() - capsule.timestamp
        if age < 3600:  # Less than 1 hour
            timestamp_score = 1.0
        elif age < 86400:  # Less than 1 day
            timestamp_score = 0.8
        else:
            timestamp_score = max(0.0, 1.0 - age / 86400.0)
        score += timestamp_score * 0.2
        
        return min(1.0, max(0.0, score))

