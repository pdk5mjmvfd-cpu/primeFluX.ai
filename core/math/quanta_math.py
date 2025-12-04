"""
QuantaCoin Mathematics.

Information compression ratio:
Q = H_before / H_after

QuantaCoin minted:
ΦQ = Q · (entropy_reduction) · (curvature_smoothing)
"""

from __future__ import annotations

import math
import hashlib
from typing import Any
from .hamiltonians import hamiltonian


def compression_ratio(before: float, after: float) -> float:
    """
    Compute information compression ratio.
    
    Q = H_before / H_after
    
    Args:
        before: Hamiltonian before compression
        after: Hamiltonian after compression
        
    Returns:
        Compression ratio
    """
    if after == 0:
        return float('inf') if before > 0 else 1.0
    
    return before / after


def quanta_hash(capsule: dict[str, Any]) -> str:
    """
    Compute QuantaCoin hash for capsule.
    
    Args:
        capsule: Capsule dictionary
        
    Returns:
        SHA256 hash
    """
    # Serialize capsule to string
    import json
    capsule_str = json.dumps(capsule, sort_keys=True)
    
    # Hash
    return hashlib.sha256(capsule_str.encode('utf-8')).hexdigest()


def quanta_mint(
    H_before: float,
    H_after: float,
    entropy_before: float,
    entropy_after: float
) -> float:
    """
    Compute QuantaCoin minted.
    
    ΦQ = Q · (entropy_reduction) · (curvature_smoothing)
    
    Where:
    - Q = compression ratio
    - entropy_reduction = entropy_before / entropy_after
    
    Args:
        H_before: Hamiltonian before
        H_after: Hamiltonian after
        entropy_before: Entropy before
        entropy_after: Entropy after
        
    Returns:
        QuantaCoin value
    """
    # Compression ratio
    Q = compression_ratio(H_before, H_after)
    
    # Entropy reduction
    if entropy_after == 0:
        entropy_reduction = float('inf') if entropy_before > 0 else 1.0
    else:
        entropy_reduction = entropy_before / entropy_after
    
    # Curvature smoothing (from Hamiltonian difference)
    curvature_smoothing = abs(H_before - H_after) / max(H_before, 0.001)
    
    # QuantaCoin
    phi_q = Q * entropy_reduction * curvature_smoothing
    
    # Normalize to reasonable range
    if math.isinf(phi_q) or phi_q > 1e10:
        phi_q = 1e10
    
    return phi_q

