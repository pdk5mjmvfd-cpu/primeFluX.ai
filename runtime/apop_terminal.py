# runtime/apop_terminal.py
# Your permanent sovereign terminal — type `apop` forever

import sys
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.quanta.mint import mint_quanta
from core.quanta.proof import CompressionProof
from core.math.pf_presence import PresenceVector
from core.math.pf_trig_osc import Oscillator
from pathlib import Path
import json
from datetime import datetime

# QuantaCoin v1.0 Ledger
LEDGER = Path("quantacoin_ledger/v1.jsonl")
LEDGER.parent.mkdir(exist_ok=True)
if not LEDGER.exists():
    LEDGER.write_text('')

def get_total_quanta() -> float:
    """Get total QuantaCoin minted from ledger."""
    try:
        content = LEDGER.read_text().strip()
        if not content:
            return 0.0
        total = sum(
            json.loads(line).get("quanta_minted", 0)
            for line in content.split("\n")
            if line.strip()
        )
        return round(total, 1)
    except:
        return 0.0

print("="*60)
print("QUANTACOIN v1.0 — OFFLINE SOVEREIGN MODE")
print("="*60)
print("You are the only miner. You are the only validator.")
print(f"Total QuantaCoin in ledger: {get_total_quanta():.1f} Q")
print("="*60)
print()

while True:
    try:
        text = input("you → ")
        if text.lower() in {"quit", "exit", "q"}: 
            break
        
        # Create compression proof
        proof = CompressionProof(text)
        quanta = proof.quanta
        
        # Create ledger entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": text,
            "quanta_minted": quanta,
            "proof": proof.serialize(),
            "note": "earned by irreversible geometric compression — verifiable by anyone"
        }
        
        # Append to ledger (immutable, append-only)
        LEDGER.write_text(LEDGER.read_text() + json.dumps(entry) + "\n")
        
        total = get_total_quanta()
        print(f"Apop → minted {quanta} QuantaCoin | ledger +1 | total ~{total:.1f} Q\n")
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"[Error: {e}]\n")
        continue

print(f"\n{'='*60}")
print(f"Session end. Ledger preserved at {LEDGER}")
print("You are now richer in real physics than when you started.")
print(f"{'='*60}\n")
