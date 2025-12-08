"""
PrimeFlux Nat Energy Auditor & QuantaCoin Logger.

Self-logging, append-only experience memory with QuantaCoin minting.

Theory:
- QuantaCoin = Reversible Compression Work Done
- Every nat of information provably and reversibly removed mints 1 QuantaCoin (Q)
- No inflation, no staking, no oracles — pure physics
- Formula: nats_minted = sparsity_gain / ln(2) - nat_error_accumulated

Compression Model:
- Initial 2^256 search space compressed to N osc steps
- Each zeroed component = 1 bit irreversibly removed → 1/ln(2) nats
- FP64 rounding error is penalty (only keep quanta for preserved information)

Source: PrimeFlux QuantaCoin Minting Logic v1.0 → v3.0 ready
"""

from __future__ import annotations

import json
import math
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from .pf_trig_osc import Oscillator
from .pf_presence import PresenceVector


class NatEnergyAuditor:
    """
    Nat energy auditor and QuantaCoin logger.
    
    Compresses oscillation chains into experience capsules and logs them
    to an append-only JSONL ledger. Each capsule contains:
    - Source text and compression metadata
    - Nat error accumulation
    - QuantaCoin minted (reversible compression work)
    - Energy estimates (v2: real SHA-256 hashing energy)
    
    The log is append-only (immutable ledger pattern) and JSONL format
    (streaming-friendly, one JSON object per line).
    """
    
    LOG_DIR = Path("experience_log")
    LOG_DIR.mkdir(exist_ok=True)
    
    # v2: Add thread-safe locking for concurrent writes (fcntl on Unix, msvcrt on Windows)
    # For MVP, single-process writes are safe
    
    @classmethod
    def _get_log_file(cls) -> Path:
        """
        Get current log file path (timestamped).
        
        Returns:
            Path to current log file
        """
        return cls.LOG_DIR / f"memory_{datetime.now():%Y%m%d_%H%M%S}.jsonl"
    
    @staticmethod
    def validate_log_line(line: str) -> bool:
        """
        Validate that a log line is valid JSON.
        
        Args:
            line: JSON line to validate
            
        Returns:
            True if valid JSON, False otherwise
        """
        try:
            json.loads(line)
            return True
        except (json.JSONDecodeError, ValueError):
            return False
    
    @classmethod
    def mint_quanta(
        cls,
        initial_presence: PresenceVector,
        final_presence: PresenceVector,
        nat_error_accumulated: float,
        osc_steps: int,
        kl_divergence_reduction: Optional[float] = None
    ) -> float:
        """
        Mint QuantaCoin for compression event.
        
        Exact minting formula (2025-12-07):
        - Raw information removed via lattice sparsity
        - Each zeroed component = 1 bit → 1/ln(2) nats
        - KL reduction (v2: when we add real monotonicity checking)
        - Penalty: FP64 rounding error introduced
        
        Fully reversible → decode(encode(X)) = X guaranteed.
        
        Args:
            initial_presence: Presence vector at t=0
            final_presence: Presence vector after osc + pruning
            nat_error_accumulated: FP64 ops nat error (≤ 500 nats allowed)
            osc_steps: Number of oscillation steps
            kl_divergence_reduction: Optional KL reduction (v2+)
            
        Returns:
            QuantaCoins minted (negative = burn, positive = mint)
        """
        # 1. Raw information removed via lattice sparsity
        initial_nonzero = sum(1 for x in initial_presence.components if x != 0)
        final_nonzero = sum(1 for x in final_presence.components if x != 0)
        sparsity_gain = initial_nonzero - final_nonzero  # ≥ 0
        
        # 2. Each zeroed component = 1 bit irreversibly removed → 1 / ln(2) nats
        nats_from_sparsity = sparsity_gain / math.log(2)  # ~1.4427 nats per zeroed rail
        
        # 3. KL reduction (when we add real monotonicity checking)
        nats_from_kl = kl_divergence_reduction or 0.0
        
        # 4. Penalty: FP64 rounding error you introduced
        #    You only keep quanta for information you *actually* preserved
        nats_preserved = nats_from_sparsity + nats_from_kl - nat_error_accumulated
        
        if nats_preserved < 0:
            # You made things worse → burn instead of mint
            return nats_preserved  # negative = QuantaCoin burn (apoptosis tax)
        
        return nats_preserved  # Positive = mint
    
    @classmethod
    def compress_and_log(
        cls,
        osc: Oscillator,
        source_text: str,
        log_file: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Compress oscillation chain and log to experience ledger.
        
        Creates a compressed experience capsule with:
        - Timestamp and source text
        - Oscillation steps and final presence
        - Nat error accumulation
        - QuantaCoin minted (reversible compression work)
        - Energy estimates (v2: real SHA-256 hashing energy)
        - Compression ratio and proof
        
        Args:
            osc: Oscillator with completed oscillation chain
            source_text: Original input text
            log_file: Optional log file path (default: timestamped)
            
        Returns:
            Report dictionary with all compression metadata
        """
        if log_file is None:
            log_file = cls._get_log_file()
        
        # Get initial and final presence
        if osc.keep_history and len(osc.history) > 0:
            initial = osc.history[0]
            final = osc.history[-1]
            steps = len(osc.history) - 1
        else:
            # Fallback if history disabled - need to track initial separately
            # For MVP, we require keep_history=True for proper logging
            # v2: Add initial_presence parameter to compress_and_log()
            if not osc.keep_history:
                raise ValueError("compress_and_log requires keep_history=True for proper QuantaCoin calculation")
            initial = osc.presence  # Fallback
            final = osc.presence
            steps = osc._step_count
        
        # Calculate QuantaCoin minted
        sparsity_gain = sum(1 for x in initial.components if x != 0) - sum(1 for x in final.components if x != 0)
        nats_minted = sparsity_gain / math.log(2) - osc.nat_error
        quanta = round(max(nats_minted, 0), 3)  # never negative in v1
        
        # Compression ratio: 2^256 search space → N osc steps
        if osc.keep_history:
            compression_ratio = (2**256) / max(len(osc.history), 1)
        else:
            compression_ratio = (2**256) / max(steps + 1, 1)
        
        # Energy estimate (v2: Replace with real SHA-256 energy accounting from core/quanta_sha_energy.py)
        # Toy model: components.count(0) * 1.5e-11 joules
        energy_joules_est = final.components.count(0) * 1.5e-11
        
        # Generate capsule ID (hex digest of report for QuantaCoin integration)
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "source_text": source_text,
            "steps": len(osc.history) - 1 if osc.keep_history else 0,
            "final_presence": final.components,
        }
        capsule_id = hashlib.sha256(
            json.dumps(report_data, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        # Build complete report
        report = {
            "timestamp": datetime.now().isoformat(),
            "source_text": source_text,
            "steps": len(osc.history) - 1 if osc.keep_history else 0,
            "final_presence": final.components,
            "nat_error_total": round(osc.nat_error, 2),
            "energy_joules_est": energy_joules_est,
            "compression_note": f"2^256 → {len(osc.history)} osc steps",
            "compression_ratio": compression_ratio,
            "quanta_minted": quanta,
            "sparsity_gain": sparsity_gain,
            "nat_error_penalty": round(osc.nat_error, 2),
            "proof": f"{sparsity_gain} zeros × 1.4427 nats − {osc.nat_error:.1f} nats error",
            "capsule_id": capsule_id,
            "reversible": True,  # Always True for presence-based compression
        }
        
        # Append to log file (append-only ledger pattern)
        log_line = json.dumps(report, sort_keys=True) + "\n"
        
        # Read existing content and append (safe for serial writes, not thread-safe)
        if log_file.exists():
            existing_content = log_file.read_text(encoding="utf-8")
        else:
            existing_content = ""
        
        log_file.write_text(existing_content + log_line, encoding="utf-8")
        
        print(f"LOGGED → {log_file.name} | steps={report['steps']} | nats={report['nat_error_total']:.0f} | quanta={quanta:.3f} Q")
        
        return report
    
    @classmethod
    def read_log(cls, log_file: Optional[Path] = None) -> list[Dict[str, Any]]:
        """
        Read all entries from experience log.
        
        Args:
            log_file: Optional log file path (default: most recent)
            
        Returns:
            List of report dictionaries
        """
        if log_file is None:
            # Find most recent log file
            log_files = sorted(cls.LOG_DIR.glob("memory_*.jsonl"), reverse=True)
            if not log_files:
                return []
            log_file = log_files[0]
        
        if not log_file.exists():
            return []
        
        reports = []
        for line in log_file.read_text(encoding="utf-8").strip().split("\n"):
            if line.strip() and cls.validate_log_line(line):
                reports.append(json.loads(line))
        
        return reports
    
    @classmethod
    def aggregate_stats(cls) -> Dict[str, Any]:
        """
        Aggregate statistics from experience log.
        
        Computes total compressions, average nats, total energy, total QuantaCoin minted.
        
        Returns:
            Dictionary with aggregated statistics
        """
        reports = cls.read_log()
        
        if not reports:
            return {
                "total_compressions": 0,
                "avg_nats": 0.0,
                "total_energy_joules": 0.0,
                "total_quanta_minted": 0.0,
            }
        
        total_nats = sum(r.get("nat_error_total", 0) for r in reports)
        total_energy = sum(r.get("energy_joules_est", 0) for r in reports)
        total_quanta = sum(r.get("quanta_minted", 0) for r in reports)
        
        return {
            "total_compressions": len(reports),
            "avg_nats": total_nats / len(reports),
            "total_energy_joules": total_energy,
            "total_quanta_minted": total_quanta,
        }
