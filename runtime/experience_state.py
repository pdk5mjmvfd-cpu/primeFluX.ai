"""
ExperienceState — compressed memory of Apop's interactions.

Maintains an exponentially-smoothed identity vector and running PF metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence
import math

from ApopToSiS.core.numpy_fallback import np


def _to_vector(values: Sequence[float], dim: int) -> list[float]:
    """
    Convert incoming sequence to a fixed-length vector.
    Pads with zeros or truncates as needed.
    """
    if values is None:
        return [0.0] * dim
    data = list(values)
    if len(data) < dim:
        data = data + [0.0] * (dim - len(data))
    elif len(data) > dim:
        data = data[:dim]
    return [float(x) for x in data]


def _vector_norm(vec: Sequence[float]) -> float:
    """Compute Euclidean norm of a vector."""
    return math.sqrt(sum(x * x for x in vec))


@dataclass
class ExperienceState:
    """
    Compressed experience state updated per capsule.
    """

    dim: int = 32
    alpha: float = 0.2
    identity_vec: list[float] = field(default_factory=list)
    interaction_count: int = 0
    avg_entropy: float = 0.0
    avg_curvature: float = 0.0
    lattice_nodes: int = 0
    lattice_strength: float = 0.0

    def __post_init__(self) -> None:
        if not self.identity_vec:
            self.identity_vec = [0.0] * self.dim

    def update(
        self,
        capsule_entropy: float,
        capsule_curvature: float,
        embedding: Sequence[float] | None,
        lattice_summary: dict[str, float] | None = None,
    ) -> dict[str, float]:
        """
        Update the compressed state from a new capsule.

        Args:
            capsule_entropy: Current capsule entropy
            capsule_curvature: Current capsule curvature
            embedding: Cognitive embedding vector
            lattice_summary: Summary dict with node / strength counts

        Returns:
            Dict with deltas applied during this update.
        """
        self.interaction_count += 1
        t = max(1, self.interaction_count)

        # Identity EMA
        embedding_vec = _to_vector(embedding or [], self.dim)
        prev_identity = self.identity_vec[:]
        self.identity_vec = [
            (1 - self.alpha) * prev + self.alpha * emb
            for prev, emb in zip(self.identity_vec, embedding_vec)
        ]
        identity_drift = _vector_norm(
            [new - old for new, old in zip(self.identity_vec, prev_identity)]
        )

        # PF metric averages
        prev_avg_entropy = self.avg_entropy
        prev_avg_curvature = self.avg_curvature
        self.avg_entropy += (capsule_entropy - self.avg_entropy) / t
        self.avg_curvature += (capsule_curvature - self.avg_curvature) / t

        entropy_delta = capsule_entropy - prev_avg_entropy
        curvature_delta = capsule_curvature - prev_avg_curvature

        # Lattice stats
        if lattice_summary:
            self.lattice_nodes = int(lattice_summary.get("nodes", self.lattice_nodes))
            self.lattice_strength = float(
                lattice_summary.get("total_strength", self.lattice_strength)
            )

        return {
            "identity_drift": identity_drift,
            "entropy_delta": entropy_delta,
            "curvature_delta": curvature_delta,
            "interaction_count": self.interaction_count,
        }

    def snapshot(self) -> dict[str, float]:
        """Return a serializable snapshot of the experience state."""
        return {
            "interaction_count": self.interaction_count,
            "avg_entropy": self.avg_entropy,
            "avg_curvature": self.avg_curvature,
            "lattice_nodes": self.lattice_nodes,
            "lattice_strength": self.lattice_strength,
        }

