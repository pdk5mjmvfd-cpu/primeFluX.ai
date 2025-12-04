"""
Context Engine.

Sliding context window with curvature/entropy trends.
Disagreement is distinction-density, not error.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import statistics
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState


@dataclass
class Context:
    """Global context management."""
    capsules: list[Capsule] = field(default_factory=list)
    max_capsules: int = 100
    
    def update(self, capsule: Capsule) -> None:
        """
        Update context with new capsule.
        
        Args:
            capsule: Capsule to add
        """
        self.capsules.append(capsule)
        
        # Maintain sliding window
        if len(self.capsules) > self.max_capsules:
            self.capsules = self.capsules[-self.max_capsules:]
    
    def last_capsules(self, n: int) -> list[Capsule]:
        """
        Get last n capsules.
        
        Args:
            n: Number of capsules
            
        Returns:
            List of capsules
        """
        return self.capsules[-n:] if len(self.capsules) >= n else self.capsules
    
    def curvature_trend(self) -> float:
        """
        Compute curvature trend.
        
        Returns:
            Trend value (positive = increasing, negative = decreasing)
        """
        if len(self.capsules) < 2:
            return 0.0
        
        curvatures = [c.curvature_snapshot for c in self.capsules[-10:]]
        
        if len(curvatures) < 2:
            return 0.0
        
        # Linear trend
        n = len(curvatures)
        x_mean = (n - 1) / 2
        y_mean = sum(curvatures) / n
        
        numerator = sum((i - x_mean) * (curvatures[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def entropy_trend(self) -> float:
        """
        Compute entropy trend.
        
        Returns:
            Trend value
        """
        if len(self.capsules) < 2:
            return 0.0
        
        entropies = [c.entropy_snapshot for c in self.capsules[-10:]]
        
        if len(entropies) < 2:
            return 0.0
        
        # Linear trend
        n = len(entropies)
        x_mean = (n - 1) / 2
        y_mean = sum(entropies) / n
        
        numerator = sum((i - x_mean) * (entropies[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def disagreement_level(self) -> float:
        """
        Compute disagreement level.
        
        Disagreement is distinction-density, not error.
        
        Returns:
            Disagreement level (flux amplitude)
        """
        if len(self.capsules) < 2:
            return 0.0
        
        # Disagreement = variance in curvature (flux amplitude)
        curvatures = [c.curvature_snapshot for c in self.capsules[-10:]]
        
        if len(curvatures) < 2:
            return 0.0
        
        # Variance = flux amplitude
        variance = statistics.variance(curvatures) if len(curvatures) > 1 else 0.0
        
        return variance
    
    def add_capsule(self, capsule: Capsule) -> None:
        """
        Add a capsule to context.
        
        Args:
            capsule: Capsule to add
        """
        self.update(capsule)
