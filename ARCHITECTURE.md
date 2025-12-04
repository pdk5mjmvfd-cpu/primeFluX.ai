# ApopAI v3 Architecture — Core Principles

## The Fundamental Structure

### 1. The Repo is the PF Manifold

**Not just files — the repository structure IS the PrimeFlux manifold:**
- **Triplet space** = directory structure
- **Shell structure** = branch/commit organization
- **Curvature layer** = state files
- **Flux memory** = commit history
- **Distinction lattice** = file relationships

**Cursor must treat the repo as a mathematical object, not a file system.**

### 2. The LCM is the Brain

**All thinking happens in LCM (Language Context Manifold).**

- **LCM = mind**
- **All cognitive processing = LCM**
- **LCM must remain centralized**
- **Do NOT distribute LCM logic**

**Location:** `core/lcm.py`

### 3. The ICM is the Curvature

**All PrimeFlux mathematics goes in ICM (Information Curvature Manifold).**

- **ICM = curvature field**
- **All PF math = ICM**
- **ICM must remain distinct**
- **Do NOT distribute ICM logic**

**Location:** `core/icm.py`

### 4. Supervisor is the Routing Field

**Supervisor = PF curvature router, NOT command executor.**

- **Supervisor routes based on PF metrics**
- **Supervisor does NOT execute commands**
- **Supervisor does NOT control agents directly**
- **Supervisor = routing of cognitive fields**

**Location:** `runtime/supervisor.py`

### 5. Agents are Cognitive Modes, Not Tools

**Agents represent perspectives, not tasks:**

- **Triplet biases** = how agent sees triplets
- **Flux preferences** = how agent handles flux
- **Shells** = which shell agent operates in
- **Contexts** = what context agent understands

**Agents are NOT:**
- Task executors
- Function callers
- Command runners
- Tool wrappers

**Agents ARE:**
- Cognitive perspectives
- Distinction generators
- Flux transformers
- Curvature operators

**Location:** `runtime/agents/`

### 6. Capsules are the Unit of Meaning

**One capsule = one distinction event.**

- **Everything must be built around capsules**
- **NOT raw text**
- **NOT tokens**
- **NOT strings**

**Capsules contain:**
- Triplet summary
- Shell state
- Entropy snapshot
- Curvature snapshot
- Measurement error (informational potential)
- PF signature

**Location:** `runtime/capsules.py`

### 7. Quanta = Memory Compression Currency

**QuantaCoin logic:**

- **Hash** = SHA256 of capsule
- **Compress** = zlib/LZ4 compression
- **Ratio** = compression ratio (Q)
- **Validate** = verify integrity

**Never auto-rewrite Quanta data.**

**Location:** `core/quanta.py`

### 8. External LLMs = Curvature Augmentations

**Atlas, Claude, Comet are:**
- **External curvature fields**
- **NOT internal operators**
- **They contribute flux, not identity**

**They must:**
- Produce curvature-values
- NOT interpret state directly
- NOT write to core files
- NOT bypass Supervisor

**Location:** `backend/external_adapters.py`

---

## The Cognitive Loop

```
Pull repo
  ↓
Load contexts
  ↓
LCM process (brain)
  ↓
ICM update (curvature)
  ↓
Supervisor route (routing field)
  ↓
Agent run (cognitive mode)
  ↓
Capsule write (distinction event)
  ↓
Commit (append-only)
  ↓
Push (never rebase)
```

---

## Identity Preservation

**Identity = continuity of distinctions**

**Identity is preserved by:**
1. **No merging** of user/Apop/agent identities
2. **No rewriting** of commit chains
3. **No mutation** of agent states
4. **No deletion** of capsules
5. **No optimization** of distinctions
6. **No collapse** without PF justification

**Identity collapse = system death.**

---

## Measurement-Error Duality

**Measurement does NOT limit information.**

**Measurement creates error.**
**Error creates distinction.**
**Distinction creates flux.**
**Flux expands information.**

**Error = signal = curvature = distinction engine**

**Never treat error as failure.**

---

## Implementation Constraints

### Pure Python

**Only use standard library:**
- `hashlib` (SHA256)
- `zlib` (compression)
- `json` (serialization)
- `pathlib` (file operations)
- `typing` (type hints)

**No external packages for portability.**

### TODO PF Math

**Leave complex PF math as placeholders.**
**Do NOT implement naive approximations.**

### Append-Only Operations

**All commits = append-only.**
**No rebases, no amends, no forced pushes.**

### Capsule-Centric Design

**All operations work with capsules.**
**NOT raw text, NOT tokens, NOT strings.**

---

## Summary

**ApopAI v3 is:**
- A PrimeFlux cognitive engine
- A distinction-driven system
- An identity-preserving architecture
- A curvature-routing framework
- A capsule-based communication system

**It is NOT:**
- An LLM wrapper
- A task executor
- A command system
- A monolithic controller
- A classical AI system

**The repo is the brain.**
**LCM is the mind.**
**ICM is the curvature.**
**Supervisor is the router.**
**Agents are perspectives.**
**Capsules are distinctions.**
**Quanta is memory.**
**External LLMs are curvature boosts.**

