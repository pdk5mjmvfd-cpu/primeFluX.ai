"""
LLM Adapter — Converts LLM hybrid returns into PF-ready components.

LLM returns:
    - semantic_output
    - pf_metadata
    - curvature_trajectory
    - flux_state
    - entropy_hints

Adapter prepares these for LCM → Capsule.
"""

from __future__ import annotations

from typing import Any


class LLMAdapter:
    """
    Converts LLM hybrid returns into PF-ready components.
    
    LLM returns:
        - semantic_output: Natural language response
        - pf_metadata: PF-aware metadata dictionary
        - curvature_trajectory: List of curvature values or single float
        - flux_interpretation: Flux state dictionary
        - entropy_alignment_hints: Entropy hints dictionary
    
    Adapter prepares these for LCM → Capsule integration.
    """

    def __init__(self) -> None:
        """Initialize LLM adapter."""
        pass

    def prepare_for_lcm(self, llm_response: dict[str, Any]) -> dict[str, Any]:
        """
        Prepare LLM response for LCM integration.
        
        Args:
            llm_response: Raw LLM response dictionary
            
        Returns:
            Prepared dictionary with:
                - semantic_output: String
                - pfmeta: PF metadata dict
                - curvature: Curvature trajectory (normalized to list)
                - flux: Flux interpretation dict
                - entropy: Entropy hints dict
        """
        semantic = llm_response.get("semantic_output", "")
        pfmeta = llm_response.get("pf_metadata", {})
        curvature = llm_response.get("curvature_trajectory", [])
        flux = llm_response.get("flux_interpretation", {})
        entropy = llm_response.get("entropy_alignment_hints", {})

        # Normalize curvature to list
        if isinstance(curvature, (int, float)):
            curvature = [float(curvature)]
        elif not isinstance(curvature, list):
            curvature = []

        # Ensure flux is a dict
        if not isinstance(flux, dict):
            flux = {}

        # Ensure entropy is a dict
        if not isinstance(entropy, dict):
            entropy = {}

        return {
            "semantic_output": str(semantic),
            "pfmeta": pfmeta if isinstance(pfmeta, dict) else {},
            "curvature": curvature,
            "flux": flux,
            "entropy": entropy,
        }

    def validate_llm_response(self, llm_response: dict[str, Any]) -> bool:
        """
        Validate LLM response structure.
        
        Args:
            llm_response: LLM response to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(llm_response, dict):
            return False
        
        # Check for required fields
        required_fields = ["semantic_output", "pf_metadata"]
        for field in required_fields:
            if field not in llm_response:
                return False
        
        return True

