"""
Quanta API - Quanta minting with reversibility checks.

Integrates reversibility checking before quanta minting.
"""

from __future__ import annotations

from typing import Optional
from core.reversibility_check import ReversibilityChecker
from experience.ledger import ReversibilityLedger
from core.distinction_packet import DistinctionPacket
import hashlib


class QuantaAPI:
    """
    Quanta API with reversibility auditing.
    
    Checks reversibility before minting quanta.
    """
    
    def __init__(self, ledger_path: str = "experience/ledger.jsonl"):
        """
        Initialize Quanta API.
        
        Args:
            ledger_path: Path to reversibility ledger
        """
        self.checker = ReversibilityChecker()
        self.ledger = ReversibilityLedger(path=ledger_path)
    
    def mint_with_check(
        self,
        input_packet: DistinctionPacket,
        output_packet: DistinctionPacket,
        base_quanta: int = 100
    ) -> int:
        """
        Mint quanta with reversibility check.
        
        Before minting, checks reversibility. If check passes,
        mints quanta and adds to ledger. Otherwise, returns 0.
        
        Args:
            input_packet: Input distinction packet
            output_packet: Output distinction packet
            base_quanta: Base quanta amount to mint
            
        Returns:
            Quanta minted (0 if check failed)
        """
        # Check reversibility
        passed = self.checker.check(
            input_packet.prime_modes,
            output_packet.prime_modes
        )
        
        # Generate hashes
        input_hash = hashlib.sha256(
            str(input_packet.prime_modes).encode('utf-8')
        ).hexdigest()[:16]
        
        output_hash = hashlib.sha256(
            str(output_packet.prime_modes).encode('utf-8')
        ).hexdigest()[:16]
        
        # Add to ledger
        quanta_minted = self.ledger.add_entry(
            input_hash=input_hash,
            output_hash=output_hash,
            passed_check=passed,
            quanta_minted=base_quanta if passed else 0,
            notes=f"Input curvature: {input_packet.curvature_value:.3f}, "
                  f"Output curvature: {output_packet.curvature_value:.3f}"
        )
        
        return quanta_minted
    
    def get_ledger_stats(self) -> dict:
        """Get ledger statistics."""
        return self.ledger.get_stats()
