# NOTE:
# This module is part of Section 13 (PF Distributed Cognitive Mesh),
# which is NOT active during v3 local runtime.
# Do not import this file in runtime until initialization of PF-DCM.

"""
Distributed Curvature Routing (PF-CR).

Routing a capsule to other nodes uses curvature:

Route(capsule, nodes) = argmin | κ_node − κ_capsule |

Capsules flow toward nodes whose internal PF curvature best matches
the capsule's curvature signature.
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.capsules import Capsule
from mesh.pf_topology import MeshNode, PFTopology


class CurvatureRouter:
    """
    PF-Curvature Router.
    
    Routes capsules to nodes based on curvature similarity.
    Creates PF-aligned clusters dynamically.
    """

    def __init__(self, topology: PFTopology) -> None:
        """
        Initialize curvature router.

        Args:
            topology: PF topology
        """
        self.topology = topology
        self.trust_threshold = 0.5  # Minimum QuantaCoin trust

    def route_capsule(
        self,
        capsule: Capsule,
        available_nodes: list[MeshNode],
        max_routes: int = 3
    ) -> list[MeshNode]:
        """
        Route capsule to nodes based on curvature.
        
        Route(capsule, nodes) = argmin | κ_node − κ_capsule |
        
        Capsules may fork into multiple nodes.
        Nodes may decline if trust (Q) < threshold.

        Args:
            capsule: Capsule to route
            available_nodes: List of available nodes
            max_routes: Maximum number of nodes to route to

        Returns:
            List of target nodes (sorted by curvature match)
        """
        # Filter nodes by trust threshold
        trusted_nodes = [
            node for node in available_nodes
            if node.quanta_trust >= self.trust_threshold
        ]
        
        if not trusted_nodes:
            return []
        
        # Compute curvature distance for each node
        curvature_distances = []
        for node in trusted_nodes:
            distance = abs(node.curvature - capsule.curvature)
            curvature_distances.append((node, distance))
        
        # Sort by curvature distance (closest first)
        curvature_distances.sort(key=lambda x: x[1])
        
        # Select top N nodes
        selected = [node for node, _ in curvature_distances[:max_routes]]
        
        return selected

    def route_with_full_adjacency(
        self,
        capsule: Capsule,
        source_node: MeshNode,
        max_routes: int = 3
    ) -> list[MeshNode]:
        """
        Route capsule using full PF adjacency (not just curvature).
        
        Uses complete adjacency function:
        Adj(A,B) = f(|κA − κB|, |ρA − ρB|, Q_A, Q_B, TripletMatch(A,B), Rail(A,B))

        Args:
            capsule: Capsule to route
            source_node: Source node
            max_routes: Maximum routes

        Returns:
            List of target nodes
        """
        # Create temporary node from capsule
        capsule_node = MeshNode(
            device_id=capsule.device_id,
            instance_id=capsule.session_id,
            curvature=capsule.curvature,
            density=capsule.density,
            quanta_trust=capsule.compression_ratio,
            rail_interference=capsule.rail_interference,
        )
        
        # Find similar nodes using full adjacency
        similar_nodes = self.topology.find_similar_nodes(
            capsule_node,
            threshold=0.5
        )
        
        # Filter by trust
        trusted = [
            node for node in similar_nodes
            if node.quanta_trust >= self.trust_threshold
        ]
        
        return trusted[:max_routes]

    def can_fork(self, capsule: Capsule) -> bool:
        """
        Determine if capsule can fork to multiple nodes.
        
        High-entropy capsules can fork.
        Low-entropy capsules route to single node.

        Args:
            capsule: Capsule to check

        Returns:
            True if capsule can fork
        """
        # High entropy = can fork (more possibilities)
        return capsule.entropy > 1.0

    def should_decline(self, node: MeshNode, capsule: Capsule) -> bool:
        """
        Determine if node should decline capsule.
        
        Nodes decline if:
        - Trust too low
        - Curvature mismatch too large
        - Capacity exceeded

        Args:
            node: Node to check
            capsule: Capsule to check

        Returns:
            True if node should decline
        """
        # Trust check
        if node.quanta_trust < self.trust_threshold:
            return True
        
        # Curvature mismatch
        curvature_diff = abs(node.curvature - capsule.curvature)
        if curvature_diff > 10.0:  # Too different
            return True
        
        return False

