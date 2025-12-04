"""
Test Capsules — JSON-Flux transport layer tests.

Tests:
- Encoding
- Decoding
- Structural consistency
- Merging
"""

import pytest
import time
from ApopToSiS.runtime.capsules import Capsule


def test_capsule_encode_decode():
    """Test capsule encoding and decoding."""
    capsule = Capsule(
        raw_tokens=["test"],
        triplets=[{"a": 0.0, "b": 1.0, "c": 1.414, "type": "presence"}],
        entropy=0.5,
        curvature=1.2,
        shell=2,
        density=0.3,
        psi=0.8,
        hamiltonian=1.1,
        reptend_entropy=0.2,
        rail_interference=1.0,
        timestamp=time.time()
    )
    
    encoded = capsule.encode()
    decoded = Capsule.decode(encoded)
    
    assert decoded.raw_tokens == capsule.raw_tokens
    assert abs(decoded.entropy - capsule.entropy) < 0.001
    assert abs(decoded.curvature - capsule.curvature) < 0.001
    assert decoded.shell == capsule.shell


def test_capsule_merge():
    """Test capsule merging."""
    capsule1 = Capsule(
        raw_tokens=["hello"],
        triplets=[],
        entropy=0.5,
        curvature=1.0,
        shell=2,
        density=0.3,
        psi=0.8,
        hamiltonian=1.0,
        reptend_entropy=0.1,
        rail_interference=0.5,
        timestamp=time.time()
    )
    
    capsule2 = Capsule(
        raw_tokens=["world"],
        triplets=[],
        entropy=0.7,
        curvature=1.4,
        shell=3,
        density=0.5,
        psi=1.0,
        hamiltonian=1.2,
        reptend_entropy=0.2,
        rail_interference=1.0,
        timestamp=time.time()
    )
    
    merged = capsule1.merge(capsule2)
    
    assert "hello" in merged.raw_tokens
    assert "world" in merged.raw_tokens
    assert merged.shell == max(capsule1.shell, capsule2.shell)
    assert abs(merged.entropy - (capsule1.entropy + capsule2.entropy) / 2.0) < 0.001


def test_capsule_to_dict():
    """Test capsule to_dict conversion."""
    capsule = Capsule(
        raw_tokens=["test"],
        entropy=0.5,
        curvature=1.2,
        shell=2,
        timestamp=time.time()
    )
    
    capsule_dict = capsule.to_dict()
    
    assert isinstance(capsule_dict, dict)
    assert "raw_tokens" in capsule_dict
    assert "entropy" in capsule_dict
    assert "curvature" in capsule_dict
    assert "shell" in capsule_dict

