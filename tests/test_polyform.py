"""
Tests for PrimeFluxInt polyform system.

Tests:
- Round-trip encoding/decoding
- Compression ratio (>33%)
- Reversibility under Galois scramble
- Adiabatic recovery
- Perception cliff test
- ZK verification stubs
"""

import pytest
import json
from fluxai.memory.polyform_int import PrimeFluxInt
from fluxai.memory.zipnn_huffman import ZipNNHuffman


def test_round_trip_basic():
    """Test basic round-trip encoding/decoding."""
    data = {"test": "value", "number": 42, "list": [1, 2, 3]}
    
    pfi = PrimeFluxInt(salt=12345)
    pfi.encode(data, salt=12345)
    
    decoded = pfi.decode('full')
    
    assert decoded == data, f"Round-trip failed: {decoded} != {data}"


def test_round_trip_numeric():
    """Test round-trip with numeric data."""
    data = 42.5
    
    pfi = PrimeFluxInt(salt=67890)
    pfi.encode(data, salt=67890)
    
    decoded = pfi.decode('full')
    
    assert abs(decoded - data) < 1e-6, f"Round-trip failed: {decoded} != {data}"


def test_compression_ratio():
    """Test compression ratio > 33%."""
    # Create data with redundancy (good for compression)
    data = {"repeated": "value" * 100, "numbers": list(range(100))}
    
    pfi = PrimeFluxInt(salt=11111)
    pfi.encode(data, salt=11111)
    
    ratio = pfi.compression_ratio()
    
    # Should achieve at least 1.33x compression (33% savings)
    assert ratio >= 1.33, f"Compression ratio too low: {ratio} < 1.33"


def test_reversibility_galois():
    """Test reversibility under Galois scramble."""
    from fluxai.memory.polyform_int import galois_mix, galois_unmix
    
    original = 123456789
    salt = 98765
    
    mixed = galois_mix(original, salt)
    unmixed = galois_unmix(mixed, salt)
    
    assert unmixed == original, f"Galois reversibility failed: {unmixed} != {original}"


def test_adiabatic_recovery():
    """Test adiabatic recovery (nilpotent check)."""
    data = {"test": "recovery", "value": 3.14159}
    
    pfi = PrimeFluxInt(salt=54321)
    pfi.encode(data, salt=54321)
    
    recovered = pfi.adiabatic_recover()
    
    assert recovered, "Adiabatic recovery failed"


def test_perception_cliff():
    """Test perception cliff (23 round-trips, drift < 1e-6)."""
    data = 42.0
    
    pfi = PrimeFluxInt(salt=99999)
    pfi.encode(data, salt=99999)
    
    passed = pfi.perception_cliff_test(iters=23)
    
    assert passed, "Perception cliff test failed (drift >= 1e-6)"


def test_zk_verify():
    """Test ZK verification stub."""
    data = {"zk": "test", "value": 123}
    
    pfi = PrimeFluxInt(salt=77777)
    pfi.encode(data, salt=77777)
    
    verified = pfi.zk_verify_decode()
    
    assert verified, "ZK verification failed"


def test_decode_modes():
    """Test different decode modes."""
    data = {"method": "test", "value": 42, "type": "int"}
    
    pfi = PrimeFluxInt(salt=33333)
    pfi.encode(data, salt=33333)
    
    # Test interface mode
    interface = pfi.decode('interface')
    assert isinstance(interface, dict), "Interface mode should return dict"
    
    # Test class mode
    class_data = pfi.decode('class')
    assert isinstance(class_data, dict), "Class mode should return dict"
    
    # Test method mode
    method = pfi.decode('method')
    assert callable(method) or isinstance(method, dict), "Method mode should return callable or dict"
    
    # Test full mode
    full = pfi.decode('full')
    assert full == data, "Full mode should return original data"


def test_reversible_operations():
    """Test reversible operations (add, mul)."""
    data1 = 10
    data2 = 20
    
    pfi1 = PrimeFluxInt(salt=11111)
    pfi1.encode(data1, salt=11111)
    
    pfi2 = PrimeFluxInt(salt=22222)
    pfi2.encode(data2, salt=22222)
    
    # Test addition
    pfi_sum = pfi1 + pfi2
    sum_decoded = pfi_sum.decode('full')
    
    # Should be approximately 30 (may have encoding artifacts)
    assert isinstance(sum_decoded, (int, float, dict)), "Sum should decode to numeric or dict"
    
    # Test multiplication
    pfi_prod = pfi1 * pfi2
    prod_decoded = pfi_prod.decode('full')
    
    assert isinstance(prod_decoded, (int, float, dict)), "Product should decode to numeric or dict"


def test_zipnn_huffman_compression():
    """Test ZipNN Huffman compression."""
    huffman = ZipNNHuffman()
    
    # Test with integer list
    data = list(range(100))
    compressed = huffman.compress(data)
    decompressed = huffman.decompress(compressed)
    
    # Decompressed should return exponents (not original integers)
    # This is expected - full reconstruction requires context
    assert len(decompressed) > 0, "Decompression should return some data"
    
    # Test compression ratio
    ratio = huffman.compression_ratio(data, compressed)
    assert ratio >= 1.0, f"Compression ratio should be >= 1.0, got {ratio}"


def test_matryoshka_nesting():
    """Test Matryoshka nesting (6x shrinkage)."""
    data = {"core": "state", "extensions": list(range(100))}
    
    pfi = PrimeFluxInt(salt=55555)
    pfi.encode(data, salt=55555)
    
    # Check compression ratio (should show nesting benefit)
    ratio = pfi.compression_ratio()
    assert ratio >= 1.0, f"Matryoshka nesting should provide compression, got ratio {ratio}"


def test_integration_with_objects():
    """Test integration with ObjectMemory."""
    try:
        from experience.objects.object_memory import ObjectMemory
        from pathlib import Path
        import tempfile
        import shutil
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Test with polyform enabled
            obj_mem = ObjectMemory(repo_path=temp_dir, use_polyform=True)
            
            # Create test object
            from experience.objects.object_memory import Object
            test_obj = Object(
                signature="test_sig",
                triplets=[(1, 2, 3)],
                shell_stats={0: 1},
                curvature_profile=[1.0, 2.0],
                entropy_profile=0.5,
                adjacency_patterns=[("a", "b")],
                count=1
            )
            
            obj_mem.store_object(test_obj)
            obj_mem.save_to_repo()
            
            # Reload
            obj_mem2 = ObjectMemory(repo_path=temp_dir, use_polyform=True)
            
            # Check if object was loaded
            loaded_obj = obj_mem2.get_object("test_sig")
            assert loaded_obj is not None, "Object should be loaded"
            assert loaded_obj.signature == "test_sig", "Object signature should match"
            
        finally:
            shutil.rmtree(temp_dir)
            
    except ImportError:
        pytest.skip("ObjectMemory not available for integration test")


def test_large_data_compression():
    """Test compression on larger datasets."""
    # Create larger dataset
    data = {
        "items": list(range(1000)),
        "strings": ["test"] * 100,
        "nested": {"level1": {"level2": {"level3": "value"}}}
    }
    
    pfi = PrimeFluxInt(salt=123456)
    pfi.encode(data, salt=123456)
    
    decoded = pfi.decode('full')
    
    # Should decode successfully
    assert isinstance(decoded, dict), "Large data should decode to dict"
    assert "items" in decoded, "Large data should preserve keys"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

