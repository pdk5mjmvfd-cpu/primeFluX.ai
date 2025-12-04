"""
Habits — repeated distinction patterns that become predictable.

Habits are recognized by:
- Repeated shell transitions
- Repeated adjacency patterns
- Repeated triplets
- Low entropy divergence
- Repeated curvature vectors

Habits lower entropy through predictability.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from datetime import datetime


@dataclass
class Habit:
    """
    A habit = repeated distinction pattern.
    
    Habits are recognized by:
    - repeated shell transitions
    - repeated adjacency patterns
    - repeated triplets
    - low entropy divergence
    - repeated curvature vectors
    """
    pattern: tuple[Any, ...]  # Hashable pattern representation
    count: int = 1
    entropy_drift: float = 0.0
    curvature_drift: float = 0.0
    last_seen: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert habit to dictionary."""
        return {
            "pattern": str(self.pattern),  # Serialize tuple
            "count": self.count,
            "entropy_drift": self.entropy_drift,
            "curvature_drift": self.curvature_drift,
            "last_seen": self.last_seen,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Habit":
        """Create habit from dictionary."""
        # Pattern is stored as string, convert back to tuple representation
        pattern_str = data.get("pattern", "()")
        # Simple tuple reconstruction (for basic patterns)
        pattern = tuple(eval(pattern_str)) if pattern_str != "()" else tuple()
        
        return cls(
            pattern=pattern,
            count=data.get("count", 1),
            entropy_drift=data.get("entropy_drift", 0.0),
            curvature_drift=data.get("curvature_drift", 0.0),
            last_seen=data.get("last_seen", 0.0),
            metadata=data.get("metadata", {}),
        )


class HabitManager:
    """
    Manages habits (repeated distinction patterns).
    
    Habits become predictable and lower entropy.
    """

    def __init__(self, repo_path: str = ".") -> None:
        """
        Initialize HabitManager.

        Args:
            repo_path: Path to repository
        """
        self.repo_path = Path(repo_path)
        self.habits: dict[str, Habit] = {}
        self._load_habits()

    def __len__(self) -> int:
        """Return number of tracked habits."""
        return len(self.habits)

    def _pattern_signature(self, pattern: tuple[Any, ...]) -> str:
        """
        Generate signature for a pattern.

        Args:
            pattern: Pattern tuple

        Returns:
            SHA256 hash signature
        """
        pattern_str = str(pattern).encode('utf-8')
        return hashlib.sha256(pattern_str).hexdigest()

    def record_pattern(
        self,
        pattern: tuple[Any, ...],
        entropy: float | None = None,
        curvature: float | None = None
    ) -> None:
        """
        Record a distinction pattern.

        Args:
            pattern: Pattern to record
            entropy: Optional entropy value
            curvature: Optional curvature value
        """
        signature = self._pattern_signature(pattern)
        current_time = datetime.now().timestamp()
        
        if signature in self.habits:
            # Update existing habit
            habit = self.habits[signature]
            habit.count += 1
            habit.last_seen = current_time
            
            # Update drift if values provided
            if entropy is not None:
                # Compute entropy drift (change from previous)
                if "last_entropy" in habit.metadata:
                    habit.entropy_drift = abs(entropy - habit.metadata["last_entropy"])
                habit.metadata["last_entropy"] = entropy
            
            if curvature is not None:
                # Compute curvature drift
                if "last_curvature" in habit.metadata:
                    habit.curvature_drift = abs(curvature - habit.metadata["last_curvature"])
                habit.metadata["last_curvature"] = curvature
        else:
            # Create new habit
            habit = Habit(
                pattern=pattern,
                count=1,
                last_seen=current_time,
                metadata={
                    "last_entropy": entropy,
                    "last_curvature": curvature,
                }
            )
            self.habits[signature] = habit

    def get_habit_strength(self, pattern: tuple[Any, ...]) -> float:
        """
        Get habit strength (0.0 to 1.0).

        Args:
            pattern: Pattern to check

        Returns:
            Habit strength (higher = more established)
        """
        signature = self._pattern_signature(pattern)
        
        if signature not in self.habits:
            return 0.0
        
        habit = self.habits[signature]
        
        # Strength based on count and low drift
        count_factor = min(habit.count / 10.0, 1.0)  # Normalize to [0, 1]
        drift_factor = 1.0 - min(habit.entropy_drift + habit.curvature_drift, 1.0)
        
        strength = (count_factor + drift_factor) / 2.0
        
        return max(0.0, min(1.0, strength))

    def stabilize(self) -> None:
        """
        Stabilize habits (remove weak ones, strengthen strong ones).
        """
        # Remove habits with low count and high drift
        to_remove = []
        for signature, habit in self.habits.items():
            if habit.count < 2 and (habit.entropy_drift > 0.5 or habit.curvature_drift > 0.5):
                to_remove.append(signature)
        
        for signature in to_remove:
            del self.habits[signature]
    
    def update_from_capsule(self, capsule: Any, state: Any) -> None:
        """
        Update habits from capsule and state.
        
        PF Logic: A habit strengthens when the PF distinction density is high.
        Density = stability.
        
        Args:
            capsule: Capsule
            state: PF state
        """
        # Extract pattern from capsule
        pattern = tuple(capsule.raw_tokens[:5]) if hasattr(capsule, 'raw_tokens') else tuple()
        
        if not pattern:
            return
        
        # Get distinction density
        density = state.density if hasattr(state, 'density') else 0.0
        curvature = state.curvature if hasattr(state, 'curvature') else 0.0
        
        # Reinforce habits with higher distinction density
        # Density = stability
        strength_increase = 0.1 * density
        
        self.record_pattern(
            pattern,
            entropy=state.entropy if hasattr(state, 'entropy') else 0.0,
            curvature=curvature
        )
    
    def summary(self) -> dict[str, float]:
        """
        Get habit strength summary.
        
        Returns:
            Dictionary of pattern -> strength
        """
        return {
            str(habit.pattern): self.get_habit_strength(habit.pattern)
            for habit in self.habits.values()
        }

    def save_to_repo(self) -> None:
        """
        Save habits to repository.
        """
        habits_dir = self.repo_path / "experience"
        habits_dir.mkdir(parents=True, exist_ok=True)
        
        habits_file = habits_dir / "habits.json"
        
        habits_data = {
            signature: habit.to_dict()
            for signature, habit in self.habits.items()
        }
        
        with open(habits_file, 'w') as f:
            json.dump(habits_data, f, indent=2)

    def _load_habits(self) -> None:
        """
        Load habits from repository.
        """
        habits_file = self.repo_path / "experience" / "habits.json"
        
        if not habits_file.exists():
            return
        
        try:
            with open(habits_file, 'r') as f:
                habits_data = json.load(f)
            
            for signature, data in habits_data.items():
                self.habits[signature] = Habit.from_dict(data)
        except Exception as e:
            print(f"Error loading habits: {e}")

