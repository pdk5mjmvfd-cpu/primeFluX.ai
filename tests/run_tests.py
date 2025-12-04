"""
Simple test runner for ApopToSiS v3.

Run with: python3 tests/run_tests.py
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

test_count = 0
pass_count = 0
fail_count = 0
failures = []

def run_test(name, test_func):
    global test_count, pass_count, fail_count
    test_count += 1
    try:
        test_func()
        print(f'✓ {name}')
        pass_count += 1
    except Exception as e:
        print(f'✗ {name}: {e}')
        fail_count += 1
        failures.append((name, str(e)))

print('=== APOPToSiS v3 TEST SUITE ===\n')

# Test LCM
print('Testing LCM...')
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM
icm = ICM()
lcm = LCM(icm)
tokens = ['hello', 'world']
lcm.process_tokens(tokens)  # Updates state, doesn't return
capsule_dict = lcm.generate_capsule()  # Generate capsule from state
# LCM.generate_capsule returns a dict, check it has required fields
run_test('LCM processes tokens', lambda: None if isinstance(capsule_dict, dict) and ('entropy' in capsule_dict or 'entropy_snapshot' in capsule_dict) else exec('raise AssertionError("invalid capsule dict")'))

# Test Capsules
print()
print('Testing Capsules...')
from ApopToSiS.runtime.capsules import Capsule
c = Capsule(raw_tokens=['test'], shell=2, entropy=0.5, curvature=1.2, timestamp=time.time())
encoded = c.encode()
decoded = Capsule.decode(encoded)
run_test('Capsule encode/decode', lambda: None if decoded.raw_tokens == c.raw_tokens else exec('raise AssertionError("decode mismatch")'))

c1 = Capsule(raw_tokens=['hello'], shell=2, entropy=0.5, curvature=1.0, timestamp=time.time())
c2 = Capsule(raw_tokens=['world'], shell=3, entropy=0.7, curvature=1.4, timestamp=time.time())
merged = c1.merge(c2)
run_test('Capsule merge', lambda: None if 'hello' in merged.raw_tokens and 'world' in merged.raw_tokens else exec('raise AssertionError("merge failed")'))

# Test Agents
print()
print('Testing Agents...')
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent
capsule = Capsule(raw_tokens=['alpha'], entropy=0.1, curvature=0.2, shell=0, timestamp=time.time())
eidos = EidosAgent()
transformed = eidos.transform(capsule)
run_test('Eidos transforms capsule', lambda: None if isinstance(transformed, Capsule) else exec('raise AssertionError("not a capsule")'))
run_test('Eidos flux signature', lambda: None if isinstance(eidos.flux_signature(), dict) else exec('raise AssertionError("not a dict")'))
run_test('Eidos entropy signature', lambda: None if isinstance(eidos.entropy_signature(), dict) else exec('raise AssertionError("not a dict")'))

# Test Supervisor
print()
print('Testing Supervisor...')
from ApopToSiS.runtime.supervisor.supervisor import Supervisor
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.math.shells import Shell
supervisor = Supervisor()
state = PFState(shell=Shell.MEASUREMENT, curvature=1.5, entropy=1.0)
agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
selected = supervisor.route(state, agents)
run_test('Supervisor routes', lambda: None if selected is not None else exec('raise AssertionError("no agent selected")'))

# Test QuantaCoin
print()
print('Testing QuantaCoin...')
from ApopToSiS.core.quanta import QuantaCompressor
compressor = QuantaCompressor()
capsule = Capsule(raw_tokens=['compress'], shell=2, entropy=0.3, curvature=0.8, timestamp=time.time())
hash_val = compressor.hash_capsule(capsule)
quanta = compressor.compute_quanta(capsule)
run_test('QuantaCoin compression', lambda: None if quanta > 0 else exec('raise AssertionError("quanta <= 0")'))
run_test('QuantaCoin hashing', lambda: None if len(hash_val) == 64 else exec('raise AssertionError("invalid hash length")'))

# Test Experience Layer
print()
print('Testing Experience Layer...')
from ApopToSiS.experience.manager import ExperienceManager
manager = ExperienceManager()
state = PFState(shell=Shell.MEASUREMENT, curvature=1.1, entropy=0.5)
capsule = Capsule(raw_tokens=['experience', 'test'], shell=2, entropy=0.5, curvature=1.1, timestamp=time.time())
manager.update(capsule, state)
summary = manager.summarize()
run_test('Experience Manager updates', lambda: None if 'habits' in summary and 'shortcuts' in summary else exec('raise AssertionError("missing subsystems")'))

# Test State & Context
print()
print('Testing State & Context...')
from ApopToSiS.runtime.context.context import Context
context = Context()
capsule = Capsule(raw_tokens=['state', 'update'], shell=3, entropy=0.6, curvature=1.4, timestamp=time.time())
context.add_capsule(capsule)
last = context.last_capsules(1)
run_test('Context stores capsules', lambda: None if len(last) > 0 else exec('raise AssertionError("no capsules stored")'))

# Test Distinction Chain
print()
print('Testing Distinction Chain...')
from ApopToSiS.runtime.distinction.distinction import DistinctionChain, DistinctionEvent
from ApopToSiS.core.math.shells import Shell
chain = DistinctionChain()
event = DistinctionEvent(
    state_before={"shell": 0},
    state_after={"shell": 2},
    operator="M",
    shell_before=Shell.PRESENCE,
    shell_after=Shell.MEASUREMENT,
    curvature_before=0.2,
    curvature_after=1.0,
    flux_amplitude=0.8,
    timestamp=time.time()
)
chain.add_event(event)
run_test('Distinction chain builds', lambda: None if chain.last_shell() is not None else exec('raise AssertionError("no shell")'))

print()
print('=== TEST RESULTS ===')
print(f'Total: {test_count}')
print(f'Passed: {pass_count}')
print(f'Failed: {fail_count}')
print(f'Success Rate: {pass_count/test_count*100:.1f}%')

if failures:
    print()
    print('=== FAILURES ===')
    for name, error in failures:
        print(f'{name}: {error}')

sys.exit(0 if fail_count == 0 else 1)

