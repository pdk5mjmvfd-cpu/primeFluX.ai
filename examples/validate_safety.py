#!/usr/bin/env python3
"""
Example: How to Validate Local Safety (Network + Cognitive)

Safety is validated via DistributedSafety.
Tests include:
- shell transitions
- curvature consistency
- triplet validity
- PF rail compatibility
- QuantaCoin trust threshold
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.distributed_safety import DistributedSafety
from ApopToSiS.core.quanta import QuantaCompressor
import time


def validate_safety():
    """Validate capsule safety."""
    print("=== Validating Local Safety ===\n")
    
    safety = DistributedSafety()
    compressor = QuantaCompressor()
    
    # Create valid capsule
    print("1. Testing valid capsule...")
    valid_capsule = Capsule(
        raw_tokens=["valid", "test"],
        shell=2,
        entropy=0.5,
        curvature=1.0,
        timestamp=time.time()
    )
    valid_capsule.compression_ratio = compressor.compute_quanta(valid_capsule)
    valid_capsule.quanta_hash = compressor.hash_capsule(valid_capsule)
    
    is_valid, error = safety.validate_network_capsule(valid_capsule)
    trust = safety.compute_trust_score(valid_capsule)
    
    print(f"   Valid: {is_valid}")
    print(f"   Trust: {trust:.4f}")
    if is_valid:
        print("   ✓ Capsule is safe for network transmission")
    
    # Test invalid capsules
    print("\n2. Testing invalid capsules...")
    
    # Invalid shell
    invalid_shell = Capsule(
        raw_tokens=["invalid"],
        shell=99,  # Invalid shell
        entropy=0.5,
        curvature=1.0,
        timestamp=time.time()
    )
    invalid_shell.compression_ratio = 1.5
    invalid_shell.quanta_hash = "test"
    is_valid, error = safety.validate_network_capsule(invalid_shell)
    print(f"   Invalid shell: valid={is_valid}, error='{error}'")
    
    # Invalid curvature
    invalid_curvature = Capsule(
        raw_tokens=["invalid"],
        shell=2,
        entropy=0.5,
        curvature=999.0,  # Too high
        timestamp=time.time()
    )
    invalid_curvature.compression_ratio = 1.5
    invalid_curvature.quanta_hash = "test"
    is_valid, error = safety.validate_network_capsule(invalid_curvature)
    print(f"   Invalid curvature: valid={is_valid}, error='{error}'")
    
    # Low trust (low compression)
    low_trust = Capsule(
        raw_tokens=["low", "trust"],
        shell=2,
        entropy=0.5,
        curvature=1.0,
        timestamp=time.time()
    )
    low_trust.compression_ratio = 0.5  # Below threshold
    low_trust.quanta_hash = compressor.hash_capsule(low_trust)
    is_valid, error = safety.validate_network_capsule(low_trust)
    trust = safety.compute_trust_score(low_trust)
    print(f"   Low trust: valid={is_valid}, trust={trust:.4f}, error='{error}'")
    
    # Test shell transition validation
    print("\n3. Testing shell transition validation...")
    prev_capsule = Capsule(
        raw_tokens=["prev"],
        shell=2,
        entropy=0.5,
        curvature=1.0,
        timestamp=time.time()
    )
    
    # Valid transition: 2 → 3
    valid_transition = Capsule(
        raw_tokens=["next"],
        shell=3,
        entropy=0.6,
        curvature=1.2,
        timestamp=time.time() + 1
    )
    is_valid, error = safety.validate_shell_transition(valid_transition, prev_capsule)
    print(f"   Valid transition (2→3): {is_valid}")
    
    # Invalid transition: 2 → 4 (skips 3)
    invalid_transition = Capsule(
        raw_tokens=["next"],
        shell=4,
        entropy=0.6,
        curvature=1.2,
        timestamp=time.time() + 1
    )
    is_valid, error = safety.validate_shell_transition(invalid_transition, prev_capsule)
    print(f"   Invalid transition (2→4): {is_valid}, error='{error}'")
    
    # Test curvature consistency
    print("\n4. Testing curvature consistency...")
    consistent = Capsule(
        raw_tokens=["consistent"],
        shell=3,
        entropy=0.6,
        curvature=1.1,  # Small change
        timestamp=time.time() + 1
    )
    is_valid, error = safety.validate_curvature_consistency(consistent, prev_capsule)
    print(f"   Consistent curvature: {is_valid}")
    
    inconsistent = Capsule(
        raw_tokens=["inconsistent"],
        shell=3,
        entropy=0.6,
        curvature=50.0,  # Huge jump
        timestamp=time.time() + 1
    )
    is_valid, error = safety.validate_curvature_consistency(inconsistent, prev_capsule)
    print(f"   Inconsistent curvature: {is_valid}, error='{error}'")
    
    print("\n✓ Safety validation tests complete!")


if __name__ == "__main__":
    validate_safety()

