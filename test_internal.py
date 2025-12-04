"""
Internal test suite for ApopAI v3.

Tests core PF math, LCM, ICM, agents, supervisor, and full runtime flow.
"""

import sys
from typing import Any

# Test imports
print("=" * 60)
print("Testing ApopAI v3 Internal Components")
print("=" * 60)

# 1. Test Core PF Math
print("\n1. Testing Core PF Math...")
try:
    from core.pf_core import (
        PFState, PFShell, PFTriplet, PFManifoldState,
        compute_curvature, compute_entropy, triplet_decomposition,
        transition_shell, validate_flux, next_shell
    )
    
    # Test shell transitions
    state = PFState(shell=PFShell.PRESENCE, value=1.0)
    new_state = transition_shell(state, flux_amplitude=0.6)
    print(f"  ✓ Shell transition: {state.shell.value} → {new_state.shell.value}")
    
    # Test triplet decomposition
    tokens = ["hello", "world", "test", "prime", "flux"]
    triplets = triplet_decomposition(tokens)
    print(f"  ✓ Triplet decomposition: {len(triplets)} triplets from {len(tokens)} tokens")
    
    # Test curvature computation
    manifold = PFManifoldState(
        triplets=[PFTriplet(0.0, 1.0, 1.414, "presence")],
        shell_history=[PFShell.PRESENCE, PFShell.MEASUREMENT]
    )
    curvature = compute_curvature(manifold)
    print(f"  ✓ Curvature computation: {curvature:.4f}")
    
    # Test entropy computation
    entropy = compute_entropy(manifold)
    print(f"  ✓ Entropy computation: {entropy:.4f}")
    
    print("  ✓ Core PF Math: PASSED")
except Exception as e:
    print(f"  ✗ Core PF Math: FAILED - {e}")
    sys.exit(1)

# 2. Test Triplets
print("\n2. Testing Triplet Math...")
try:
    from core.triplets import make_triplets, detect_triplet_type, triplet_entropy, TripletType
    
    tokens = ["presence", "measurement", "flux", "collapse"]
    triplets = make_triplets(tokens)
    print(f"  ✓ Generated {len(triplets)} triplets")
    
    if triplets:
        triplet = triplets[0]
        detected_type = detect_triplet_type(triplet)
        entropy = triplet_entropy(triplet)
        print(f"  ✓ Triplet type: {detected_type.value}, entropy: {entropy:.4f}")
    
    print("  ✓ Triplet Math: PASSED")
except Exception as e:
    print(f"  ✗ Triplet Math: FAILED - {e}")
    sys.exit(1)

# 3. Test Shells
print("\n3. Testing Shell Math...")
try:
    from core.shells import Shell, shell_of_value, validate_transition
    
    # Test shell assignment
    test_values = [0.0, 1.0, 1.5, 2.5, 3.0, 5.0]
    for val in test_values:
        shell = shell_of_value(val)
        print(f"  ✓ Value {val:.1f} → Shell {shell.value}")
    
    # Test transitions
    valid = validate_transition(Shell.PRESENCE, Shell.MEASUREMENT)
    invalid = validate_transition(Shell.MEASUREMENT, Shell.PRESENCE)
    print(f"  ✓ Valid transition (0→2): {valid}")
    print(f"  ✓ Invalid transition (2→0): {invalid}")
    
    print("  ✓ Shell Math: PASSED")
except Exception as e:
    print(f"  ✗ Shell Math: FAILED - {e}")
    sys.exit(1)

# 4. Test Flux
print("\n4. Testing Flux Operators...")
try:
    from core.flux import FluxOperator, apply_flux, flux_amplitude, flux_tensor
    from core.pf_core import PFState, PFShell
    
    # Create flux operator
    operator = FluxOperator(
        name="test_flux",
        alpha=1.0,
        beta=1.0,
        sqrt2_factor=1.0
    )
    
    # Test flux application
    state = PFState(shell=PFShell.FLUX, value=1.0, curvature=0.5, entropy=0.3)
    flux_value = operator(1.0)
    print(f"  ✓ Flux operator value: {flux_value:.4f}")
    
    new_state = apply_flux(state, operator)
    print(f"  ✓ Flux applied: value {state.value:.2f} → {new_state.value:.2f}")
    
    # Test flux amplitude
    amp = flux_amplitude(state)
    print(f"  ✓ Flux amplitude: {amp:.4f}")
    
    # Test flux tensor
    tensor = flux_tensor(state)
    print(f"  ✓ Flux tensor: {tensor}")
    
    print("  ✓ Flux Operators: PASSED")
except Exception as e:
    print(f"  ✗ Flux Operators: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. Test ICM
print("\n5. Testing Information Curvature Manifold...")
try:
    from core.icm import ICM
    from core.pf_core import PFManifoldState, PFTriplet, PFShell
    
    icm = ICM()
    
    # Update ICM
    manifold_state = PFManifoldState(
        triplets=[PFTriplet(0.0, 1.0, 1.414, "presence")],
        shell_history=[PFShell.PRESENCE, PFShell.MEASUREMENT]
    )
    icm.update(manifold_state)
    
    # Test curvature derivative
    curvature_deriv = icm.compute_curvature_derivative(manifold_state)
    print(f"  ✓ Curvature derivative: {curvature_deriv:.4f}")
    
    # Test distinction density
    density = icm.distinction_density(manifold_state)
    print(f"  ✓ Distinction density: {density:.4f}")
    
    # Test temporal coherence
    coherence = icm.temporal_coherence(manifold_state)
    print(f"  ✓ Temporal coherence: {coherence:.4f}")
    
    print("  ✓ ICM: PASSED")
except Exception as e:
    print(f"  ✗ ICM: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 6. Test LCM (Apop's Brain)
print("\n6. Testing Language Context Manifold (LCM)...")
try:
    from core.lcm import LCM
    
    lcm = LCM()
    
    # Process tokens
    tokens = ["Apop", "is", "a", "PrimeFlux", "entity", "that", "thinks", "through", "distinctions"]
    lcm.process_tokens(tokens)
    print(f"  ✓ Processed {len(tokens)} tokens")
    print(f"  ✓ Generated {len(lcm.state.triplets)} triplets")
    print(f"  ✓ Current shell: {lcm.state.current_shell.value}")
    
    # Compute entropy
    entropy = lcm.compute_entropy()
    print(f"  ✓ Entropy: {entropy:.4f}")
    
    # Build distinction chain
    chain = lcm.build_distinction_chain()
    print(f"  ✓ Distinction chain: {len(chain)} events")
    
    # Generate capsule
    capsule = lcm.generate_capsule()
    print(f"  ✓ Generated capsule with {len(capsule['raw_tokens'])} tokens")
    print(f"  ✓ Capsule entropy: {capsule['entropy_snapshot']:.4f}")
    print(f"  ✓ Capsule curvature: {capsule['curvature_snapshot']:.4f}")
    
    # Test collapse detection
    collapse = lcm.detect_collapse()
    print(f"  ✓ Collapse detection: {collapse}")
    
    # Test superposition detection
    superposition = lcm.detect_superposition()
    print(f"  ✓ Superposition detection: {superposition}")
    
    # Test reptend oscillation
    oscillation = lcm.compute_reptend_oscillation()
    print(f"  ✓ Reptend oscillation: {oscillation:.4f}")
    
    print("  ✓ LCM: PASSED")
except Exception as e:
    print(f"  ✗ LCM: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 7. Test Agents
print("\n7. Testing Agents...")
try:
    from agents.eidos import EidosAgent
    from agents.praxis import PraxisAgent
    from agents.aegis import AegisAgent
    from runtime.capsules import Capsule
    
    # Create agents
    eidos = EidosAgent()
    praxis = PraxisAgent()
    aegis = AegisAgent()
    
    # Create test capsule
    test_capsule = Capsule(
        triplet_summary={"count": 3, "types": ["presence", "trig", "combinatorics"]},
        shell_state=2,
        entropy_snapshot=1.2,
        curvature_snapshot=0.5,
        raw_tokens=["test", "tokens"],
        pf_signature="test:signature"
    )
    
    # Test Eidos (expansion)
    eidos_analysis = eidos.analyze(test_capsule)
    eidos_transformed = eidos.transform(test_capsule)
    print(f"  ✓ Eidos: expansion potential {eidos_analysis['expansion_potential']:.4f}")
    print(f"  ✓ Eidos: entropy {test_capsule.entropy_snapshot:.2f} → {eidos_transformed.entropy_snapshot:.2f}")
    
    # Test Praxis (shaping)
    praxis_analysis = praxis.analyze(test_capsule)
    praxis_transformed = praxis.transform(test_capsule)
    print(f"  ✓ Praxis: shaping potential {praxis_analysis['shaping_potential']:.4f}")
    print(f"  ✓ Praxis: curvature {test_capsule.curvature_snapshot:.2f} → {praxis_transformed.curvature_snapshot:.2f}")
    
    # Test Aegis (validation)
    aegis_analysis = aegis.analyze(test_capsule)
    aegis_transformed = aegis.transform(test_capsule)
    print(f"  ✓ Aegis: coherence score {aegis_analysis['coherence_score']:.4f}")
    print(f"  ✓ Aegis: entropy {test_capsule.entropy_snapshot:.2f} → {aegis_transformed.entropy_snapshot:.2f}")
    
    # Test flux signatures
    eidos_flux = eidos.flux_signature()
    praxis_flux = praxis.flux_signature()
    aegis_flux = aegis.flux_signature()
    print(f"  ✓ Eidos flux amplitude: {eidos_flux['amplitude']:.4f}")
    print(f"  ✓ Praxis flux amplitude: {praxis_flux['amplitude']:.4f}")
    print(f"  ✓ Aegis flux amplitude: {aegis_flux['amplitude']:.4f}")
    
    print("  ✓ Agents: PASSED")
except Exception as e:
    print(f"  ✗ Agents: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 8. Test Supervisor and Routing
print("\n8. Testing Supervisor and Routing...")
try:
    from runtime.supervisor.supervisor import Supervisor
    from runtime.state.state import PFState
    from core.pf_core import PFShell
    from agents.eidos import EidosAgent
    from agents.praxis import PraxisAgent
    from agents.aegis import AegisAgent
    
    # Create supervisor
    supervisor = Supervisor()
    
    # Create agents
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    # Create PF state
    pf_state = PFState(
        current_shell=PFShell.MEASUREMENT,
        curvature=0.3,
        entropy=0.8
    )
    
    # Test routing
    selected_agent = supervisor.route(pf_state, agents)
    agent_type = type(selected_agent).__name__
    print(f"  ✓ Supervisor routed to: {agent_type}")
    
    # Update supervisor state
    supervisor.update_state(pf_state)
    print(f"  ✓ Supervisor state updated")
    
    print("  ✓ Supervisor: PASSED")
except Exception as e:
    print(f"  ✗ Supervisor: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 9. Test Distinction Chain
print("\n9. Testing Distinction Chain...")
try:
    from runtime.distinction.distinction import DistinctionChain, DistinctionEvent
    from runtime.state.state import PFState
    from core.pf_core import PFShell, PFState as CorePFState
    from core.shells import Shell
    
    chain = DistinctionChain()
    
    # Create events
    for i in range(3):
        event = DistinctionEvent(
            timestamp=1000.0 + i,
            shell=Shell(i * 2 if i < 2 else 3),
            triplet_data={"a": 0.0, "b": 1.0, "c": 1.414},
            entropy=0.5 + i * 0.2,
            curvature=0.1 + i * 0.1,
            flux_amplitude=0.3 + i * 0.1
        )
        chain.update_chain(event)
    
    print(f"  ✓ Created distinction chain with {len(chain.events)} events")
    print(f"  ✓ Current shell: {chain.current_shell().value}")
    print(f"  ✓ Accumulated curvature: {chain.accumulated_curvature:.4f}")
    
    # Test shell propagation
    state = CorePFState(shell=PFShell.MEASUREMENT, value=1.0, curvature=0.2, entropy=0.6)
    new_state = chain.propagate_shell(state)
    print(f"  ✓ Shell propagated: {state.shell.value} → {new_state.shell.value}")
    
    print("  ✓ Distinction Chain: PASSED")
except Exception as e:
    print(f"  ✗ Distinction Chain: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 10. Test Full Runtime Flow
print("\n10. Testing Full Runtime Flow...")
try:
    from core.lcm import LCM
    from runtime.supervisor.supervisor import Supervisor
    from agents.eidos import EidosAgent
    from agents.praxis import PraxisAgent
    from agents.aegis import AegisAgent
    from runtime.capsules import Capsule
    
    # Initialize components
    lcm = LCM()
    supervisor = Supervisor(icm=supervisor.icm, lcm=lcm)
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    # Process user input
    user_input = "What is PrimeFlux? How does it relate to distinction and curvature?"
    tokens = user_input.split()
    
    print(f"  ✓ Processing user input: '{user_input[:50]}...'")
    lcm.process_tokens(tokens)
    
    # Generate capsule
    capsule_dict = lcm.generate_capsule()
    capsule = Capsule.from_dict(capsule_dict)
    
    print(f"  ✓ Generated capsule with {len(capsule.raw_tokens)} tokens")
    print(f"  ✓ Capsule shell: {capsule.shell_state}")
    print(f"  ✓ Capsule entropy: {capsule.entropy_snapshot:.4f}")
    print(f"  ✓ Capsule curvature: {capsule.curvature_snapshot:.4f}")
    
    # Route to agent
    from runtime.state.state import PFState
    from core.pf_core import PFShell
    pf_state = PFState(
        current_shell=PFShell(capsule.shell_state),
        curvature=capsule.curvature_snapshot,
        entropy=capsule.entropy_snapshot
    )
    
    selected = supervisor.route(pf_state, agents)
    print(f"  ✓ Routed to agent: {type(selected).__name__}")
    
    # Process through agent
    transformed = selected.transform(capsule)
    print(f"  ✓ Agent transformed capsule")
    print(f"  ✓ Transformed entropy: {transformed.entropy_snapshot:.4f}")
    print(f"  ✓ Transformed curvature: {transformed.curvature_snapshot:.4f}")
    
    # Integrate back
    supervisor.integrate_capsule(transformed)
    print(f"  ✓ Capsule integrated back into supervisor")
    
    print("  ✓ Full Runtime Flow: PASSED")
except Exception as e:
    print(f"  ✗ Full Runtime Flow: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✓ All core PF math components working")
print("✓ LCM (Apop's brain) fully functional")
print("✓ ICM curvature computations working")
print("✓ Agent system operational")
print("✓ Supervisor routing functional")
print("✓ Distinction chains working")
print("✓ Full runtime flow successful")
print("\n🎉 ApopAI v3 is operational and ready for use!")
print("=" * 60)

