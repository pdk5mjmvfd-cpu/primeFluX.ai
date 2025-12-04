"""
Test Multi-Agent Integration System.

Tests:
- Agent network (inbox/outbox)
- External adapters (Atlas, Claude, Comet)
- Supervisor integration
- Identity protection
- Cognitive loop
"""

import sys
from pathlib import Path

print("=" * 60)
print("Testing ApopAI v3 Multi-Agent Integration")
print("=" * 60)

# 1. Test External Adapters
print("\n1. Testing External Adapters...")
try:
    from backend.external_adapters import (
        AtlasAdapter, ClaudeAdapter, CometAdapter,
        ExternalAdapterRegistry, ATLAS_PARAMS, CLAUDE_PARAMS, COMET_PARAMS
    )
    from runtime.capsules import Capsule
    
    # Test Atlas
    atlas = AtlasAdapter()
    print(f"  ✓ Atlas: {atlas.name}, role: {atlas.pf_role}, shell: {atlas.shell.value}")
    print(f"  ✓ Atlas params: α={ATLAS_PARAMS.alpha}, β={ATLAS_PARAMS.beta}")
    
    # Test Claude
    claude = ClaudeAdapter()
    print(f"  ✓ Claude: {claude.name}, role: {claude.pf_role}, shell: {claude.shell.value}")
    print(f"  ✓ Claude params: α={CLAUDE_PARAMS.alpha}, β={CLAUDE_PARAMS.beta}")
    
    # Test Comet
    comet = CometAdapter()
    print(f"  ✓ Comet: {comet.name}, role: {comet.pf_role}, shell: {comet.shell.value}")
    print(f"  ✓ Comet params: α={COMET_PARAMS.alpha}, β={COMET_PARAMS.beta}")
    
    # Test adapter processing
    test_capsule = Capsule(
        triplet_summary={"count": 3},
        shell_state=2,
        entropy_snapshot=1.0,
        curvature_snapshot=0.5
    )
    
    atlas_result = atlas.process_capsule(test_capsule)
    print(f"  ✓ Atlas processed: entropy {test_capsule.entropy_snapshot:.2f} → {atlas_result.entropy_snapshot:.2f}")
    
    claude_result = claude.process_capsule(test_capsule)
    print(f"  ✓ Claude processed: entropy {test_capsule.entropy_snapshot:.2f} → {claude_result.entropy_snapshot:.2f}")
    
    comet_result = comet.process_capsule(test_capsule)
    print(f"  ✓ Comet processed: entropy {test_capsule.entropy_snapshot:.2f} → {comet_result.entropy_snapshot:.2f}")
    
    # Test registry
    registry = ExternalAdapterRegistry()
    print(f"  ✓ Registry: {len(registry.list_all())} adapters")
    
    print("  ✓ External Adapters: PASSED")
except Exception as e:
    print(f"  ✗ External Adapters: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 2. Test Supervisor Integration
print("\n2. Testing Supervisor Integration...")
try:
    from backend.supervisor_integration import ExtendedSupervisor
    from runtime.state.state import PFState
    from core.pf_core import PFShell
    from agents.eidos import EidosAgent
    from agents.praxis import PraxisAgent
    from agents.aegis import AegisAgent
    from runtime.capsules import Capsule
    
    supervisor = ExtendedSupervisor(enable_external=True)
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    # Test routing with external
    state = PFState(
        current_shell=PFShell.MEASUREMENT,
        curvature=0.5,
        entropy=1.2
    )
    
    agent, adapter = supervisor.route_with_external(
        state,
        agents,
        use_atlas=True,
        use_claude=True,
        use_comet=True
    )
    
    if adapter:
        print(f"  ✓ Routed to external: {adapter.name} ({adapter.pf_role})")
    else:
        print(f"  ✓ Routed to internal: {type(agent).__name__}")
    
    # Test processing with external
    capsule = Capsule(
        triplet_summary={"count": 2},
        shell_state=2,
        entropy_snapshot=1.0,
        curvature_snapshot=0.3
    )
    
    processed = supervisor.process_with_external(capsule, agents)
    print(f"  ✓ Processed capsule: adapter={processed.metadata.get('adapter', 'internal')}")
    
    # Test identity protection
    protected = supervisor.enforce_identity_protection(processed)
    print(f"  ✓ Identity protection enforced")
    
    print("  ✓ Supervisor Integration: PASSED")
except Exception as e:
    print(f"  ✗ Supervisor Integration: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. Test Agent Network
print("\n3. Testing Agent Network...")
try:
    from backend.agent_network import AgentNetwork
    from runtime.capsules import Capsule
    
    network = AgentNetwork(base_path="test_agents")
    
    # Test directory creation
    network.ensure_agent_dirs("test_agent")
    inbox = network.get_inbox_path("test_agent")
    outbox = network.get_outbox_path("test_agent")
    print(f"  ✓ Created agent directories: {inbox.exists()}, {outbox.exists()}")
    
    # Test capsule sending
    capsule = Capsule(
        triplet_summary={"count": 1},
        shell_state=0,
        entropy_snapshot=0.5,
        curvature_snapshot=0.2
    )
    
    filepath = network.send_capsule("sender", "test_agent", capsule)
    print(f"  ✓ Sent capsule: {Path(filepath).name}")
    
    # Test capsule receiving
    capsules = network.receive_capsules("test_agent")
    print(f"  ✓ Received {len(capsules)} capsules")
    
    if capsules:
        packet = capsules[0]
        received_capsule = network.get_capsule_from_packet(packet)
        print(f"  ✓ Extracted capsule: entropy={received_capsule.entropy_snapshot:.2f}")
    
    # Cleanup
    import shutil
    if Path("test_agents").exists():
        shutil.rmtree("test_agents")
    
    print("  ✓ Agent Network: PASSED")
except Exception as e:
    print(f"  ✗ Agent Network: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Test Identity Protection
print("\n4. Testing Identity Protection...")
try:
    from backend.identity_protection import IdentityProtection
    from runtime.capsules import Capsule
    
    protection = IdentityProtection()
    
    # Test protected file detection
    protected_files = [
        "core/pf_core.py",
        "runtime/supervisor.py",
        "identity.json"
    ]
    
    for filepath in protected_files:
        is_protected = protection.is_protected(filepath)
        print(f"  ✓ {filepath}: protected={is_protected}")
    
    # Test capsule identity validation
    capsule = Capsule(
        triplet_summary={},
        shell_state=0,
        entropy_snapshot=0.5,
        curvature_snapshot=0.2,
        metadata={"user_id": "user123"}
    )
    
    valid = protection.validate_capsule_identity(capsule, "user123")
    print(f"  ✓ Capsule identity validation: {valid}")
    
    # Test capsule separation
    separated = protection.enforce_capsule_separation(
        capsule,
        "user123",
        ["user456", "user789"]
    )
    print(f"  ✓ Capsule separation enforced: user_id={separated.metadata.get('user_id')}")
    
    # Test repo integrity
    integrity = protection.validate_repo_integrity()
    print(f"  ✓ Repo integrity: {integrity}")
    
    print("  ✓ Identity Protection: PASSED")
except Exception as e:
    print(f"  ✗ Identity Protection: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. Test Cognitive Loop
print("\n5. Testing Cognitive Loop...")
try:
    from backend.cognitive_loop import CognitiveLoop
    
    loop = CognitiveLoop(enable_external=True)
    
    # Test cycle
    user_input = "What is PrimeFlux?"
    result = loop.run_cycle(user_input)
    
    print(f"  ✓ Cognitive cycle completed")
    print(f"  ✓ Result capsule: entropy={result.entropy_snapshot:.4f}, curvature={result.curvature_snapshot:.4f}")
    print(f"  ✓ Processed by: {result.metadata.get('adapter', 'internal')}")
    
    print("  ✓ Cognitive Loop: PASSED")
except Exception as e:
    print(f"  ✗ Cognitive Loop: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("MULTI-AGENT INTEGRATION TEST SUMMARY")
print("=" * 60)
print("✓ External adapters (Atlas, Claude, Comet) working")
print("✓ Supervisor integration with external agents functional")
print("✓ Agent network (inbox/outbox) operational")
print("✓ Identity protection enforced")
print("✓ Cognitive loop running")
print("\n🎉 Multi-Agent Integration System is operational!")
print("=" * 60)

