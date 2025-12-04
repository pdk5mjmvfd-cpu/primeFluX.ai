"""
Experience Manager — orchestrates all experience subsystems.

The Experience Layer is where Apop builds:
- habits
- shortcuts
- object memories
- skills
- user-specific preferences
- PF distinction continuity
- PF curvature reinforcement
- internal experience-graphs
- conceptual schemas
- manifold-level identity
"""

from __future__ import annotations

from typing import Any
from .habits.habits import HabitManager
from .shortcuts.shortcuts import ShortcutManager
from .objects.object_memory import ObjectMemory
from .skills.skills import SkillManager
from .pattern_recognition.pattern_recognition import (
    detect_repetition,
    detect_triplet_pattern,
    detect_flux_pattern,
    detect_entropy_trend,
    detect_curvature_pattern,
)
from .experience_graph.experience_graph import ExperienceGraph
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState


class ExperienceManager:
    """
    Experience Manager — orchestrates all experience subsystems.
    
    Updates after every Supervisor step.
    """

    def __init__(self, repo_path: str = ".") -> None:
        """
        Initialize Experience Manager.

        Args:
            repo_path: Path to repository
        """
        self.habits = HabitManager(repo_path=repo_path)
        self.shortcuts = ShortcutManager(repo_path=repo_path)
        self.objects = ObjectMemory(repo_path=repo_path)
        self.skills = SkillManager(
            repo_path=repo_path,
            habit_manager=self.habits,
            shortcut_manager=self.shortcuts,
            object_memory=self.objects
        )
        self.patterns = None  # Pattern recognition is functional
        self.graph = ExperienceGraph(repo_path=repo_path)
        # Lightweight reinforcement trackers (per Patch 007B spec)
        self.habit_counts: dict[str, int] = {}
        self.shortcut_counts: dict[tuple[str, str], int] = {}
        self.object_counts: dict[str, int] = {}
        # Back-compat aliases
        self.habit_signals = self.habit_counts
        self.shortcut_signals = self.shortcut_counts
        self.object_signals = self.object_counts
        self._last_state: PFState | None = None

    def update(self, capsule: Capsule, state: PFState) -> None:
        """
        Update all experience subsystems from capsule.
        
        All experience subsystems learn from capsule.

        Args:
            capsule: Capsule to learn from
            state: Current PF state
        """
        # Update habits
        self.habits.update_from_capsule(capsule, state)
        
        # Update shortcuts
        self.shortcuts.update_from_capsule(capsule, state)
        
        # Update object memory
        self.objects.update_from_capsule(capsule, state)
        
        # Update skills
        self.skills.update_from_capsule(capsule, state)
        
        # Update experience graph
        self.graph.update_from_capsule(capsule, state)

    def attach_state(self, state: PFState) -> None:
        """Attach a PF state reference for autonomous updates."""
        self._last_state = state

    def update_from_capsule(
        self,
        capsule: Capsule,
        state: PFState | None = None
    ) -> dict[str, int]:
        """
        Lightweight update used for reinforcement summaries.
        
        Args:
            capsule: Capsule to learn from
            state: Optional PF state
        
        Returns:
            Dictionary with habit/shortcut/object sizes
        """
        if state is not None:
            self._last_state = state
        active_state = state or self._last_state
        if active_state is not None:
            self.update(capsule, active_state)

        tokens = getattr(capsule, "raw_tokens", []) or []

        for token in tokens:
            self.habit_counts[token] = self.habit_counts.get(token, 0) + 1

        if len(tokens) >= 2:
            pair = (tokens[0], tokens[-1])
            self.shortcut_counts[pair] = self.shortcut_counts.get(pair, 0) + 1

        if len(tokens) > 3:
            obj = " ".join(tokens[:3])
            self.object_counts[obj] = self.object_counts.get(obj, 0) + 1

        summary = {
            "habits_size": len(self.habit_counts),
            "shortcuts_size": len(self.shortcut_counts),
            "objects_size": len(self.object_counts),
        }

        return summary

    def summarize(self) -> dict[str, Any]:
        """
        Get summary of all experience subsystems.

        Returns:
            Dictionary with summaries
        """
        return {
            "habits": self.habits.summary(),
            "shortcuts": self.shortcuts.summary(),
            "objects": self.objects.summary(),
            "skills": self.skills.summary(),
            "experience_graph": self.graph.summary(),
        }
    
    def get_experience_factor(self) -> float:
        """
        Compute experience factor for routing.
        
        experience_factor = (
            habit_strength
          + shortcut_density
          + object_stability
          + skill_curvature
          + graph_connectivity
        )
        
        Returns:
            Experience factor
        """
        # Habit strength
        habits_summary = self.habits.summary()
        habit_strength = sum(habits_summary.values()) / max(len(habits_summary), 1)
        
        # Shortcut density
        shortcuts_summary = self.shortcuts.summary()
        shortcut_density = len(shortcuts_summary) / 10.0  # Normalize
        
        # Object stability
        objects_summary = self.objects.summary()
        object_stability = sum(obj.get("count", 0) for obj in objects_summary.values()) / max(len(objects_summary), 1)
        
        # Skill curvature
        skills_summary = self.skills.summary()
        skill_curvature = sum(skill.get("curvature", 0.0) for skill in skills_summary.values()) / max(len(skills_summary), 1)
        
        # Graph connectivity
        graph_summary = self.graph.summary()
        graph_connectivity = len(graph_summary.get("edges", [])) / 10.0  # Normalize
        
        # Combined experience factor
        experience_factor = (
            habit_strength * 0.2 +
            shortcut_density * 0.2 +
            object_stability * 0.2 +
            skill_curvature * 0.2 +
            graph_connectivity * 0.2
        )
        
        return experience_factor

