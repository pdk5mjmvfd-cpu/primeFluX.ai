"""
Flux Divergence Risk (FDR) — Cognitive Risk Assessment.

PF-internal risk about Apop's thinking stability:
- Will a shortcut misfire?
- Will a habit destabilize thought?
- Will a collapse be premature?
- Will curvature diverge?
- Will entropy spike?
- Will shell transitions break sequence?
- Will the flux destabilize?

This is mathematical, not moral.
This is PrimeFlux physics, not ethics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.combinatoric.interpreter import CombinatoricDistinctionPacket


@dataclass
class FDRResult:
    """Result of Flux Divergence Risk assessment."""
    risk_score: float  # 0.0 (stable) to 1.0 (high divergence risk)
    stability: float  # 0.0 (unstable) to 1.0 (stable)
    divergence_indicators: dict[str, Any]
    recommendation: str  # "safe", "caution", "avoid"


class FluxDivergenceRisk:
    """
    Assesses cognitive risk (Flux Divergence Risk).
    
    Evaluates:
    - Thought stability
    - Consistency
    - Predictability
    - Memory integrity
    - Identity continuity
    - Avoiding runaway cascades
    """

    def assess_shortcut_risk(
        self,
        shortcut: Any,
        current_state: Any
    ) -> FDRResult:
        """
        Assess risk of applying a shortcut.

        Args:
            shortcut: Shortcut to assess
            current_state: Current PF state

        Returns:
            FDRResult with risk assessment
        """
        indicators = {}
        risk_score = 0.0
        
        # Check entropy drop (too much drop = instability)
        if hasattr(shortcut, 'entropy_drop'):
            if shortcut.entropy_drop > 0.8:
                indicators["high_entropy_drop"] = True
                risk_score += 0.2
        
        # Check curvature consistency
        if hasattr(shortcut, 'curvature_consistency'):
            if shortcut.curvature_consistency < 0.5:
                indicators["low_curvature_consistency"] = True
                risk_score += 0.2
        
        # Check error variance
        if hasattr(shortcut, 'error_variance'):
            if shortcut.error_variance > 0.5:
                indicators["high_error_variance"] = True
                risk_score += 0.2
        
        # Check shortcut validity
        if hasattr(shortcut, 'valid'):
            if not shortcut.valid:
                indicators["invalid_shortcut"] = True
                risk_score += 0.3
        
        # Check count (new shortcuts are riskier)
        if hasattr(shortcut, 'count'):
            if shortcut.count < 3:
                indicators["low_usage_count"] = True
                risk_score += 0.1
        
        stability = 1.0 - risk_score
        risk_score = min(1.0, max(0.0, risk_score))
        
        # Recommendation
        if risk_score < 0.3:
            recommendation = "safe"
        elif risk_score < 0.6:
            recommendation = "caution"
        else:
            recommendation = "avoid"
        
        return FDRResult(
            risk_score=risk_score,
            stability=stability,
            divergence_indicators=indicators,
            recommendation=recommendation
        )

    def assess_habit_risk(
        self,
        habit: Any,
        current_state: Any
    ) -> FDRResult:
        """
        Assess risk of applying a habit.

        Args:
            habit: Habit to assess
            current_state: Current PF state

        Returns:
            FDRResult with risk assessment
        """
        indicators = {}
        risk_score = 0.0
        
        # Check entropy drift
        if hasattr(habit, 'entropy_drift'):
            if habit.entropy_drift > 0.5:
                indicators["high_entropy_drift"] = True
                risk_score += 0.2
        
        # Check curvature drift
        if hasattr(habit, 'curvature_drift'):
            if habit.curvature_drift > 0.5:
                indicators["high_curvature_drift"] = True
                risk_score += 0.2
        
        # Check habit strength
        if hasattr(habit, 'count'):
            if habit.count < 2:
                indicators["weak_habit"] = True
                risk_score += 0.2
        
        stability = 1.0 - risk_score
        risk_score = min(1.0, max(0.0, risk_score))
        
        # Recommendation
        if risk_score < 0.3:
            recommendation = "safe"
        elif risk_score < 0.6:
            recommendation = "caution"
        else:
            recommendation = "avoid"
        
        return FDRResult(
            risk_score=risk_score,
            stability=stability,
            divergence_indicators=indicators,
            recommendation=recommendation
        )

    def assess_flux_stability(
        self,
        capsule: Capsule,
        packet: CombinatoricDistinctionPacket | None = None
    ) -> FDRResult:
        """
        Assess overall flux stability.

        Args:
            capsule: Current capsule
            packet: Optional combinatoric packet

        Returns:
            FDRResult with stability assessment
        """
        indicators = {}
        risk_score = 0.0
        
        # Check entropy spike (lower threshold)
        if capsule.entropy_snapshot > 1.5:
            indicators["entropy_spike"] = True
            risk_score += 0.3
        elif capsule.entropy_snapshot > 2.5:
            indicators["extreme_entropy_spike"] = True
            risk_score += 0.5
        
        # Check curvature divergence
        if capsule.curvature_snapshot > 10.0:
            indicators["curvature_divergence"] = True
            risk_score += 0.2
        
        # Check error accumulation
        if capsule.measurement_error > 2.0:
            indicators["error_accumulation"] = True
            risk_score += 0.2
        
        # Check shell transition validity
        if packet:
            shell_seq = packet.shell_suggestions
            for i in range(len(shell_seq) - 1):
                # Check for invalid transitions (e.g., 2→0, 3→2)
                if shell_seq[i] == 2 and shell_seq[i+1] == 0:
                    indicators["invalid_shell_transition"] = True
                    risk_score += 0.3
                elif shell_seq[i] == 3 and shell_seq[i+1] == 2:
                    indicators["backward_shell_transition"] = True
                    risk_score += 0.2
        
        stability = 1.0 - risk_score
        risk_score = min(1.0, max(0.0, risk_score))
        
        # Recommendation
        if risk_score < 0.3:
            recommendation = "safe"
        elif risk_score < 0.6:
            recommendation = "caution"
        else:
            recommendation = "avoid"
        
        return FDRResult(
            risk_score=risk_score,
            stability=stability,
            divergence_indicators=indicators,
            recommendation=recommendation
        )

