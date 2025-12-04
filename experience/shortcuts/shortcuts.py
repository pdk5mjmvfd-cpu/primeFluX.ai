"""
Shortcuts — stabilized flux sequences that can be executed without full computation.

Shortcuts are detected by:
- Pattern repetition
- Entropy drop
- Curvature consistency
- Same shell sequence (e.g., 0→2→3→4)
- Low error variance

Shortcut = compressed flux chain.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from collections import Counter


@dataclass
class Shortcut:
    """
    A shortcut = compressed flux chain.
    
    Shortcuts are detected by:
    - pattern repetition
    - entropy drop
    - curvature consistency
    - same shell sequence
    - low error variance
    """
    signature: str  # SHA256 hash of pattern
    flux_sequence: list[dict[str, Any]] = field(default_factory=list)
    shell_sequence: list[int] = field(default_factory=list)
    entropy_drop: float = 0.0
    curvature_consistency: float = 1.0
    error_variance: float = 0.0
    count: int = 1
    valid: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert shortcut to dictionary."""
        return {
            "signature": self.signature,
            "flux_sequence": self.flux_sequence,
            "shell_sequence": self.shell_sequence,
            "entropy_drop": self.entropy_drop,
            "curvature_consistency": self.curvature_consistency,
            "error_variance": self.error_variance,
            "count": self.count,
            "valid": self.valid,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Shortcut":
        """Create shortcut from dictionary."""
        return cls(
            signature=data["signature"],
            flux_sequence=data.get("flux_sequence", []),
            shell_sequence=data.get("shell_sequence", []),
            entropy_drop=data.get("entropy_drop", 0.0),
            curvature_consistency=data.get("curvature_consistency", 1.0),
            error_variance=data.get("error_variance", 0.0),
            count=data.get("count", 1),
            valid=data.get("valid", True),
            metadata=data.get("metadata", {}),
        )


class ShortcutManager:
    """
    Manages shortcuts (stabilized flux sequences).
    
    Shortcuts can be executed without full flux computation.
    """

    def __init__(self, repo_path: str = ".") -> None:
        """
        Initialize ShortcutManager.

        Args:
            repo_path: Path to repository
        """
        self.repo_path = Path(repo_path)
        self.shortcuts: dict[str, Shortcut] = {}
        self._load_shortcuts()

    def _chain_signature(self, shell_sequence: list[int]) -> str:
        """
        Generate signature for a shell sequence.

        Args:
            shell_sequence: Shell sequence

        Returns:
            SHA256 hash signature
        """
        sequence_str = str(tuple(shell_sequence)).encode('utf-8')
        return hashlib.sha256(sequence_str).hexdigest()

    def detect_shortcut(
        self,
        shell_sequence: list[int],
        flux_sequence: list[dict[str, Any]] | None = None,
        entropy_history: list[float] | None = None,
        curvature_history: list[float] | None = None,
        error_history: list[float] | None = None
    ) -> Shortcut | None:
        """
        Detect if a chain qualifies as a shortcut.

        Args:
            shell_sequence: Shell sequence
            flux_sequence: Optional flux sequence
            entropy_history: Optional entropy history
            curvature_history: Optional curvature history
            error_history: Optional error history

        Returns:
            Shortcut if detected, None otherwise
        """
        if len(shell_sequence) < 2:
            return None
        
        signature = self._chain_signature(shell_sequence)
        
        # Check if already exists
        if signature in self.shortcuts:
            shortcut = self.shortcuts[signature]
            shortcut.count += 1
            return shortcut
        
        # Check shortcut criteria
        # 1. Pattern repetition (check if sequence appears multiple times)
        # 2. Entropy drop
        entropy_drop = 0.0
        if entropy_history and len(entropy_history) >= 2:
            entropy_drop = entropy_history[0] - entropy_history[-1]
        
        # 3. Curvature consistency
        curvature_consistency = 1.0
        if curvature_history and len(curvature_history) >= 2:
            from statistics import stdev
            if len(curvature_history) > 1:
                std = stdev(curvature_history)
                curvature_consistency = 1.0 / (1.0 + std)  # Higher consistency = lower std
        
        # 4. Error variance
        error_variance = 0.0
        if error_history and len(error_history) >= 2:
            from statistics import variance
            error_variance = variance(error_history) if len(error_history) > 1 else 0.0
        
        # Create shortcut if criteria met
        if entropy_drop > 0 or curvature_consistency > 0.7 or error_variance < 0.1:
            shortcut = Shortcut(
                signature=signature,
                flux_sequence=flux_sequence or [],
                shell_sequence=shell_sequence,
                entropy_drop=entropy_drop,
                curvature_consistency=curvature_consistency,
                error_variance=error_variance,
            )
            self.shortcuts[signature] = shortcut
            return shortcut
        
        return None

    def get_shortcut(self, signature: str) -> Shortcut | None:
        """
        Get shortcut by signature.

        Args:
            signature: Shortcut signature

        Returns:
            Shortcut if found, None otherwise
        """
        return self.shortcuts.get(signature)

    def apply_shortcut(self, state: Any, signature: str) -> Any:
        """
        Apply a shortcut to a state.

        Args:
            state: Current state
            signature: Shortcut signature

        Returns:
            New state after shortcut application
        """
        shortcut = self.get_shortcut(signature)
        
        if not shortcut or not shortcut.valid:
            return state
        
        # Apply flux sequence if available
        # TODO: Implement full flux application
        # For now, return state with metadata
        if hasattr(state, 'metadata'):
            state.metadata["shortcut_applied"] = signature
            state.metadata["shortcut_count"] = shortcut.count
        
        return state

    def save_to_repo(self) -> None:
        """
        Save shortcuts to repository.
        """
        shortcuts_dir = self.repo_path / "experience"
        shortcuts_dir.mkdir(parents=True, exist_ok=True)
        
        shortcuts_file = shortcuts_dir / "shortcuts.json"
        
        shortcuts_data = {
            sig: shortcut.to_dict()
            for sig, shortcut in self.shortcuts.items()
        }
        
        with open(shortcuts_file, 'w') as f:
            json.dump(shortcuts_data, f, indent=2)

    def _load_shortcuts(self) -> None:
        """
        Load shortcuts from repository.
        """
        shortcuts_file = self.repo_path / "experience" / "shortcuts.json"
        
        if not shortcuts_file.exists():
            return
        
        try:
            with open(shortcuts_file, 'r') as f:
                shortcuts_data = json.load(f)
            
            for signature, data in shortcuts_data.items():
                self.shortcuts[signature] = Shortcut.from_dict(data)
        except Exception as e:
            print(f"Error loading shortcuts: {e}")
    
    def update_from_capsule(self, capsule: Any, state: Any) -> None:
        """
        Update shortcuts from capsule and state.
        
        PF Logic: Shortcuts form when the Hamiltonian is low and curvature is collapsing.
        Collapsed curvature → stable → shortcut.
        
        Args:
            capsule: Capsule
            state: PF state
        """
        from core.math.hamiltonians import hamiltonian
        
        H = hamiltonian(state.curvature) if hasattr(state, 'curvature') else 0.0
        
        # Low-energy state = shortcut
        if H < 1.0:
            # Create shortcut from capsule tokens
            if hasattr(capsule, 'raw_tokens') and capsule.raw_tokens:
                key = tuple(capsule.raw_tokens[:3])
                shell_sequence = [capsule.shell] if hasattr(capsule, 'shell') else [0]
                
                # Detect shortcut
                self.detect_shortcut(
                    shell_sequence,
                    entropy_history=[capsule.entropy] if hasattr(capsule, 'entropy') else [0.0],
                    curvature_history=[state.curvature] if hasattr(state, 'curvature') else [0.0],
                    error_history=[capsule.measurement_error] if hasattr(capsule, 'measurement_error') else [0.0]
                )
    
    def summary(self) -> dict[str, Any]:
        """
        Get shortcuts summary.
        
        Returns:
            Dictionary of shortcut signatures -> data
        """
        return {
            sig: shortcut.to_dict()
            for sig, shortcut in self.shortcuts.items()
        }

