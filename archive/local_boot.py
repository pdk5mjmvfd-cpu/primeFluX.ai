#!/usr/bin/env python3

"""
ApopToSiS v3 – Local Boot Script

--------------------------------

This script boots a fully-local Apop instance with:

- LCM
- PFState
- Supervisor + Router
- Trinity Agents (Eidos, Praxis, Aegis)
- Experience Layer
- JSON-Flux Capsules
- QuantaCoin
- Local logging

This is intended for LOCAL USAGE ONLY.
"""

import os
import json
import datetime
from pathlib import Path

# -----------------------------
# Import Apop Runtime Components
# -----------------------------
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.runtime.supervisor.supervisor import Supervisor
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.device_identity import DeviceIdentity, get_device_identity
from ApopToSiS.runtime.sync_queue import SyncQueue
from ApopToSiS.runtime.experience_merge import ExperienceMerge
from ApopToSiS.agents.registry.registry import AgentRegistry
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent
from ApopToSiS.core.icm import ICM
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.quanta import QuantaCompressor
from ApopToSiS.experience.manager import ExperienceManager

# -----------------------------
# Paths
# -----------------------------
HOME = Path.home()
APOP_DIR = HOME / ".apoptosis"
CAPSULE_LOG_DIR = APOP_DIR / "local_capsules"
STATE_LOG_DIR = APOP_DIR / "local_state"
EXPERIENCE_LOG_DIR = APOP_DIR / "local_experience"

for d in [APOP_DIR, CAPSULE_LOG_DIR, STATE_LOG_DIR, EXPERIENCE_LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Helper Functions
# -----------------------------
def timestamp():
    return datetime.datetime.utcnow().isoformat() + "Z"

def save_capsule(capsule):
    """Save capsule JSON to local log."""
    path = CAPSULE_LOG_DIR / f"{capsule.capsule_id}.json"
    with open(path, "w") as f:
        json.dump(capsule.encode(), f, indent=2)
    return path

def save_state(state):
    """Save PFState snapshot."""
    path = STATE_LOG_DIR / f"state_{timestamp()}.json".replace(":", "_")
    state_dict = {
        "shell": state.shell.value if hasattr(state.shell, 'value') else int(state.shell),
        "curvature": state.curvature,
        "entropy": state.entropy,
        "density": state.density,
        "hamiltonian": state.hamiltonian,
        "psi": state.psi,
        "distinction_chain_length": len(state.distinction_chain),
        "history_length": len(state.history),
    }
    with open(path, "w") as f:
        json.dump(state_dict, f, indent=2)
    return path

def save_experience(experience):
    """Save experience graph or summary."""
    path = EXPERIENCE_LOG_DIR / f"exp_{timestamp()}.json".replace(":", "_")
    with open(path, "w") as f:
        json.dump(experience, f, indent=2)
    return path

# -----------------------------
# Boot Procedure
# -----------------------------
def boot_apop():
    print("\n🧬  Booting ApopToSiS v3 (Local Runtime)...")
    
    # Device identity (local)
    device_identity = get_device_identity()
    device_id = device_identity.get_device_id()
    session_id = device_identity.get_instance_id()
    
    print(f"   Device ID:  {device_id[:16]}...")
    print(f"   Session ID: {session_id[:16]}...")
    
    # 1. Initialize ICM (geometric interior)
    icm = ICM()
    
    # 2. Initialize LCM (linguistic cortex)
    lcm = LCM(icm=icm)
    
    # 3. Initialize Experience Manager
    experience_manager = ExperienceManager()
    lcm.experience_manager = experience_manager
    
    # 4. Initialize PFState
    state = PFState()
    
    # 5. Initialize Context
    context = Context()
    
    # 6. Initialize Trinity Agents
    eidos = EidosAgent()
    praxis = PraxisAgent()
    aegis = AegisAgent()
    
    # 7. Register agents
    registry = AgentRegistry()
    registry.register("eidos", eidos)
    registry.register("praxis", praxis)
    registry.register("aegis", aegis)
    agents = [eidos, praxis, aegis]
    
    print("   Trinity Agents loaded: Eidos, Praxis, Aegis")
    
    # 8. Initialize Supervisor
    supervisor = Supervisor(icm=icm, lcm=lcm)
    supervisor.integrate_experience(experience_manager)
    
    # 9. Initialize Quanta Compressor
    quanta_compressor = QuantaCompressor()
    
    print("   Runtime components initialized.\n")
    
    return {
        "state": state,
        "context": context,
        "supervisor": supervisor,
        "agents": agents,
        "registry": registry,
        "lcm": lcm,
        "icm": icm,
        "experience_manager": experience_manager,
        "quanta_compressor": quanta_compressor,
        "device_id": device_id,
        "session_id": session_id,
    }

# -----------------------------
# Main Loop
# -----------------------------
def run_cli_apop():
    runtime = boot_apop()
    
    state = runtime["state"]
    context = runtime["context"]
    supervisor = runtime["supervisor"]
    agents = runtime["agents"]
    lcm = runtime["lcm"]
    experience_manager = runtime["experience_manager"]
    quanta_compressor = runtime["quanta_compressor"]
    device_id = runtime["device_id"]
    session_id = runtime["session_id"]
    
    sync_queue = SyncQueue()
    
    print("✨ ApopToSiS v3 is ready.")
    print("Type a message and press Enter.")
    print("Type '/exit' to quit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "/exit", "quit"]:
            print("\n🫧 Shutting down ApopToSiS v3. See you soon.\n")
            break
        
        if not user_input:
            continue
        
        try:
            # --- 1. Process tokens through LCM ---
            tokens = user_input.split()
            lcm.process_tokens(tokens)
            
            # --- 2. Generate capsule from LCM ---
            capsule_dict = lcm.generate_capsule()
            capsule = Capsule.decode(capsule_dict) if isinstance(capsule_dict, dict) else Capsule(raw_tokens=tokens)
            
            # Add identity fields
            capsule.device_id = device_id
            capsule.session_id = session_id
            
            # --- 3. Compress and hash capsule (QuantaCoin) ---
            quanta_hash = quanta_compressor.hash_capsule(capsule)
            quanta_value = quanta_compressor.compute_quanta(capsule)
            capsule.quanta_hash = quanta_hash
            capsule.compression_ratio = quanta_value
            
            # --- 4. Update state from capsule ---
            state.update(capsule.to_dict())
            context.add_capsule(capsule)
            
            # --- 5. Supervisor routing ---
            selected_agent = supervisor.route(state, agents)
            
            # --- 6. Process capsule through selected agent ---
            if selected_agent:
                processed_capsule = selected_agent.transform(capsule)
                processed_capsule.agent_trace.append(selected_agent.__class__.__name__)
            else:
                processed_capsule = capsule
            
            # --- 7. Update experience layer ---
            experience_manager.update(processed_capsule, state)
            
            # --- 8. Extract experience delta ---
            exp_delta = ExperienceMerge.extract_experience_delta(processed_capsule, experience_manager)
            processed_capsule.experience_delta = exp_delta
            
            # --- 9. Integrate capsule into Supervisor ---
            supervisor.integrate_capsule(processed_capsule)
            
            # --- 10. Save capsule & state locally ---
            cap_path = save_capsule(processed_capsule)
            state_path = save_state(state)
            
            # --- 11. Save experience summary ---
            exp_summary = experience_manager.summarize()
            exp_path = save_experience(exp_summary)
            
            # --- 12. Print results ---
            print("\n--- APOPTOSIS RESPONSE ---------------------------------")
            print(f"Capsule Shell:        {processed_capsule.shell}")
            print(f"Entropy:              {processed_capsule.entropy:.4f}")
            print(f"Curvature:            {processed_capsule.curvature:.4f}")
            print(f"QuantaCoin (ΦQ):      {quanta_value:.4f}")
            print(f"Agent Trace:          {processed_capsule.agent_trace}")
            print(f"Selected Agent:       {selected_agent.__class__.__name__ if selected_agent else 'None'}")
            print(f"Capsule saved to:     {cap_path}")
            print(f"State snapshot saved: {state_path}")
            print(f"Experience saved:     {exp_path}")
            print("---------------------------------------------------------\n")
            
        except Exception as e:
            print(f"\n❌ Error processing input: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    return

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    run_cli_apop()

