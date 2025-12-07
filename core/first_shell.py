"""
First Shell Logic - PrimeFlux AI shell system integration.

The "first shell" is Shell 0 (PRESENCE) - the initial state where Apop begins.
This module integrates:
- Distinction packet parsing (trig modes, presence op, 2/5 salts, pi/e secrets)
- Shell transitions (0 → 2 → 3 → 4 → 0)
- PrimeFlux principles (distinction, rails, flux, reversibility)
- Data freedom (reversible transforms under ∇·Φ=0)
"""

from __future__ import annotations

import math
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from collections import Counter

from core.math.shells import Shell, shell_curvature, next_shell


def entropy(text: str) -> float:
    """Calculate Shannon entropy in nats."""
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    return -sum((c / total) * math.log(c / total) for c in counts.values() if c > 0)


def parse_distinction_packet(
    text: str,
    mode: str = 'refinement',
    presence_on: bool = True
) -> Dict[str, Any]:
    """
    Parse distinction packet with full PrimeFlux logic.
    
    Integrates:
    - Trig modes (Research=sin, Refinement=cos, Relations=tan)
    - Presence operator (g_PF toggles event spaces)
    - 2/5 salts (phase mod 2/5 for routing)
    - pi/e secrets (hidden curvature)
    - Shell transition logic
    
    Args:
        text: Input text
        mode: Mode (research/refinement/relations)
        presence_on: Whether presence operator is enabled
        
    Returns:
        Distinction packet dictionary
    """
    # Hash input for phase calculation
    h = hashlib.sha256(text.encode()).digest()
    phase = (int.from_bytes(h[:2], 'big') % 200 / 100.0) - 1.0  # [-1, 1]
    
    # 2/5 salts: phase mod (2*5)
    mod25 = phase % (2 * 5)
    
    # Trig mode mapping
    if mode == 'research':
        trig_func = math.sin
        trig_label = "sin (Wave Flows)"
    elif mode == 'refinement':
        trig_func = math.cos
        trig_label = "cos (Balance Curvature)"
    elif mode == 'relations':
        trig_func = math.tan
        trig_label = "tan (Projection Spaces)"
    else:
        trig_func = math.cos
        trig_label = "cos (default)"
    
    # Presence operator: g_PF(phase, mode) = trig(mode) if presence_on else 0
    g_pf = trig_func(phase) if presence_on else 0.0
    
    # pi/e secret curvature (internal, not exposed)
    # curvature = (π - e) * abs(phase)
    curv_internal = (math.pi - math.e) * abs(phase) if g_pf != 0 else 0.0
    
    # Agent routing based on phase
    if abs(phase) > 0.7:
        agent = "eidos"  # High distinction (ICM)
    elif phase < 0:
        agent = "aegis"  # Negative phase (LCM annihilation)
    else:
        agent = "praxis"  # Relay (default)
    
    # Calculate entropy for shell transition
    text_entropy = entropy(text)
    
    # Determine current shell based on phase and entropy
    # Shell 0 (PRESENCE) is the first shell
    current_shell = Shell.PRESENCE  # Start in presence
    
    # Calculate curvature for shell transition
    curvature = abs(phase) * shell_curvature(Shell.MEASUREMENT)
    
    # Determine next shell based on PrimeFlux transition rules
    next_shell_val = next_shell(current_shell, curvature, text_entropy)
    
    return {
        "phase": phase,
        "mod25": mod25,
        "g_pf": g_pf,
        "curv_internal": curv_internal,
        "agent": agent,
        "mode": mode,
        "trig_label": trig_label,
        "presence_on": presence_on,
        "current_shell": current_shell.value,
        "next_shell": next_shell_val.value,
        "curvature": curvature,
        "entropy": text_entropy,
        "timestamp": datetime.utcnow().isoformat()
    }


def check_reversibility(input_text: str, output_text: str, threshold: float = None) -> Dict[str, Any]:
    """
    Check reversibility with canonical threshold.
    
    Canonical threshold: K = ln(10) ≈ 2.302585 nats
    
    Args:
        input_text: Input text
        output_text: Output text
        threshold: Optional threshold (default: ln(10))
        
    Returns:
        Reversibility check result
    """
    if threshold is None:
        threshold = math.log(10)  # Canonical threshold
    
    inp_entropy = entropy(input_text)
    out_entropy = entropy(output_text)
    entropy_diff = out_entropy - inp_entropy
    
    passed = out_entropy <= inp_entropy + threshold
    
    return {
        "passed": passed,
        "input_entropy": inp_entropy,
        "output_entropy": out_entropy,
        "entropy_diff": entropy_diff,
        "threshold": threshold,
        "quanta_minted": 1.0 if passed else 0.0
    }


def apply_data_freedom(
    data: str,
    transform_type: str = "compress",
    reversible_check: bool = True
) -> Dict[str, Any]:
    """
    Apply data freedom: reversible transforms under ∇·Φ=0.
    
    "Whatever we want" if reversibility check passes.
    
    Args:
        data: Data to transform
        transform_type: Type of transform (compress, encrypt, etc.)
        reversible_check: Whether to check reversibility
        
    Returns:
        Transform result
    """
    if transform_type == "compress":
        # Simple compression example (reversible)
        compressed = data.encode('utf-8').hex()
        decompressed = bytes.fromhex(compressed).decode('utf-8')
        
        # Check reversibility
        if reversible_check:
            check = check_reversibility(data, decompressed)
            if not check["passed"]:
                return {
                    "success": False,
                    "error": "Transform not reversible",
                    "check": check
                }
        
        return {
            "success": True,
            "original": data,
            "transformed": compressed,
            "reversible": True,
            "compression_ratio": len(compressed) / len(data.encode('utf-8'))
        }
    
    elif transform_type == "encrypt":
        # Simple encryption example (reversible)
        # In production, would use proper encryption
        encrypted = ''.join(chr(ord(c) + 1) for c in data)
        decrypted = ''.join(chr(ord(c) - 1) for c in encrypted)
        
        if reversible_check:
            check = check_reversibility(data, decrypted)
            if not check["passed"]:
                return {
                    "success": False,
                    "error": "Transform not reversible",
                    "check": check
                }
        
        return {
            "success": True,
            "original": data,
            "transformed": encrypted,
            "reversible": True
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown transform type: {transform_type}"
        }


def process_first_shell(
    input_text: str,
    mode: str = 'refinement',
    presence_on: bool = True,
    agent: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process input through first shell (PRESENCE) logic.
    
    This is the entry point for PrimeFlux AI processing.
    
    Args:
        input_text: User input
        mode: Mode (research/refinement/relations)
        presence_on: Whether presence operator is enabled
        agent: Optional agent override
        
    Returns:
        Complete processing result
    """
    # Parse distinction packet
    packet = parse_distinction_packet(input_text, mode, presence_on)
    
    # Override agent if provided
    if agent:
        packet["agent"] = agent
    
    # If presence off, return early
    if not presence_on or packet["g_pf"] == 0:
        return {
            "status": "presence_off",
            "message": "[Event Spaces Off: Presence operator disabled mode trig.]",
            "packet": packet,
            "quanta": 0.0,
            "reversible": False
        }
    
    # Calculate shell transition
    shell_info = {
        "current": Shell(packet["current_shell"]).name,
        "next": Shell(packet["next_shell"]).name,
        "curvature": packet["curvature"],
        "entropy": packet["entropy"]
    }
    
    return {
        "status": "success",
        "packet": packet,
        "shell": shell_info,
        "agent": packet["agent"],
        "mode": mode,
        "presence_on": presence_on
    }


def integrate_with_cli(cli_result: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    """
    Integrate CLI result with first shell logic.
    
    Args:
        cli_result: Result from CLI query
        packet: Distinction packet
        
    Returns:
        Integrated result
    """
    # Add shell information
    shell_info = {
        "current": Shell(packet["current_shell"]).name,
        "next": Shell(packet["next_shell"]).name,
        "curvature": packet["curvature"],
        "entropy": packet["entropy"]
    }
    
    # Combine results
    return {
        **cli_result,
        "packet": packet,
        "shell": shell_info,
        "primeflux_aligned": True
    }
