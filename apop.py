#!/usr/bin/env python3
"""
ApopToSiS v3 — PrimeFlux Cognitive Engine

Main entry point for ApopToSiS v3 runtime.

Usage:
    python apop.py "your input text here"
    
Or interactive mode:
    python apop.py
"""

import sys
import os
import json
import argparse

# ANSI color codes for terminal output
RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

# Setup path so ApopToSiS imports work
# The current directory IS the ApopToSiS package root
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)

# Add parent directory so Python can find "ApopToSiS" as a package
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Also add current directory for direct imports
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Now we can import using ApopToSiS prefix
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM
from ApopToSiS.runtime.supervisor.supervisor import Supervisor
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.runtime.autonomous_loop import AutonomousCognitionLoop
from ApopToSiS.quanta.quanta import QuantaCompressor
from ApopToSiS.agents.registry.registry import AgentRegistry
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent
# LLM Bridge imports (optional, will fail gracefully if not available)
try:
    from ApopToSiS.api.remote_llm_bridge import RemoteLLMBridge
    from ApopToSiS.runtime.llm_adapter import LLMAdapter
    LLM_BRIDGE_AVAILABLE = True
except ImportError:
    LLM_BRIDGE_AVAILABLE = False

from ApopToSiS.runtime.recursive_engine import RecursiveLearningEngine
from ApopToSiS.runtime.concept_lattice import ConceptLattice
from ApopToSiS.runtime.identity_core import IdentityCore
from ApopToSiS.experience.manager import ExperienceManager
from ApopToSiS.runtime.experience_state import ExperienceState
# CoSy and PrimeFS imports
from ApopToSiS.core.consensus import CoSyBridgeMain
from ApopToSiS.pf_json import PFJsonGenerator, PFExpander
# PF-aware agent router
try:
    from ApopToSiS.agents.router import AgentRouter
    from ApopToSiS.core.distinction_packet import DistinctionPacket
    AGENT_ROUTER_AVAILABLE = True
except ImportError:
    AGENT_ROUTER_AVAILABLE = False
    AgentRouter = None
    DistinctionPacket = None

# QuantaCoin integration (optional)
try:
    from fluxai.quanta.quanta_core import QuantaCoin
    QUANTA_AVAILABLE = True
except ImportError:
    QUANTA_AVAILABLE = False
    QuantaCoin = None

# Agora integration (optional)
try:
    from fluxai.agora.agora_core import AgoraEcosystem
    AGORA_AVAILABLE = True
except ImportError:
    AGORA_AVAILABLE = False
    AgoraEcosystem = None


def init_runtime():
    """Initialize PF-LCM, state, agents, supervisor."""
    print("⚡ Initializing ApopToSiS v3 runtime...")

    # Initialize ICM and LCM
    icm = ICM()
    lcm = LCM(icm=icm)
    
    # Initialize state and context
    state = PFState()
    context = Context()

    # Initialize Experience Manager
    experience_manager = ExperienceManager()
    lcm.experience_manager = experience_manager
    state.experience_manager = experience_manager
    experience_manager.attach_state(state)

    # Initialize CoSy consensus engine
    cosy = CoSyBridgeMain()

    # Initialize Supervisor
    supervisor = Supervisor(icm=icm, lcm=lcm)
    supervisor.integrate_experience(experience_manager)

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

    # Initialize Recursive Learning Engine (RLE)
    concept_lattice = ConceptLattice()
    identity_core = IdentityCore()
    experience_state = ExperienceState(dim=32)
    rle = RecursiveLearningEngine(
        experience_layer=experience_manager,
        concept_lattice=concept_lattice,
        identity_core=identity_core,
        experience_state=experience_state,
    )

    print("✓ PFState loaded")
    print("✓ LCM initialized")
    print("✓ Supervisor ready")
    print("✓ Agents registered")
    print("✓ Recursive Learning Engine initialized")
    print("✓ CoSy consensus active")

    return state, context, lcm, supervisor, registry, agents, rle, cosy, experience_state


def handle_quanta_command(
    user_input: str,
    supervisor: Supervisor,
    experience_manager: ExperienceManager
) -> dict[str, Any]:
    """
    Handle quanta commands.
    
    Examples:
        quanta txn: budget 250 scheels
        quanta mint: telemetry
        quanta stake: 100
        quanta yield: 2
    
    Args:
        user_input: User input string
        supervisor: Supervisor instance
        experience_manager: ExperienceManager instance
        
    Returns:
        Command result dictionary
    """
    if not QUANTA_AVAILABLE:
        return {
            "status": "error",
            "message": "QuantaCoin not available"
        }
    
    tokens = user_input.lower().split()
    
    if len(tokens) < 2:
        return {
            "status": "error",
            "message": "Invalid quanta command. Use: quanta txn|mint|stake|yield"
        }
    
    command = tokens[1]
    
    if command == "txn" or command == "transaction":
        # Parse transaction: "quanta txn: budget 250 scheels"
        # Extract amount and merchant
        amount = None
        merchant = "unknown"
        
        # Look for numbers in the input
        import re
        numbers = re.findall(r'\d+\.?\d*', user_input)
        if numbers:
            amount = float(numbers[0])
        
        # Look for merchant name (after amount or in input)
        merchant_keywords = ["scheels", "merchant", "store", "shop"]
        for keyword in merchant_keywords:
            if keyword in user_input.lower():
                merchant = keyword
                break
        
        if amount is None:
            return {
                "status": "error",
                "message": "No amount specified in transaction"
            }
        
        # Route through supervisor's quanta_router
        txn_data = {
            "amount": amount,
            "merchant": merchant,
            "holder_prime": 2  # Default prime
        }
        
        result = supervisor.quanta_router(txn_data)
        
        # Etch to experience manager
        if result.get("status") == "success":
            quanta_used = result.get("burned", 0.0)
            experience_delta = {
                "txn_amount": amount,
                "merchant": merchant,
                "quanta_burned": quanta_used
            }
            experience_manager.quanta_etch(
                experience_delta,
                int(quanta_used),
                holder_prime=2
            )
        
        return result
    
    elif command == "mint":
        # Mint from telemetry compression
        try:
            from fluxai.quanta.mining_pilot import MiningPilot
            
            pilot = MiningPilot(quanta_coin=supervisor.quanta_coin)
            telemetry = pilot.generate_telemetry()
            compression_ratio, quanta_minted = pilot.compress_telemetry(telemetry)
            
            return {
                "status": "success",
                "action": "mint",
                "quanta_minted": quanta_minted,
                "compression_ratio": compression_ratio,
                "telemetry": telemetry
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Minting failed: {str(e)}"
            }
    
    elif command == "stake":
        # Stake balance
        import re
        numbers = re.findall(r'\d+\.?\d*', user_input)
        if not numbers:
            return {
                "status": "error",
                "message": "No amount specified for staking"
            }
        
        amount = float(numbers[0])
        holder_prime = 2  # Default
        
        if supervisor.quanta_coin:
            staked = supervisor.quanta_coin.stake_balance(amount, holder_prime, ttl_epochs=30)
            return {
                "status": "success",
                "action": "stake",
                "amount": amount,
                "staked_with_yield": staked,
                "holder_prime": holder_prime
            }
        else:
            return {
                "status": "error",
                "message": "QuantaCoin not initialized"
            }
    
    elif command == "yield":
        # Calculate yield
        import re
        numbers = re.findall(r'\d+', user_input)
        holder_prime = int(numbers[0]) if numbers else 2
        epoch = int(numbers[1]) if len(numbers) > 1 else 0
        
        if supervisor.quanta_coin:
            yield_info = supervisor.quanta_coin.agora_yield_calc(holder_prime, epoch)
            return {
                "status": "success",
                "action": "yield",
                "holder_prime": holder_prime,
                "epoch": epoch,
                **yield_info
            }
        else:
            return {
                "status": "error",
                "message": "QuantaCoin not initialized"
            }
    
    else:
        return {
            "status": "error",
            "message": f"Unknown quanta command: {command}"
        }


def handle_agora_command(
    user_input: str,
    supervisor: Supervisor,
    experience_manager: ExperienceManager
) -> dict[str, Any]:
    """
    Handle agora commands.
    
    Examples:
        agora txn: budget 250 scheels
        agora query: reversal curse
        agora mining: telemetry
    
    Args:
        user_input: User input string
        supervisor: Supervisor instance
        experience_manager: ExperienceManager instance
        
    Returns:
        Command result dictionary
    """
    if not AGORA_AVAILABLE:
        return {
            "status": "error",
            "message": "Agora ecosystem not available"
        }
    
    tokens = user_input.lower().split()
    
    if len(tokens) < 2:
        return {
            "status": "error",
            "message": "Invalid agora command. Use: agora txn|query|mining"
        }
    
    command = tokens[1]
    
    if command == "txn" or command == "transaction":
        # Parse transaction: "agora txn: budget 250 scheels"
        import re
        numbers = re.findall(r'\d+\.?\d*', user_input)
        if not numbers:
            return {
                "status": "error",
                "message": "No amount specified in transaction"
            }
        
        amount = float(numbers[0])
        merchant = "unknown"
        merchant_keywords = ["scheels", "merchant", "store", "shop"]
        for keyword in merchant_keywords:
            if keyword in user_input.lower():
                merchant = keyword
                break
        
        # Route through supervisor's agora_router
        txn_data = {
            "amount": amount,
            "merchant": merchant
        }
        
        result = supervisor.agora_router("txn", txn_data)
        
        # Etch to experience manager
        if result.get("status") == "success":
            agent_prime = result.get("agent_prime", 2)
            quanta_used = result.get("burn_stake", {}).get("burned", 0.0)
            event_delta = {
                "txn_amount": amount,
                "merchant": merchant,
                "quanta_burned": quanta_used
            }
            experience_manager.agora_etch(
                event_delta,
                int(quanta_used),
                agent_prime=agent_prime
            )
        
        return result
    
    elif command == "query":
        # Query: "agora query: reversal curse"
        query = user_input.split(":", 1)[1].strip() if ":" in user_input else " ".join(tokens[2:])
        
        if not query:
            return {
                "status": "error",
                "message": "No query specified"
            }
        
        # Route through supervisor's agora_router
        query_data = {
            "query": query
        }
        
        result = supervisor.agora_router("query", query_data)
        
        # Etch to experience manager
        if result.get("status") == "success":
            agent_prime = result.get("agent_prime", 2)
            grok_result = result.get("grokepedia_result", {})
            quanta_minted = grok_result.get("compressed", {}).get("quanta_minted", 0)
            event_delta = {
                "query": query,
                "quanta_minted": quanta_minted
            }
            experience_manager.agora_etch(
                event_delta,
                quanta_minted,
                agent_prime=agent_prime
            )
        
        return result
    
    elif command == "mining":
        # Mining: "agora mining: telemetry"
        # Generate telemetry data
        try:
            from fluxai.quanta.mining_pilot import MiningPilot
            
            pilot = MiningPilot(quanta_coin=supervisor.quanta_coin)
            telemetry = pilot.generate_telemetry()
            
            # Route through supervisor's agora_router
            mining_data = {
                "telemetry": telemetry
            }
            
            result = supervisor.agora_router("mining", mining_data)
            
            # Etch to experience manager
            if result.get("status") == "success":
                agent_prime = result.get("agent_prime", 2)
                quanta_minted = result.get("quanta_minted", 0)
                event_delta = {
                    "mining": True,
                    "quanta_minted": quanta_minted
                }
                experience_manager.agora_etch(
                    event_delta,
                    quanta_minted,
                    agent_prime=agent_prime
                )
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Mining failed: {str(e)}"
            }
    
    else:
        return {
            "status": "error",
            "message": f"Unknown agora command: {command}"
        }


def print_capsule(capsule: Capsule):
    """Pretty-print capsule JSON in a readable way."""
    data = capsule.encode()
    print(GREEN + "\n=== CAPSULE OUTPUT ===" + RESET)
    print(json.dumps(data, indent=2))


def run_apop_conversation():
    """
    Apop Autonomous Conversational Loop (Patch 005).
    
    Fully offline, cognitive engine-driven conversation.
    """
    # Initialize runtime
    (
        state,
        context,
        lcm,
        supervisor,
        registry,
        agents,
        rle,
        cosy,
        experience_state,
    ) = init_runtime()
    
    # Initialize cognitive engine (autonomous mode)
    from ApopToSiS.cognitive.engine import CognitiveEngine
    
    # Get experience manager from init_runtime
    experience_manager = state.experience_manager
    
    cog = CognitiveEngine(experience_state=experience_state)
    cog.attach_experience(experience_manager)
    
    auto_loop = AutonomousCognitionLoop(
        state=state,
        context=context,
        lcm=lcm,
        rle=rle,
        interval=2.0,
    )
    auto_loop.start()
    print("✓ Autonomous Cognition Loop active (background thinking enabled)")
    
    print("\n" + CYAN + "🌑 ApopToSiS v3 Autonomous Mode Enabled." + RESET)
    print("Speak to Apop. Type 'exit' to stop.\n")
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\n" + CYAN + "Apop: I will remain. Until next time." + RESET + "\n")
                    break
                
                if not user_input:
                    continue
                
                # Check for quanta commands
                if user_input.lower().startswith("quanta"):
                    quanta_result = handle_quanta_command(user_input, supervisor, experience_manager)
                    if quanta_result:
                        print("\n" + GREEN + "=== QUANTACOIN (ΦQ) ===" + RESET)
                        print(json.dumps(quanta_result, indent=2))
                        print(GREEN + "=========================" + RESET + "\n")
                    continue
                
                # Check for agora commands
                if user_input.lower().startswith("agora"):
                    agora_result = handle_agora_command(user_input, supervisor, experience_manager)
                    if agora_result:
                        print("\n" + GREEN + "=== AGORA ECOSYSTEM ===" + RESET)
                        print(json.dumps(agora_result, indent=2))
                        print(GREEN + "========================" + RESET + "\n")
                    continue
                
                # 1. Process through LCM → Capsule
                tokens = user_input.split()
                lcm.process_tokens(tokens)
                capsule_dict = lcm.generate_capsule(tokens=tokens, user_text=user_input)
                capsule = Capsule.decode(capsule_dict) if isinstance(capsule_dict, dict) else Capsule(raw_tokens=tokens)
                capsule.agent_trace = []
                
                # Set measurement_error (duality principle)
                estimated_entropy = capsule.entropy
                observed_entropy = lcm.compute_entropy(tokens) if tokens else 0.0
                capsule.measurement_error = max(0.0, min(1.0, abs(estimated_entropy - observed_entropy)))
                
                # Set quanta hash and compression ratio
                from ApopToSiS.quanta.quanta import QuantaCompressor
                compressor = QuantaCompressor()
                capsule.quanta_hash = compressor.hash_capsule(capsule)
                raw_json = json.dumps(capsule.encode(), sort_keys=True)
                compressed = compressor.compress_capsule(capsule)
                capsule.compression_ratio = compressor.compression_ratio(
                    raw_json.encode("utf-8"),
                    compressed,
                ) if compressed else 1.0
                
                # 2. Update state from capsule
                state.update_from_capsule(capsule)
                
                # 2.5. PF-aware agent routing (if available)
                agent = None
                if AGENT_ROUTER_AVAILABLE and AgentRouter and DistinctionPacket:
                    try:
                        # Create distinction packet from input
                        pkt = DistinctionPacket.from_input(user_input)
                        
                        # Route using PF-aware router
                        agent_router = AgentRouter()
                        agent_name = agent_router.route(pkt)
                        
                        # Log route to experience graph
                        if experience_manager and hasattr(experience_manager, 'graph'):
                            agent_router.log_route(pkt, agent_name, experience_manager.graph)
                        
                        # Find agent by name
                        agent = next((a for a in agents if a.__class__.__name__.lower().startswith(agent_name)), None)
                    except Exception:
                        # Fallback to supervisor routing
                        pass
                
                # 3. Supervisor: Route to an agent (fallback if PF router didn't work)
                if agent is None:
                    agent = supervisor.route(state, agents)
                
                if agent:
                    capsule.agent_trace.append(agent.__class__.__name__)
                    capsule = agent.transform(capsule)
                
                # 4. Update state from processed capsule
                updated_state = supervisor.update_state(capsule)
                state = updated_state
                
                # 5. Integrate capsule (triggers cognitive engine)
                supervisor.integrate_capsule(capsule)
                
                # 6. Recursive learning updates
                learning_report = rle.process(capsule, state)
                
                # 7. Cognitive Engine generates semantic output
                cog_output = cog.process_capsule(
                    capsule,
                    state,
                    context,
                    lattice_summary=learning_report.get("lattice_snapshot"),
                )
                
                # Store in capsule metadata
                capsule.metadata["cog_response"] = cog_output
                capsule.metadata["experience_state"] = cog_output.get("experience_state")
                capsule.experience_delta = cog_output.get("experience_delta", {})
                
                # 8. Store cognitive trace in state
                state.last_cognitive_trace = cog_output
                
                # 9. Display Apop's response (human-facing)
                print("\n" + CYAN + "=== APOP SPEAKS ===" + RESET)
                print(CYAN + cog_output.get('engine_output', cog_output.get('text', 'Processing...')) + RESET)
                if cog_output.get('flux_state'):
                    print(YELLOW + f"(Flux: {cog_output['flux_state']})" + RESET)
                print(CYAN + "=== END OF APOP SPEAKS ===" + RESET + "\n")
                
                # 10. Display recursive learning report
                print("\033[90m=== RECURSIVE LEARNING REPORT ===\033[0m")
                lattice_snapshot = learning_report.get('lattice_snapshot', {})
                identity_snapshot = learning_report.get('identity_snapshot', {})
                experience_snapshot = cog_output.get('experience_state', {})
                experience_delta = cog_output.get('experience_delta', {})
                node_key = 'node_count' if 'node_count' in lattice_snapshot else 'nodes'
                print(f"Lattice Nodes: {lattice_snapshot.get(node_key, 0)}")
                print(f"Identity Drift: {identity_snapshot.get('identity_drift', 0.0):.4f}")
                print(f"Experience Delta: {len(learning_report.get('experience_delta', {}))} updates")
                if experience_snapshot:
                    print(f"Avg Entropy: {experience_snapshot.get('avg_entropy', 0.0):.2f}")
                    print(f"Avg Curvature: {experience_snapshot.get('avg_curvature', 0.0):.2f}")
                    print(f"Interactions: {experience_snapshot.get('interaction_count', 0)}")
                if experience_delta:
                    print(f"Identity Drift Δ: {experience_delta.get('identity_drift', 0.0):.4f}")
                print("\033[90m===================================\033[0m\n")
                
                # 11. Run reversible mining on capsule
                pf_json = PFJsonGenerator().generate(None)
                trust_result = cosy.compile_capsule_trust([])
                coord = trust_result.get("trust_score", 1.0)
                
                print("\033[90m=== APOP COGNITION ===\033[0m")
                print("\033[90mCoSy active. Capsules streaming.\033[0m")
                print(f"\033[90mMined coordinate placeholder: {coord}\033[0m")
                print("\033[90m========================\033[0m\n")
                
                # 12. Print capsule output
                print_capsule(capsule)
                
            except KeyboardInterrupt:
                print("\n" + CYAN + "Apop: I will remain. Until next time." + RESET + "\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                print()
    finally:
        auto_loop.stop()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="ApopToSiS v3 — PrimeFlux Cognitive Engine")
    parser.add_argument("--offline", action="store_true", help="Use offline LLM mode")
    parser.add_argument("--llm-salt", type=str, help="LLM salt (eidos, praxis, aegis)")
    parser.add_argument("input", nargs="?", help="Input text (optional, will use interactive mode if not provided)")
    
    args = parser.parse_args()
    
    # If offline mode, use offline LLM
    if args.offline:
        try:
            from ApopToSiS.runtime.llm_salts import OfflineLLM
            from ApopToSiS.core.distinction_packet import DistinctionPacket
            
            offline_llm = OfflineLLM()
            if args.input:
                # Process single input
                salt = args.llm_salt or "praxis"
                packet = DistinctionPacket.from_input(args.input)
                response = offline_llm.query_salt(salt, args.input)
                print(f"Agent: {salt}")
                print(f"Response: {response}")
                return 0
        except ImportError:
            print("Warning: Offline LLM not available, falling back to normal mode")
    
    # If input provided, process it
    if args.input:
        # Process single input (simplified)
        print(f"Processing: {args.input}")
        # Would integrate with full pipeline here
        return 0
    
    # Run autonomous conversational loop
    run_apop_conversation()
    return 0


if __name__ == "__main__":
    sys.exit(main())
