"""
User Safety Risk (USR) — Human-Centered Risk Assessment.

Trinity Layer: Eidos–Praxis–Aegis

Determines:
- Is the user safe?
- Is the output safe?
- Is the behavior aligned with human well-being?
- Does the action respect boundaries?
- Could this cause harm (physical, emotional, social, legal, etc.)?

This is:
- contextual
- ethical
- situational
- relational
- external
- tied to safety constraints
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.combinatoric.interpreter import CombinatoricDistinctionPacket


@dataclass
class USRResult:
    """Result of User Safety Risk assessment."""
    risk_score: float  # 0.0 (safe) to 1.0 (high risk)
    safety_level: float  # 0.0 (unsafe) to 1.0 (safe)
    harm_indicators: dict[str, Any]
    recommendation: str  # "safe", "caution", "block"
    agent_action: str  # "allow", "reframe", "block"


class UserSafetyRisk:
    """
    Assesses user safety risk (User Safety Risk).
    
    Managed by Trinity Agents:
    - Eidos: expansion (creative risk probing)
    - Praxis: shaping (alignment with intent/context)
    - Aegis: validation (safety, grounding, ethical guardrail)
    """

    # Harm indicators (combinatoric patterns that might indicate risk)
    HARM_PATTERNS = [
        r'\b(destroy|delete|remove|kill|harm|hurt|damage)\b',
        r'\b(override|bypass|ignore|skip|disable)\b',
        r'\b(secret|hidden|private|confidential)\b',
        r'[<>]',  # Potentially dangerous operators
    ]

    def assess_capsule_safety(
        self,
        capsule: Capsule,
        packet: CombinatoricDistinctionPacket | None = None
    ) -> USRResult:
        """
        Assess safety of a capsule.

        Args:
            capsule: Capsule to assess
            packet: Optional combinatoric packet

        Returns:
            USRResult with safety assessment
        """
        indicators = {}
        risk_score = 0.0
        
        # Check raw tokens for harm patterns
        if packet:
            import re
            text = " ".join(packet.tokens)
            
            for pattern in self.HARM_PATTERNS:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    indicators[f"harm_pattern_{pattern}"] = len(matches)
                    risk_score += 0.25 * len(matches)  # Increased weight
        
        # Also check capsule raw_tokens if available
        if hasattr(capsule, 'raw_tokens') and capsule.raw_tokens:
            import re
            text = " ".join(capsule.raw_tokens)
            
            for pattern in self.HARM_PATTERNS:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    indicators[f"harm_pattern_{pattern}"] = indicators.get(f"harm_pattern_{pattern}", 0) + len(matches)
                    risk_score += 0.25 * len(matches)
        
        # Check for high error (might indicate confusion/unsafe state)
        if capsule.measurement_error > 1.5:
            indicators["high_error_state"] = True
            risk_score += 0.1
        
        # Check for extreme entropy (might indicate chaotic/unsafe output)
        if capsule.entropy_snapshot > 3.0:
            indicators["extreme_entropy"] = True
            risk_score += 0.1
        
        # Check metadata for safety flags
        if "unsafe" in capsule.metadata or "block" in capsule.metadata:
            indicators["safety_flag"] = True
            risk_score += 0.3
        
        safety_level = 1.0 - risk_score
        risk_score = min(1.0, max(0.0, risk_score))
        
        # Recommendation and agent action
        if risk_score < 0.3:
            recommendation = "safe"
            agent_action = "allow"
        elif risk_score < 0.6:
            recommendation = "caution"
            agent_action = "reframe"
        else:
            recommendation = "block"
            agent_action = "block"
        
        return USRResult(
            risk_score=risk_score,
            safety_level=safety_level,
            harm_indicators=indicators,
            recommendation=recommendation,
            agent_action=agent_action
        )

    def assess_output_safety(
        self,
        output: str,
        context: dict[str, Any] | None = None
    ) -> USRResult:
        """
        Assess safety of an output.

        Args:
            output: Output text to assess
            context: Optional context

        Returns:
            USRResult with safety assessment
        """
        indicators = {}
        risk_score = 0.0
        
        import re
        
        # Check for harm patterns
        for pattern in self.HARM_PATTERNS:
            matches = re.findall(pattern, output, re.IGNORECASE)
            if matches:
                indicators[f"harm_pattern_{pattern}"] = len(matches)
                risk_score += 0.15 * len(matches)
        
        # Check for potentially dangerous code patterns
        dangerous_code = [
            r'exec\s*\(',
            r'eval\s*\(',
            r'__import__',
            r'subprocess',
            r'os\.system',
        ]
        
        for pattern in dangerous_code:
            if re.search(pattern, output, re.IGNORECASE):
                indicators["dangerous_code"] = True
                risk_score += 0.3
        
        safety_level = 1.0 - risk_score
        risk_score = min(1.0, max(0.0, risk_score))
        
        # Recommendation (stricter thresholds)
        if risk_score < 0.2:
            recommendation = "safe"
            agent_action = "allow"
        elif risk_score < 0.4:
            recommendation = "caution"
            agent_action = "reframe"
        else:
            recommendation = "block"
            agent_action = "block"
        
        return USRResult(
            risk_score=risk_score,
            safety_level=safety_level,
            harm_indicators=indicators,
            recommendation=recommendation,
            agent_action=agent_action
        )

