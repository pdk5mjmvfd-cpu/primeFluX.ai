"""
Pattern Recognition — generic pattern detection.

Detects:
- Repetition
- Triplet patterns
- Flux patterns
- Entropy trends
- Curvature patterns

All math = simple heuristics.
TODO for PF-level math.
"""

from __future__ import annotations

from typing import Any
from collections import Counter
import math


def detect_repetition(data: list[Any], min_count: int = 2) -> dict[Any, int]:
    """
    Detect repetition patterns in data.

    Args:
        data: List of data items
        min_count: Minimum count to consider as repetition

    Returns:
        Dictionary of item -> count for repeated items
    """
    counts = Counter(data)
    return {item: count for item, count in counts.items() if count >= min_count}


def detect_triplet_pattern(triplets: list[tuple[Any, Any, Any]]) -> dict[str, Any]:
    """
    Detect triplet patterns.

    Args:
        triplets: List of triplets

    Returns:
        Dictionary with pattern information
    """
    if not triplets:
        return {"pattern_type": "none", "frequency": 0}
    
    # Count triplet occurrences
    triplet_counts = Counter(triplets)
    most_common = triplet_counts.most_common(1)
    
    if most_common:
        pattern, count = most_common[0]
        frequency = count / len(triplets)
        
        return {
            "pattern_type": "repeated",
            "pattern": pattern,
            "frequency": frequency,
            "count": count,
        }
    
    return {"pattern_type": "none", "frequency": 0}


def detect_flux_pattern(
    shell_sequence: list[int],
    min_length: int = 3
) -> dict[str, Any]:
    """
    Detect flux patterns in shell sequences.

    Args:
        shell_sequence: List of shell values (0, 2, 3, 4)
        min_length: Minimum pattern length

    Returns:
        Dictionary with flux pattern information
    """
    if len(shell_sequence) < min_length:
        return {"pattern_type": "none", "sequence": []}
    
    # Look for repeated subsequences
    patterns = {}
    
    for length in range(min_length, len(shell_sequence) // 2 + 1):
        for i in range(len(shell_sequence) - length + 1):
            pattern = tuple(shell_sequence[i:i+length])
            if pattern not in patterns:
                patterns[pattern] = 0
            patterns[pattern] += 1
    
    # Find most common pattern
    if patterns:
        most_common = max(patterns.items(), key=lambda x: x[1])
        pattern, count = most_common
        
        return {
            "pattern_type": "repeated_sequence",
            "sequence": list(pattern),
            "count": count,
            "frequency": count / len(shell_sequence),
        }
    
    return {"pattern_type": "none", "sequence": []}


def detect_entropy_trend(entropy_history: list[float]) -> dict[str, Any]:
    """
    Detect entropy trends.

    Args:
        entropy_history: List of entropy values over time

    Returns:
        Dictionary with trend information
    """
    if len(entropy_history) < 2:
        return {"trend": "insufficient_data", "slope": 0.0}
    
    # Simple linear trend
    n = len(entropy_history)
    x_mean = (n - 1) / 2
    y_mean = sum(entropy_history) / n
    
    numerator = sum((i - x_mean) * (entropy_history[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        slope = 0.0
    else:
        slope = numerator / denominator
    
    # Determine trend
    if slope > 0.01:
        trend = "increasing"
    elif slope < -0.01:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        "trend": trend,
        "slope": slope,
        "current": entropy_history[-1],
        "average": y_mean,
    }


def detect_curvature_pattern(
    curvature_history: list[float],
    threshold: float = 0.1
) -> dict[str, Any]:
    """
    Detect curvature patterns.

    Args:
        curvature_history: List of curvature values
        threshold: Threshold for pattern detection

    Returns:
        Dictionary with curvature pattern information
    """
    if len(curvature_history) < 2:
        return {"pattern_type": "insufficient_data"}
    
    # Compute variance
    mean_curvature = sum(curvature_history) / len(curvature_history)
    variance = sum((c - mean_curvature) ** 2 for c in curvature_history) / len(curvature_history)
    std_dev = math.sqrt(variance)
    
    # Pattern classification
    if std_dev < threshold:
        pattern_type = "stable"
    elif std_dev < threshold * 2:
        pattern_type = "moderate_variance"
    else:
        pattern_type = "high_variance"
    
    # Detect oscillations
    oscillations = 0
    for i in range(1, len(curvature_history)):
        if (curvature_history[i] - curvature_history[i-1]) * \
           (curvature_history[i-1] - curvature_history[max(0, i-2)]) < 0:
            oscillations += 1
    
    return {
        "pattern_type": pattern_type,
        "mean": mean_curvature,
        "variance": variance,
        "std_dev": std_dev,
        "oscillations": oscillations,
        "oscillation_rate": oscillations / max(len(curvature_history) - 1, 1),
    }

