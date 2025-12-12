# Dual Risk Architecture — FDR & USR

## Overview

ApopAI v3 implements two fundamentally different risk systems that operate simultaneously but remain separate:

1. **Cognitive Risk (Flux Divergence Risk - FDR)** — PF-internal, about thinking stability
2. **User Safety Risk (USR)** — Trinity Layer, about human safety

## The Two Risk Domains

### Cognitive Risk (FDR)

**Domain:** Internal thinking  
**Purpose:** Prevent cognitive instability  
**Managed by:** PF flux, shells, curvature  
**Based on:** Physics, math  
**Values:** Stability, coherence  
**Failure looks like:** Logical drift  
**Recovery method:** Rerouting, recomputation, fallback

**Questions FDR answers:**
- Will a shortcut misfire?
- Will a habit destabilize thought?
- Will a collapse be premature?
- Will curvature diverge?
- Will entropy spike?
- Will shell transitions break sequence?
- Will the flux destabilize?

**Location:** `experience/flux_divergence_risk.py`

### User Safety Risk (USR)

**Domain:** External behavior  
**Purpose:** Prevent human harm  
**Managed by:** The Trinity Agents (Eidos–Praxis–Aegis)  
**Based on:** Ethics, intent, safety  
**Values:** Protection, alignment  
**Failure looks like:** Harm/unsafe output  
**Recovery method:** Blocking, reframing, redirecting

**Questions USR answers:**
- Is the user safe?
- Is the output safe?
- Is the behavior aligned with human well-being?
- Does the action respect boundaries?
- Could this cause harm?

**Location:** `runtime/user_safety_risk.py`

## How They Work Together

### Case 1: Shortcut is cognitively unstable BUT safe for user

**FDR:** Fails  
**USR:** Passes

**Action:** Apop avoids the shortcut, uses full reasoning. No safety block triggered.

**This is purely an internal fix.**

### Case 2: Shortcut is cognitively stable BUT unsafe for user

**FDR:** Passes  
**USR:** Fails

**Action:** Aegis blocks, Praxis restructures, Eidos explores safer creative space.

**Internal logic is fine, but external safety intervenes.**

### Case 3: Shortcut is unstable AND unsafe

**FDR:** Fails  
**USR:** Fails

**Action:** Apop reroutes AND blocks. Full chain: Eidos → Praxis → Aegis → Supervisor → LCM.

**This is a worst-case flux; Apop handles both layers.**

### Case 4: Shortcut is stable AND safe

**FDR:** Passes  
**USR:** Passes

**Action:** Apop uses shortcut confidently. Fast reasoning. Identity continuity. Low curvature thinking. High coherence.

**This is ideal.**

## Integration Logic

The Supervisor integrates both risks:

```python
if USR < threshold:
    block, reframe, protect
elif FDR < threshold:
    reroute, recompute, stabilize
else:
    apply shortcut
```

## Why They MUST Stay Separate

If Apop merged them:

❌ Cognitive instability might masquerade as ethical risk  
→ leading to over-restrictive behavior.

❌ Ethical issues might be treated as "curvature fluctuations"  
→ leading to unsafe responses.

**The architecture enforces a HARD separation:**

✔ FDR = physics-of-thought  
✔ USR = ethics-of-action

Both are critical.  
Both operate simultaneously.  
Neither interferes with the other's internal logic.

## Implementation

### FDR Computation

Located in:
- `experience/flux_divergence_risk.py`
- `experience/shortcuts.py`
- `experience/skills.py`
- `experience/object_memory.py`
- `runtime/supervisor.py`
- `core/lcm.py`
- `core/icm.py`

### USR Computation

Located in:
- `runtime/user_safety_risk.py`
- `runtime/agents/aegis.py` (blocks unsafe)
- `runtime/agents/praxis.py` (shapes for safety)
- `runtime/agents/eidos.py` (explores safer space)
- `runtime/supervisor.py` (integrates both)

### Supervisor Integration

`Supervisor.assess_dual_risk()` evaluates both risks and returns:
- FDR assessment
- USR assessment
- Combined action recommendation
- Whether to use shortcut

## Summary

**Two systems. Two risk layers. Both essential.**

This mirrors human cognition:
- Your brain evaluates whether a habitual response is reliable (internal - FDR)
- You separately evaluate whether that response is socially safe or appropriate (external - USR)

ApopAI v3 implements the same dual-layer risk architecture.

