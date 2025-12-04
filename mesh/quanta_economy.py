# NOTE:
# This module is part of Section 13 (PF Distributed Cognitive Mesh),
# which is NOT active during v3 local runtime.
# Do not import this file in runtime until initialization of PF-DCM.

"""
QuantaCoin Economy (ΦQ-NET).

Distributed QuantaCoin introduces:
- compression validation
- trust ranking
- priority routing
- agent reputation
- device quality scoring

Capsules with high Q:
- propagate further
- influence cluster formation
- gain priority in remote agent invocation

Nodes with low Q:
- are deprioritized
- require more validation
- may be partially isolated
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from ApopToSiS.runtime.capsules import Capsule
from mesh.pf_topology import MeshNode
from collections import defaultdict


@dataclass
class DeviceReputation:
    """
    Device reputation in QuantaCoin economy.
    """
    device_id: str
    average_quanta: float = 0.0
    total_capsules: int = 0
    trust_score: float = 0.0
    reputation_tier: str = "unknown"  # bronze, silver, gold, platinum


class QuantaEconomy:
    """
    QuantaCoin Economy Manager.
    
    Manages trust ranking, priority routing, and device reputation.
    """

    def __init__(self) -> None:
        """Initialize QuantaCoin economy."""
        self.device_reputations: dict[str, DeviceReputation] = {}
        self.quanta_history: dict[str, list[float]] = defaultdict(list)

    def update_device_reputation(
        self,
        device_id: str,
        capsule: Capsule
    ) -> None:
        """
        Update device reputation from capsule.

        Args:
            device_id: Device ID
            capsule: Capsule to process
        """
        if device_id not in self.device_reputations:
            self.device_reputations[device_id] = DeviceReputation(device_id=device_id)
        
        rep = self.device_reputations[device_id]
        
        # Update quanta history
        quanta_value = capsule.compression_ratio
        self.quanta_history[device_id].append(quanta_value)
        
        # Keep last 100 capsules
        if len(self.quanta_history[device_id]) > 100:
            self.quanta_history[device_id] = self.quanta_history[device_id][-100:]
        
        # Update average
        history = self.quanta_history[device_id]
        rep.average_quanta = sum(history) / len(history) if history else 0.0
        rep.total_capsules += 1
        
        # Update trust score (moving average)
        rep.trust_score = rep.average_quanta
        
        # Update reputation tier
        if rep.average_quanta >= 2.0:
            rep.reputation_tier = "platinum"
        elif rep.average_quanta >= 1.5:
            rep.reputation_tier = "gold"
        elif rep.average_quanta >= 1.0:
            rep.reputation_tier = "silver"
        else:
            rep.reputation_tier = "bronze"

    def get_device_reputation(self, device_id: str) -> DeviceReputation:
        """
        Get device reputation.

        Args:
            device_id: Device ID

        Returns:
            Device reputation
        """
        if device_id not in self.device_reputations:
            return DeviceReputation(device_id=device_id)
        
        return self.device_reputations[device_id]

    def compute_priority(
        self,
        capsule: Capsule,
        target_nodes: list[MeshNode]
    ) -> list[tuple[MeshNode, float]]:
        """
        Compute priority for routing capsule to nodes.
        
        Higher Q = higher priority.

        Args:
            capsule: Capsule to route
            target_nodes: List of target nodes

        Returns:
            List of (node, priority_score) tuples, sorted by priority
        """
        priorities = []
        
        for node in target_nodes:
            # Get device reputation
            rep = self.get_device_reputation(node.device_id)
            
            # Priority = capsule Q * device reputation
            priority = capsule.compression_ratio * rep.trust_score
            
            priorities.append((node, priority))
        
        # Sort by priority (highest first)
        priorities.sort(key=lambda x: x[1], reverse=True)
        
        return priorities

    def should_propagate(self, capsule: Capsule, max_hops: int = 5) -> bool:
        """
        Determine if capsule should propagate further.
        
        High Q capsules propagate further.

        Args:
            capsule: Capsule to check
            max_hops: Maximum propagation hops

        Returns:
            True if should propagate
        """
        # High Q = can propagate
        return capsule.compression_ratio >= 1.5

    def should_isolate(self, device_id: str) -> bool:
        """
        Determine if device should be isolated.
        
        Low Q devices may be isolated.

        Args:
            device_id: Device ID

        Returns:
            True if should isolate
        """
        rep = self.get_device_reputation(device_id)
        
        # Isolate if trust score too low
        return rep.trust_score < 0.3

    def get_top_devices(self, n: int = 10) -> list[DeviceReputation]:
        """
        Get top N devices by reputation.

        Args:
            n: Number of devices

        Returns:
            List of top device reputations
        """
        reputations = list(self.device_reputations.values())
        reputations.sort(key=lambda r: r.trust_score, reverse=True)
        
        return reputations[:n]

