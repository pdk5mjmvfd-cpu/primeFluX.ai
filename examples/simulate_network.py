#!/usr/bin/env python3
"""
Example: How to Simulate Network Behavior Offline

Offline capsules are stored in the sync queue.
You can simulate network transmission, validation, and state reconstruction.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.sync_queue import SyncQueue
from ApopToSiS.runtime.network_sync_protocol import NetworkSyncProtocol, NSPSyncRequest, NSPSyncResponse
from ApopToSiS.runtime.device_identity import get_device_identity
from ApopToSiS.runtime.state_merge import StateMerge
from ApopToSiS.runtime.distributed_safety import DistributedSafety
import time


def simulate_network_behavior():
    """Simulate network behavior offline."""
    print("=== Simulating Network Behavior Offline ===\n")
    
    # Get device identity
    device = get_device_identity()
    
    # Create sync queue
    queue = SyncQueue()
    
    # Create some capsules
    print("1. Creating capsules...")
    capsules = []
    for i in range(3):
        capsule = Capsule(
            raw_tokens=[f"network", f"test", f"{i}"],
            shell=2,
            entropy=0.5 + i * 0.1,
            curvature=1.0 + i * 0.2,
            timestamp=time.time() + i
        )
        capsules.append(capsule)
        print(f"   Created capsule {i+1}: {capsule.capsule_id[:16]}...")
    
    # Enqueue capsules
    print("\n2. Enqueueing capsules...")
    for capsule in capsules:
        queue.enqueue_capsule(capsule)
    print(f"   Queue size: {queue.get_queue_size()}")
    
    # Dequeue capsules (simulates offline → online sync)
    print("\n3. Dequeueing capsules (offline → online sync)...")
    queued_capsules = queue.dequeue_capsules()
    print(f"   Dequeued {len(queued_capsules)} capsules")
    
    # Simulate network transmission
    print("\n4. Simulating network transmission...")
    protocol = NetworkSyncProtocol(device)
    
    prepared_capsules = []
    for capsule in queued_capsules:
        prepared = protocol.prepare_capsule_for_send(capsule)
        prepared_capsules.append(prepared)
        print(f"   Prepared capsule: {prepared['capsule_id'][:16]}...")
    
    # Simulate receiving and validating
    print("\n5. Validating received capsules...")
    safety = DistributedSafety()
    validated_capsules = []
    
    for capsule_data in prepared_capsules:
        received = protocol.receive_capsule(capsule_data)
        if received:
            is_valid, error = safety.validate_network_capsule(received)
            if is_valid:
                validated_capsules.append(received)
                trust = safety.compute_trust_score(received)
                print(f"   ✓ Validated: trust={trust:.2f}")
            else:
                print(f"   ✗ Invalid: {error}")
        else:
            print(f"   ✗ Failed to decode")
    
    # Reconstruct PFState from validated capsules
    print("\n6. Reconstructing PFState from capsules...")
    merge = StateMerge()
    new_state = merge.merge_capsules(validated_capsules)
    
    print(f"   State reconstructed:")
    print(f"     Shell: {new_state.shell.value if hasattr(new_state.shell, 'value') else new_state.shell}")
    print(f"     Curvature: {new_state.curvature:.4f}")
    print(f"     Entropy: {new_state.entropy:.4f}")
    
    # Clear processed capsules
    print("\n7. Clearing processed capsules...")
    processed_ids = [c.capsule_id for c in validated_capsules]
    queue.clear_processed(processed_ids)
    print(f"   Remaining in queue: {queue.get_queue_size()}")
    
    return validated_capsules, new_state


if __name__ == "__main__":
    capsules, state = simulate_network_behavior()
    print("\n✓ Network simulation complete!")

