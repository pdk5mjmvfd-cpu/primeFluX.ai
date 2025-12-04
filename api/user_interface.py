"""
User Interface — Core entry point for ApopToSiS v3.

This is the exact mouth-to-brain integration point for the LLM.
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.supervisor.supervisor import Supervisor
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.runtime.distinction.distinction import DistinctionChain
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.agents.registry.registry import AgentRegistry
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent
from ApopToSiS.experience.manager import ExperienceManager
from ApopToSiS.core.quanta import QuantaCompressor
from ApopToSiS.api.remote_llm_bridge import RemoteLLMBridge
from ApopToSiS.runtime.llm_adapter import LLMAdapter


class UserInterface:
    """
    User Interface — core entry point.
    
    Processes text input and returns PF capsule.
    This is the exact mouth-to-brain integration point for the LLM.
    """

    def __init__(self, supervisor: Supervisor | None = None, lcm: LCM | None = None) -> None:
        """
        Initialize User Interface.

        Args:
            supervisor: Optional Supervisor instance
            lcm: Optional LCM instance
        """
        # Initialize ICM and LCM
        self.icm = ICM()
        self.lcm = lcm or LCM(icm=self.icm)
        
        # Initialize Supervisor
        self.supervisor = supervisor or Supervisor(icm=self.icm, lcm=self.lcm)
        
        # Initialize Experience Manager
        self.experience_manager = ExperienceManager()
        self.lcm.experience_manager = self.experience_manager
        self.supervisor.integrate_experience(self.experience_manager)
        
        # Initialize Quanta Compressor
        self.quanta_compressor = QuantaCompressor()
        
        # Initialize Agent Registry
        self.registry = AgentRegistry()
        self.registry.register("eidos", EidosAgent())
        self.registry.register("praxis", PraxisAgent())
        self.registry.register("aegis", AegisAgent())
        
        # Get agents
        self.agents = [
            self.registry.get("eidos"),
            self.registry.get("praxis"),
            self.registry.get("aegis"),
        ]
        
        # Initialize LLM Bridge (optional)
        self.llm_bridge = None
        self.llm_adapter = None
        try:
            import os
            import json
            config_path = os.path.join(os.path.dirname(__file__), "llm_bridge_config.json")
            if os.path.exists(config_path):
                with open(config_path) as f:
                    llm_config = json.load(f)
                self.llm_bridge = RemoteLLMBridge(llm_config)
                self.llm_adapter = LLMAdapter()
        except Exception:
            # LLM bridge optional, continue without it
            pass

    def run_apop(self, input_text: str) -> dict[str, Any]:
        """
        Process input text through full ApopToSiS pipeline.
        
        Function: `run_apop(text)` → processes text → returns PF capsule.
        This is the exact mouth-to-brain integration point for the LLM.

        Args:
            input_text: Input text from user or LLM

        Returns:
            Dictionary with capsule and processing results
        """
        # Tokenize input
        tokens = input_text.split()
        
        if not tokens:
            # Empty input
            return {
                "capsule": None,
                "error": "Empty input",
            }
        
        # Process tokens through LCM
        capsule_dict = self.lcm.process_tokens(tokens)
        
        # Create capsule from LCM output
        capsule = Capsule.decode(capsule_dict) if isinstance(capsule_dict, dict) else Capsule(raw_tokens=tokens)
        
        # Compress and hash capsule (QuantaCoin)
        quanta_hash = self.quanta_compressor.hash_capsule(capsule)
        quanta_value = self.quanta_compressor.compute_quanta(capsule)
        
        # Update capsule with quanta hash
        capsule.quanta_hash = quanta_hash
        
        # Get current state
        state = PFState()
        state.update(capsule.to_dict())
        
        # Route through Supervisor
        selected_agent = self.supervisor.route(state, self.agents)
        
        # Process capsule through selected agent
        if selected_agent:
            processed_capsule = selected_agent.transform(capsule)
        else:
            processed_capsule = capsule
        
        # Update experience layer
        self.experience_manager.update(processed_capsule, state)
        
        # LLM Bridge integration (Hybrid Mode) - optional
        if self.llm_bridge and self.llm_adapter:
            try:
                # Send capsule to LLM
                llm_output = self.llm_bridge.send_capsule(processed_capsule.to_dict())
                
                # Convert LLM hybrid metadata
                bridge_data = self.llm_adapter.prepare_for_lcm(llm_output)
                
                # Feed PF metadata forward into LCM-derived capsule generation
                capsule_dict = self.lcm.integrate_llm_feedback(
                    processed_capsule.to_dict(),
                    pf_meta=bridge_data["pfmeta"],
                    curvature_hint=bridge_data["curvature"],
                    flux_hint=bridge_data["flux"],
                    entropy_hint=bridge_data["entropy"]
                )
                
                # Update capsule with integrated feedback
                processed_capsule = Capsule.decode(capsule_dict)
            except Exception:
                # LLM bridge optional, continue with local capsule
                pass
        
        # Integrate capsule into Supervisor
        self.supervisor.integrate_capsule(processed_capsule)
        
        # Optional: surface background cognition updates if present
        metadata = getattr(processed_capsule, "metadata", {}) or {}
        background_cog = metadata.get("background_cog")
        if background_cog:
            text = background_cog.get("engine_output") or background_cog.get("text") or "[no output]"
            flux = background_cog.get("flux_state", "unknown")
            print("\n=== BACKGROUND COGNITION UPDATE ===")
            print(text)
            print(f"Flux: {flux}")
        
        # Return result
        return {
            "capsule": processed_capsule.encode(),
            "raw_tokens": processed_capsule.raw_tokens,
            "shell": processed_capsule.shell,
            "curvature": processed_capsule.curvature,
            "entropy": processed_capsule.entropy,
            "quanta_hash": quanta_hash,
            "quanta_value": quanta_value,
            "routed_agent": selected_agent.__class__.__name__ if selected_agent else None,
            "state": {
                "shell": state.shell.value if hasattr(state.shell, 'value') else state.shell,
                "curvature": state.curvature,
                "entropy": state.entropy,
                "density": state.density,
            },
        }


# Convenience function
def run_apop(input_text: str) -> dict[str, Any]:
    """
    Convenience function to run Apop.
    
    Args:
        input_text: Input text
        
    Returns:
        Processing result
    """
    ui = UserInterface()
    return ui.run_apop(input_text)
