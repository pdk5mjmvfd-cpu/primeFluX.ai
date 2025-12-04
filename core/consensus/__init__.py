"""
CoSy (Consensus System) Bridge — PrimeFlux consensus engine.
"""

from .cosy_bridge import CoSyBridge

# Alias for compatibility
CoSyBridgeMain = CoSyBridge

__all__ = [
    "CoSyBridge",
    "CoSyBridgeMain",
]

