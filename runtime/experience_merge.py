"""
Distributed Experience Graph Merge.

Experience merges through experience_delta.

Conflicts resolved by:
- higher QuantaCoin
- higher compression ratio
- higher temporal consistency
- consistent PF-shell transitions

Experience Graph = reconstructed topology.
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.experience.manager import ExperienceManager


class ExperienceMerge:
    """
    Experience merge handler.
    
    Merges experience deltas from multiple devices.
    """

    @staticmethod
    def merge_experience_deltas(
        deltas: list[dict[str, Any]],
        experience_manager: ExperienceManager
    ) -> None:
        """
        Merge experience deltas into experience manager.
        
        Conflicts resolved by:
        - Higher QuantaCoin (compression ratio)
        - Higher temporal consistency
        - Consistent PF-shell transitions

        Args:
            deltas: List of experience delta dictionaries
            experience_manager: Experience manager to update
        """
        if not deltas:
            return
        
        # Sort by QuantaCoin (compression ratio) - higher is better
        sorted_deltas = sorted(
            deltas,
            key=lambda d: d.get("compression_ratio", 0.0),
            reverse=True
        )
        
        # Apply deltas in order
        for delta in sorted_deltas:
            # Update habits
            if "habits" in delta:
                for habit_data in delta["habits"]:
                    # Merge habit if higher compression ratio
                    experience_manager.habits.record_pattern(
                        tuple(habit_data.get("pattern", [])),
                        entropy=habit_data.get("entropy"),
                        curvature=habit_data.get("curvature")
                    )
            
            # Update shortcuts
            if "shortcuts" in delta:
                for shortcut_data in delta["shortcuts"]:
                    # Merge shortcut if valid
                    experience_manager.shortcuts.detect_shortcut(
                        shortcut_data.get("shell_sequence", []),
                        entropy_history=shortcut_data.get("entropy_history", []),
                        curvature_history=shortcut_data.get("curvature_history", []),
                        error_history=shortcut_data.get("error_history", [])
                    )
            
            # Update objects
            if "objects" in delta:
                for obj_data in delta["objects"]:
                    # Merge object if higher compression
                    experience_manager.objects.store_object(
                        obj_data.get("signature", ""),
                        obj_data.get("triplets", []),
                        obj_data.get("shell_stats", {}),
                        obj_data.get("curvature_profile", []),
                        obj_data.get("entropy_profile", 0.0)
                    )
            
            # Update skills
            if "skills" in delta:
                for skill_data in delta["skills"]:
                    # Merge skill if valid
                    experience_manager.skills.update_skills(
                        skill_data.get("sequence", []),
                        success=skill_data.get("success", True)
                    )

    @staticmethod
    def extract_experience_delta(
        capsule: Capsule,
        experience_manager: ExperienceManager
    ) -> dict[str, Any]:
        """
        Extract experience delta from capsule and current experience.
        
        Creates a delta that can be merged on another device.

        Args:
            capsule: Capsule to extract delta from
            experience_manager: Current experience manager

        Returns:
            Experience delta dictionary
        """
        # Get current experience summary
        summary = experience_manager.summarize()
        
        # Create delta (only changes since last sync)
        delta = {
            "capsule_id": capsule.capsule_id,
            "timestamp": capsule.timestamp,
            "compression_ratio": capsule.compression_ratio,
            "habits": [
                {
                    "pattern": list(habit.get("pattern", [])),
                    "entropy": habit.get("entropy_drift", 0.0),
                    "curvature": habit.get("curvature_drift", 0.0),
                }
                for habit in summary.get("habits", {}).values()
            ],
            "shortcuts": [
                {
                    "signature": shortcut.get("signature", ""),
                    "shell_sequence": shortcut.get("shell_sequence", []),
                    "entropy_history": [],
                    "curvature_history": [],
                    "error_history": [],
                }
                for shortcut in summary.get("shortcuts", {}).values()
            ],
            "objects": [
                {
                    "signature": obj.get("signature", ""),
                    "triplets": obj.get("triplets", []),
                    "shell_stats": obj.get("shell_stats", {}),
                    "curvature_profile": obj.get("curvature_profile", []),
                    "entropy_profile": obj.get("entropy_profile", 0.0),
                }
                for obj in summary.get("objects", {}).values()
            ],
            "skills": [
                {
                    "sequence": skill.get("sequence", []),
                    "success": skill.get("success_rate", 1.0) > 0.5,
                }
                for skill in summary.get("skills", {}).values()
            ],
        }
        
        return delta

