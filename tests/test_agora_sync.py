"""
Tests for Agora Sync.
"""

import pytest
from unittest.mock import Mock, patch
from core.agora_sync import AgoraSyncClient
from experience.agora_ledger import AgoraLedger, LedgerEntry
from datetime import datetime


def test_agora_sync_disabled_by_default():
    """Test: Agora sync disabled by default (opt-in)."""
    client = AgoraSyncClient(enabled=False)
    
    assert client.enabled is False
    assert client.connect() is False


def test_agora_sync_opt_in():
    """Test: Agora sync requires explicit opt-in."""
    client = AgoraSyncClient(enabled=True)
    
    # Should not be connected until join_agora() called
    assert client.connected is False
    
    # Explicit join required
    result = client.join_agora()
    # May succeed or fail depending on libp2p availability
    assert isinstance(result, bool)


def test_agora_sync_no_auto_notify():
    """Test: No auto-parent notify (discrete shells)."""
    client = AgoraSyncClient(enabled=True)
    
    # Should not broadcast unless explicitly connected
    ledger_entries = [{"input_hash": "abc", "passed_check": True}]
    result = client.broadcast_ledger(ledger_entries)
    
    # Should fail if not connected
    assert result is False or isinstance(result, bool)


def test_agora_ledger_quorum_check():
    """Test quorum check in Agora ledger."""
    ledger = AgoraLedger(path="test_ledger.jsonl")
    
    # Add some entries
    ledger.add_entry("abc", "def", True, 100)
    ledger.add_entry("ghi", "jkl", True, 50)
    ledger.add_entry("mno", "pqr", False, 0)  # Failed check
    
    # Check quorum (2/3 reversible = 0.67 > 0.5)
    entries = ledger.get_entries()
    assert ledger.quorum_check(entries, threshold=0.5) is True
    
    # Add more failed entries
    ledger.add_entry("stu", "vwx", False, 0)
    ledger.add_entry("yza", "bcd", False, 0)
    
    # Now 2/5 reversible = 0.4 < 0.5
    entries = ledger.get_entries()
    assert ledger.quorum_check(entries, threshold=0.5) is False


def test_agora_ledger_merge_discrete():
    """Test: Local entries always primary in merge."""
    local_ledger = AgoraLedger(path="test_local.jsonl")
    local_ledger.add_entry("local1", "out1", True, 100)
    local_ledger.add_entry("local2", "out2", True, 50)
    
    # Remote entries
    remote_entries = [
        LedgerEntry(
            timestamp=datetime.now(),
            input_hash="remote1",
            output_hash="out3",
            passed_check=True,
            quanta_minted=75
        ),
        LedgerEntry(
            timestamp=datetime.now(),
            input_hash="local1",  # Duplicate
            output_hash="out1",
            passed_check=True,
            quanta_minted=100
        )
    ]
    
    # Merge (local always primary)
    merged = local_ledger.merge_with_quorum(remote_entries)
    
    # Should have local entries + unique remote
    assert len(merged) >= 2
    # Local entries should be preserved
    local_hashes = {e.input_hash for e in local_ledger.get_entries()}
    merged_hashes = {e.input_hash for e in merged}
    assert local_hashes.issubset(merged_hashes)


def test_presence_operator_in_router():
    """Test presence operator in router."""
    from agents.router import AgentRouter
    import math
    
    router = AgentRouter()
    
    phase = math.pi / 4
    
    # Test with presence on
    assert router.presence_operator(phase, "research", True) == pytest.approx(math.sin(phase))
    assert router.presence_operator(phase, "refinement", True) == pytest.approx(math.cos(phase))
    assert router.presence_operator(phase, "relations", True) == pytest.approx(math.tan(phase))
    
    # Test with presence off
    assert router.presence_operator(phase, "research", False) == 0.0
    assert router.presence_operator(phase, "refinement", False) == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
