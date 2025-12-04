#!/usr/bin/env python3
"""
Example: How to Test PF-State Merge Locally

PFState merging relies on:
- ordered capsules
- device_id precedence
- chain continuity
- QuantaCoin trust
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state_merge import StateMerge
from ApopToSiS.runtime.device_identity import get_device_identity
import time


def test_state_merge():
    """Test PF-state merge locally."""
    print("=== Testing PF-State Merge ===\n")
    
    device = get_device_identity()
    
    # Create capsules from different "devices" (simulated)
    print("1. Creating capsules from different devices...")
    capsules = []
    
    # Device 1 capsules
    prev_id = None
    for i in range(3):
        capsule = Capsule(
            raw_tokens=[f"device1", f"capsule{i}"],
            shell=2 + (i % 2),
            entropy=0.5 + i * 0.1,
            curvature=1.0 + i * 0.2,
            timestamp=time.time() + i,
            device_id=device.get_device_id(),
            prev_capsule_id=prev_id or "",
        )
        prev_id = capsule.capsule_id
        capsules.append(capsule)
        print(f"   Device 1 capsule {i+1}: shell={capsule.shell}, curvature={capsule.curvature:.2f}")
    
    # Device 2 capsules (simulated different device)
    device2_id = "device2_" + device.get_device_id()[:16]
    prev_id = None
    for i in range(2):
        capsule = Capsule(
            raw_tokens=[f"device2", f"capsule{i}"],
            shell=2 + (i % 2),
            entropy=0.6 + i * 0.1,
            curvature=1.2 + i * 0.2,
            timestamp=time.time() + 10 + i,  # Later timestamps
            device_id=device2_id,
            prev_capsule_id=prev_id or "",
        )
        prev_id = capsule.capsule_id
        capsules.append(capsule)
        print(f"   Device 2 capsule {i+1}: shell={capsule.shell}, curvature={capsule.curvature:.2f}")
    
    # Merge capsules
    print("\n2. Merging capsules...")
    merge = StateMerge()
    new_state = merge.merge_capsules(capsules, device_id=device.get_device_id())
    
    print(f"   Merged state:")
    print(f"     Shell: {new_state.shell.value if hasattr(new_state.shell, 'value') else new_state.shell}")
    print(f"     Curvature: {new_state.curvature:.4f}")
    print(f"     Entropy: {new_state.entropy:.4f}")
    print(f"     History length: {len(new_state.history)}")
    
    # Test integrity
    print("\n3. Testing integrity...")
    assert new_state.shell.value in [0, 2, 3, 4] if hasattr(new_state.shell, 'value') else new_state.shell in [0, 2, 3, 4], "Invalid shell"
    assert len(new_state.history) == len(capsules), "History length mismatch"
    print("   ✓ Integrity checks passed")
    
    # Test conflict resolution
    print("\n4. Testing conflict resolution...")
    # Create conflicting capsules (same timestamp)
    conflict_capsules = [
        Capsule(
            raw_tokens=["conflict1"],
            shell=2,
            entropy=0.5,
            curvature=1.0,
            timestamp=time.time() + 100,
            compression_ratio=1.5,  # Lower trust
        ),
        Capsule(
            raw_tokens=["conflict2"],
            shell=3,
            entropy=0.6,
            curvature=1.2,
            timestamp=time.time() + 100,  # Same timestamp
            compression_ratio=2.0,  # Higher trust
        ),
    ]
    
    resolved = merge.resolve_conflicts(conflict_capsules, time.time() + 100)
    print(f"   Resolved {len(conflict_capsules)} conflicts to {len(resolved)} capsules")
    if resolved:
        print(f"   Selected capsule: shell={resolved[0].shell}, compression={resolved[0].compression_ratio:.2f}")
    
    # Test chain validation
    print("\n5. Testing chain validation...")
    is_valid, error = merge.validate_capsule_chain(capsules)
    print(f"   Chain valid: {is_valid}")
    if not is_valid:
        print(f"   Error: {error}")
    
    print("\n✓ State merge tests complete!")
    return new_state


if __name__ == "__main__":
    state = test_state_merge()

