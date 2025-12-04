#!/usr/bin/env python3
"""
Example: How to Test QuantaCoin (ΦQ)

Every capsule has:
- compression_ratio
- quanta_hash
- curvature signature
- entropy signature
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.core.quanta import QuantaCompressor
from ApopToSiS.runtime.distributed_safety import DistributedSafety
import time


def test_quanta():
    """Test QuantaCoin computation and trust."""
    print("=== Testing QuantaCoin (ΦQ) ===\n")
    
    # Create compressor
    compressor = QuantaCompressor()
    
    # Create capsule
    print("1. Creating capsule...")
    capsule = Capsule(
        raw_tokens=["quanta", "test", "capsule", "with", "multiple", "tokens"],
        shell=2,
        entropy=0.5,
        curvature=1.0,
        timestamp=time.time()
    )
    
    # Compute compression
    print("\n2. Computing compression...")
    compressed = compressor.compress_capsule(capsule)
    quanta_value = compressor.compute_quanta(capsule)
    hash_value = compressor.hash_capsule(capsule)
    
    print(f"   Raw size: {len(str(capsule.encode()).encode('utf-8'))} bytes")
    print(f"   Compressed size: {len(compressed)} bytes")
    print(f"   QuantaCoin (ΦQ): {quanta_value:.4f}")
    print(f"   Hash: {hash_value[:16]}...")
    
    # Update capsule with compression ratio
    capsule.compression_ratio = quanta_value
    capsule.quanta_hash = hash_value
    
    # Test trust scoring
    print("\n3. Testing trust scoring...")
    safety = DistributedSafety()
    trust_score = safety.compute_trust_score(capsule)
    
    print(f"   Trust score: {trust_score:.4f}")
    print(f"   Trust threshold: 0.5")
    
    if trust_score > 0.5:
        print("   ✓ Capsule passes network trust thresholds")
    else:
        print("   ✗ Capsule below trust threshold")
    
    # Test validation
    print("\n4. Testing capsule validation...")
    is_valid, error = safety.validate_network_capsule(capsule)
    
    if is_valid:
        print("   ✓ Capsule is valid for network transmission")
    else:
        print(f"   ✗ Capsule invalid: {error}")
    
    # Test multiple capsules
    print("\n5. Testing multiple capsules...")
    capsules = []
    for i in range(3):
        c = Capsule(
            raw_tokens=[f"test{i}"] * (i + 1),
            shell=2,
            entropy=0.5 + i * 0.1,
            curvature=1.0 + i * 0.2,
            timestamp=time.time() + i
        )
        c.compression_ratio = compressor.compute_quanta(c)
        c.quanta_hash = compressor.hash_capsule(c)
        capsules.append(c)
        
        trust = safety.compute_trust_score(c)
        print(f"   Capsule {i+1}: Q={c.compression_ratio:.2f}, trust={trust:.2f}")
    
    print("\n✓ QuantaCoin tests complete!")
    return capsules


if __name__ == "__main__":
    capsules = test_quanta()

