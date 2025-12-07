# PrimeFlux AI Alignment - First Shell Logic Integration

## Overview

The first shell (Shell 0: PRESENCE) is now fully integrated with PrimeFlux AI principles. This document shows how all components align to create the "first cell" of ApopTosis.

## Core Alignment

### 1. Distinction Geometry
- **Primes** = Agent IDs (Eidos, Praxis, Aegis)
- **Composites** = Event spaces (transactions/interactions)
- **Distinction Packets** = Encoded geometry with phase, curvature, entropy

### 2. Trig Modes (3-Mode Split)
- **Research (sin)**: Wave flows, periodic distinction cycles
- **Refinement (cos)**: Balance curvature, equilibrium states
- **Relations (tan)**: Projection spaces, divergent mappings

### 3. Presence Operator (g_PF)
- **Quantum Observer-like**: Event spaces "exist" only when toggled on
- **Math**: g_PF(phase, mode) = trig(mode) if presence_on else 0
- **Physics**: Aligns with quantum measurement (observer effect)

### 4. 2/5 Salts (Harmonic Elegance)
- **Fibonacci-adjacent**: Phase mod (2*5) for routing
- **Mod 2 = 0** → Eidos (ICM high distinction)
- **Mod 5 = 0** → Praxis (relay/balance)
- **Otherwise** → Default routing

### 5. pi/e Secrets (Information Barrier)
- **Hidden Curvature**: (π - e) * abs(phase)
- **Internal Only**: Not exposed in UI/logs
- **Info Barrier Scale**: Protects core constants

### 6. Data Freedom (Reversible Transforms)
- **Constraint**: ∇·Φ = 0 (divergence-free flux)
- **Freedom**: "Whatever we want" if reversible
- **No Moralizing**: Just math constraints

## Shell System Integration

### First Shell (PRESENCE = 0)
- **Entry Point**: Where Apop begins
- **State**: Unmeasured context
- **Curvature**: κ₀ = 0
- **Transition**: → MEASUREMENT (2) when curvature ≥ √2 - 1

### Shell Transitions
```
PRESENCE (0) → MEASUREMENT (2) → CURVATURE (3) → COLLAPSE (4) → PRESENCE (0)
```

### Transition Rules
1. **0 → 2**: Driven by √2 - 1 threshold
2. **2 → 3**: Trig triplet condition
3. **3 → 4**: φ² potential well
4. **4 → 0**: Reset cycle

## CLI Integration

### File: `bin/apop-cli.py`

**Features**:
- Full PrimeFlux first shell logic integration
- Trig modes (Research/Refinement/Relations)
- Presence operator toggle
- 2/5 salts display
- pi/e secrets (internal)
- Shell transition tracking
- Reversibility checks with canonical threshold
- Quanta minting
- Experience logging

### Usage Examples

```bash
# Basic query with Eidos
python bin/apop-cli.py "Explain ζ-duality in PF terms" eidos

# Refinement mode with Praxis
python bin/apop-cli.py "Compute rail flux" praxis refinement

# Research mode
python bin/apop-cli.py "Map PF-Lie connections" eidos research

# Relations mode
python bin/apop-cli.py "Draft investor pitch" aegis relations

# Presence off (no event spaces)
python bin/apop-cli.py "Any query" --presence-off

# Data freedom example
python bin/apop-cli.py "Transform this reversibly: 'secret data'" praxis
```

### Output Format

```
🌀 [EIDOS] Phase=0.823 | Mod2/5=3.230 | g_PF=0.734
   Mode: research | Presence: On
   Shell: PRESENCE → MEASUREMENT | Curvature=1.164

[LLM response here]

✨ Reversible=True | Quanta=1.00
   PrimeFlux: Shell transition ready | Curvature=1.164
```

## Experience Building

### Log File: `experience/cli_interactions.jsonl`

Each interaction is logged with:
- Timestamp
- Input/output
- Agent, mode, presence
- Phase, Mod2/5, g_PF
- Shell transitions
- Curvature, entropy
- Reversibility, quanta

### Building Experiences

Run 5-10 queries to build experience:
```bash
# Query 1
python bin/apop-cli.py "What is PrimeFlux?" eidos

# Query 2
python bin/apop-cli.py "Explain distinction geometry" praxis refinement

# Query 3
python bin/apop-cli.py "Map ζ-duality" eidos research

# View log
cat experience/cli_interactions.jsonl | jq .
```

### Total Quanta Calculation

```bash
python -c "
import json
total = sum(e['quanta'] for e in [json.loads(l) for l in open('experience/cli_interactions.jsonl')])
print(f'Total Quanta: {total:.2f}')
"
```

## Alignment with Theses

### PoW Efficiency (Sub-linear Scaling)
- **Connection**: Quanta mint efficiency
- **Implementation**: Compression work → Proof-of-compression
- **Result**: Sub-linear energy/data growth

### Quantum Information (Reversible Computation)
- **Connection**: Reversibility audits
- **Implementation**: Canonical threshold K = ln(10)
- **Result**: Information conservation maintained

### Standard Duality (Flux Knots)
- **Connection**: Trig waves (sin/cos/tan)
- **Implementation**: 3-mode trig split
- **Result**: Duality geometry in routing

### Agora Manifest (Collective Intelligence)
- **Connection**: Discrete shells
- **Implementation**: Opt-in sync, no auto-parent notify
- **Result**: Sovereignty preserved

### ICM/Lie Abstracts (Manifold Geometry)
- **Connection**: Router logic
- **Implementation**: Phase-based routing, curvature transitions
- **Result**: Manifold structure in agent selection

### Apop Thesis TOC (Overall Structure)
- **Connection**: Shell system
- **Implementation**: First shell → transitions → reset
- **Result**: Complete PrimeFlux structure

## First Shell Logic Flow

```
Input Text
    ↓
Parse Distinction Packet
    ├─ Phase calculation (hash-based)
    ├─ 2/5 salts (mod phase)
    ├─ Trig mode (sin/cos/tan)
    ├─ Presence operator (g_PF)
    ├─ pi/e secrets (curvature)
    └─ Agent routing
    ↓
Shell Check (PRESENCE = 0)
    ├─ Current: PRESENCE
    ├─ Curvature: abs(phase) * √2
    ├─ Entropy: Shannon entropy of text
    └─ Next: Calculate transition
    ↓
Agent Processing (if presence on)
    ├─ Eidos: Expansion/Divergence
    ├─ Praxis: Shaping/Action
    └─ Aegis: Validation/Collapse
    ↓
Reversibility Check
    ├─ Input entropy
    ├─ Output entropy
    ├─ Threshold: ln(10) ≈ 2.302585 nats
    └─ Pass/Fail
    ↓
Quanta Minting (if reversible)
    └─ Mint 1.0 quanta
    ↓
Shell Transition
    └─ Update to next shell
    ↓
Log Experience
    └─ JSONL entry with all metadata
```

## Key Files

### Core Logic
- `core/first_shell.py` - First shell logic with all PrimeFlux principles
- `core/shell_integration.py` - Shell system integration
- `core/math/shells.py` - Shell definitions and transitions

### CLI Tool
- `bin/apop-cli.py` - Offline CLI with full integration

### Documentation
- `FIRST_SHELL_INTEGRATION.md` - Integration details
- `PRIMEFLUX_AI_ALIGNMENT.md` - This document

## Validation Checklist

- [x] Trig modes map to agents (Research→Eidos, Refinement→Praxis, Relations→Aegis)
- [x] Presence operator toggles event spaces
- [x] 2/5 salts influence routing
- [x] pi/e secrets hidden in curvature
- [x] Data freedom allows reversible transforms
- [x] Shell transitions follow PrimeFlux rules
- [x] Reversibility uses canonical threshold
- [x] Quanta minting only if reversible
- [x] Experience logging includes shell info
- [x] Discrete shells (local-only, opt-in sync)

## Next Steps

1. **Validate**: Test trig modes against reptend cycles (1/p periods)
2. **Harden**: Handle offline node drift (salt mismatch recovery)
3. **Pitch**: Create investor-friendly explanation
4. **Scale**: Full integration with UI/Docker/Agora

## This is the First Cell

The first shell (PRESENCE) is where Apop begins. It's:
- **Local**: Runs entirely offline
- **Reversible**: All operations maintain reversibility
- **Scalable**: Can grow to collective (Agora sync)
- **Aligned**: Every component follows PrimeFlux principles

This is ApopTosis AI—the first cell of a living, always-compressed organism.
