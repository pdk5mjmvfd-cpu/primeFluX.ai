# NOTE:
# This module is part of Section 13 (PF Distributed Cognitive Mesh),
# which is NOT active during v3 local runtime.
# Do not import this file in runtime until initialization of PF-DCM.

"""
Remote Agent Invocation (RAI).

Any node can ask another node: "Run an agent for me."

Protocol:
1. Send capsule
2. Remote node routes capsule to one of its agents
3. Remote agent transforms capsule
4. Remote node returns transformed capsule
5. Local node integrates capsule
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.agents.base.base_agent import PFBaseAgent
from mesh.curvature_routing import CurvatureRouter
from mesh.pf_topology import MeshNode


@dataclass
class RemoteAgentRequest:
    """
    Request to invoke remote agent.
    """
    capsule: Capsule
    source_device_id: str
    target_device_id: str
    agent_name: str | None = None  # None = let remote node choose
    metadata: dict[str, Any] = None


@dataclass
class RemoteAgentResponse:
    """
    Response from remote agent invocation.
    """
    transformed_capsule: Capsule
    agent_name: str
    source_device_id: str
    target_device_id: str
    processing_time: float = 0.0
    metadata: dict[str, Any] = None


class RemoteAgentInvocation:
    """
    Remote Agent Invocation handler.
    
    Enables distributed reasoning, delegation, and agent borrowing.
    """

    def __init__(self, local_agents: dict[str, PFBaseAgent]) -> None:
        """
        Initialize RAI handler.

        Args:
            local_agents: Dictionary of local agents (name -> agent)
        """
        self.local_agents = local_agents

    def handle_remote_request(
        self,
        request: RemoteAgentRequest
    ) -> RemoteAgentResponse:
        """
        Handle incoming remote agent request.
        
        Routes capsule to appropriate agent and returns transformed capsule.

        Args:
            request: Remote agent request

        Returns:
            Remote agent response
        """
        import time
        start_time = time.time()
        
        # Select agent
        if request.agent_name and request.agent_name in self.local_agents:
            agent = self.local_agents[request.agent_name]
        else:
            # Let local routing decide
            # In full implementation, would use Supervisor routing
            agent = list(self.local_agents.values())[0]  # Simplified
        
        # Transform capsule
        transformed = agent.transform(request.capsule)
        
        processing_time = time.time() - start_time
        
        return RemoteAgentResponse(
            transformed_capsule=transformed,
            agent_name=agent.name if hasattr(agent, 'name') else "unknown",
            source_device_id=request.target_device_id,  # Response source
            target_device_id=request.source_device_id,  # Response target
            processing_time=processing_time,
        )

    def create_remote_request(
        self,
        capsule: Capsule,
        target_device_id: str,
        agent_name: str | None = None
    ) -> RemoteAgentRequest:
        """
        Create remote agent request.

        Args:
            capsule: Capsule to send
            target_device_id: Target device
            agent_name: Optional specific agent

        Returns:
            Remote agent request
        """
        return RemoteAgentRequest(
            capsule=capsule,
            source_device_id=capsule.device_id,
            target_device_id=target_device_id,
            agent_name=agent_name,
        )

    def find_specialized_agents(
        self,
        topology: PFTopology,
        agent_type: str
    ) -> list[MeshNode]:
        """
        Find nodes with specialized agents.
        
        Example: Find nodes with "Financial Praxis" or "Physics Aegis" agents.

        Args:
            topology: PF topology
            agent_type: Type of agent to find (e.g., "financial_praxis")

        Returns:
            List of nodes with matching agents
        """
        # In full implementation, would query mesh for agent registry
        # For now, return nodes with high trust (likely to have good agents)
        nodes = [
            node for node in topology.nodes.values()
            if node.quanta_trust > 0.7
        ]
        
        # Sort by trust
        nodes.sort(key=lambda n: n.quanta_trust, reverse=True)
        
        return nodes

