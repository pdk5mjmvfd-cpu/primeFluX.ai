"""
Agent Router - PF-aware routing based on distinction packets.

Routes agents based on curvature and rail phase from distinction packets.
Includes presence operator for event space toggling.
"""

from __future__ import annotations

import math
from typing import Optional
from core.distinction_packet import DistinctionPacket


class AgentRouter:
    """
    PF-aware agent router.
    
    Routes based on distinction packet properties:
    - High curvature (>0.7) → Eidos (ICM high distinction)
    - Negative rail phase (<0) → Aegis (LCM annihilation)
    - Otherwise → Praxis (relay)
    """
    
    def __init__(self):
        """Initialize agent router."""
        self.routing_history: list[dict] = []
    
    def route(self, packet: DistinctionPacket) -> str:
        """
        Route packet to appropriate agent.
        
        Args:
            packet: Distinction packet
            
        Returns:
            Agent name: "eidos", "aegis", or "praxis"
        """
        # High curvature (>0.7) → Eidos (ICM high distinction)
        if packet.curvature_value > 0.7:
            return "eidos"
        
        # Negative rail phase (<0) → Aegis (LCM annihilation)
        if packet.rail_phase < 0:
            return "aegis"
        
        # Otherwise → Praxis (relay)
        return "praxis"
    
    def log_route(
        self,
        packet: DistinctionPacket,
        agent: str,
        experience_graph: Optional[Any] = None
    ) -> None:
        """
        Log route to experience graph.
        
        Adds edge to graph with curvature metadata.
        
        Args:
            packet: Distinction packet
            agent: Selected agent name
            experience_graph: Optional experience graph instance
        """
        route_entry = {
            "agent": agent,
            "curvature": packet.curvature_value,
            "rail_phase": packet.rail_phase,
            "prime_modes": packet.prime_modes,
            "timestamp": packet.timestamp.isoformat()
        }
        
        self.routing_history.append(route_entry)
        
        # Add edge to experience graph if available
        if experience_graph and hasattr(experience_graph, 'add_edge'):
            try:
                experience_graph.add_edge(
                    source=f"input_{packet.timestamp.isoformat()}",
                    target=f"agent_{agent}",
                    metadata={
                        "curvature": packet.curvature_value,
                        "rail_phase": packet.rail_phase,
                        "prime_modes": packet.prime_modes
                    }
                )
            except Exception:
                # Silently fail if graph update fails
                pass
    
    def get_routing_history(self) -> list[dict]:
        """Get routing history."""
        return self.routing_history.copy()
    
    def presence_operator(
        self,
        phase: float,
        mode: str,
        presence_on: bool = True
    ) -> float:
        """
        Presence operator: g_PF(phase, mode) = trig(mode) if presence_on else 0.
        
        Args:
            phase: Rail phase
            mode: Mode (research/refinement/relations)
            presence_on: Whether presence is enabled
            
        Returns:
            Presence value
        """
        if not presence_on:
            return 0.0
        
        if mode == "research":
            return math.sin(phase)
        elif mode == "refinement":
            return math.cos(phase)
        elif mode == "relations":
            return math.tan(phase)
        else:
            return 0.0
