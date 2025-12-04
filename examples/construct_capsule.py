#!/usr/bin/env python3
"""
Example: How to Construct a Capsule (Manually)

A capsule is the fundamental unit of cognition and network transport.
Every input → a capsule
Every output → a capsule
Every experience delta → a capsule
Every state update → a capsule
Every agent interaction → a capsule
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.device_identity import get_device_identity
import time


def construct_capsule_manually():
    """Construct a capsule manually."""
    print("=== Constructing Capsule Manually ===\n")
    
    # Get device identity
    device = get_device_identity()
    
    # Construct capsule
    capsule = Capsule(
        raw_tokens=["hello", "apop"],
        triplets=[],
        shell=0,
        entropy=0.12,
        curvature=0.03,
        density=0.01,
        psi=1.0,
        hamiltonian=0.0,
        reptend_entropy=0.0,
        rail_interference=0.0,
        timestamp=time.time(),
        device_id=device.get_device_id(),
        session_id=device.get_instance_id(),
    )
    
    print(f"Capsule created:")
    print(f"  Device ID: {capsule.device_id[:16]}...")
    print(f"  Capsule ID: {capsule.capsule_id[:16]}...")
    print(f"  Tokens: {capsule.raw_tokens}")
    print(f"  Shell: {capsule.shell}")
    print(f"  Entropy: {capsule.entropy:.4f}")
    print(f"  Curvature: {capsule.curvature:.4f}")
    
    return capsule


def construct_capsule_via_lcm():
    """Construct a capsule via LCM (recommended)."""
    print("\n=== Constructing Capsule via LCM (Recommended) ===\n")
    
    from core.lcm import LCM
    from core.icm import ICM
    
    # Initialize LCM
    icm = ICM()
    lcm = LCM(icm)
    
    # Process tokens
    tokens = ["hello", "apop"]
    lcm.process_tokens(tokens)
    
    # Generate capsule
    capsule_dict = lcm.generate_capsule()
    capsule = Capsule.decode(capsule_dict) if isinstance(capsule_dict, dict) else Capsule(raw_tokens=tokens)
    
    print(f"Capsule created via LCM:")
    print(f"  Tokens: {capsule.raw_tokens}")
    print(f"  Shell: {capsule.shell}")
    print(f"  Entropy: {capsule.entropy:.4f}")
    print(f"  Curvature: {capsule.curvature:.4f}")
    print(f"  Triplets: {len(capsule.triplets)}")
    
    return capsule


if __name__ == "__main__":
    # Manual construction
    manual_capsule = construct_capsule_manually()
    
    # LCM construction (recommended)
    lcm_capsule = construct_capsule_via_lcm()
    
    print("\n✓ Both methods work!")

