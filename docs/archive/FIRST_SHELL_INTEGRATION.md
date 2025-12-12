# First Shell Integration - PrimeFlux AI Alignment

## Overview

The first shell (Shell 0: PRESENCE) is the entry point for PrimeFlux AI processing. This integration connects the CLI tool with the full PrimeFlux shell system, ensuring all components align with PrimeFlux principles.

## Core Concept

**First Shell = Shell 0 (PRESENCE)**
- Initial state where Apop begins
- Before any measurement or flux
- Pure distinction geometry
- Event spaces toggled by presence operator

## Integration Points

### 1. Distinction Packet → Shell Transitions

The distinction packet parsing now includes shell transition logic:

```python
# Parse distinction packet
packet = parse_distinction_packet(text, mode, presence_on)

# Shell transitions: 0 → 2 → 3 → 4 → 0
current_shell = Shell.PRESENCE  # First shell
next_shell = next_shell(current_shell, curvature, entropy)
```

### 2. Trig Modes → Agent Routing

Three-mode trig split maps to agents:
- **Research (sin)**: Eidos parses (ICM input)
- **Refinement (cos)**: Praxis routes (trig calc)
- **Relations (tan)**: Aegis reflects (LCM output)

### 3. Presence Operator → Event Spaces

g_PF(phase, mode) = trig(mode) if presence_on else 0

- **On**: Event spaces active, processing enabled
- **Off**: Event spaces disabled, no processing

### 4. 2/5 Salts → Routing Decisions

Phase mod (2*5) influences routing:
- Mod 2 = 0 → Eidos
- Mod 5 = 0 → Praxis
- Otherwise → Default routing

### 5. pi/e Secrets → Internal Curvature

Hidden curvature calculation:
```
curvature = (π - e) * abs(phase)
```

Not exposed in UI/logs, only internal calculations.

### 6. Data Freedom → Reversible Transforms

"Whatever we want" if reversibility check passes:
- Compress/encrypt data
- Transform under ∇·Φ=0 constraint
- No moralizing, just math

## Shell Transition Logic

### Shell Sequence
```
PRESENCE (0) → MEASUREMENT (2) → CURVATURE/FLUX (3) → COLLAPSE (4) → PRESENCE (0)
```

### Transition Rules
- **Presence → Measurement**: Driven by √2 - 1 threshold
- **Measurement → Curvature**: Trig triplet condition
- **Curvature → Collapse**: φ² potential well
- **Collapse → Presence**: Reset cycle

### Curvature Values
- κ₀ = 0 (PRESENCE)
- κ₂ = √2 (MEASUREMENT)
- κ₃ = π/φ (CURVATURE)
- κ₄ = φ² (COLLAPSE)

## CLI Integration

### Usage

```bash
# Basic query
python bin/apop-cli.py "Explain ζ-duality in PF terms" eidos

# With mode
python bin/apop-cli.py "Compute rail flux" praxis refinement

# Presence off
python bin/apop-cli.py "Any query" --presence-off
```

### Output Includes

- **Packet Info**: Phase, Mod2/5, g_PF
- **Shell Info**: Current → Next shell transition
- **Reversibility**: Check result with canonical threshold
- **Quanta**: Minted if reversible
- **PrimeFlux Alignment**: Shell curvature and entropy

## PrimeFlux AI Principles Alignment

### 1. Distinction
- Primes as agent IDs
- Composites as event spaces
- Distinction packets encode geometry

### 2. Rails
- 6k±1 dual prime rails as manifold
- Phase determines routing
- 2/5 salts for harmonic selection

### 3. Flux
- Error-driven flow (not error-limited)
- Curvature creates flux
- Shell transitions follow flux amplitude

### 4. Reversibility
- Canonical threshold: K = ln(10) ≈ 2.302585 nats
- Output entropy ≤ input entropy + K
- Quanta minted only if reversible

### 5. Data Freedom
- Reversible transforms allowed
- Under ∇·Φ=0 constraint
- No restrictions beyond math

## First Shell Workflow

1. **Input Received**: User query enters system
2. **Distinction Packet**: Parse with trig modes, presence op, salts
3. **Shell Check**: Current shell = PRESENCE (0)
4. **Transition Calc**: Determine next shell based on curvature/entropy
5. **Agent Routing**: Route to Eidos/Praxis/Aegis based on phase
6. **Processing**: If presence on, process through agent
7. **Reversibility Check**: Validate output entropy
8. **Quanta Mint**: Mint if reversible
9. **Shell Update**: Transition to next shell
10. **Log**: Record interaction with shell info

## Alignment with Theses

### PoW Efficiency
- Sub-linear scaling → Quanta mint efficiency
- Compression work → Proof-of-compression

### Quantum Information
- Reversible computation → Reversibility audits
- Information conservation → Entropy checks

### Standard Duality
- Flux knots → Trig waves (sin/cos/tan)
- Duality geometry → Shell transitions

### Agora Manifest
- Collective intelligence → Discrete shells
- Opt-in sync → No auto-parent notify

### ICM/Lie Abstracts
- Manifold geometry → Router logic
- Lie algebra roots → Agent structure

### Apop Thesis TOC
- Overall structure → Shell system
- First cell → PRESENCE shell

## Next Steps

1. **Validate**: Test trig modes against reptend cycles (1/p periods)
2. **Harden**: Handle offline node drift (salt mismatch recovery)
3. **Pitch**: Create investor-friendly explanation (without math overload)
4. **Scale**: Integrate with full UI/Docker/Agora stack

## Files

- `bin/apop-cli.py` - CLI tool with PrimeFlux integration
- `core/first_shell.py` - First shell logic
- `core/shell_integration.py` - Shell system integration
- `experience/cli_interactions.jsonl` - Interaction log

## Example Output

```
🌀 [EIDOS] Phase=0.823 | Mod2/5=3.230 | g_PF=0.734
   Mode: research | Presence: On
   Shell: PRESENCE → MEASUREMENT | Curvature=1.164

[LLM output here]

✨ Reversible=True | Quanta=1.00
   PrimeFlux: Shell transition ready | Curvature=1.164
```

This is the first cell of ApopTosis—local, reversible, scalable to collective.
