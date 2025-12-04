"""
Supervisor — PF routing and capsule integration engine.

The Supervisor:
- Routes capsules to appropriate agents based on PF metrics
- Integrates capsules back into state
- Maintains consistency via ConsistencyEngine
- Coordinates with Experience Manager
"""

from __future__ import annotations

from typing import Any, Optional
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.core.icm import ICM
from ApopToSiS.core.lcm import LCM
from ApopToSiS.runtime.supervisor.consistency import ConsistencyEngine
from ApopToSiS.runtime.router.router import (
    compute_agent_scores,
    select_agent,
)
# CoSy and PrimeFS imports
from ApopToSiS.core.consensus import CoSyBridgeMain
from ApopToSiS.pf_json import PFJsonGenerator, PFExpander


class Supervisor:
    """
    Supervisor — PF routing and capsule integration engine.
    
    Routes capsules to agents and integrates results back into state.
    """

    def __init__(
        self,
        icm: Optional[ICM] = None,
        lcm: Optional[LCM] = None,
        experience_manager: Any = None
    ) -> None:
        """
        Initialize Supervisor.
        
        Args:
            icm: ICM instance
            lcm: LCM instance
            experience_manager: Optional ExperienceManager instance
        """
        self.icm = icm or ICM()
        self.lcm = lcm or LCM(icm=self.icm)
        self.experience_manager = experience_manager
        self.consistency_engine = ConsistencyEngine()
        # Initialize consensus engine
        self.cosy = CoSyBridgeMain()
        self._last_capsule: Optional[Capsule] = None

    def route(
        self,
        state: PFState,
        agents: list[Any]
    ) -> Any:
        """
        Route capsule to appropriate agent based on PF metrics.
        
        Uses PF-based routing with consistency bias.
        
        Args:
            state: Current PF state
            agents: List of available agents
            
        Returns:
            Selected agent (or None if no agents)
        """
        if not agents:
            return None
        
        # Compute base agent scores
        scores = compute_agent_scores(state, agents, self.icm, self.lcm)
        
        # Apply consistency bias if we have a last capsule
        if self._last_capsule:
            consistency_metrics = self.consistency_engine.update(self._last_capsule)
            bias = consistency_metrics.get("bias_vector", 0.0)
            
            # Apply bias as soft weight (modulate scores, don't block)
            for agent in scores:
                # Slight boost for agents that align with consistency
                scores[agent] *= (1.0 + bias * 0.1)
        
        # Select best agent
        selected = select_agent(scores, agents)
        return selected

    def integrate_capsule(self, capsule: Capsule) -> None:
        """
        Integrate capsule into Supervisor state.
        
        Updates:
        - LCM state
        - ICM state
        - Experience Manager (if available)
        - Consistency Engine
        
        Args:
            capsule: Capsule to integrate
        """
        # Update LCM with capsule data
        if capsule.raw_tokens:
            self.lcm.process_tokens(capsule.raw_tokens)
        
        # Update ICM from capsule PF metrics
        self.icm.update_curvature(
            capsule.raw_tokens,
            [t for t in self.lcm.state.triplets if hasattr(t, 'a')]
        )
        self.icm.update_entropy(
            capsule.raw_tokens,
            [t for t in self.lcm.state.triplets if hasattr(t, 'a')]
        )
        
        # Update experience manager if available
        if self.experience_manager and hasattr(self.experience_manager, 'update'):
            # We need state, but we can create a minimal one
            state = PFState()
            state.update_from_capsule(capsule)
            self.experience_manager.update(capsule, state)
        
        # Update consistency engine
        self.consistency_engine.update(capsule)
        
        # Store as last capsule
        self._last_capsule = capsule

    def update_state(self, capsule: Capsule) -> PFState:
        """
        Update PF state from capsule.
        
        Args:
            capsule: Capsule to extract state from
            
        Returns:
            Updated PF state
        """
        state = PFState()
        state.update_from_capsule(capsule)
        return state

    def process_capsule(
        self,
        capsule: Capsule,
        agents: list[Any]
    ) -> dict[str, Any]:
        """
        Process capsule through full supervisor pipeline.
        
        This is a convenience method that:
        1. Routes to agent
        2. Transforms capsule
        3. Integrates capsule
        4. Returns processing result
        
        Args:
            capsule: Input capsule
            agents: List of available agents
            
        Returns:
            Processing result dictionary
        """
        # Create state from capsule
        state = PFState()
        state.update_from_capsule(capsule)
        
        # Route to agent
        selected_agent = self.route(state, agents)
        agent_sequence = []
        
        if selected_agent:
            agent_sequence.append(selected_agent.__class__.__name__)
            capsule = selected_agent.transform(capsule)
            capsule.agent_trace.append(selected_agent.__class__.__name__)
        
        # Integrate capsule
        self.integrate_capsule(capsule)
        
        # Update state again
        final_state = self.update_state(capsule)
        
        # Compute flux metrics
        flux_metrics = {
            "entropy": capsule.entropy,
            "curvature": capsule.curvature,
            "density": capsule.density,
            "psi": capsule.psi,
            "hamiltonian": capsule.hamiltonian,
        }
        
        # Quanta metrics
        quanta_minted = {
            "quanta_hash": capsule.quanta_hash,
            "compression_ratio": capsule.compression_ratio,
        }
        
        return {
            "final_capsule": capsule,
            "state": final_state,
            "agent_sequence": agent_sequence,
            "flux_metrics": flux_metrics,
            "quanta_minted": quanta_minted,
        }

    def integrate_experience(self, experience_manager: Any) -> None:
        """
        Attach experience manager to supervisor.
        
        Args:
            experience_manager: ExperienceManager instance
        """
        self.experience_manager = experience_manager

