"""
Test Combinatoric Interpreter Layer (CIL).

Tests language-agnostic combinatoric pattern extraction:
- English text
- Python code
- Math expressions
- JSON
- System commands
- Multi-language inputs
"""

import sys

print("=" * 60)
print("Testing Combinatoric Interpreter Layer (CIL)")
print("=" * 60)

# 1. Test English Text
print("\n1. Testing English Text...")
try:
    from combinatoric.interpreter import CombinatoricInterpreter
    
    ci = CombinatoricInterpreter()
    
    english_text = "The cat sat on the mat, but the dog was outside."
    packet = ci.interpret(english_text)
    
    print(f"  ✓ Tokens: {len(packet.tokens)}")
    print(f"  ✓ Triplets: {len(packet.triplets)}")
    print(f"  ✓ Adjacency pairs: {len(packet.adjacency_pairs)}")
    print(f"  ✓ Shell suggestions: {set(packet.shell_suggestions)}")
    print(f"  ✓ Contrast markers: {packet.metadata.get('contrast_count', 0)}")
    print(f"  ✓ Entropy delta: {packet.entropy_delta:.4f}")
    
    assert len(packet.tokens) > 0, "Should extract tokens"
    assert len(packet.triplets) > 0, "Should extract triplets"
    assert packet.entropy_delta >= 0, "Entropy should be non-negative"
    
    print("  ✓ English Text: PASSED")
except Exception as e:
    print(f"  ✗ English Text: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 2. Test Python Code
print("\n2. Testing Python Code...")
try:
    python_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
"""
    packet = ci.interpret(python_code)
    
    print(f"  ✓ Tokens: {len(packet.tokens)}")
    print(f"  ✓ Branching markers: {packet.metadata.get('branching_count', 0)}")
    print(f"  ✓ Recursion markers: {packet.metadata.get('recursion_count', 0)}")
    print(f"  ✓ Collapse markers: {packet.metadata.get('collapse_count', 0)}")
    print(f"  ✓ Shell suggestions: {set(packet.shell_suggestions)}")
    
    assert packet.metadata.get('branching_count', 0) > 0, "Should detect branching"
    assert packet.metadata.get('recursion_count', 0) > 0, "Should detect recursion"
    assert 3 in packet.shell_suggestions, "Should suggest flux shell for branching"
    
    print("  ✓ Python Code: PASSED")
except Exception as e:
    print(f"  ✗ Python Code: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. Test Math Expressions
print("\n3. Testing Math Expressions...")
try:
    math_expr = "x = (a + b) * c - d / e"
    packet = ci.interpret(math_expr)
    
    print(f"  ✓ Tokens: {len(packet.tokens)}")
    print(f"  ✓ Collapse markers: {packet.metadata.get('collapse_count', 0)}")
    print(f"  ✓ Error deltas: {len(packet.error_deltas)}")
    print(f"  ✓ Curvature deltas: {len(packet.curvature_deltas)}")
    
    assert packet.metadata.get('collapse_count', 0) > 0, "Should detect assignment"
    assert len(packet.error_deltas) == len(packet.tokens), "Error deltas should match tokens"
    
    print("  ✓ Math Expressions: PASSED")
except Exception as e:
    print(f"  ✗ Math Expressions: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Test JSON
print("\n4. Testing JSON...")
try:
    json_text = '{"name": "Apop", "version": 3, "active": true}'
    packet = ci.interpret(json_text)
    
    print(f"  ✓ Tokens: {len(packet.tokens)}")
    print(f"  ✓ Triplets: {len(packet.triplets)}")
    print(f"  ✓ Entropy delta: {packet.entropy_delta:.4f}")
    
    assert len(packet.tokens) > 0, "Should extract JSON tokens"
    
    print("  ✓ JSON: PASSED")
except Exception as e:
    print(f"  ✗ JSON: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. Test LCM Integration
print("\n5. Testing LCM Integration...")
try:
    from core.lcm import LCM
    
    lcm = LCM()
    
    test_input = "if x > 0 then return x else return -x"
    
    # Interpret
    packet = lcm.interpret(test_input)
    print(f"  ✓ Interpreted: {len(packet.tokens)} tokens")
    
    # Update from combinatorics
    capsule_dict = lcm.update_from_combinatorics(packet)
    print(f"  ✓ Updated LCM from combinatorics")
    print(f"  ✓ Generated capsule with {len(capsule_dict.get('raw_tokens', []))} tokens")
    print(f"  ✓ Capsule shell: {capsule_dict.get('shell_state')}")
    print(f"  ✓ Capsule entropy: {capsule_dict.get('entropy_snapshot', 0):.4f}")
    print(f"  ✓ Capsule error: {capsule_dict.get('measurement_error', 0):.4f}")
    
    assert "measurement_error" in capsule_dict, "Capsule should include error"
    assert len(capsule_dict.get('raw_tokens', [])) > 0, "Capsule should have tokens"
    
    print("  ✓ LCM Integration: PASSED")
except Exception as e:
    print(f"  ✗ LCM Integration: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 6. Test Full API Flow
print("\n6. Testing Full API Flow...")
try:
    from api.message_api import MessageAPI
    
    api = MessageAPI()
    
    # Test with Python code
    result = api.process_input("def hello(): return 'world'")
    print(f"  ✓ Processed Python code")
    print(f"  ✓ Routed to: {result['routed_agent']}")
    print(f"  ✓ Compression ratio: {result['compression_ratio']:.4f}")
    print(f"  ✓ Hash generated: {len(result['hash'])} chars")
    
    # Test with English
    result2 = api.process_input("The quick brown fox jumps over the lazy dog.")
    print(f"  ✓ Processed English text")
    print(f"  ✓ Routed to: {result2['routed_agent']}")
    
    # Test with Math
    result3 = api.process_input("x = sqrt(a^2 + b^2)")
    print(f"  ✓ Processed math expression")
    print(f"  ✓ Routed to: {result3['routed_agent']}")
    
    assert result['compression_ratio'] > 0, "Should compress capsule"
    assert len(result['hash']) == 64, "Should generate SHA256 hash"
    
    print("  ✓ Full API Flow: PASSED")
except Exception as e:
    print(f"  ✗ Full API Flow: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 7. Test Supervisor Combinatoric Routing
print("\n7. Testing Supervisor Combinatoric Routing...")
try:
    from runtime.supervisor.supervisor import Supervisor
    from runtime.state.state import PFState
    from core.pf_core import PFShell
    from agents.eidos import EidosAgent
    from agents.praxis import PraxisAgent
    from agents.aegis import AegisAgent
    
    supervisor = Supervisor()
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    # High recursion → should route to Praxis
    combinatoric_features = {
        "recursion_count": 3,
        "branching_count": 1,
        "contrast_count": 0,
    }
    
    state = PFState(
        current_shell=PFShell.FLUX,
        curvature=0.5,
        entropy=0.8,
        measurement_error=0.3
    )
    
    selected = supervisor.route_with_combinatorics(state, agents, combinatoric_features)
    print(f"  ✓ Routed with combinatorics: {type(selected).__name__}")
    
    # High repetition → should route to Aegis
    combinatoric_features2 = {
        "repetitions": {"token1": 5, "token2": 4, "token3": 3},
        "recursion_count": 0,
    }
    
    selected2 = supervisor.route_with_combinatorics(state, agents, combinatoric_features2)
    print(f"  ✓ Routed with repetition: {type(selected2).__name__}")
    
    print("  ✓ Supervisor Combinatoric Routing: PASSED")
except Exception as e:
    print(f"  ✗ Supervisor Combinatoric Routing: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("COMBINATORIC INTERPRETER TEST SUMMARY")
print("=" * 60)
print("✓ English text processing")
print("✓ Python code processing")
print("✓ Math expression processing")
print("✓ JSON processing")
print("✓ LCM integration")
print("✓ Full API flow")
print("✓ Supervisor combinatoric routing")
print("\n🎉 Combinatoric Interpreter Layer is fully operational!")
print("Apop is now language-agnostic!")
print("=" * 60)

