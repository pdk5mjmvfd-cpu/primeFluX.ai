"""
QuantaCoin v1.0 — Production-Ready, Legal-Aware, Offline-First.

Thermodynamically honest proof-of-compression currency.
"""

from .mint import mint_quanta
from .proof import CompressionProof

__all__ = ["mint_quanta", "CompressionProof"]
