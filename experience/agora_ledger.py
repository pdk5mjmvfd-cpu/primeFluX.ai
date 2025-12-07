"""
Agora Ledger - Extended ledger with quorum checks.

Discrete shells: Local copy always primary, merge only on quorum.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from experience.ledger import ReversibilityLedger, LedgerEntry
import logging

logger = logging.getLogger(__name__)


class AgoraLedger(ReversibilityLedger):
    """
    Extended ledger with quorum checks for Agora sync.
    
    Discrete: Local copy always primary.
    Merge only on quorum (majority reversible).
    """
    
    def quorum_check(
        self,
        entries: List[LedgerEntry],
        threshold: float = 0.5
    ) -> bool:
        """
        Check if entries meet quorum (majority reversible).
        
        Args:
            entries: List of ledger entries
            threshold: Threshold for quorum (default: 0.5 = majority)
            
        Returns:
            True if quorum met, False otherwise
        """
        if not entries:
            return False
        
        reversible_count = sum(1 for e in entries if e.passed_check)
        ratio = reversible_count / len(entries)
        
        return ratio >= threshold
    
    def merge_with_quorum(
        self,
        remote_entries: List[LedgerEntry],
        threshold: float = 0.5
    ) -> List[LedgerEntry]:
        """
        Merge remote entries with local, checking quorum.
        
        Discrete: Local entries always primary.
        
        Args:
            remote_entries: Remote ledger entries
            threshold: Quorum threshold
            
        Returns:
            Merged entries (local always included)
        """
        # Check quorum
        if not self.quorum_check(remote_entries, threshold):
            logger.warning("Quorum check failed: insufficient reversible entries")
            return self.entries.copy()
        
        # Merge (local always primary)
        merged = self.entries.copy()
        
        # Add remote entries that aren't duplicates
        local_hashes = {e.input_hash for e in merged}
        for remote_entry in remote_entries:
            if remote_entry.input_hash not in local_hashes:
                merged.append(remote_entry)
        
        return merged
    
    def get_reversible_count(self) -> int:
        """Get count of reversible entries."""
        return sum(1 for e in self.entries if e.passed_check)
    
    def get_reversibility_ratio(self) -> float:
        """Get ratio of reversible entries."""
        if not self.entries:
            return 0.0
        return self.get_reversible_count() / len(self.entries)
