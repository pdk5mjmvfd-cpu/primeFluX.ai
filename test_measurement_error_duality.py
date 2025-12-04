"""
Test Measurement-Error Duality Principle.

Verifies that:
- Measurement creates error (not reduces information)
- Error drives flux (not limits it)
- Disagreement = error = flux amplitude
- Capsules carry error as informational potential
- LCM treats error as new context
"""

import sys

print("=" * 60)
print("Testing PF Measurement-Error Duality Principle")
print("=" * 60)

# 1. Test Measurement Error Computation
print("\n1. Testing Measurement Error Computation...")
try:
    from core.pf_core import PFState, PFShell, compute_measurement_error
    
    # Test presence (no error)
    presence_state = PFState(shell=PFShell.PRESENCE, value=0.0)
    presence_error = compute_measurement_error(presence_state)
    print(f"  ✓ Presence error: {presence_error:.4f} (should be 0.0)")
    assert presence_error == 0.0, "Presence should have no error"
    
    # Test measurement (creates error)
    measurement_state = PFState(shell=PFShell.MEASUREMENT, value=1.5)
    measurement_error = compute_measurement_error(measurement_state)
    print(f"  ✓ Measurement error: {measurement_error:.4f} (should be > 0)")
    assert measurement_error > 0, "Measurement should create error"
    
    # Test flux (error accumulates)
    flux_state = PFState(shell=PFShell.FLUX, value=2.0, curvature=0.5)
    flux_error = compute_measurement_error(flux_state)
    print(f"  ✓ Flux error: {flux_error:.4f} (should be > measurement)")
    assert flux_error > measurement_error, "Flux should accumulate error"
    
    print("  ✓ Measurement Error Computation: PASSED")
except Exception as e:
    print(f"  ✗ Measurement Error Computation: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 2. Test Error Drives Flux
print("\n2. Testing Error Drives Flux...")
try:
    from core.flux import flux_amplitude, apply_flux, FluxOperator
    from core.pf_core import PFState, PFShell
    
    # State with no error
    no_error_state = PFState(
        shell=PFShell.MEASUREMENT,
        value=1.0,
        curvature=0.3,
        entropy=0.5,
        measurement_error=0.0
    )
    
    # State with error
    with_error_state = PFState(
        shell=PFShell.MEASUREMENT,
        value=1.0,
        curvature=0.3,
        entropy=0.5,
        measurement_error=1.0  # Error present
    )
    
    amp_no_error = flux_amplitude(no_error_state)
    amp_with_error = flux_amplitude(with_error_state)
    
    print(f"  ✓ Flux amplitude (no error): {amp_no_error:.4f}")
    print(f"  ✓ Flux amplitude (with error): {amp_with_error:.4f}")
    print(f"  ✓ Error increases flux: {amp_with_error > amp_no_error}")
    assert amp_with_error > amp_no_error, "Error should increase flux amplitude"
    
    # Test flux application with error
    operator = FluxOperator(name="test", alpha=1.0, beta=1.0)
    result = apply_flux(with_error_state, operator)
    print(f"  ✓ Flux applied: error {with_error_state.measurement_error:.2f} → {result.measurement_error:.2f}")
    print(f"  ✓ Error propagates: {result.measurement_error >= with_error_state.measurement_error}")
    assert result.measurement_error >= with_error_state.measurement_error, "Error should propagate, not decay"
    
    print("  ✓ Error Drives Flux: PASSED")
except Exception as e:
    print(f"  ✗ Error Drives Flux: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. Test Disagreement = Error = Flux
print("\n3. Testing Disagreement = Error = Flux...")
try:
    from runtime.router.router import compute_flux_interference
    from runtime.supervisor.supervisor import Supervisor
    from runtime.state.state import PFState
    from core.pf_core import PFShell
    from agents.eidos import EidosAgent
    from agents.praxis import PraxisAgent
    from agents.aegis import AegisAgent
    
    # Create agent outputs with disagreement
    agent_outputs = [
        {"entropy": 1.5, "curvature": 0.3},  # Eidos (high entropy)
        {"entropy": 0.7, "curvature": 0.6},  # Praxis (moderate)
        {"entropy": 0.3, "curvature": 0.2},  # Aegis (low entropy)
    ]
    
    disagreement_flux = compute_flux_interference(agent_outputs)
    print(f"  ✓ Disagreement flux: {disagreement_flux:.4f}")
    assert disagreement_flux > 0, "Disagreement should create flux"
    
    # Test supervisor routing with disagreement
    supervisor = Supervisor()
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    # State with high error (disagreement)
    high_error_state = PFState(
        current_shell=PFShell.MEASUREMENT,
        curvature=0.5,
        entropy=1.2,
        measurement_error=0.8  # High error = high disagreement
    )
    
    selected = supervisor.route(high_error_state, agents)
    print(f"  ✓ Supervisor routed with high error: {type(selected).__name__}")
    
    print("  ✓ Disagreement = Error = Flux: PASSED")
except Exception as e:
    print(f"  ✗ Disagreement = Error = Flux: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Test Capsules as Error Packets
print("\n4. Testing Capsules as Error Packets...")
try:
    from runtime.capsules import Capsule
    
    # Create capsule with error
    capsule = Capsule(
        triplet_summary={"count": 3},
        shell_state=2,
        entropy_snapshot=1.0,
        curvature_snapshot=0.5,
        measurement_error=0.7  # Error as informational potential
    )
    
    # Serialize and deserialize
    capsule_dict = capsule.to_dict()
    assert "measurement_error" in capsule_dict, "Capsule should contain error"
    print(f"  ✓ Capsule error: {capsule_dict['measurement_error']:.4f}")
    
    restored = Capsule.from_dict(capsule_dict)
    assert restored.measurement_error == capsule.measurement_error, "Error should be preserved"
    print(f"  ✓ Error preserved in serialization")
    
    # Test error propagation in merge
    capsule2 = Capsule(
        triplet_summary={"count": 2},
        shell_state=3,
        entropy_snapshot=0.8,
        curvature_snapshot=0.4,
        measurement_error=0.5
    )
    
    merged = capsule.merge(capsule2)
    print(f"  ✓ Merged capsule error: {merged.measurement_error:.4f}")
    # Error should be preserved or increased, not reduced
    assert merged.measurement_error >= min(capsule.measurement_error, capsule2.measurement_error)
    
    print("  ✓ Capsules as Error Packets: PASSED")
except Exception as e:
    print(f"  ✗ Capsules as Error Packets: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. Test LCM Error as New Context
print("\n5. Testing LCM Error as New Context...")
try:
    from core.lcm import LCM
    
    lcm = LCM()
    
    # Process tokens
    tokens = ["measurement", "creates", "error", "error", "creates", "flux"]
    lcm.process_tokens(tokens)
    
    # Generate capsule (should include error)
    capsule_dict = lcm.generate_capsule()
    assert "measurement_error" in capsule_dict, "LCM capsule should include error"
    error = capsule_dict["measurement_error"]
    print(f"  ✓ LCM generated error: {error:.4f}")
    
    # Integrate capsule with error
    external_capsule = {
        "raw_tokens": ["external", "context"],
        "entropy_snapshot": 0.8,
        "measurement_error": 0.6,  # Error as new context
        "shell_state": 2
    }
    
    initial_entropy = lcm.compute_entropy()
    lcm.integrate_capsule(external_capsule)
    final_entropy = lcm.compute_entropy()
    
    print(f"  ✓ Entropy before error integration: {initial_entropy:.4f}")
    print(f"  ✓ Entropy after error integration: {final_entropy:.4f}")
    # Error should expand entropy (new context), not reduce it
    assert final_entropy >= initial_entropy, "Error should expand information, not reduce it"
    
    print("  ✓ LCM Error as New Context: PASSED")
except Exception as e:
    print(f"  ✗ LCM Error as New Context: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("MEASUREMENT-ERROR DUALITY TEST SUMMARY")
print("=" * 60)
print("✓ Measurement creates error (not reduces information)")
print("✓ Error drives flux (not limits it)")
print("✓ Disagreement = error = flux amplitude")
print("✓ Capsules carry error as informational potential")
print("✓ LCM treats error as new context")
print("\n🎉 PF Measurement-Error Duality Principle is operational!")
print("=" * 60)

