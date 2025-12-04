# AI Collaboration Guide — FluxAI Runtime

**Purpose:** This guide helps AI assistants (Grok, ChatGPT, Auto) understand and work with the FluxAI codebase effectively.

**Last Updated:** 2024

---

## Quick Start for AI Assistants

### 1. Understanding the Codebase

**FluxAI (formerly ApopToSiS v3)** is a PrimeFlux cognitive engine that:
- Processes information through PrimeFlux mathematics
- Uses capsules (JSON-Flux format) as the unit of meaning
- Implements dual-layer consciousness (ICM + LCM)
- Operates offline-first with local LLM support (planned)

### 2. Key Architectural Principles

**DO:**
- ✅ Treat capsules as the fundamental unit (not tokens, not strings)
- ✅ Preserve PrimeFlux mathematical integrity
- ✅ Maintain offline-first operation
- ✅ Use reversible operators where possible
- ✅ Follow the boot sequence order

**DON'T:**
- ❌ Modify core PF math without understanding implications
- ❌ Break the capsule protocol
- ❌ Add network dependencies to core runtime
- ❌ Store raw JSON when integer compression is possible
- ❌ Change boot sequence order

### 3. Entry Points for Changes

#### **Adding New Features:**
1. **Memory System:** `fluxai/memory/` (NEW - to be created)
2. **Local LLM:** `fluxai/local/` (NEW - to be created)
3. **Agents:** `agents/` or `fluxai/trinity/` (NEW - to be created)
4. **Operators:** `core/flux.py` or `fluxai/operator_core/` (NEW)

#### **Modifying Existing Code:**
1. **LCM (Brain):** `core/lcm.py` — Be careful, this is central
2. **ICM (Curvature):** `core/icm.py` — PF math core
3. **Capsules:** `runtime/capsules.py` — Transport layer
4. **Supervisor:** `runtime/supervisor/supervisor.py` — Routing logic

### 4. Reading the Codebase

**Start Here:**
1. `README.md` — Overview
2. `ARCHITECTURE.md` — Core principles
3. `FLUXAI_REFINEMENT_ROADMAP.md` — Current state and plans
4. `SYSTEM_OVERVIEW.md` — System description

**Then Explore:**
- `core/lcm.py` — How thinking happens
- `runtime/capsules.py` — How information flows
- `agents/` — How agents work
- `experience/` — How learning happens

### 5. Making Changes

#### **Before Making Changes:**
1. Read `FLUXAI_REFINEMENT_ROADMAP.md` to understand the vision
2. Check `IMPLEMENTATION_STATUS.md` (if exists) for current work
3. Understand the PrimeFlux principles in `ARCHITECTURE.md`

#### **When Making Changes:**
1. **Preserve Capsule Protocol:** Don't break capsule encode/decode
2. **Maintain Offline-First:** Don't add network dependencies to core
3. **Follow PF Math:** Use existing PF operators, don't invent new math
4. **Test Thoroughly:** Run `python apop.py` to verify

#### **After Making Changes:**
1. Update relevant documentation
2. Add tests if adding new features
3. Update `IMPLEMENTATION_STATUS.md` if working on roadmap items

### 6. Common Patterns

#### **Creating a New Agent:**
```python
from ApopToSiS.agents.base.base_agent import PFBaseAgent
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState

class MyAgent(PFBaseAgent):
    def analyze(self, capsule: Capsule, state: PFState) -> dict[str, Any]:
        # Analyze capsule
        return {"metric": value}
    
    def transform(self, capsule: Capsule) -> Capsule:
        # Transform capsule
        return transformed_capsule
    
    def flux_signature(self) -> dict[str, Any]:
        # Return flux characteristics
        return {"amplitude": 1.0, "direction": "forward"}
    
    def entropy_signature(self) -> dict[str, Any]:
        # Return entropy profile
        return {"base_entropy": 0.5, "tendency": "increase"}
```

#### **Working with Capsules:**
```python
from ApopToSiS.runtime.capsules import Capsule

# Create capsule
capsule = Capsule(raw_tokens=["hello", "world"], entropy=1.0)

# Encode to JSON
capsule_dict = capsule.encode()

# Decode from JSON
capsule = Capsule.decode(capsule_dict)

# Merge capsules
merged = capsule1.merge(capsule2)
```

#### **Using LCM:**
```python
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM

icm = ICM()
lcm = LCM(icm=icm)

# Process tokens
tokens = ["hello", "world"]
lcm.process_tokens(tokens)

# Generate capsule
capsule_dict = lcm.generate_capsule(tokens=tokens, user_text="hello world")
```

### 7. Testing Your Changes

**Quick Test:**
```bash
python apop.py "test input"
```

**Run Tests:**
```bash
python tests/run_tests.py
```

**Check for Errors:**
```bash
python -m pytest tests/ -v
```

### 8. Understanding PrimeFlux Concepts

**Key Terms:**
- **ICM:** Information Curvature Manifold (geometric interior)
- **LCM:** Language Context Manifold (linguistic cortex)
- **Capsule:** Unit of meaning (JSON-Flux format)
- **Triplet:** PrimeFlux geometric structure (presence, trig, combinatoric)
- **Shell:** PF state level (0, 2, 3, 4)
- **Curvature (κ):** Information geometry measure
- **Entropy (H):** Information measure
- **Flux:** Derivative of distinction
- **QuantaCoin:** Memory compression currency

**Shell Pipeline:**
```
0 (Presence) → 2 (Measurement) → 3 (Flux) → 4 (Collapse) → reset
```

### 9. Working on Refinement Directions

If working on items from `FLUXAI_REFINEMENT_ROADMAP.md`:

**Direction 1 (FluxAI.Local):**
- Create `fluxai/local/` module
- Integrate ONNX/llama.cpp
- Make LLM optional

**Direction 2 (FluxAI.Memory):**
- Create `fluxai/memory/` module
- Implement `MemoryPacket` with integer encoding
- Replace JSON storage

**Direction 3 (FluxAI.OperatorCore):**
- Create `fluxai/operator_core/` module
- Implement reversible transforms
- Domain ↔ range duality

**Direction 4 (FluxAI.Trinity):**
- Create `fluxai/trinity/` module
- Implement STEM/LANG/SAFE agents
- Domain-based routing

**Direction 5 (FluxAI Runtime):**
- Integrate all components
- Create unified runtime

**Direction 6 (FluxAI.Evolution):**
- Create `fluxai/evolution/` module
- Compression-based learning

**Direction 7 (FluxAI.LedgerSync):**
- Create `fluxai/ledger_sync/` module
- Grok/X integration

### 10. Asking Questions

If you're an AI assistant and need clarification:

1. **Check Documentation First:**
   - `FLUXAI_REFINEMENT_ROADMAP.md` — Current plans
   - `ARCHITECTURE.md` — Core principles
   - `SYSTEM_OVERVIEW.md` — System description

2. **Look for Examples:**
   - `examples/` directory
   - `tests/` directory

3. **Understand the Pattern:**
   - Read similar code in the codebase
   - Follow existing patterns

4. **When in Doubt:**
   - Preserve existing behavior
   - Make minimal changes
   - Document your assumptions

### 11. Code Style

**Python Style:**
- Use type hints
- Follow PEP 8
- Use dataclasses for data structures
- Document with docstrings

**PrimeFlux Style:**
- Use PF terminology correctly
- Preserve mathematical integrity
- Maintain capsule protocol
- Follow boot sequence

### 12. Common Pitfalls

**Avoid These:**
1. ❌ Breaking capsule encode/decode
2. ❌ Adding network dependencies to core
3. ❌ Modifying PF math without understanding
4. ❌ Changing boot sequence order
5. ❌ Storing raw JSON when compression is possible
6. ❌ Creating agents that don't follow PFBaseAgent pattern
7. ❌ Modifying LCM/ICM without careful consideration

**Do These Instead:**
1. ✅ Test capsule encode/decode after changes
2. ✅ Keep network code in `api/` or `fluxai/ledger_sync/`
3. ✅ Use existing PF operators
4. ✅ Preserve boot sequence
5. ✅ Use integer compression for memory
6. ✅ Follow PFBaseAgent pattern
7. ✅ Extend LCM/ICM rather than modify core logic

---

## Summary

**For AI Assistants Working on This Codebase:**

1. **Read First:** `FLUXAI_REFINEMENT_ROADMAP.md` and `ARCHITECTURE.md`
2. **Understand:** Capsules, LCM, ICM, PrimeFlux principles
3. **Follow:** Existing patterns, boot sequence, capsule protocol
4. **Test:** Always test with `python apop.py`
5. **Document:** Update docs when making significant changes

**The codebase is well-structured and documented. Follow the patterns, preserve the principles, and you'll be able to contribute effectively.**

---

**Questions?** Check the documentation files or look for examples in `examples/` and `tests/`.

