#!/usr/bin/env python3

"""
ApopToSiS v3 — Local Runtime Boot Script

This starts a live PF-LCM runtime, with capsules, experience graph,
supervisor routing, and QuantaCoin compression active.
"""

import sys
import json
import uuid
import datetime

from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM
from ApopToSiS.runtime.supervisor.supervisor import Supervisor
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.quanta.quanta import QuantaCompressor
from ApopToSiS.agents.registry.registry import AgentRegistry
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent


def init_runtime():
    """Initialize PF-LCM, state, agents, supervisor."""
    print("⚡ Initializing ApopToSiS v3 runtime...")

    # Initialize ICM and LCM
    icm = ICM()
    lcm = LCM(icm=icm)
    
    # Initialize state and context
    state = PFState()
    context = Context()

    # Initialize Supervisor
    supervisor = Supervisor(icm=icm, lcm=lcm)

    # Register agents
    registry = AgentRegistry()
    eidos = EidosAgent()
    praxis = PraxisAgent()
    aegis = AegisAgent()
    
    registry.register("Eidos", eidos)
    registry.register("Praxis", praxis)
    registry.register("Aegis", aegis)
    
    # Get agents list for routing
    agents = [eidos, praxis, aegis]

    print("✓ PFState loaded")
    print("✓ LCM initialized")
    print("✓ Supervisor ready")
    print("✓ Agents registered")

    return state, context, lcm, supervisor, registry, agents


def print_capsule(capsule: Capsule):
    """Pretty-print capsule JSON in a readable way."""
    data = capsule.encode()
    print("\n=== CAPSULE OUTPUT ===")
    print(json.dumps(data, indent=2))


def main_loop():
    """Run the interactive capsule → agent → capsule loop."""
    state, context, lcm, supervisor, registry, agents = init_runtime()
    compressor = QuantaCompressor()

    print("\nApopToSiS v3 is now running.")
    print("Type a message to create your first capsule.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() in ("exit", "quit"):
            print("Shutting down ApopToSiS runtime...")
            break

        try:
            # 1. Tokenize input
            tokens = user_input.split()
            
            if not tokens:
                print("Empty input, please try again.\n")
                continue

            # 2. LCM: Process tokens and generate capsule
            lcm.process_tokens(tokens)
            capsule_dict = lcm.generate_capsule()
            capsule = Capsule.decode(capsule_dict) if isinstance(capsule_dict, dict) else Capsule(raw_tokens=tokens)
            capsule.agent_trace = []

            # 3. Update state from capsule
            state.update(capsule.to_dict())

            # 4. Supervisor: Route to an agent
            agent = supervisor.route(state, agents)
            
            if agent:
                capsule.agent_trace.append(agent.__class__.__name__)

                # 5. Agent: Transform Capsule
                capsule = agent.transform(capsule)

            # 6. Update State from processed capsule
            updated_state = supervisor.update_state(capsule)
            state = updated_state

            # 7. Update Context
            context.add_capsule(capsule)

            # 8. QuantaCoin compression
            compressed = compressor.compress_capsule(capsule)
            raw_json = json.dumps(capsule.encode(), sort_keys=True)
            capsule.compression_ratio = compressor.compression_ratio(
                raw_json.encode("utf-8"),
                compressed,
            )
            capsule.quanta_hash = compressor.hash_capsule(capsule)

            # 9. Print capsule
            print_capsule(capsule)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print()


if __name__ == "__main__":
    main_loop()

