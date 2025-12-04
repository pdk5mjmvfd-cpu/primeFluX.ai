"""
Quanta API — memory compression interface.

Every capsule has QuantaCoin value.
Compression rate = "proof-of-compression".
This is fully usable on capsule #1.
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.core.quanta import QuantaCompressor
from ApopToSiS.runtime.capsules import Capsule


class QuantaAPI:
    """
    Quanta API — memory compression interface.
    
    Immediate effect:
    - Every capsule has QuantaCoin value
    - Compression rate = "proof-of-compression"
    - This is fully usable on capsule #1
    """

    def __init__(self) -> None:
        """Initialize Quanta API."""
        self.compressor = QuantaCompressor()

    def compress_capsule(self, capsule: Capsule) -> bytes:
        """
        Compress a capsule.

        Args:
            capsule: Capsule to compress

        Returns:
            Compressed bytes
        """
        return self.compressor.compress_capsule(capsule)

    def hash_capsule(self, capsule: Capsule) -> str:
        """
        Hash a capsule.

        Args:
            capsule: Capsule to hash

        Returns:
            SHA-256 hash (hex)
        """
        return self.compressor.hash_capsule(capsule)

    def compute_quanta(self, capsule: Capsule) -> float:
        """
        Compute QuantaCoin value for a capsule.
        
        QuantaCoin = compression ratio.

        Args:
            capsule: Capsule to compute QuantaCoin for

        Returns:
            QuantaCoin value (compression ratio)
        """
        # Get raw size
        raw_dict = capsule.encode()
        import json
        raw_json = json.dumps(raw_dict, sort_keys=True)
        raw_size = len(raw_json.encode("utf-8"))
        
        # Get compressed size
        compressed = self.compressor.compress_capsule(capsule)
        compressed_size = len(compressed)
        
        # Compute compression ratio = QuantaCoin
        quanta = self.compressor.compression_ratio(raw_json, compressed)
        
        return quanta

    def mint_quanta(self, capsule: Capsule) -> dict[str, Any]:
        """
        Mint QuantaCoin for a capsule.
        
        Returns compression ratio, hash, and metadata.

        Args:
            capsule: Capsule to mint QuantaCoin for

        Returns:
            Dictionary with QuantaCoin data
        """
        quanta_value = self.compute_quanta(capsule)
        quanta_hash = self.hash_capsule(capsule)
        
        return {
            "quanta_value": quanta_value,
            "quanta_hash": quanta_hash,
            "compression_ratio": quanta_value,
            "capsule_hash": quanta_hash,
        }

