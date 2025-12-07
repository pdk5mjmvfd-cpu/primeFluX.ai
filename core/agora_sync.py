"""
Agora Sync - libp2p-based sync for Agora ecosystem.

Opt-in sync with discrete shells. No auto-parent notify unless explicit.
"""

from __future__ import annotations

from typing import Optional, Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

# Try to import libp2p (stub if unavailable)
try:
    # libp2p-py may not be stable, use stub for now
    LIBP2P_AVAILABLE = False
    # import libp2p
    # LIBP2P_AVAILABLE = True
except ImportError:
    LIBP2P_AVAILABLE = False


class AgoraSyncClient:
    """
    Agora sync client with opt-in connection.
    
    Only connects if --agora flag is set. No auto-parent notify.
    User must explicitly "join_agora" in UI/CLI.
    """
    
    def __init__(self, enabled: bool = False):
        """
        Initialize Agora sync client.
        
        Args:
            enabled: Whether sync is enabled (opt-in)
        """
        self.enabled = enabled
        self.connected = False
        self.peers: List[str] = []
        self.local_ledger_path: str = "experience/ledger.jsonl"
        self.local_graph_path: str = "experience/graph.json"
        
        if not enabled:
            logger.info("Agora sync disabled (opt-in required)")
    
    def connect(self) -> bool:
        """
        Connect to Agora network (opt-in only).
        
        Returns:
            True if connected, False otherwise
        """
        if not self.enabled:
            logger.warning("Agora sync not enabled. Use --agora flag to enable.")
            return False
        
        if LIBP2P_AVAILABLE:
            # Full libp2p implementation would go here
            logger.info("Connecting to Agora network...")
            self.connected = True
            return True
        else:
            # Stub implementation
            logger.info("Agora sync stub: libp2p not available")
            self.connected = False
            return False
    
    def join_agora(self) -> bool:
        """
        Explicitly join Agora (user consent required).
        
        Returns:
            True if joined, False otherwise
        """
        if not self.enabled:
            return False
        
        logger.info("User explicitly joined Agora")
        return self.connect()
    
    def broadcast_ledger(
        self,
        ledger_entries: List[Dict[str, Any]],
        phase_mod_2_5: Optional[float] = None
    ) -> bool:
        """
        Broadcast ledger entries to peers.
        
        Includes 2/5 mod in broadcast phase.
        
        Args:
            ledger_entries: List of ledger entries
            phase_mod_2_5: Optional phase mod 2/5 value
            
        Returns:
            True if broadcast successful
        """
        if not self.connected:
            return False
        
        try:
            # Broadcast logic would go here
            logger.debug(f"Broadcasting {len(ledger_entries)} ledger entries")
            if phase_mod_2_5 is not None:
                logger.debug(f"Phase mod 2/5: {phase_mod_2_5}")
            return True
        except Exception as e:
            logger.error(f"Broadcast failed: {e}")
            return False
    
    def broadcast_graph(
        self,
        graph_data: Dict[str, Any],
        presence_value: Optional[float] = None
    ) -> bool:
        """
        Broadcast graph data to peers.
        
        Args:
            graph_data: Graph data dictionary
            presence_value: Optional presence operator value
            
        Returns:
            True if broadcast successful
        """
        if not self.connected:
            return False
        
        try:
            # Broadcast logic would go here
            logger.debug("Broadcasting graph data")
            if presence_value is not None:
                logger.debug(f"Presence value: {presence_value}")
            return True
        except Exception as e:
            logger.error(f"Graph broadcast failed: {e}")
            return False
    
    def merge_ledger(
        self,
        remote_entries: List[Dict[str, Any]],
        quorum_check: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Merge remote ledger entries with local.
        
        Discrete: Local copy always primary. Merge only on quorum.
        
        Args:
            remote_entries: Remote ledger entries
            quorum_check: Whether to check quorum (majority reversible)
            
        Returns:
            Merged entries
        """
        if not self.connected:
            return []
        
        try:
            # Load local ledger
            local_entries = self._load_local_ledger()
            
            # Quorum check if enabled
            if quorum_check:
                # Check if majority of entries are reversible
                reversible_count = sum(
                    1 for e in remote_entries
                    if e.get("passed_check", False)
                )
                if reversible_count < len(remote_entries) / 2:
                    logger.warning("Quorum check failed: insufficient reversible entries")
                    return local_entries
            
            # Merge (local always primary)
            merged = local_entries.copy()
            for remote_entry in remote_entries:
                # Only add if not already present
                if remote_entry not in merged:
                    merged.append(remote_entry)
            
            return merged
        except Exception as e:
            logger.error(f"Ledger merge failed: {e}")
            return []
    
    def _load_local_ledger(self) -> List[Dict[str, Any]]:
        """Load local ledger entries."""
        try:
            from pathlib import Path
            ledger_path = Path(self.local_ledger_path)
            if not ledger_path.exists():
                return []
            
            entries = []
            with open(ledger_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entries.append(json.loads(line))
            return entries
        except Exception:
            return []
    
    def disconnect(self):
        """Disconnect from Agora network."""
        if self.connected:
            logger.info("Disconnecting from Agora network")
            self.connected = False
            self.peers = []
