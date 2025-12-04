"""
Remote LLM Bridge — Hybrid Mode for ApopToSiS v3.

Local Apop sends a PF capsule.
The LLM returns semantic output + PF-aware metadata:
    - semantic_output (string)
    - pf_metadata (dict)
    - curvature_trajectory (list/float)
    - flux_interpretation (dict)
    - entropy_hints (dict)

Local Apop then builds the final capsule from these hints.
"""

from __future__ import annotations

import json
import uuid
import time
from typing import Any, Optional
try:
    import requests
except ImportError:
    requests = None  # Optional dependency


class RemoteLLMBridge:
    """
    Hybrid-mode LLM bridge for ApopToSiS v3.
    
    Local Apop sends a PF capsule.
    The LLM returns semantic output + PF-aware metadata.
    Local Apop then builds the final capsule from these hints.
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize LLM bridge.
        
        Args:
            config: Configuration dictionary with:
                - api_url: URL of LLM API endpoint
                - model: Model name (default: "gpt-apop")
                - mode: Bridge mode (default: "hybrid")
        """
        self.api_url = config.get("api_url", "http://localhost:4000/apop_llm")
        self.model = config.get("model", "gpt-apop-v1")
        self.mode = config.get("mode", "hybrid")
        self.headers = {"Content-Type": "application/json"}
        self.timeout = config.get("timeout", 30.0)
        self.enabled = config.get("enabled", True)

    def send_capsule(self, capsule: dict[str, Any]) -> dict[str, Any]:
        """
        Send capsule to LLM and receive hybrid response.
        
        Args:
            capsule: PF capsule dictionary
            
        Returns:
            LLM response with:
                - semantic_output: Natural language response
                - pf_metadata: PF-aware metadata
                - curvature_trajectory: Curvature hints
                - flux_interpretation: Flux state hints
                - entropy_alignment_hints: Entropy hints
                
        Raises:
            ImportError: If requests library not available
            requests.RequestException: If API call fails
        """
        if not self.enabled:
            # Return mock response when disabled
            return self._mock_response(capsule)
        
        if requests is None:
            raise ImportError(
                "requests library required for LLM bridge. "
                "Install with: pip install requests"
            )
        
        payload = {
            "model": self.model,
            "capsule": capsule,
            "mode": "hybrid_pf",
            "timestamp": time.time(),
            "request_id": str(uuid.uuid4()),
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Fallback to mock response on error
            print(f"⚠️  LLM bridge error: {e}. Using mock response.")
            return self._mock_response(capsule)

    def _mock_response(self, capsule: dict[str, Any]) -> dict[str, Any]:
        """
        Generate mock LLM response for testing/fallback.
        
        Args:
            capsule: Input capsule
            
        Returns:
            Mock response with default values
        """
        return {
            "semantic_output": f"Processed capsule with {len(capsule.get('raw_tokens', []))} tokens.",
            "pf_metadata": {
                "shell_suggestion": capsule.get("shell", 0),
                "curvature_confidence": 0.5,
                "entropy_estimate": capsule.get("entropy", 0.0),
            },
            "curvature_trajectory": [capsule.get("curvature", 0.0)],
            "flux_interpretation": {
                "amplitude": capsule.get("curvature", 0.0) * 0.1,
                "direction": "forward",
            },
            "entropy_alignment_hints": {
                "amplifier": 0.0,
                "suggestion": "stable",
            },
        }

    def test_connection(self) -> bool:
        """
        Test connection to LLM API.
        
        Returns:
            True if connection successful, False otherwise
        """
        if not self.enabled or requests is None:
            return False
        
        try:
            test_payload = {
                "model": self.model,
                "capsule": {"raw_tokens": ["test"]},
                "mode": "test",
            }
            response = requests.post(
                self.api_url,
                json=test_payload,
                headers=self.headers,
                timeout=5.0
            )
            return response.status_code == 200
        except Exception:
            return False

