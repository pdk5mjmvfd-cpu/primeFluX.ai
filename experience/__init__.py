"""
Experience Layer — Apop's learning and identity continuity system.

Allows Apop to:
- Build experiences
- Form habits
- Generate shortcuts
- Refine flux operators
- Learn internal tools
- Construct object-models
- Maintain identity continuity per user
"""

from .experience_layer import ExperienceLayer
from .habits import HabitManager
from .shortcuts import ShortcutManager
from .objects.object_memory import ObjectMemory
from .skills import SkillManager
from .pattern_recognition import (
    detect_repetition,
    detect_triplet_pattern,
    detect_flux_pattern,
    detect_entropy_trend,
    detect_curvature_pattern,
)
from .experience_graph import ExperienceGraph

__all__ = [
    "ExperienceLayer",
    "HabitManager",
    "ShortcutManager",
    "ObjectMemory",
    "SkillManager",
    "detect_repetition",
    "detect_triplet_pattern",
    "detect_flux_pattern",
    "detect_entropy_trend",
    "detect_curvature_pattern",
    "ExperienceGraph",
]

