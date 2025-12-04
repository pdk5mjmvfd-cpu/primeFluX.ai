"""
Quanta — memory compression and QuantaCoin mechanics.

QuantaCoin (ΦQ) = proof-of-compression.
Higher compression = more Quanta minted.

Capsules are the unit of memory compression and QuantaCoin minting.
Every capsule has QuantaCoin value.
Compression rate = "proof-of-compression".
This works from the first capsule.
"""

from __future__ import annotations

from typing import Any
import hashlib
import json
import zlib
from ApopToSiS.runtime.capsules import Capsule


class QuantaCompressor:
    """
    QuantaCoin memory compression.
    
    Converts capsules into compressed, verifiable representations.
    Every capsule has QuantaCoin value.
    Compression rate = "proof-of-compression".
    This is fully usable on capsule #1.
    """

    def compress_capsule(self, capsule: Capsule | dict[str, Any]) -> bytes:
        """
        Compress a capsule.
        
        Converts capsule into compressed JSON.
        This is the unit of memory compression and QuantaCoin minting.

        Args:
            capsule: Capsule instance or dictionary

        Returns:
            Compressed bytes
        """
        # Convert capsule to dict if needed
        if isinstance(capsule, Capsule):
            capsule_dict = capsule.encode()
        else:
            capsule_dict = capsule
        
        # Convert capsule to JSON-Flux format
        raw_json = json.dumps(capsule_dict, sort_keys=True)
        
        # Compress using zlib
        compressed = zlib.compress(raw_json.encode("utf-8"))
        
        return compressed

    def hash_capsule(self, capsule: Capsule | dict[str, Any]) -> str:
        """
        Hash a capsule.
        
        Computes SHA-256 hash of compressed capsule.
        This is the QuantaCoin hash for identity continuity.

        Args:
            capsule: Capsule instance or dictionary

        Returns:
            SHA-256 hash (hex)
        """
        compressed = self.compress_capsule(capsule)
        hash_value = hashlib.sha256(compressed).hexdigest()
        
        # Update capsule's quanta_hash if it's a Capsule object
        if isinstance(capsule, Capsule):
            capsule.quanta_hash = hash_value
            capsule.compression_hash = hash_value
        
        return hash_value

    def compression_ratio(self, raw: bytes | str, compressed: bytes) -> float:
        """
        Compute compression ratio.
        
        ΦQ (QuantaCoin) = compression_ratio
        Higher compression = more Quanta minted.

        Args:
            raw: Raw data (bytes or string)
            compressed: Compressed data

        Returns:
            Compression ratio (higher = better compression)
        """
        if isinstance(raw, str):
            raw_bytes = raw.encode("utf-8")
        else:
            raw_bytes = raw
        
        if len(compressed) == 0:
            return 1.0
        
        return len(raw_bytes) / max(1, len(compressed))
    
    def compute_quanta(self, capsule: Capsule | dict[str, Any]) -> float:
        """
        Compute QuantaCoin value for a capsule.
        
        QuantaCoin = compression ratio.
        This gives immediate memory compression and proof-of-compression.

        Args:
            capsule: Capsule instance or dictionary

        Returns:
            QuantaCoin value (compression ratio)
        """
        # Get raw size
        if isinstance(capsule, Capsule):
            raw_dict = capsule.encode()
        else:
            raw_dict = capsule
        
        raw_json = json.dumps(raw_dict, sort_keys=True)
        raw_size = len(raw_json.encode("utf-8"))
        
        # Get compressed size
        compressed = self.compress_capsule(capsule)
        compressed_size = len(compressed)
        
        # Compute compression ratio = QuantaCoin
        quanta = self.compression_ratio(raw_json, compressed)
        
        return quanta
