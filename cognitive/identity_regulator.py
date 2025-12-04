"""
Identity regulator.

Slowly forms an identity vector by accumulating experience.
"""

from __future__ import annotations

from ApopToSiS.core.numpy_fallback import np
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ApopToSiS.runtime.capsules import Capsule
else:
    # Runtime import - handle both absolute and relative
    try:
        from ApopToSiS.runtime.capsules import Capsule
    except ImportError:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from runtime.capsules import Capsule


class IdentityRegulator:
    """
    Identity regulator.
    
    Slowly forms an identity vector by accumulating experience.
    This creates continuity and personality over time.
    """

    def __init__(self, dim: int = 32) -> None:
        """
        Initialize identity regulator.
        
        Args:
            dim: Embedding dimension
        """
        self.identity_vec: np.ndarray | None = None
        self.experience_count = 0
        self.dim = dim
        self.curvature_history: list[float] = []
        self.entropy_history: list[float] = []
        self.last_identity_drift: float = 0.0

    def update(self, capsule: Capsule, vec: np.ndarray) -> None:
        """
        Update identity from capsule and embedding.
        
        Args:
            capsule: PF capsule
            vec: Embedding vector
        """
        # Initialize identity vector if needed
        if self.identity_vec is None:
            self.identity_vec = vec.copy()
        else:
            # Moving average (98% old, 2% new)
            # This creates slow, stable identity formation
            self.identity_vec = 0.98 * self.identity_vec + 0.02 * vec
        
        # Track PF metrics
        self.curvature_history.append(capsule.curvature)
        self.entropy_history.append(capsule.entropy)
        
        # Keep history limited
        if len(self.curvature_history) > 100:
            self.curvature_history = self.curvature_history[-100:]
        if len(self.entropy_history) > 100:
            self.entropy_history = self.entropy_history[-100:]
        
        # Normalize identity vector to keep it bounded
        if self.identity_vec is not None:
            norm = float(np.linalg.norm(self.identity_vec))
            if norm > 0:
                self.identity_vec = self.identity_vec / norm

        # Track drift and damp runaway changes
        drift = self.get_identity_drift()
        self.last_identity_drift = drift
        if drift > 3.0 and self.identity_vec is not None:
            self.identity_vec = self.identity_vec * 0.7

        self.experience_count += 1

    def export(self) -> dict[str, Any]:
        """
        Export identity regulator state.
        
        Returns:
            Dictionary with identity state
        """
        # Convert identity_vec to list for JSON serialization
        identity_vec_list = None
        if self.identity_vec is not None:
            if hasattr(self.identity_vec, 'tolist'):
                identity_vec_list = self.identity_vec.tolist()
            elif hasattr(self.identity_vec, 'data'):
                # ArrayLike object
                identity_vec_list = list(self.identity_vec.data)
            elif isinstance(self.identity_vec, (list, tuple)):
                identity_vec_list = list(self.identity_vec)
            else:
                identity_vec_list = [float(self.identity_vec)] if isinstance(self.identity_vec, (int, float)) else []
        
        return {
            "identity_vec": identity_vec_list,
            "experience_count": self.experience_count,
            "curvature_history_length": len(self.curvature_history),
            "entropy_history_length": len(self.entropy_history),
            "last_identity_drift": self.last_identity_drift,
        }

    def get_identity_drift(self) -> float:
        """
        Compute identity drift (how much identity has changed).
        
        Returns:
            Drift value (0.0 = stable, higher = changing)
        """
        if len(self.curvature_history) < 2:
            return 0.0
        
        # Compute variance in curvature
        import statistics
        try:
            variance = statistics.variance(self.curvature_history[-20:])
            return variance
        except statistics.StatisticsError:
            return 0.0

    def summary(self) -> dict[str, Any]:
        """
        Get identity summary.
        
        Returns:
            Dictionary with identity statistics
        """
        return {
            "interactions": self.experience_count,
            "identity_formed": self.identity_vec is not None,
            "curvature_history_length": len(self.curvature_history),
            "entropy_history_length": len(self.entropy_history),
            "identity_drift": self.last_identity_drift or self.get_identity_drift(),
        }

