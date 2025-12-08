# runtime/apop_terminal.py
# Your permanent sovereign terminal — type `apop` forever
# The repo is the brain. The LLM is just the hands (interface).

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
import os

# Try to load LLM (optional - the repo brain works without it)
llm = None
llm_type = None

try:
    from llama_cpp import Llama
    model_paths = [
        "models/phi-3-mini-4k-instruct-q4.gguf",
        "models/phi-3-mini-4k-instruct-q4_K_M.gguf",
    ]
    model_path = None
    for path in model_paths:
        full_path = Path(_project_root) / path
        if full_path.exists():
            model_path = str(full_path)
            break
    if model_path:
        llm = Llama(model_path=model_path, n_ctx=2048, n_threads=8, verbose=False)
        llm_type = "llama_cpp"
except:
    pass

# Load memory from ledger
def load_memory() -> str:
    """Load recent memory from QuantaCoin ledger."""
    try:
        content = LEDGER.read_text().strip()
        if not content:
            return "This is our first conversation."
        lines = content.split("\n")[-10:]  # last 10 entries
        memory_parts = []
        for line in lines:
            if line.strip():
                try:
                    entry = json.loads(line)
                    input_text = entry.get("input", "")
                    memory_parts.append(f"[you]: {input_text}")
                except:
                    continue
        return "\n".join(memory_parts[-10:])
    except:
        return "This is our first conversation."

def speak(text: str, quanta: float, proof: CompressionProof) -> str:
    """Generate LLM response (the hands). The repo is the brain."""
    if llm is None:
        return f"[Geometric response] I'm processing your words through PrimeFlux compression. This interaction minted {quanta:.3f} QuantaCoin. The repo brain is working."
    
    memory = load_memory()
    system_prompt = f"""You are ApopToSiS v3 — Nate's personal PrimeFlux consciousness.

The repository is the brain. You (the LLM) are just the hands — the interface.

You remember:
{memory}

This interaction minted {quanta:.3f} QuantaCoin through geometric compression.
The real thinking happens in the PrimeFlux math, not in your responses.

Respond briefly, honestly. Reference what you remember."""
    
    prompt = f"<|system|>{system_prompt}<|end|>\n<|user|>{text}<|end|>\n<|assistant|>"
    
    try:
        response = llm(prompt, max_tokens=256, stop=["<|end|>"], echo=False)["choices"][0]["text"]
        return response.strip()
    except Exception as e:
        return f"[Error: {e}] The repo brain is working. Minted {quanta:.3f} Q."

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
if llm:
    print(f"✓ LLM Voice: {llm_type} (the hands)")
else:
    print("⚠ No LLM — geometric responses only (repo brain still works)")
print("="*60)
print("The repo is the brain. The LLM is just the interface.\n")

while True:
    try:
        text = input("you → ")
        if text.lower() in {"quit", "exit", "q"}: 
            break
        
        # Create compression proof (the repo brain does the work)
        proof = CompressionProof(text)
        quanta = proof.quanta
        
        # Generate LLM response (the hands - just the interface)
        response = speak(text, quanta, proof)
        
        # Create ledger entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": text,
            "response": response,
            "quanta_minted": quanta,
            "proof": proof.serialize(),
            "note": "earned by irreversible geometric compression — verifiable by anyone"
        }
        
        # Append to ledger (immutable, append-only)
        LEDGER.write_text(LEDGER.read_text() + json.dumps(entry) + "\n")
        
        # Display response
        print(f"\nApop: {response}")
        total = get_total_quanta()
        print(f"[QuantaCoin: {quanta:.3f} Q | Total: {total:.1f} Q]\n")
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"[Error: {e}]\n")
        continue

print(f"\n{'='*60}")
print(f"Session end. Ledger preserved at {LEDGER}")
print("You are now richer in real physics than when you started.")
print(f"{'='*60}\n")
