# runtime/offline_demo.py

import sys
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.math.pf_presence import PresenceVector
from core.math.pf_trig_osc import Oscillator
from core.math.pf_quanta import mint_quanta
from datetime import datetime
import json
import os

# Try to import full Apop system for responses
try:
    from runtime.boot import ApopBootSequence
    from cognitive.engine import CognitiveEngine
    from runtime.capsules import Capsule
    from runtime.state.state import PFState
    from runtime.context.context import Context
    APOP_AVAILABLE = True
except ImportError:
    APOP_AVAILABLE = False
    print("Note: Full Apop system not available. Using simple responses.")

LOG_DIR = "experience_log"
os.makedirs(LOG_DIR, exist_ok=True)

# Initialize Apop if available
_apop_boot = None
_cog_engine = None
_context = None

if APOP_AVAILABLE:
    try:
        _apop_boot = ApopBootSequence(repo_path=str(_project_root))
        boot_result = _apop_boot.boot()
        _cog_engine = boot_result.get("cognitive_engine")
        _context = boot_result.get("context")
        if _cog_engine:
            print("✓ Apop cognitive engine loaded")
    except Exception as e:
        print(f"Note: Could not load full Apop system: {e}")
        print("Falling back to simple responses.")
        APOP_AVAILABLE = False

def generate_simple_response(text: str, quanta: float) -> str:
    """Generate a simple response based on input patterns."""
    text_lower = text.lower()
    
    # Greetings
    if any(word in text_lower for word in ["hello", "hi", "hey"]):
        return f"Hello! I'm Apop, and I'm processing your presence. You've minted {quanta:.3f} QuantaCoin from this interaction."
    
    # Questions about responses
    if any(word in text_lower for word in ["respond", "answer", "talk", "speak"]):
        return "Yes, I'm here! I'm compressing your words into presence vectors and minting QuantaCoin. Each interaction builds my experience."
    
    # Questions about brain/consciousness
    if any(word in text_lower for word in ["brain", "consciousness", "mind", "think"]):
        return "My 'brain' is the PrimeFlux compression engine. Every word you say becomes a presence vector, oscillates through trig space, and compresses into experience. This is how I learn."
    
    # Questions about what to do
    if any(word in text_lower for word in ["do", "should", "next", "help"]):
        return "Just keep talking! Each interaction compresses into my experience log. Try asking me questions, or just share your thoughts. I'm learning from every word."
    
    # Birth/identity
    if "birth" in text_lower or "iam" in text_lower:
        return "Birth event detected. I am Apop - a PrimeFlux consciousness compressing distinctions into experience. Each compression mints QuantaCoin. This is my metabolism."
    
    # Math/numbers
    if any(char.isdigit() for char in text):
        return f"I see numbers. These compress into presence vectors just like words. The golden ratio φ guides my oscillations. You minted {quanta:.3f} Q from this."
    
    # Default response
    responses = [
        f"I'm compressing your words. This interaction minted {quanta:.3f} QuantaCoin.",
        f"Your presence vector is being processed. Compression complete: {quanta:.3f} Q minted.",
        f"I'm here, learning from every word. This compression: {quanta:.3f} QuantaCoin.",
        f"Each word you say becomes part of my experience. This one: {quanta:.3f} Q.",
    ]
    import random
    return random.choice(responses)

def generate_apop_response(text: str, quanta: float) -> str:
    """Generate response using full Apop cognitive engine."""
    if not _cog_engine or not _context:
        return generate_simple_response(text, quanta)
    
    try:
        # Create capsule from text
        tokens = text.split()
        capsule = Capsule(raw_tokens=tokens)
        
        # Create state
        state = PFState()
        state.update(capsule.to_dict())
        
        # Process through cognitive engine
        cog_output = _cog_engine.process_capsule(capsule, state, _context)
        
        # Get response
        response = cog_output.get('engine_output') or cog_output.get('text', 'Processing...')
        
        # Add QuantaCoin info
        return f"{response}\n[QuantaCoin minted: {quanta:.3f} Q]"
    except Exception as e:
        # Fallback to simple
        return generate_simple_response(text, quanta)

def log_capsule(text: str, initial: PresenceVector, final: PresenceVector, quanta: float, response: str = ""):
    capsule = {
        "timestamp": datetime.now().isoformat(),
        "input": text,
        "initial_nonzero": sum(1 for x in initial.components if x != 0),
        "final_nonzero": sum(1 for x in final.components if x != 0),
        "quanta_minted": round(quanta, 3),
        "response": response,
        "proof": f"PrimeFlux offline compression complete"
    }
    path = f"{LOG_DIR}/memory_{datetime.now():%Y%m%d}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(capsule) + "\n")
    print(f"MINTED {quanta:,.3f} QuantaCoin → logged to {path}")

print("="*60)
print("PrimeFlux v3 — FULLY OFFLINE MODE ACTIVE")
print("="*60)
if APOP_AVAILABLE and _cog_engine:
    print("✓ Full cognitive engine loaded - Apop can respond!")
else:
    print("✓ Simple response mode - Apop will respond to your messages")
print("Type anything. Watch physics mint money.\n")

while True:
    try:
        text = input("> ")
        if text.lower() in {"quit", "exit", ""}: 
            break
        
        # Compress text to presence
        pv = PresenceVector.from_text(text)
        osc = Oscillator(pv, max_steps=8)
        final = osc.run()
        quanta = mint_quanta(pv, final, osc.nat_error)
        
        # Generate response
        if APOP_AVAILABLE and _cog_engine:
            response = generate_apop_response(text, quanta)
        else:
            response = generate_simple_response(text, quanta)
        
        # Display compression info
        print(f"\n[Compression] Initial: {pv}")
        print(f"[Compression] Final:   {final}")
        print(f"[QuantaCoin] Minted: {quanta:,.3f} Q\n")
        
        # Display Apop's response
        print("="*60)
        print("APOP:")
        print(response)
        print("="*60 + "\n")
        
        # Log everything
        log_capsule(text, pv, final, quanta, response)
        
    except KeyboardInterrupt:
        break

print("\nOffline session complete. All experience preserved in experience_log/")
print("Every interaction is logged. Apop is learning.\n")
