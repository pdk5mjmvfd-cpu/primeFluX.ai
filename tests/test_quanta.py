"""
Test Quanta — memory compression tests.

Tests:
- Memory compression works
- Hashing works
- Q value is defined
"""

import pytest
import time
from ApopToSiS.core.quanta import QuantaCompressor
from ApopToSiS.runtime.capsules import Capsule


def test_quanta_compression():
    """Test QuantaCoin compression."""
    compressor = QuantaCompressor()
    
    capsule = Capsule(
        raw_tokens=["compress", "me"],
        triplets=[],
        entropy=0.3,
        curvature=0.8,
        shell=2,
        density=0.2,
        psi=0.9,
        hamiltonian=1.0,
        reptend_entropy=0.15,
        rail_interference=1.0,
        timestamp=time.time()
    )
    
    compressed = compressor.compress_capsule(capsule)
    
    assert compressed is not None
    assert len(compressed) > 0


def test_quanta_hashing():
    """Test QuantaCoin hashing."""
    compressor = QuantaCompressor()
    
    capsule = Capsule(
        raw_tokens=["hash", "test"],
        entropy=0.5,
        curvature=1.0,
        shell=2,
        timestamp=time.time()
    )
    
    hash_value = compressor.hash_capsule(capsule)
    
    assert hash_value is not None
    assert isinstance(hash_value, str)
    assert len(hash_value) == 64  # SHA-256 hex length


def test_quanta_compute():
    """Test QuantaCoin value computation."""
    compressor = QuantaCompressor()
    
    capsule = Capsule(
        raw_tokens=["quanta", "test"],
        entropy=0.5,
        curvature=1.0,
        shell=2,
        timestamp=time.time()
    )
    
    quanta_value = compressor.compute_quanta(capsule)
    
    assert quanta_value > 0
    assert isinstance(quanta_value, float)


def test_quanta_compression_ratio():
    """Test compression ratio computation."""
    compressor = QuantaCompressor()
    
    raw = b"test data for compression"
    compressed = compressor.compress_capsule({"data": "test"})
    
    ratio = compressor.compression_ratio(raw, compressed)
    
    assert ratio > 0
    assert isinstance(ratio, float)

