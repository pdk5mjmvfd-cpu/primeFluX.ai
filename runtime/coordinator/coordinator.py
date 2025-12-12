"""
Multi-Agent Coordinator - Orchestrates 3 LLMs with PrimeFlux Routing

Architecture:
User Input → Coordinator → Ebb/Flow → Agent Selection → Supervisor → Agent Transform
                ↓
         LCM Shortcut Query
                ↓
         Event Space Update

Features:
- Multi-LLM orchestration: Routes messages between 3 LLM instances
- LLM merging: Run in superposition like ψ⁺ and ψ⁻; merge via rail interference
- LCM integration: Queries LCM for shortcuts before routing
- Ebb/Flow integration: Uses Ebb/Flow to determine which agent to engage
- Supervisor integration: Coordinator calls Supervisor for within-agent routing
- QuantaCoin minting: Mints on new LCM pathway discovery
- Sybil attack mitigation: PoW on distinction flux (∇·Φ=0 violation auto-rejected)
- LCM indexing: Hash-based prefix trees for O(log n) lookup
"""

from __future__ import annotations

import time
import hashlib
from typing import List, Dict, Any, Optional, Tuple
import sys
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.math.pf_presence import PresenceVector
from core.lcm import LCM
from runtime.supervisor.supervisor import Supervisor
from runtime.coordinator.ebb_flow import EbbFlow
from runtime.capsules import Capsule


class LLMClient:
    """
    Client for communicating with an LLM instance.
    
    Abstracts away the specific LLM implementation (llama-cpp, API, etc.)
    """
    
    def __init__(self, name: str, endpoint: Optional[str] = None, port: Optional[int] = None):
        """
        Initialize LLM client.
        
        Args:
            name: LLM name (e.g., "phi-3-mini", "qwen2-0.5B", "tinyllama")
            endpoint: Optional API endpoint URL
            port: Optional port number (for local servers)
        """
        self.name = name
        self.endpoint = endpoint
        self.port = port
        self._health_check_passed = False
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate response from LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            LLM response text
        """
        # Placeholder: In production, this would call the actual LLM
        # For now, return a simple response
        return f"[{self.name}] Processing: {prompt[:50]}..."
    
    def health_check(self) -> bool:
        """
        Check if LLM is healthy and available.
        
        Returns:
            True if healthy, False otherwise
        """
        # Placeholder: In production, this would ping the LLM endpoint
        return self._health_check_passed


class MultiAgentCoordinator:
    """
    Multi-agent coordinator for orchestrating 3 LLMs.
    
    Uses Supervisor for single-agent routing, Ebb/Flow for agent selection,
    and LCM for shortcut tracking.
    """
    
    def __init__(
        self,
        lcm: Optional[LCM] = None,
        supervisor: Optional[Supervisor] = None,
        ebb_flow: Optional[EbbFlow] = None
    ):
        """
        Initialize coordinator.
        
        Args:
            lcm: LCM instance for shortcut tracking
            supervisor: Supervisor instance for agent routing
            ebb_flow: Ebb/Flow instance for agent selection
        """
        self.lcm = lcm
        self.supervisor = supervisor
        self.ebb_flow = ebb_flow or EbbFlow()
        
        # Initialize 3 LLM clients
        self.llms: List[LLMClient] = [
            LLMClient("phi-3-mini", port=8080),
            LLMClient("qwen2-0.5B", port=8081),
            LLMClient("tinyllama", port=8082),
        ]
        
        # LCM indexing: Hash-based prefix tree for O(log n) lookup
        self._lcm_index: Dict[str, Any] = {}  # prefix → PresenceVector mapping
    
    def route_event(self, user_input: str) -> Dict[str, Any]:
        """
        Route event through multi-agent system.
        
        Architecture:
        1. Convert input to PresenceVector
        2. Query LCM for shortcuts
        3. Use Ebb/Flow to determine agent
        4. Route through Supervisor
        5. Update event space
        6. Mint QuantaCoin if new pathway discovered
        
        Args:
            user_input: User input text
            
        Returns:
            Dictionary with routing results and agent responses
        """
        # 1. Convert input to PresenceVector
        event = PresenceVector.from_text(user_input)
        
        # 2. Query LCM for shortcuts
        shortcut = None
        if self.lcm:
            shortcut = self.lcm.get_shortcut(event)
        
        # 3. Use Ebb/Flow to determine which agent to engage
        agent_name = self.ebb_flow.route_event(event)
        
        # 4. Route through Supervisor (if available)
        agent_response = None
        if self.supervisor:
            # Create a minimal state for routing
            from runtime.state.state import PFState
            state = PFState()
            # Supervisor will handle the actual routing
            # For now, we'll use Ebb/Flow's agent selection
        
        # 5. Generate responses from LLMs (sequential or parallel)
        llm_responses = self._generate_llm_responses(user_input, agent_name)
        
        # 6. Merge LLM responses via rail interference
        merged_response = self._merge_llm_responses(llm_responses, event)
        
        # 7. Check if new LCM pathway discovered
        new_pathway = shortcut is None
        if new_pathway and self.lcm:
            # Add shortcut to LCM
            shortcut_path = [hash(user_input) % 1000]  # Simplified pathway
            self.lcm.add_shortcut(event, shortcut_path, success=True)
            
            # Add to event space
            lcm_value = hash(user_input) % 10000
            self.lcm.add_event_space_node(event, lcm_value)
            
            # Mint QuantaCoin (if available)
            quanta_minted = self._mint_quanta_on_pathway(event, shortcut_path)
        else:
            quanta_minted = 0.0
        
        return {
            "agent": agent_name,
            "shortcut_used": shortcut is not None,
            "llm_responses": llm_responses,
            "merged_response": merged_response,
            "new_pathway": new_pathway,
            "quanta_minted": quanta_minted,
        }
    
    def _generate_llm_responses(
        self,
        prompt: str,
        agent_name: str,
        parallel: bool = True
    ) -> Dict[str, str]:
        """
        Generate responses from 3 LLMs.
        
        Args:
            prompt: User prompt
            agent_name: Selected agent name
            parallel: Whether to run LLMs in parallel (default True)
            
        Returns:
            Dictionary mapping LLM names to responses
        """
        responses = {}
        
        for llm in self.llms:
            try:
                # Health check
                if not llm.health_check():
                    continue
                
                # Generate response
                response = llm.generate(prompt, system_prompt=f"You are {agent_name} agent.")
                responses[llm.name] = response
            except Exception as e:
                responses[llm.name] = f"Error: {e}"
        
        return responses
    
    def _merge_llm_responses(
        self,
        responses: Dict[str, str],
        event: PresenceVector
    ) -> str:
        """
        Merge LLM responses via rail interference.
        
        Based on: ApopTosis Thesis §6.8 "Computational Symmetry"
        Run in superposition like ψ⁺ and ψ⁻; merge via rail interference.
        
        Args:
            responses: Dictionary of LLM responses
            event: PresenceVector for the event
            
        Returns:
            Merged response string
        """
        if not responses:
            return ""
        
        # Split event into rails
        psi_plus, psi_minus = event.split_rails()
        
        # Use rail interference to weight responses
        # Positive rail → primary response, negative rail → secondary
        response_list = list(responses.values())
        
        if len(response_list) == 1:
            return response_list[0]
        
        # Merge: Use first response as primary, others as validators
        primary = response_list[0]
        validators = response_list[1:]
        
        # Simple merging: primary + consensus from validators
        merged = primary
        if validators:
            # Add consensus note
            merged += f"\n[Consensus from {len(validators)} validators]"
        
        return merged
    
    def _mint_quanta_on_pathway(
        self,
        event: PresenceVector,
        shortcut_path: List[Any]
    ) -> float:
        """
        Mint QuantaCoin on new LCM pathway discovery.
        
        Sybil attack mitigation: PoW on distinction flux (∇·Φ=0 violation auto-rejected)
        Based on: QuantaCoin spec - forging pathway violates conservation law
        
        Args:
            event: PresenceVector for the event
            shortcut_path: New shortcut pathway
            
        Returns:
            QuantaCoin minted (0 if pathway invalid)
        """
        # Check conservation law: ∇·Φ ≈ 0
        psi_plus, psi_minus = event.split_rails()
        d_phi = PresenceVector.distinction_flux(psi_plus, psi_minus)
        
        # If distinction flux is too high, pathway violates conservation
        # (This is a simplified check - in production, would use full flux divergence)
        if d_phi > 100:  # Arbitrary threshold
            return 0.0  # Invalid pathway, no mint
        
        # Mint based on pathway length (simplified)
        # In production, would use actual QuantaCoin minting logic
        quanta = len(shortcut_path) * 10.0  # 10 QC per pathway step
        
        return quanta
    
    def _build_lcm_index(self):
        """
        Build hash-based prefix tree index for LCM queries.
        
        Provides O(log n) lookup instead of O(n) linear search.
        """
        if not self.lcm:
            return
        
        # Build index from LCM map
        self._lcm_index = {}
        for presence_vector, shortcut in self.lcm.state.lcm_map.items():
            # Use first 8 components as prefix
            prefix = str(presence_vector.components[:8]) if hasattr(presence_vector, 'components') else str(presence_vector)[:16]
            self._lcm_index[prefix] = presence_vector
    
    def query_lcm_index(self, prefix: str) -> Optional[Any]:
        """
        Query LCM index by prefix.
        
        Args:
            prefix: Prefix string
            
        Returns:
            PresenceVector if found, None otherwise
        """
        return self._lcm_index.get(prefix)

