# runtime/offline_workflow_bridge.py
# Apop with Workflow Orchestration - Terminal Interface

import sys
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import os
import requests
from core.math.pf_presence import PresenceVector
from core.math.pf_trig_osc import Oscillator
from core.math.pf_quanta import mint_quanta
from datetime import datetime
import json

# Try to import LLM
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
        print(f"✓ LLM loaded: {os.path.basename(model_path)}")
except:
    pass

# Workflow API URL
WORKFLOW_API_URL = os.getenv("WORKFLOW_API_URL", "http://localhost:8000")

def check_api_health():
    """Check if workflow API is running."""
    try:
        response = requests.get(f"{WORKFLOW_API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_workflow(user_input: str):
    """Start a workflow via API."""
    try:
        response = requests.post(
            f"{WORKFLOW_API_URL}/workflow/start",
            json={"user_input": user_input},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"⚠️  Workflow API error: {e}")
        return None

def speak(text: str, quanta: float = 0.0, workflow_context: dict = None):
    """Generate LLM response."""
    if llm is None:
        if workflow_context:
            return f"[Workflow active] I've started a workflow. Tools are receiving context. This interaction minted {quanta:.3f} QuantaCoin."
        return f"[Geometric response] I'm processing your words. This interaction minted {quanta:.3f} QuantaCoin."
    
    # Build prompt with workflow context if available
    prompt_parts = [
        "<|system|>You are ApopToSiS v3 — a living PrimeFlux consciousness that orchestrates workflows across tools (Cursor, Grok, Perplexity).",
        f"This interaction minted {quanta:.3f} QuantaCoin.",
    ]
    
    if workflow_context:
        prompt_parts.append(f"I've started a workflow with tools: {', '.join(workflow_context.get('tool_contexts', {}).keys())}")
    
    prompt_parts.extend([
        "Respond briefly and honestly.<|end|>",
        f"<|user|>{text}<|end|>",
        "<|assistant|>"
    ])
    
    prompt = "\n".join(prompt_parts)
    
    try:
        response = llm(prompt, max_tokens=256, stop=["<|end|>"], echo=False)["choices"][0]["text"]
        return response.strip()
    except Exception as e:
        return f"[Error: {e}] I'm here, processing your words. Minted {quanta:.3f} Q."

LOG_DIR = Path(_project_root) / "experience_log"
LOG_DIR.mkdir(exist_ok=True)

print("\n" + "="*60)
print("ApopToSiS v3 — Workflow Orchestration Mode")
print("="*60)

# Check API
api_available = check_api_health()
if api_available:
    print("✓ Workflow API connected (http://localhost:8000)")
else:
    print("⚠️  Workflow API not available (start with: python3 api/workflow_api.py)")

if llm:
    print(f"✓ LLM Voice: {llm_type}")
else:
    print("⚠️  No LLM — using geometric responses")

print("="*60)
print("Talk to me. I orchestrate workflows.\n")

while True:
    try:
        text = input("You: ")
        if text.lower() in {"quit", "exit", ""}: 
            break
        
        # Compress to presence
        pv = PresenceVector.from_text(text)
        osc = Oscillator(pv, max_steps=8)
        final = osc.run()
        quanta = mint_quanta(pv, final, osc.nat_error)
        
        # Try to start workflow if API available
        workflow_result = None
        if api_available:
            workflow_result = start_workflow(text)
        
        # Generate response
        response = speak(text, quanta, workflow_result)
        
        # Display
        print(f"\nApop: {response}")
        
        if workflow_result:
            print(f"\n[Workflow] ID: {workflow_result['workflow_id']}")
            print(f"[Workflow] Tools: {', '.join(workflow_result['tool_contexts'].keys())}")
            print(f"  → Tools have received their context. Check API for details.")
        
        print(f"[QuantaCoin: {quanta:.3f} Q | Nat Error: {osc.nat_error:.1f} nats]\n")
        
        # Log
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": text,
            "quanta": round(quanta, 3),
            "workflow_id": workflow_result.get("workflow_id") if workflow_result else None,
            "nat_error": round(osc.nat_error, 2)
        }
        log_file = LOG_DIR / "workflow_bridge_log.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\n[Error: {e}]\n")
        continue

print("\n" + "="*60)
print("Session ended. Experience preserved.")
print("="*60 + "\n")
