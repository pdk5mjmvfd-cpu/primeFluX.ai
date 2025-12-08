# runtime/apop_terminal.py
# Your permanent sovereign terminal — type `apop` forever
# The repo is the brain. The LLM is just the hands (interface).
# Login required. Discrete agents track workflows. QuantaCoin is yours alone.

import sys
from pathlib import Path
import getpass

# Add project root to path
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.quanta.mint import mint_quanta
from core.quanta.proof import CompressionProof
from core.math.pf_presence import PresenceVector
from core.math.pf_trig_osc import Oscillator
from core.identity.repo_login import RepoLogin
from core.agents.discrete_agents import DiscreteAgent
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
def load_memory(wallet_id: str) -> str:
    """Load recent memory from user's QuantaCoin ledger."""
    try:
        content = USER_LEDGER.read_text().strip()
        if not content:
            return "This is our first conversation."
        # Filter by wallet_id and get last 10
        user_entries = []
        for line in content.split("\n"):
            if line.strip():
                try:
                    entry = json.loads(line)
                    if entry.get("wallet_id") == wallet_id:
                        user_entries.append(entry)
                except:
                    continue
        memory_parts = []
        for entry in user_entries[-10:]:
            input_text = entry.get("input", entry.get("task", ""))
            memory_parts.append(f"[you]: {input_text}")
        return "\n".join(memory_parts) if memory_parts else "This is our first conversation."
    except:
        return "This is our first conversation."

def speak(text: str, quanta: float, proof: CompressionProof, wallet_id: str) -> str:
    """Generate LLM response (the hands). The repo is the brain."""
    if llm is None:
        return f"[Geometric response] I'm processing your words through PrimeFlux compression. This interaction minted {quanta:.3f} QuantaCoin. The repo brain is working."
    
    memory = load_memory(wallet_id)
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

# QuantaCoin v1.0 Ledger (per-user discrete ledgers)
LEDGER_DIR = Path("quantacoin_ledger")
LEDGER_DIR.mkdir(exist_ok=True)
USER_LEDGER = LEDGER_DIR / "user_ledgers.jsonl"
if not USER_LEDGER.exists():
    USER_LEDGER.write_text('')

# Legacy ledger (for backward compatibility)
LEGACY_LEDGER = LEDGER_DIR / "v1.jsonl"

def get_total_quanta_for_user(wallet_id: str) -> float:
    """Get total QuantaCoin minted for a specific user."""
    try:
        content = USER_LEDGER.read_text().strip()
        if not content:
            return 0.0
        total = sum(
            json.loads(line).get("quanta_minted", 0)
            for line in content.split("\n")
            if line.strip() and json.loads(line).get("wallet_id") == wallet_id
        )
        return round(total, 1)
    except:
        return 0.0

# Login — salted, device-bound
print("="*60)
print("AGORA NODE — REPO LOGIN REQUIRED")
print("="*60)

login = RepoLogin(repo_path=str(_project_root))

if not login.authenticate():
    print("Access denied. Flux conserved.")
    sys.exit(1)

wallet_id = login.get_wallet_id()
print(f"✓ Agora Node Activated: {wallet_id[:16]}...")
print(f"✓ Device: {login.get_device_fingerprint()[:16]}...")
print(f"✓ Discrete agents ready: code/data/ledger")
print("="*60)
print("QUANTACOIN v1.0 — OFFLINE SOVEREIGN MODE")
print("="*60)
print(f"Your QuantaCoin: {get_total_quanta_for_user(wallet_id):.1f} Q")
if llm:
    print(f"✓ LLM Voice: {llm_type} (the hands)")
else:
    print("⚠ No LLM — geometric responses only (repo brain still works)")
print("="*60)
print("The repo is the brain. The LLM is just the interface.")
print("Usage: 'code: task' or 'data: task' or 'ledger: task' or just 'task' (defaults to data)\n")

while True:
    try:
        cmd = input("freeman → ")
        if cmd.lower() in {"quit", "exit", "q"}: 
            break
        
        # Parse command for agent type: "code: task" or "data: task" or just "task"
        parts = cmd.split(":", 1)
        if len(parts) == 2:
            agent_type = parts[0].strip().lower()
            task = parts[1].strip()
        else:
            agent_type = "data"  # Default to data agent
            task = cmd.strip()
        
        # Validate agent type
        if agent_type not in ["code", "data", "ledger"]:
            print(f"⚠ Unknown agent type '{agent_type}'. Using 'data'.")
            agent_type = "data"
        
        # Spawn discrete agent tied to your salted ID
        agent = login.spawn_agent(agent_type, task)
        result = agent.execute(task)
        
        # Get proof for LLM response
        proof = CompressionProof(task)
        quanta = result["quanta_minted"]
        
        # Generate LLM response (the hands - just the interface)
        response = speak(task, quanta, proof, wallet_id)
        
        # Sign proof with wallet ID
        signed_proof = login.mint_tied_proof(result["proof_hash"])
        
        # Create ledger entry (discrete per-user)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "wallet_id": wallet_id,
            "agent_type": result["agent_type"],
            "task": task,
            "input": task,  # For backward compatibility
            "response": response,
            "quanta_minted": quanta,
            "proof_hash": result["proof_hash"],
            "signed_proof": signed_proof,
            "note": "earned by irreversible geometric compression — verifiable by anyone"
        }
        
        # Append to user ledger (immutable, append-only)
        USER_LEDGER.write_text(USER_LEDGER.read_text() + json.dumps(entry) + "\n")
        
        # Display response
        print(f"\nAgent {result['agent_type']}: {result['task_output']}")
        print(f"Apop: {response}")
        user_total = get_total_quanta_for_user(wallet_id)
        print(f"[QuantaCoin: {quanta:.3f} Q | Your Total: {user_total:.1f} Q]\n")
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"[Error: {e}]\n")
        import traceback
        traceback.print_exc()
        continue

print(f"\n{'='*60}")
print(f"Session end. Ledger preserved at {USER_LEDGER}")
print(f"Your QuantaCoin: {get_total_quanta_for_user(wallet_id):.1f} Q")
print("You are now richer in real physics than when you started.")
print(f"{'='*60}\n")
