# NOTE:
# This module is part of Section 13 (PF Distributed Cognitive Mesh),
# which is NOT active during v3 local runtime.
# Do not import this file in runtime until initialization of PF-DCM.

"""
PF-Distributed Cognitive Mesh Topology (PF-TOPO).

The PF-DCM uses a PF-invariant topology, not geographic or IP-based adjacency.

Nodes are linked by:
1. curvature similarity (κ proximity)
2. distinction density similarity
3. triplet composition match
4. quanta trust score
5. rail interference signature

Adj(A,B) = f(|κA − κB|, |ρA − ρB|, Q_A, Q_B, TripletMatch(A,B), Rail(A,B))
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.device_identity import DeviceIdentity


@dataclass
class MeshNode:
    """
    A node in the PF-Distributed Cognitive Mesh.
    
    Each node:
    - maintains its own PFState
    - maintains its own experience graph
    - merges only capsules, never raw context
    - reconstructs identical results from capsule flow
    - maintains identity continuity by device_id
    - validates others via QuantaCoin
    """
    device_id: str
    instance_id: str
    curvature: float = 0.0
    density: float = 0.0
    quanta_trust: float = 0.0
    triplet_signature: dict[str, Any] = field(default_factory=dict)
    rail_interference: float = 0.0
    last_seen: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MeshEdge:
    """
    An edge in the PF mesh topology.
    
    Represents PF-invariant adjacency between nodes.
    """
    source_node: str  # device_id
    target_node: str  # device_id
    curvature_proximity: float = 0.0
    density_proximity: float = 0.0
    quanta_trust_combined: float = 0.0
    triplet_match: float = 0.0
    rail_compatibility: float = 0.0
    adjacency_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class PFTopology:
    """
    PF-invariant mesh topology.
    
    Creates a mathematical mesh, not a network-topological one.
    Nodes cluster by PF curvature similarity, not geographic proximity.
    """

    def __init__(self) -> None:
        """Initialize PF topology."""
        self.nodes: dict[str, MeshNode] = {}
        self.edges: list[MeshEdge] = []

    def add_node(self, node: MeshNode) -> None:
        """
        Add node to mesh.

        Args:
            node: Mesh node
        """
        self.nodes[node.device_id] = node

    def compute_adjacency(self, node_a: MeshNode, node_b: MeshNode) -> float:
        """
        Compute PF-invariant adjacency between two nodes.
        
        Adj(A,B) = f(|κA − κB|, |ρA − ρB|, Q_A, Q_B, TripletMatch(A,B), Rail(A,B))

        Args:
            node_a: First node
            node_b: Second node

        Returns:
            Adjacency score (0.0 to 1.0, higher = more similar)
        """
        # Curvature proximity (inverse distance)
        curvature_diff = abs(node_a.curvature - node_b.curvature)
        curvature_proximity = 1.0 / (1.0 + curvature_diff)
        
        # Density proximity
        density_diff = abs(node_a.density - node_b.density)
        density_proximity = 1.0 / (1.0 + density_diff)
        
        # QuantaCoin trust (average)
        quanta_combined = (node_a.quanta_trust + node_b.quanta_trust) / 2.0
        
        # Triplet match (simplified - compare signatures)
        triplet_match = self._compute_triplet_match(node_a, node_b)
        
        # Rail compatibility
        rail_compatibility = 1.0 - abs(node_a.rail_interference - node_b.rail_interference) / 10.0
        rail_compatibility = max(0.0, min(1.0, rail_compatibility))
        
        # Combined adjacency score
        adjacency = (
            curvature_proximity * 0.3 +
            density_proximity * 0.2 +
            quanta_combined * 0.2 +
            triplet_match * 0.15 +
            rail_compatibility * 0.15
        )
        
        return adjacency

    def _compute_triplet_match(self, node_a: MeshNode, node_b: MeshNode) -> float:
        """
        Compute triplet composition match.

        Args:
            node_a: First node
            node_b: Second node

        Returns:
            Match score (0.0 to 1.0)
        """
        sig_a = node_a.triplet_signature
        sig_b = node_b.triplet_signature
        
        if not sig_a or not sig_b:
            return 0.5  # Neutral if no signatures
        
        # Compare signature keys
        keys_a = set(sig_a.keys())
        keys_b = set(sig_b.keys())
        
        if not keys_a and not keys_b:
            return 1.0
        
        intersection = len(keys_a & keys_b)
        union = len(keys_a | keys_b)
        
        return intersection / union if union > 0 else 0.0

    def update_node_from_capsule(self, device_id: str, capsule: Capsule) -> None:
        """
        Update node state from capsule.

        Args:
            device_id: Device ID
            capsule: Capsule to extract state from
        """
        if device_id not in self.nodes:
            self.nodes[device_id] = MeshNode(
                device_id=device_id,
                instance_id=capsule.session_id,
            )
        
        node = self.nodes[device_id]
        node.curvature = capsule.curvature
        node.density = capsule.density
        node.quanta_trust = capsule.compression_ratio
        node.rail_interference = capsule.rail_interference
        node.last_seen = capsule.timestamp
        
        # Update triplet signature
        node.triplet_signature = {
            "count": len(capsule.triplets),
            "types": [t.get("type", "unknown") for t in capsule.triplets if isinstance(t, dict)],
        }

    def find_similar_nodes(self, target_node: MeshNode, threshold: float = 0.5) -> list[MeshNode]:
        """
        Find nodes similar to target node.

        Args:
            target_node: Target node
            threshold: Minimum adjacency score

        Returns:
            List of similar nodes
        """
        similar = []
        
        for node in self.nodes.values():
            if node.device_id == target_node.device_id:
                continue
            
            adjacency = self.compute_adjacency(target_node, node)
            if adjacency >= threshold:
                similar.append((node, adjacency))
        
        # Sort by adjacency score
        similar.sort(key=lambda x: x[1], reverse=True)
        
        return [node for node, _ in similar]

    def build_mesh_edges(self, threshold: float = 0.5) -> list[MeshEdge]:
        """
        Build mesh edges based on PF adjacency.

        Args:
            threshold: Minimum adjacency for edge creation

        Returns:
            List of mesh edges
        """
        edges = []
        
        node_list = list(self.nodes.values())
        for i, node_a in enumerate(node_list):
            for node_b in node_list[i+1:]:
                adjacency = self.compute_adjacency(node_a, node_b)
                
                if adjacency >= threshold:
                    edge = MeshEdge(
                        source_node=node_a.device_id,
                        target_node=node_b.device_id,
                        curvature_proximity=1.0 / (1.0 + abs(node_a.curvature - node_b.curvature)),
                        density_proximity=1.0 / (1.0 + abs(node_a.density - node_b.density)),
                        quanta_trust_combined=(node_a.quanta_trust + node_b.quanta_trust) / 2.0,
                        triplet_match=self._compute_triplet_match(node_a, node_b),
                        rail_compatibility=1.0 - abs(node_a.rail_interference - node_b.rail_interference) / 10.0,
                        adjacency_score=adjacency,
                    )
                    edges.append(edge)
        
        self.edges = edges
        return edges

