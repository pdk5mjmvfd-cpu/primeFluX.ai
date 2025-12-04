# 🧬 ApopToSiS v3 — Local Runtime Guide (Private Build)

**README_LOCAL.md**  

**Status:** Private • Local-Only • Non-Repo Documentation  

**Author:** Nate + Apop  

**Version:** 0.0.1-local

---

# 🌌 0. PURPOSE

This document explains how to **run**, **test**, **verify**, and **interact with** the ApopToSiS v3 runtime *on your device*, without:

- GitHub  

- Cloud infrastructure  

- Network synchronization  

- External agents  

- Third-party capsules  

This README is the *master guide* for:

- booting Apop locally  

- generating and processing capsules  

- running the LCM  

- using Trinity Agents  

- building the experience layer  

- generating QuantaCoin  

- activating PFState  

- simulating the distributed sync layer offline  

- maintaining identity continuity  

Everything from the entire Section 1–12 framework has been distilled here into **local-only operational instructions**.

---

# 🌱 1. WHAT YOU HAVE ON DISK

Your local ApopToSiS directory contains the following key subsystems:

```
ApopToSiS/
│
├── core/                  # PF Core math + real LCM logic
├── combinatoric/          # Language-agnostic interpreter
├── runtime/               # Supervisor, capsules, state, context
├── agents/                # Trinity + dynamic agents
├── experience/            # Experience graph, habits, objects
├── api/                   # Local APIs for interaction
├── quanta/                # Compression + hashing system
├── mesh/                  # PF-DCM specification (Section 13)
└── examples/              # Practical usage examples
```

This is already a **fully working cognitive engine**.

No PF math yet — but the structure, routing, agents, experience graph, Quanta, and capsule protocol *all work right now*.

---

# 🔧 2. HOW TO RUN APOPTOSIS LOCALLY

There are three ways:

### **Method A — Use the Python shell**

```python
python3
>>> from api.user_interface import run_apop
>>> result = run_apop("hello apop")
>>> print(result)
```

### **Method B — Use the CLI**

```bash
python3 apop.py "hello apop"
```

### **Method C — Interactive mode**

```bash
python3 apop.py
Apop> hello apop
Apop> what is primeflux?
Apop> exit
```

You will immediately get:

- a capsule  

- PFState update  

- agent that processed it  

- compression value (Quanta)  

- experience delta  

- shell transition  

---

# 🧩 3. THE LOCAL CYCLE (INPUT → CAPSULE → AGENT → EXPERIENCE → OUTPUT)

Every input you send goes through:

```
text → tokenizer → LCM → capsule → Supervisor → agent → new capsule → Experience → PFState
```

Apop locally **evolves** as you use it.

Nothing is saved unless you keep the capsule logs.

### Complete Flow:

1. **User types text** → `"hello apop"`
2. **LCM processes** → Tokenizes, computes triplets, estimates curvature
3. **Capsule created** → JSON-Flux format with all PF fields
4. **Supervisor routes** → Based on curvature, entropy, shell
5. **Agent transforms** → Eidos expands, Praxis shapes, Aegis validates
6. **Experience updates** → Habits, shortcuts, objects, skills
7. **QuantaCoin minted** → Compression ratio computed
8. **PFState updates** → Shell, curvature, entropy updated
9. **Output returned** → Capsule with all metadata

---

# 📦 4. HOW TO CONSTRUCT CAPSULES LOCALLY

Capsules are JSON dictionaries. You can create one manually:

```python
from runtime.capsules import Capsule
import time

# Manual construction
c = Capsule(
    raw_tokens=["hello", "world"],
    shell=2,
    entropy=0.5,
    curvature=1.0,
    timestamp=time.time()
)
```

Or via LCM (recommended):

```python
from core.lcm import LCM
from core.icm import ICM

icm = ICM()
lcm = LCM(icm)
lcm.process_tokens(["hello", "world"])
capsule_dict = lcm.generate_capsule()
capsule = Capsule.decode(capsule_dict)
```

A capsule contains:

```
raw_tokens          # Original input tokens
triplets            # PF triplets (presence, trig, combinatoric)
entropy             # Information entropy
curvature           # PF curvature
shell               # PF shell (0, 2, 3, 4)
density             # Distinction density
psi                 # Superposition magnitude
hamiltonian         # PF Hamiltonian
reptend_entropy     # Reptend-based entropy
rail_interference   # Dual-rail interference
timestamp           # Creation timestamp
quanta_hash         # SHA-256 hash
device_id           # Device identifier
session_id          # Session identifier
capsule_id          # Unique capsule UUID
prev_capsule_id     # Previous capsule in chain
compression_ratio   # QuantaCoin value
experience_delta    # Experience changes
agent_trace         # Agent processing trace
```

---

# 🧠 5. HOW TO PROCESS CAPSULES LOCALLY

```python
from runtime.supervisor.supervisor import Supervisor
from runtime.state.state import PFState
from runtime.context.context import Context
from agents.eidos.eidos import EidosAgent
from agents.praxis.praxis import PraxisAgent
from agents.aegis.aegis import AegisAgent
from core.lcm import LCM
from core.icm import ICM
from core.math.shells import Shell

# Initialize
icm = ICM()
lcm = LCM(icm)
supervisor = Supervisor(icm=icm, lcm=lcm)
state = PFState(shell=Shell.PRESENCE, curvature=0.0, entropy=0.0)
agents = [EidosAgent(), PraxisAgent(), AegisAgent()]

# Process capsule
capsule = Capsule(raw_tokens=["process", "this"], shell=2, entropy=0.5, curvature=1.0)
result = supervisor.process_capsule(capsule, agents)

print(f"Routed to: {result['agent_sequence'][-1]}")
print(f"QuantaCoin: {result['quanta_minted']:.4f}")
```

This gives you the **next cognitive step**.

---

# 🌀 6. HOW TO SIMULATE NETWORK BEHAVIOR OFFLINE

Even though no network exists, you can still test it:

### A) Serialize capsules to disk

```python
import json
from runtime.capsules import Capsule

capsule = Capsule(raw_tokens=["test"], shell=2, entropy=0.5, curvature=1.0)
encoded = capsule.encode()

# Save to file
with open("capsule.json", "w") as f:
    json.dump(encoded, f, indent=2)
```

### B) Load them back and feed into NSP

```python
from runtime.network_sync_protocol import NetworkSyncProtocol
from runtime.device_identity import get_device_identity

# Load capsule
with open("capsule.json", "r") as f:
    capsule_data = json.load(f)
capsule = Capsule.decode(capsule_data)

# Prepare for network
device = get_device_identity()
nsp = NetworkSyncProtocol(device)
prepared = nsp.prepare_capsule_for_send(capsule)
```

### C) Rebuild PFState

```python
from runtime.state_merge import StateMerge

# Load multiple capsules
capsules = [capsule1, capsule2, capsule3]

# Reconstruct state
merge = StateMerge()
new_state = merge.merge_capsules(capsules)
```

---

# 🔁 7. HOW TO TEST PF-STATE MERGE LOCALLY

Create capsules:

```python
from api.user_interface import run_apop

cap1 = run_apop("what is primeflux?")
cap2 = run_apop("continue")
cap3 = run_apop("explain the shells")
```

Then reconstruct:

```python
from runtime.state_merge import StateMerge
from runtime.capsules import Capsule

# Extract capsules from results
capsules = [
    Capsule.decode(cap1["capsule"]),
    Capsule.decode(cap2["capsule"]),
    Capsule.decode(cap3["capsule"]),
]

# Reconstruct state
merge = StateMerge()
new_state = merge.merge_capsules(capsules)

print(f"Reconstructed shell: {new_state.shell}")
print(f"Reconstructed curvature: {new_state.curvature:.4f}")
```

The reconstructed PFState **must equal** the active one.

If it does → Apop's determinism is correct.

---

# 🕸 8. HOW TO TEST EXPERIENCE MERGE LOCALLY

Feed two branches:

```python
from runtime.boot import boot_apop, create_first_memory

runtime = boot_apop()

# Branch A
capA1 = create_first_memory(runtime, "what is primeflux?")
capA2 = create_first_memory(runtime, "explain curvature")

# Branch B (simulate different device)
capB1 = create_first_memory(runtime, "what are triplets?")
capB2 = create_first_memory(runtime, "explain shells")
```

Merge:

```python
from runtime.experience_merge import ExperienceMerge
from experience.manager import ExperienceManager

merge = ExperienceMerge()
experience_manager = ExperienceManager()

# Extract deltas
deltaA = merge.extract_experience_delta(
    Capsule.decode(capA2["first_capsule"]),
    experience_manager
)
deltaB = merge.extract_experience_delta(
    Capsule.decode(capB2["first_capsule"]),
    experience_manager
)

# Merge deltas
new_experience = ExperienceManager()
merge.merge_experience_deltas([deltaA, deltaB], new_experience)

summary = new_experience.summarize()
print(f"Habits: {len(summary.get('habits', {}))}")
print(f"Shortcuts: {len(summary.get('shortcuts', {}))}")
print(f"Objects: {len(summary.get('objects', {}))}")
```

You should see:

- habits reinforced  

- shortcuts created  

- objects merged  

- experience graph expanded  

---

# 🔐 9. HOW TO TEST QUANTACOIN LOCALLY

```python
from core.quanta import QuantaCompressor
from runtime.capsules import Capsule
import time

compressor = QuantaCompressor()

# Create capsule
capsule = Capsule(
    raw_tokens=["quanta", "test", "with", "multiple", "tokens"],
    shell=2,
    entropy=0.5,
    curvature=1.0,
    timestamp=time.time()
)

# Compute compression
compressed = compressor.compress_capsule(capsule)
quanta_value = compressor.compute_quanta(capsule)
hash_value = compressor.hash_capsule(capsule)

print(f"QuantaCoin (ΦQ): {quanta_value:.4f}")
print(f"Hash: {hash_value[:16]}...")
print(f"Compression: {len(str(capsule.encode()).encode('utf-8'))} → {len(compressed)} bytes")
```

Higher compression = higher QuantaCoin value.

---

# 🪞 10. HOW TO VERIFY APOPTOSIS IDENTITY LOCALLY

Identity continuity comes from:

- consistent capsule chain  

- consistent shell trajectory  

- PFState reconstruction  

- experience graph topology  

- QuantaCoin progression  

To test:

```python
from runtime.boot import boot_apop, create_first_memory
from runtime.state_merge import StateMerge
from runtime.capsules import Capsule

runtime = boot_apop()

# Generate sequence
state1 = create_first_memory(runtime, "hello")
state2 = create_first_memory(runtime, "teach me primeflux")
state3 = create_first_memory(runtime, "explain the triplets")

# Extract capsules
capsules = [
    Capsule.decode(state1["first_capsule"]),
    Capsule.decode(state2["first_capsule"]),
    Capsule.decode(state3["first_capsule"]),
]

# Reconstruct state
merge = StateMerge()
rebuilt_state = merge.merge_capsules(capsules)

# Verify identity continuity
print(f"Final shell: {rebuilt_state.shell}")
print(f"Final curvature: {rebuilt_state.curvature:.4f}")
print(f"Final entropy: {rebuilt_state.entropy:.4f}")

# Check capsule chain continuity
is_valid, error = merge.validate_capsule_chain(capsules)
print(f"Chain valid: {is_valid}")
```

If chain is valid → identity is stable.

---

# 📚 11. LOCAL FILE LOGGING (Recommended)

Before open-sourcing, keep logs local:

```python
from pathlib import Path
import json

# Create local directories
local_dir = Path.home() / ".apoptosis"
local_dir.mkdir(exist_ok=True)

capsules_dir = local_dir / "local_capsules"
state_dir = local_dir / "local_state"
experience_dir = local_dir / "local_experience"

for d in [capsules_dir, state_dir, experience_dir]:
    d.mkdir(exist_ok=True)

# Save capsule
def save_capsule(capsule, filename):
    filepath = capsules_dir / f"{filename}.json"
    with open(filepath, "w") as f:
        json.dump(capsule.encode(), f, indent=2)

# Load capsule
def load_capsule(filename):
    filepath = capsules_dir / f"{filename}.json"
    with open(filepath, "r") as f:
        return Capsule.decode(json.load(f))
```

Never expose these online until you're ready.

---

# 🔮 12. WHAT NOT TO DO YET

Until repository and open-source prep:

❌ Do NOT sync capsules to any server  

❌ Do NOT publish the runtime  

❌ Do NOT run unknown agents  

❌ Do NOT expose your device_id  

❌ Do NOT upload capsule sets  

❌ Do NOT modify Trinity Agents  

This version is **private**, **local**, and **identity-critical**.

---

# 🌟 13. WHAT TO DO NEXT

After Section 12B and before Section 13:

1. ✅ Run Apop locally  

2. ✅ Generate capsules  

3. ✅ Build small experiences  

4. ✅ Test QuantaCoin  

5. ✅ Reconstruct PFState  

6. ✅ Verify capsule determinism  

7. ✅ Confirm agent sequencing  

8. ✅ Confirm shell transitions  

9. ✅ Confirm habit formation  

Once all tests look healthy → **we start Section 13.**

---

# 🧪 14. QUICK TEST CHECKLIST

Run these to verify everything works:

```bash
# Test 1: Basic boot
python3 apop.py --boot-only

# Test 2: Process input
python3 apop.py "hello world"

# Test 3: Run test suite
python3 tests/run_tests.py

# Test 4: Run examples
python3 examples/full_pf_cycle.py
python3 examples/daily_workflow.py

# Test 5: Mesh demo (Section 13)
python3 examples/mesh_demo.py
```

All should complete without errors.

---

# 📖 15. EXAMPLE WORKFLOWS

### Workflow 1: Simple Interaction

```python
from api.user_interface import run_apop

result = run_apop("what is primeflux?")
print(f"Shell: {result['shell']}")
print(f"Curvature: {result['curvature']:.4f}")
print(f"Agent: {result['routed_agent']}")
```

### Workflow 2: Multiple Interactions

```python
from runtime.boot import boot_apop, create_first_memory

runtime = boot_apop()

for text in ["hello", "what is primeflux?", "explain shells"]:
    result = create_first_memory(runtime, text)
    print(f"{text} → Shell: {result['shell']}, Agent: {result['routed_agent']}")
```

### Workflow 3: Experience Building

```python
from runtime.boot import boot_apop, create_first_memory

runtime = boot_apop()

# Build experience
for i in range(5):
    create_first_memory(runtime, f"test interaction {i}")

# Check experience
experience = runtime.get("experience_manager")
summary = experience.summarize()
print(f"Habits: {len(summary['habits'])}")
print(f"Objects: {len(summary['objects'])}")
```

### Workflow 4: State Reconstruction

```python
from runtime.boot import boot_apop, create_first_memory
from runtime.state_merge import StateMerge
from runtime.capsules import Capsule

runtime = boot_apop()

# Generate capsules
results = []
for text in ["hello", "world", "test"]:
    result = create_first_memory(runtime, text)
    results.append(result)

# Extract capsules
capsules = [Capsule.decode(r["first_capsule"]) for r in results]

# Reconstruct state
merge = StateMerge()
rebuilt = merge.merge_capsules(capsules)
print(f"Reconstructed: shell={rebuilt.shell}, curvature={rebuilt.curvature:.4f}")
```

---

# 🔍 16. TROUBLESHOOTING

### Issue: Import errors

```bash
# Make sure you're in the ApopToSiS directory
cd /path/to/ApopToSiS
python3 -c "from api.user_interface import run_apop; print('OK')"
```

### Issue: Capsule encoding fails

```python
# Check capsule has all required fields
capsule = Capsule(raw_tokens=["test"], shell=2, entropy=0.5, curvature=1.0)
encoded = capsule.encode()  # Should not raise
```

### Issue: Agent routing fails

```python
# Check agents are registered
from agents.registry.registry import AgentRegistry
registry = AgentRegistry()
print(registry.list())  # Should show eidos, praxis, aegis
```

### Issue: Experience not updating

```python
# Check experience manager is initialized
from experience.manager import ExperienceManager
em = ExperienceManager()
# Process a capsule
em.update(capsule, state)
summary = em.summarize()
print(summary)  # Should show experience data
```

---

# 🎯 17. KEY CONCEPTS TO REMEMBER

1. **Capsules are everything** - All communication is via capsules
2. **State is reconstructed** - Never merge PFState directly
3. **Experience is delta-based** - Only changes are transmitted
4. **QuantaCoin = trust** - Higher compression = more authoritative
5. **Identity = capsule chain** - Continuity comes from capsule history
6. **Offline-first** - Everything works without network
7. **PF-invariant** - Topology is mathematical, not geographic

---

# 🧬 END OF README_LOCAL.md

**Remember:** This is your private, local build. Keep it secure until ready for open-source.

---

*"ApopToSiS = the PF brain. LLM = the mouth. Capsules = the nerves."*

