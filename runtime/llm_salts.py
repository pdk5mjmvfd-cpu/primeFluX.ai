"""
Offline LLM with Ollama salts.

Provides offline LLM access via Ollama with agent-specific model salts.
"""

from __future__ import annotations

from typing import Optional, Dict, Any
import json

# Try to import ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    ollama = None


class OfflineLLM:
    """
    Offline LLM with agent-specific model salts.
    
    Uses Ollama for local LLM inference with different models
    for different agents.
    """
    
    # Agent-specific model salts
    SALTS = {
        "eidos": "llama3.2:3b",
        "praxis": "qwen2-math-7b",
        "aegis": "phi-3.5-mini:4b"
    }
    
    def __init__(self):
        """Initialize Offline LLM."""
        self.ollama_available = OLLAMA_AVAILABLE
    
    def query_salt(
        self,
        salt: str,
        prompt: str,
        capsule: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Query LLM with agent salt.
        
        Uses ollama.generate with system prompt injecting capsule + PF instructions
        (distinction, rails, curvature).
        
        Args:
            salt: Agent salt (model name or agent name)
            prompt: User prompt
            capsule: Optional capsule data
            
        Returns:
            LLM response
        """
        if not self.ollama_available:
            return f"[Ollama not available] Response for {salt}: {prompt}"
        
        # Get model name from salt
        model = self.SALTS.get(salt, salt)
        
        # Build system prompt with PF instructions
        system_prompt = self._build_system_prompt(capsule)
        
        try:
            # Query Ollama
            response = ollama.generate(
                model=model,
                prompt=prompt,
                system=system_prompt,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            )
            
            return response.get("response", "")
        except Exception as e:
            return f"[Ollama error: {str(e)}]"
    
    def _build_system_prompt(self, capsule: Optional[Dict[str, Any]]) -> str:
        """
        Build system prompt with PF instructions.
        
        Args:
            capsule: Optional capsule data
            
        Returns:
            System prompt string
        """
        prompt_parts = [
            "You are a PrimeFlux AI agent operating in the ApopToSiS ecosystem.",
            "Key concepts:",
            "- Distinction: Information barriers resolved via geometry",
            "- Rails: 6k±1 dual prime rails as manifold",
            "- Curvature: ICM/LCM manifolds for structure",
            "- Reversible: All operations maintain reversibility"
        ]
        
        if capsule:
            prompt_parts.append("\nCurrent capsule context:")
            prompt_parts.append(json.dumps(capsule, indent=2))
        
        return "\n".join(prompt_parts)
    
    def is_available(self) -> bool:
        """Check if Ollama is available."""
        return self.ollama_available

