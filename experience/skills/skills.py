"""
Skills — persistent multi-step patterns that Apop can execute automatically.

Skills are larger than shortcuts.
Examples: "Summarizing," "Planning," "Fixing code," etc.

Skill = combination of habits + shortcuts + object interactions.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from collections import Counter


@dataclass
class Skill:
    """
    A skill = multi-step pattern.
    
    Skill = combination of:
    - habits
    - shortcuts
    - object interactions
    """
    signature: str  # SHA256 hash of sequence
    sequence: list[dict[str, Any]] = field(default_factory=list)
    habits_used: list[str] = field(default_factory=list)  # Habit signatures
    shortcuts_used: list[str] = field(default_factory=list)  # Shortcut signatures
    objects_used: list[str] = field(default_factory=list)  # Object signatures
    count: int = 1
    success_rate: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert skill to dictionary."""
        return {
            "signature": self.signature,
            "sequence": self.sequence,
            "habits_used": self.habits_used,
            "shortcuts_used": self.shortcuts_used,
            "objects_used": self.objects_used,
            "count": self.count,
            "success_rate": self.success_rate,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Skill":
        """Create skill from dictionary."""
        return cls(
            signature=data["signature"],
            sequence=data.get("sequence", []),
            habits_used=data.get("habits_used", []),
            shortcuts_used=data.get("shortcuts_used", []),
            objects_used=data.get("objects_used", []),
            count=data.get("count", 1),
            success_rate=data.get("success_rate", 1.0),
            metadata=data.get("metadata", {}),
        )


class SkillManager:
    """
    Manages skills (multi-step patterns).
    
    Skills are larger than shortcuts and combine habits, shortcuts, and objects.
    """

    def __init__(
        self,
        repo_path: str = ".",
        habit_manager: Any = None,
        shortcut_manager: Any = None,
        object_memory: Any = None
    ) -> None:
        """
        Initialize SkillManager.

        Args:
            repo_path: Path to repository
            habit_manager: Optional HabitManager instance
            shortcut_manager: Optional ShortcutManager instance
            object_memory: Optional ObjectMemory instance
        """
        self.repo_path = Path(repo_path)
        self.skills: dict[str, Skill] = {}
        self.habit_manager = habit_manager
        self.shortcut_manager = shortcut_manager
        self.object_memory = object_memory
        self._load_skills()

    def _sequence_signature(self, sequence: list[dict[str, Any]]) -> str:
        """
        Generate signature for a sequence.

        Args:
            sequence: Sequence of steps

        Returns:
            SHA256 hash signature
        """
        sequence_str = str(sequence).encode('utf-8')
        return hashlib.sha256(sequence_str).hexdigest()

    def update_skills(
        self,
        sequence: list[dict[str, Any]],
        habits: list[str] | None = None,
        shortcuts: list[str] | None = None,
        objects: list[str] | None = None,
        success: bool = True
    ) -> Skill:
        """
        Update skills from a sequence.

        Args:
            sequence: Sequence of steps
            habits: Optional list of habit signatures used
            shortcuts: Optional list of shortcut signatures used
            objects: Optional list of object signatures used
            success: Whether sequence was successful

        Returns:
            Updated or created Skill
        """
        signature = self._sequence_signature(sequence)
        
        if signature in self.skills:
            # Update existing skill
            skill = self.skills[signature]
            skill.count += 1
            
            # Update success rate
            total = skill.count
            current_successes = skill.success_rate * (total - 1)
            if success:
                current_successes += 1
            skill.success_rate = current_successes / total
            
            # Update components
            if habits:
                skill.habits_used.extend(habits)
                skill.habits_used = list(set(skill.habits_used))
            
            if shortcuts:
                skill.shortcuts_used.extend(shortcuts)
                skill.shortcuts_used = list(set(skill.shortcuts_used))
            
            if objects:
                skill.objects_used.extend(objects)
                skill.objects_used = list(set(skill.objects_used))
        else:
            # Create new skill
            skill = Skill(
                signature=signature,
                sequence=sequence,
                habits_used=habits or [],
                shortcuts_used=shortcuts or [],
                objects_used=objects or [],
                success_rate=1.0 if success else 0.0,
            )
            self.skills[signature] = skill
        
        return skill

    def match_skill(self, packet: Any) -> Skill | None:
        """
        Match a skill to a combinatoric packet.

        Args:
            packet: CombinatoricDistinctionPacket or similar

        Returns:
            Matched skill if found, None otherwise
        """
        # TODO: Implement skill matching logic
        # For now, return most used skill
        if not self.skills:
            return None
        
        most_used = max(self.skills.values(), key=lambda s: s.count)
        return most_used

    def apply_skill(self, state: Any, skill: Skill) -> Any:
        """
        Apply a skill to a state.

        Args:
            state: Current state
            skill: Skill to apply

        Returns:
            New state after skill application
        """
        # TODO: Implement skill application
        # For now, return state with metadata
        if hasattr(state, 'metadata'):
            state.metadata["skill_applied"] = skill.signature
            state.metadata["skill_count"] = skill.count
            state.metadata["skill_success_rate"] = skill.success_rate
        
        return state

    def save_to_repo(self) -> None:
        """
        Save skills to repository.
        """
        skills_dir = self.repo_path / "experience"
        skills_dir.mkdir(parents=True, exist_ok=True)
        
        skills_file = skills_dir / "skills.json"
        
        skills_data = {
            sig: skill.to_dict()
            for sig, skill in self.skills.items()
        }
        
        with open(skills_file, 'w') as f:
            json.dump(skills_data, f, indent=2)

    def _load_skills(self) -> None:
        """
        Load skills from repository.
        """
        skills_file = self.repo_path / "experience" / "skills.json"
        
        if not skills_file.exists():
            return
        
        try:
            with open(skills_file, 'r') as f:
                skills_data = json.load(f)
            
            for signature, data in skills_data.items():
                self.skills[signature] = Skill.from_dict(data)
        except Exception as e:
            print(f"Error loading skills: {e}")
    
    def update_from_capsule(self, capsule: Any, state: Any) -> None:
        """
        Update skills from capsule and state.
        
        PF Logic: Skills are "stable curvature transformations" learned over time.
        
        Args:
            capsule: Capsule
            state: PF state
        """
        if not hasattr(capsule, 'triplets'):
            return
        
        # Create sequence from triplets
        sequence = []
        for triplet in capsule.triplets:
            if isinstance(triplet, dict):
                sequence.append({
                    "type": triplet.get("type", "unknown"),
                    "a": triplet.get("a", 0.0),
                    "b": triplet.get("b", 0.0),
                    "c": triplet.get("c", 0.0),
                })
        
        if sequence:
            # Update skill
            self.update_skills(
                sequence,
                success=True
            )
    
    def summary(self) -> dict[str, Any]:
        """
        Get skills summary.
        
        Returns:
            Dictionary of skill signatures -> data
        """
        return {
            sig: skill.to_dict()
            for sig, skill in self.skills.items()
        }

