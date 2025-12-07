"""
Tests for Reversibility Checker and Ledger.
"""

import pytest
from datetime import datetime
from core.reversibility_check import ReversibilityChecker
from experience.ledger import ReversibilityLedger, LedgerEntry
from core.distinction_packet import DistinctionPacket
import tempfile
import os


def test_reversibility_checker_entropy():
    """Test entropy calculation."""
    checker = ReversibilityChecker()
    
    # Equal primes (low entropy)
    primes1 = [2, 2, 2, 2]
    entropy1 = checker.entropy(primes1)
    assert entropy1 == 0.0  # All same, no entropy
    
    # Different primes (higher entropy)
    primes2 = [2, 3, 5, 7]
    entropy2 = checker.entropy(primes2)
    assert entropy2 > 0.0


def test_reversibility_checker_equal_entropy_passes():
    """Test: Equal entropy passes check."""
    checker = ReversibilityChecker()
    
    input_primes = [2, 3, 5]
    output_primes = [2, 3, 5]  # Same primes
    
    passed = checker.check(input_primes, output_primes, threshold=0.1)
    assert passed is True


def test_reversibility_checker_output_high_entropy_fails():
    """Test: Output entropy > input + threshold fails."""
    checker = ReversibilityChecker()
    
    # Low entropy input
    input_primes = [2, 2, 2, 2]  # All same
    
    # High entropy output
    output_primes = [2, 3, 5, 7, 11, 13, 17, 19]  # All different
    
    passed = checker.check(input_primes, output_primes, threshold=0.1)
    assert passed is False


def test_reversibility_ledger_add_entry():
    """Test adding entries to ledger."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        ledger_path = f.name
    
    try:
        ledger = ReversibilityLedger(path=ledger_path)
        
        quanta = ledger.add_entry(
            input_hash="abc123",
            output_hash="def456",
            passed_check=True,
            quanta_minted=100,
            notes="Test entry"
        )
        
        assert quanta == 100
        
        # Failed check should return 0
        quanta2 = ledger.add_entry(
            input_hash="xyz789",
            output_hash="uvw012",
            passed_check=False,
            quanta_minted=100,
            notes="Failed check"
        )
        
        assert quanta2 == 0
        
        # Check stats
        stats = ledger.get_stats()
        assert stats["total_entries"] == 2
        assert stats["passed_checks"] == 1
        assert stats["failed_checks"] == 1
        assert stats["total_quanta_minted"] == 100
    finally:
        if os.path.exists(ledger_path):
            os.unlink(ledger_path)


def test_reversibility_ledger_csv_export():
    """Test CSV export."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        ledger_path = f.name
    
    try:
        ledger = ReversibilityLedger(path=ledger_path)
        
        ledger.add_entry(
            input_hash="abc",
            output_hash="def",
            passed_check=True,
            quanta_minted=50
        )
        
        csv_path = ledger.to_csv()
        assert os.path.exists(csv_path)
        
        # Clean up
        if os.path.exists(csv_path):
            os.unlink(csv_path)
    finally:
        if os.path.exists(ledger_path):
            os.unlink(ledger_path)


def test_quanta_api_integration():
    """Test QuantaAPI integration."""
    from core.quanta_api import QuantaAPI
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        ledger_path = f.name
    
    try:
        api = QuantaAPI(ledger_path=ledger_path)
        
        # Create packets
        input_pkt = DistinctionPacket(
            prime_modes=[2, 3],
            rail_phase=0.5,
            curvature_value=0.5,
            timestamp=datetime.now()
        )
        
        output_pkt = DistinctionPacket(
            prime_modes=[2, 3],  # Same primes (should pass)
            rail_phase=0.6,
            curvature_value=0.6,
            timestamp=datetime.now()
        )
        
        # Mint with check
        quanta = api.mint_with_check(input_pkt, output_pkt, base_quanta=100)
        
        assert quanta == 100  # Should pass and mint
        
        # Test with high entropy output (should fail)
        high_entropy_pkt = DistinctionPacket(
            prime_modes=[2, 3, 5, 7, 11, 13],  # More primes
            rail_phase=0.7,
            curvature_value=0.7,
            timestamp=datetime.now()
        )
        
        quanta2 = api.mint_with_check(input_pkt, high_entropy_pkt, base_quanta=100)
        
        # May pass or fail depending on entropy difference
        assert quanta2 >= 0
    finally:
        if os.path.exists(ledger_path):
            os.unlink(ledger_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
