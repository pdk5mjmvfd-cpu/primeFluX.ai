"""
Reversibility Ledger - Tracks transformation audits.

Stores ledger entries for reversibility checks and quanta minting.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
import csv


@dataclass
class LedgerEntry:
    """Ledger entry for a transformation audit."""
    timestamp: datetime
    input_hash: str
    output_hash: str
    passed_check: bool
    quanta_minted: int
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "passed_check": self.passed_check,
            "quanta_minted": self.quanta_minted,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LedgerEntry":
        """Create from dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            input_hash=data["input_hash"],
            output_hash=data["output_hash"],
            passed_check=data["passed_check"],
            quanta_minted=data["quanta_minted"],
            notes=data.get("notes")
        )


class ReversibilityLedger:
    """
    Reversibility ledger for tracking transformation audits.
    
    Stores entries in JSONL format and provides CSV export.
    """
    
    def __init__(self, path: str = "experience/ledger.jsonl"):
        """
        Initialize reversibility ledger.
        
        Args:
            path: Path to ledger JSONL file
        """
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: list[LedgerEntry] = []
        self._load_entries()
    
    def _load_entries(self):
        """Load existing entries from file."""
        if not self.path.exists():
            return
        
        try:
            with open(self.path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entry_dict = json.loads(line)
                        entry = LedgerEntry.from_dict(entry_dict)
                        self.entries.append(entry)
        except Exception:
            # Silently fail if loading fails
            pass
    
    def add_entry(
        self,
        input_hash: str,
        output_hash: str,
        passed_check: bool,
        quanta_minted: int = 0,
        notes: Optional[str] = None
    ) -> int:
        """
        Add entry to ledger.
        
        Args:
            input_hash: Hash of input
            output_hash: Hash of output
            passed_check: Whether reversibility check passed
            quanta_minted: Quanta minted (0 if check failed)
            notes: Optional notes
            
        Returns:
            Quanta minted (0 if check failed)
        """
        entry = LedgerEntry(
            timestamp=datetime.now(),
            input_hash=input_hash,
            output_hash=output_hash,
            passed_check=passed_check,
            quanta_minted=quanta_minted if passed_check else 0,
            notes=notes
        )
        
        self.entries.append(entry)
        
        # Append to JSONL file
        try:
            with open(self.path, 'a') as f:
                f.write(json.dumps(entry.to_dict()) + '\n')
        except Exception:
            # Silently fail if write fails
            pass
        
        # Return quanta if passed, else 0
        return entry.quanta_minted
    
    def to_csv(self, output_path: Optional[str] = None) -> str:
        """
        Export ledger to CSV.
        
        Args:
            output_path: Optional output path (default: ledger.csv in same dir)
            
        Returns:
            Path to CSV file
        """
        if output_path is None:
            output_path = str(self.path.with_suffix('.csv'))
        
        csv_path = Path(output_path)
        
        try:
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # Header
                writer.writerow([
                    "timestamp",
                    "input_hash",
                    "output_hash",
                    "passed_check",
                    "quanta_minted",
                    "notes"
                ])
                
                # Rows
                for entry in self.entries:
                    writer.writerow([
                        entry.timestamp.isoformat(),
                        entry.input_hash,
                        entry.output_hash,
                        entry.passed_check,
                        entry.quanta_minted,
                        entry.notes or ""
                    ])
        except Exception:
            # Silently fail if CSV export fails
            pass
        
        return str(csv_path)
    
    def get_entries(self) -> list[LedgerEntry]:
        """Get all entries."""
        return self.entries.copy()
    
    def get_stats(self) -> dict:
        """Get ledger statistics."""
        total = len(self.entries)
        passed = sum(1 for e in self.entries if e.passed_check)
        total_quanta = sum(e.quanta_minted for e in self.entries)
        
        return {
            "total_entries": total,
            "passed_checks": passed,
            "failed_checks": total - passed,
            "pass_rate": passed / total if total > 0 else 0.0,
            "total_quanta_minted": total_quanta
        }
