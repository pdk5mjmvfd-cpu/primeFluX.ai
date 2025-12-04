"""
Experience Layer — orchestrator for experience processing.

This is the middle layer between:
- LCM (brain)
- Repo Memory (identity)

It allows Apop to:
- Build experiences
- Form habits
- Generate shortcuts
- Refine flux operators
- Learn internal tools
- Construct object-models
- Maintain identity continuity per user
"""

from __future__ import annotations

from typing import Any
from pathlib import Path
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.combinatoric.interpreter import CombinatoricDistinctionPacket
from ApopToSiS.core.quanta import QuantaCompressor
from .habits.habits import HabitManager
from .shortcuts.shortcuts import ShortcutManager
from .objects.object_memory import ObjectMemory
from .skills.skills import SkillManager
from .pattern_recognition.pattern_recognition import (
    detect_repetition,
    detect_triplet_pattern,
    detect_flux_pattern,
)
from .experience_graph import ExperienceGraph


class ExperienceLayer:
    """
    Experience Layer orchestrator.
    
    Processes capsules and extracts patterns to build experience.
    """

    def __init__(self, repo_path: str = ".") -> None:
        """
        Initialize ExperienceLayer.

        Args:
            repo_path: Path to repository
        """
        self.repo_path = Path(repo_path)
        self.habits = HabitManager(repo_path)
        self.shortcuts = ShortcutManager(repo_path)
        self.objects = ObjectMemory(repo_path)
        self.skills = SkillManager(
            repo_path,
            habit_manager=self.habits,
            shortcut_manager=self.shortcuts,
            object_memory=self.objects
        )
        self.graph = ExperienceGraph(repo_path)
        self.compressor = QuantaCompressor()

    def process_capsule(
        self,
        capsule: Capsule,
        combinatoric_packet: CombinatoricDistinctionPacket | None = None
    ) -> dict[str, Any]:
        """
        Process a capsule through the experience layer.

        1. Extract distinction patterns from capsule
        2. Update habits
        3. Update shortcuts
        4. Update object memory
        5. Update skills
        6. Compress and hash via QuantaCoin
        7. Commit updated structures back to repo

        Args:
            capsule: Capsule to process
            combinatoric_packet: Optional combinatoric packet

        Returns:
            Dictionary with experience updates
        """
        # 1. Extract patterns
        patterns = self._extract_patterns(capsule, combinatoric_packet)
        
        # 2. Update habits
        self.update_habits(patterns)
        
        # 3. Update shortcuts
        if combinatoric_packet:
            self.update_shortcuts(combinatoric_packet)
        
        # 4. Update object memory
        if combinatoric_packet:
            self.update_objects(combinatoric_packet)
        
        # 5. Update skills
        self.update_skills(patterns)
        
        # 6. Integrate curvature
        self.integrate_curvature(capsule)
        
        # 7. Compress and hash
        capsule_dict = capsule.to_dict()
        compressed = self.compressor.compress_capsule(capsule_dict)
        hash_value = self.compressor.hash_capsule(capsule_dict)
        
        # 8. Save to repo
        self.save_to_repo()
        
        return {
            "habits_updated": len(self.habits.habits),
            "shortcuts_updated": len(self.shortcuts.shortcuts),
            "objects_updated": len(self.objects.objects),
            "skills_updated": len(self.skills.skills),
            "compression_ratio": compressed.compression_ratio,
            "hash": hash_value,
        }

    def _extract_patterns(
        self,
        capsule: Capsule,
        combinatoric_packet: CombinatoricDistinctionPacket | None
    ) -> dict[str, Any]:
        """
        Extract distinction patterns from capsule.

        Args:
            capsule: Capsule
            combinatoric_packet: Optional combinatoric packet

        Returns:
            Dictionary of patterns
        """
        patterns = {}
        
        # Extract shell transitions
        if combinatoric_packet:
            patterns["shell_sequence"] = combinatoric_packet.shell_suggestions
            patterns["triplets"] = combinatoric_packet.triplets
            patterns["adjacency_pairs"] = combinatoric_packet.adjacency_pairs
        
        # Extract from capsule
        patterns["entropy"] = capsule.entropy_snapshot
        patterns["curvature"] = capsule.curvature_snapshot
        patterns["error"] = capsule.measurement_error
        
        return patterns

    def update_habits(self, patterns: dict[str, Any]) -> None:
        """
        Update habits from patterns.

        Args:
            patterns: Extracted patterns
        """
        # Record shell transition patterns
        if "shell_sequence" in patterns:
            shell_seq = patterns["shell_sequence"]
            for i in range(len(shell_seq) - 1):
                transition = (shell_seq[i], shell_seq[i + 1])
                self.habits.record_pattern(
                    transition,
                    entropy=patterns.get("entropy"),
                    curvature=patterns.get("curvature")
                )
        
        # Record triplet patterns
        if "triplets" in patterns:
            for triplet in patterns["triplets"][:5]:  # Limit to recent
                self.habits.record_pattern(
                    triplet,
                    entropy=patterns.get("entropy"),
                    curvature=patterns.get("curvature")
                )
        
        # Stabilize habits
        self.habits.stabilize()

    def update_shortcuts(self, packet: CombinatoricDistinctionPacket) -> None:
        """
        Update shortcuts from combinatoric packet.

        Args:
            packet: CombinatoricDistinctionPacket
        """
        shell_sequence = packet.shell_suggestions
        
        if len(shell_sequence) >= 2:
            # Detect shortcut
            shortcut = self.shortcuts.detect_shortcut(
                shell_sequence,
                entropy_history=[packet.entropy_delta],
                curvature_history=packet.curvature_deltas,
                error_history=packet.error_deltas
            )
            
            if shortcut:
                # Shortcut detected and stored
                pass

    def update_objects(self, packet: CombinatoricDistinctionPacket) -> None:
        """
        Update object memory from combinatoric packet.

        Args:
            packet: CombinatoricDistinctionPacket
        """
        self.objects.update_from_combinatorics(packet)

    def update_skills(self, patterns: dict[str, Any]) -> None:
        """
        Update skills from patterns.

        Args:
            patterns: Extracted patterns
        """
        # Create sequence from patterns
        sequence = []
        
        if "shell_sequence" in patterns:
            for shell in patterns["shell_sequence"]:
                sequence.append({"type": "shell", "value": shell})
        
        if sequence:
            # Get habit/shortcut/object signatures used
            habits_used = []
            shortcuts_used = []
            objects_used = []
            
            # Match habits
            if "shell_sequence" in patterns:
                shell_seq = patterns["shell_sequence"]
                for i in range(len(shell_seq) - 1):
                    transition = (shell_seq[i], shell_seq[i + 1])
                    habit_strength = self.habits.get_habit_strength(transition)
                    if habit_strength > 0.5:
                        habit_sig = self.habits._pattern_signature(transition)
                        habits_used.append(habit_sig)
            
            # Update skill
            self.skills.update_skills(
                sequence,
                habits=habits_used,
                shortcuts=shortcuts_used,
                objects=objects_used,
                success=True
            )

    def integrate_curvature(self, capsule: Capsule) -> None:
        """
        Integrate curvature from capsule.

        Args:
            capsule: Capsule with curvature data
        """
        # Update graph with curvature information
        curvature = capsule.curvature_snapshot
        entropy = capsule.entropy_snapshot
        error = capsule.measurement_error
        
        # Add curvature node
        self.graph.add_node(
            f"curvature_{len(self.graph.nodes)}",
            "curvature",
            {"value": curvature, "entropy": entropy, "error": error}
        )

    def save_to_repo(self) -> None:
        """
        Save all experience data to repository.
        """
        # Save individual components
        self.habits.save_to_repo()
        self.shortcuts.save_to_repo()
        self.objects.save_to_repo()
        self.skills.save_to_repo()
        
        # Update and save graph
        self.graph.update_from_experience(
            {sig: h.to_dict() for sig, h in self.habits.habits.items()},
            {sig: s.to_dict() for sig, s in self.shortcuts.shortcuts.items()},
            {sig: o.to_dict() for sig, o in self.objects.objects.items()},
            {sig: s.to_dict() for sig, s in self.skills.skills.items()},
        )
        self.graph.save_to_repo()

