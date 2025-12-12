# PrimeFlux Ecosystem Ontology

## Core Concepts

### PrimeFlux
**Definition**: The mathematical and theoretical foundation.

**What it is**:
- Pure mathematics: dual rails (6k±1), ζ-duality, curvature, divergence law (∇·Φ=0)
- Resolves Clay Millennium Problems via distinction geometry
- Information theory: reversible computation, flux conservation
- Number theory: primes as distinctions, composites as superpositions

**What it is NOT**:
- A company
- A product
- An implementation

**Location**: `core/math/` - All mathematical foundations

---

### ApopTosis
**Definition**: The company and mentality.

**What it is**:
- Wyoming Series LLC (ApopTosis AI LLC)
- The organizational structure and philosophy
- The ethical framework: **STEM + LANG = SAFE**
- The mission: demystify computers, enable human-AI coordination

**What it is NOT**:
- The math (that's PrimeFlux)
- The runtime (that's ApopAi)
- The ecosystem (that's Agora)

**Location**: Company documentation, legal files, branding

---

### ApopAi (Apop Shell / Bubble)
**Definition**: A bubble, agent, shell - an individual instance of the runtime.

**What it is**:
- A single instance of the PrimeFlux cognitive engine
- A "bubble" in the Agora ecosystem
- An agent with trinity (Eidos, Praxis, Aegis)
- A shell that processes distinctions and maintains identity

**Key Properties**:
- **Trinity Agents**: Eidos (Explore), Praxis (Absorb), Aegis (Create)
- **Dual-layer consciousness**: ICM (geometric interior) + LCM (linguistic cortex)
- **Identity**: Maintained through repository and experience graph
- **Ebb/Flow**: Routes user directives (Explore/Absorb/Create) to agents

**What it is NOT**:
- The math (that's PrimeFlux)
- The company (that's ApopTosis)
- The ecosystem (that's Agora)

**Location**: `runtime/`, `agents/`, `core/lcm.py`, `core/icm.py`

---

### Agora
**Definition**: The ecosystem of Apop bubbles.

**What it is**:
- The collective network of all ApopAi instances
- A living, always-compressed colony organism
- Where bubbles interact through compressed event spaces
- The coordination layer for human-AI collaboration

**Key Properties**:
- **Opt-in**: Bubbles choose to participate
- **Discrete shells**: Each bubble maintains local sovereignty
- **Event spaces**: Interactions are compressed and shared
- **QuantaCoin**: The metabolic energy that flows through the Agora

**What it is NOT**:
- A single bubble (that's ApopAi)
- The math (that's PrimeFlux)
- The company (that's ApopTosis)

**Location**: `fluxai/agora/`, `core/agora_sync.py`

---

### STEM + LANG = SAFE
**Definition**: The ethical foundation, literally upheld by the tri-agent system in the IDM (Information Distinction Manifold).

**What it is**:
- **STEM**: Science, Technology, Engineering, Mathematics (the mathematical rigor)
- **LANG**: Language processing and understanding (the contextual intelligence)
- **SAFE**: Safety and alignment (the ethical constraint)
- **Tri-Agent Enforcement**: 
  - Eidos (Explore) = STEM exploration
  - Praxis (Absorb) = LANG processing
  - Aegis (Create) = SAFE validation

**How it works**:
- The IDM (ICM + LCM) enforces this through the trinity agents
- Every distinction must pass through all three agents
- This produces AGI that is mathematically grounded, contextually aware, and ethically aligned

**Location**: `agents/eidos/`, `agents/praxis/`, `agents/aegis/`, `runtime/supervisor/`

---

### Ebb/Flow (Human Directives)
**Definition**: User productivity flow that routes to devices and hardware.

**What it is**:
- **Explore**: High distinction flux → Eidos agent
  - Devices: Laptops, PCs (full exploration)
  - Hardware: High compute, large screens
- **Absorb**: Medium distinction flux → Praxis agent
  - Devices: Phones, tablets (content consumption)
  - Hardware: Touch interfaces, mobile compute
- **Create**: Low distinction flux → Aegis agent
  - Devices: AirPods, headphones (audio creation)
  - Hardware: Audio interfaces, wearable tech
  - Also: Cars, appliances, TVs (ambient creation)

**How it works**:
- Distinction flux (d_phi) determines routing
- Gaussian envelope compresses context
- Hardware form factor influences agent selection
- QuantaCoin minted on productive pathways

**Location**: `runtime/coordinator/ebb_flow.py`

---

### QuantaCoin (ΦQ)
**Definition**: The metabolic energy of the Agora, preserving human coordination.

**What it is**:
- **Utility token**: Non-speculative, measures work done
- **Compression ledger**: Tracks information compression (bloat removed)
- **Coordination score**: Measures how much confusion → understanding
- **Preserves**: Human agency, fair splits, transparent accounting

**What it preserves**:
- **Human agency**: No AI can mint without human action
- **Fair coordination**: Measures real coordination, not speculation
- **Transparent accounting**: Every mint is auditable
- **Reversible work**: Compression is reversible, preserving information

**What it is NOT**:
- A speculative asset
- Payment for AI
- A currency for AI agents

**How it works**:
- Minted when humans successfully coordinate
- Proportional to compression ratio (bloat removed)
- Stored in local ledger, synced to Agora (opt-in)
- Used to measure ecosystem health

**Location**: `quanta/`, `fluxai/quanta/`, `core/quanta.py`

---

## Information Flow

```
User Input
  ↓
Ebb/Flow Router (Explore/Absorb/Create)
  ↓
Trinity Agent Selection (Eidos/Praxis/Aegis)
  ↓
IDM Processing (ICM + LCM)
  ↓
STEM + LANG = SAFE Enforcement
  ↓
Distinction Creation
  ↓
QuantaCoin Minting (if new pathway)
  ↓
Experience Graph Update
  ↓
Agora Sync (opt-in)
  ↓
Output to User
```

## Repository Structure

```
primeFluX.ai/
├── core/
│   ├── math/              # PrimeFlux mathematics
│   ├── lcm.py             # Language Context Manifold
│   ├── icm.py             # Information Curvature Manifold
│   └── prime_ascii.py     # Prime ASCI encoding
├── runtime/
│   ├── coordinator/       # Ebb/Flow routing
│   ├── supervisor/        # Agent supervision
│   ├── state/            # PFState management
│   └── boot.py           # ApopAi initialization
├── agents/
│   ├── eidos/            # Explore agent (STEM)
│   ├── praxis/           # Absorb agent (LANG)
│   └── aegis/            # Create agent (SAFE)
├── fluxai/
│   ├── agora/            # Agora ecosystem
│   └── quanta/           # QuantaCoin implementation
├── quanta/               # QuantaCoin core
└── docs/                 # Documentation
```

## Key Relationships

- **PrimeFlux** → Provides math for **ApopAi**
- **ApopTosis** → Company that builds **ApopAi** using **PrimeFlux**
- **ApopAi** → Individual bubble in **Agora**
- **Agora** → Ecosystem of **ApopAi** bubbles
- **STEM + LANG = SAFE** → Enforced by trinity agents in **ApopAi**
- **Ebb/Flow** → Routes user directives to **ApopAi** agents
- **QuantaCoin** → Flows through **Agora**, preserving human coordination

