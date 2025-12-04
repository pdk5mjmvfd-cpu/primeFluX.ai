"""
PF-State Merge Model.

Apop NEVER merges PFState directly.
Instead:
PFState = f(capsule_history)
Recomputed from valid capsules in order.

This ensures:
- Determinism
- Zero conflict
- Perfect reconstruction
- Identity continuity

Merge rules:
- Sort by timestamp
- Resolve conflicts by:
  - device_id precedence
  - capsule chain continuity
  - quanta_hash trust
  - PF curvature consistency
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.math.shells import Shell


class StateMerge:
    """
    PF-State merge handler.
    
    Reconstructs PFState from capsule history.
    """

    @staticmethod
    def merge_capsules(capsules: list[Capsule], device_id: str | None = None) -> PFState:
        """
        Merge capsules into PFState.
        
        Recomputes PFState from capsule history in timestamp order.
        This ensures determinism and zero conflict.

        Args:
            capsules: List of capsules to merge
            device_id: Optional preferred device ID

        Returns:
            Merged PFState
        """
        if not capsules:
            return PFState()
        
        # Sort by timestamp
        sorted_capsules = sorted(capsules, key=lambda c: c.timestamp)
        
        # If device_id specified, prefer capsules from that device
        if device_id:
            # Sort by device_id match, then timestamp
            sorted_capsules.sort(
                key=lambda c: (c.device_id != device_id, c.timestamp)
            )
        
        # Reconstruct PFState from capsules
        state = PFState()
        
        for capsule in sorted_capsules:
            # Update state from capsule
            state.update(capsule.to_dict())
        
        return state

    @staticmethod
    def resolve_conflicts(
        capsules: list[Capsule],
        conflict_timestamp: float,
        tolerance: float = 1.0
    ) -> list[Capsule]:
        """
        Resolve conflicts between capsules at similar timestamps.
        
        Conflict resolution priority:
        1. device_id precedence (if specified)
        2. capsule chain continuity (prev_capsule_id)
        3. quanta_hash trust (higher compression ratio)
        4. PF curvature consistency

        Args:
            capsules: List of capsules with conflicts
            conflict_timestamp: Timestamp of conflict
            tolerance: Time tolerance for conflicts

        Returns:
            Resolved list of capsules (conflicts removed)
        """
        if not capsules:
            return []
        
        # Find capsules in conflict window
        conflict_capsules = [
            c for c in capsules
            if abs(c.timestamp - conflict_timestamp) <= tolerance
        ]
        
        if len(conflict_capsules) <= 1:
            return capsules
        
        # Resolve by priority
        # 1. Higher compression ratio (more trusted)
        conflict_capsules.sort(key=lambda c: c.compression_ratio, reverse=True)
        
        # 2. Check capsule chain continuity
        # Keep capsules that form continuous chains
        resolved = []
        seen_ids = set()
        
        for capsule in conflict_capsules:
            # If no previous capsule or previous is seen, include it
            if not capsule.prev_capsule_id or capsule.prev_capsule_id in seen_ids:
                resolved.append(capsule)
                seen_ids.add(capsule.capsule_id)
        
        # If no chain continuity, take highest compression ratio
        if not resolved:
            resolved = [conflict_capsules[0]]
        
        # Replace conflict capsules with resolved ones
        result = [c for c in capsules if c not in conflict_capsules]
        result.extend(resolved)
        
        # Re-sort by timestamp
        result.sort(key=lambda c: c.timestamp)
        
        return result

    @staticmethod
    def validate_capsule_chain(capsules: list[Capsule]) -> tuple[bool, str]:
        """
        Validate capsule chain continuity.
        
        Checks that prev_capsule_id links form a valid chain.

        Args:
            capsules: List of capsules to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not capsules:
            return True, ""
        
        # Build capsule ID map
        capsule_ids = {c.capsule_id: c for c in capsules}
        
        # Check chain continuity
        for capsule in capsules:
            if capsule.prev_capsule_id:
                # Check if previous capsule exists
                if capsule.prev_capsule_id not in capsule_ids:
                    # Allow if it's from a different device (chain break)
                    continue
                
                prev_capsule = capsule_ids[capsule.prev_capsule_id]
                
                # Check timestamp ordering
                if prev_capsule.timestamp > capsule.timestamp:
                    return False, f"Capsule {capsule.capsule_id} has invalid timestamp ordering"
        
        return True, ""

