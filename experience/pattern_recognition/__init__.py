"""
Pattern Recognition — generic pattern detection.
"""

from .pattern_recognition import (
    detect_repetition,
    detect_triplet_pattern,
    detect_flux_pattern,
    detect_entropy_trend,
    detect_curvature_pattern,
)

__all__ = [
    "detect_repetition",
    "detect_triplet_pattern",
    "detect_flux_pattern",
    "detect_entropy_trend",
    "detect_curvature_pattern",
]

