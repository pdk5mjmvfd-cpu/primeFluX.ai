#!/usr/bin/env python3
"""
Example: PF-DCM Mesh Demonstration

Demonstrates PF-Distributed Cognitive Mesh concepts:
- PF topology formation
- Curvature routing
- Consensus validation
- QuantaCoin economy
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mesh.pf_topology import PFTopology, MeshNode
from mesh.curvature_routing import CurvatureRouter
from mesh.pf_consensus import PFConsensus
from mesh.quanta_economy import QuantaEconomy
from mesh.mesh_cognition import MeshCognition
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.math.shells import Shell
import time


def demonstrate_pf_dcm():
    """Demonstrate PF-DCM concepts."""
    print("=== PF-Distributed Cognitive Mesh Demo ===\n")
    
    # 1. Create PF topology
    print("1. Creating PF Topology...")
    topology = PFTopology()
    
    # Create multiple nodes (simulating different devices)
    nodes = []
    for i in range(5):
        node = MeshNode(
            device_id=f"device_{i}",
            instance_id=f"inst_{i}",
            curvature=1.0 + i * 0.5,
            density=0.5 + i * 0.1,
            quanta_trust=1.0 + i * 0.2,
            rail_interference=i * 0.5,
        )
        topology.add_node(node)
        nodes.append(node)
        print(f"   Node {i}: curvature={node.curvature:.2f}, trust={node.quanta_trust:.2f}")
    
    # 2. Compute adjacency
    print("\n2. Computing PF Adjacency...")
    for i in range(len(nodes) - 1):
        adj = topology.compute_adjacency(nodes[i], nodes[i+1])
        print(f"   Adj(device_{i}, device_{i+1}): {adj:.4f}")
    
    # 3. Build mesh edges
    print("\n3. Building Mesh Edges...")
    edges = topology.build_mesh_edges(threshold=0.3)
    print(f"   Created {len(edges)} edges")
    
    # 4. Test curvature routing
    print("\n4. Testing Curvature Routing...")
    router = CurvatureRouter(topology)
    capsule = Capsule(
        raw_tokens=["mesh", "test"],
        shell=2,
        entropy=0.5,
        curvature=1.5,
        timestamp=time.time()
    )
    targets = router.route_capsule(capsule, nodes, max_routes=3)
    print(f"   Routed capsule (curvature={capsule.curvature:.2f}) to {len(targets)} nodes")
    for target in targets:
        print(f"     → {target.device_id} (curvature={target.curvature:.2f})")
    
    # 5. Test consensus
    print("\n5. Testing PF Consensus...")
    consensus = PFConsensus()
    checks = consensus.validate_capsule_for_consensus(capsule)
    instant = consensus.is_instant_consensus(capsule)
    print(f"   Validation: {sum(checks.values())}/{len(checks)} checks passed")
    print(f"   Instant consensus: {instant}")
    
    # 6. Test QuantaCoin economy
    print("\n6. Testing QuantaCoin Economy...")
    economy = QuantaEconomy()
    for i, node in enumerate(nodes):
        test_capsule = Capsule(
            raw_tokens=[f"test{i}"],
            shell=2,
            entropy=0.5,
            curvature=node.curvature,
            timestamp=time.time() + i,
            compression_ratio=node.quanta_trust
        )
        economy.update_device_reputation(node.device_id, test_capsule)
    
    top_devices = economy.get_top_devices(n=3)
    print(f"   Top 3 devices:")
    for rep in top_devices:
        print(f"     {rep.device_id}: {rep.reputation_tier}, trust={rep.trust_score:.2f}")
    
    # 7. Test mesh cognition
    print("\n7. Testing Mesh Cognition...")
    local_device_id = nodes[0].device_id
    mesh_cog = MeshCognition(topology, local_device_id)
    
    result = mesh_cog.process_capsule_through_mesh(
        capsule,
        PFState(shell=Shell.MEASUREMENT, curvature=1.5, entropy=0.5),
        {}  # Empty agents dict for demo
    )
    
    print(f"   Mesh processing: {result.get('processed', False)}")
    print(f"   Target nodes: {result.get('target_nodes', 0)}")
    print(f"   Consensus: {result.get('consensus', False)}")
    
    # 8. Form cluster
    print("\n8. Forming PF Cluster...")
    cluster = mesh_cog.form_cluster(nodes[0], cluster_threshold=0.4)
    print(f"   Cluster size: {len(cluster)} nodes")
    
    # 9. Compute mesh curvature
    print("\n9. Computing Global Mesh Curvature...")
    mesh_curvature = mesh_cog.compute_mesh_curvature()
    print(f"   Global mesh curvature: {mesh_curvature:.4f}")
    
    print("\n✓ PF-DCM demonstration complete!")
    return topology, mesh_cog


if __name__ == "__main__":
    topology, mesh_cog = demonstrate_pf_dcm()

