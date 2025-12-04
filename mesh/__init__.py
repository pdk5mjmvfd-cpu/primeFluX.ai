"""
PF-Distributed Cognitive Mesh (PF-DCM).

Multi-node, network-level cognitive architecture.

This module defines the specification and architecture for PF-DCM.
Network transport and mesh coordinator implementation will be in Section 14.
"""

from .pf_topology import PFTopology, MeshNode, MeshEdge
from .curvature_routing import CurvatureRouter
from .remote_agent_invocation import RemoteAgentInvocation, RemoteAgentRequest, RemoteAgentResponse
from .pf_consensus import PFConsensus, ConsensusVote, ConsensusResult
from .quanta_economy import QuantaEconomy, DeviceReputation
from .mesh_cognition import MeshCognition

__all__ = [
    "PFTopology",
    "MeshNode",
    "MeshEdge",
    "CurvatureRouter",
    "RemoteAgentInvocation",
    "RemoteAgentRequest",
    "RemoteAgentResponse",
    "PFConsensus",
    "ConsensusVote",
    "ConsensusResult",
    "QuantaEconomy",
    "DeviceReputation",
    "MeshCognition",
]

