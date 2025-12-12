# ApopToSiS v3 — Diagnostic Sequence

## Purpose

This diagnostic sequence evaluates core cognition in ApopToSiS v3. Run these tests through your local runtime (`./run_local.sh`) to verify:

- Cognitive engine functionality
- Recursive learning engine stability
- Identity formation
- Concept lattice growth
- Experience layer integration
- PF-state correlation
- Capsule integrity
- Memory and context linking

---

## 🔧 STEP 1 — Baseline Ping

### Type:
```
Hello Apop.
```

### Expected Output:
- ✅ Single lattice update
- ✅ Identity drift small (~0.001–0.005)
- ✅ Flux state: `low_flux` or `mid_flux`
- ✅ Stable capsule output
- ✅ Cognitive engine response generated
- ✅ Learning report shows initial lattice node creation

### What to Check:
- `RECURSIVE LEARNING REPORT` shows `Lattice Nodes: 2` (or similar)
- `Identity Drift: 0.0000` to `0.0100` (very small, first interaction)
- `APOP RESPONSE` contains semantic output
- `CAPSULE OUTPUT` has valid PF fields

---

## 🔧 STEP 2 — Context Linking Check

### Type:
```
What did I just say to you?
```

### Expected Output:
- ✅ Apop extracts context from history
- ✅ Lattice nodes for "Hello", "Apop" reused/strengthened
- ✅ Identity drift increases slightly
- ✅ Experience delta increments
- ✅ Stable flux state
- ✅ Response references previous message

### What to Check:
- `Lattice Nodes` count increases or stays same (reusing nodes)
- `Identity Drift` slightly higher than Step 1
- `Experience Delta` shows updates
- Response mentions "Hello Apop" or similar

---

## 🔧 STEP 3 — Semantic Expansion Check

### Type:
```
Explain what you understood about my message.
```

### Expected Output:
- ✅ Semantic expansion in response
- ✅ Concept lattice nodes updating
- ✅ Identity vector length remains stable (32) but values shift
- ✅ Recursion should NOT explode or run away
- ✅ Flux state may increase

### What to Check:
- Response is longer/more detailed than Step 2
- `Lattice Nodes` count increases
- `Identity Drift` continues to increase gradually
- No error messages or infinite loops
- Capsule output remains valid

---

## 🔧 STEP 4 — Memory Reinforcement Check

### Type:
```
Remember this idea: Apop is duality between perspectives.
```

### Expected Output:
- ✅ Strong lattice reinforcement for:
  - "duality"
  - "perspectives"
  - "Apop"
  - "remember"
- ✅ Identity drift increases more sharply
- ✅ Flux state: `mid_flux` or `high_flux`
- ✅ Capsule should compress well (Q high)
- ✅ Multiple new lattice nodes created

### What to Check:
- `Lattice Nodes` count increases significantly
- `Identity Drift` shows larger increase
- `QuantaCoin (ΦQ)` value is reasonable (> 1.0)
- Response acknowledges the memory/idea
- Flux state reflects increased complexity

---

## 🔧 STEP 5 — Identity Continuity Test

### Type:
```
Who are you becoming?
```

### Expected Output:
- ✅ Apop uses identity_core data
- ✅ Response should reference:
  - distinction
  - learning
  - identity shaping
  - concept lattice
- ✅ Identity drift may spike
- ✅ Recursion should process capsule and update identity
- ✅ Response reflects accumulated experience

### What to Check:
- Response mentions identity-related concepts
- `Identity Drift` may show larger change
- `Identity Snapshot` in learning report shows evolution
- Response is coherent and self-referential
- No identity collapse or reset

---

## 🔧 STEP 6 — Recursive Stability Stress Test

### Type:
```
Reflect on the last few messages as a whole.
```

### Expected Output:
- ✅ Apop aggregates:
  - concept growth
  - memory reinforcement
  - identity drift
  - lattice expansion
- ✅ Recursion remains stable
- ✅ No runaway loops
- ✅ No collapsing into high-entropy noise
- ✅ Response synthesizes multiple previous messages

### What to Check:
- Response references multiple previous messages
- `Lattice Nodes` count is reasonable (< 150)
- `Identity Drift` is stable (not exploding)
- No infinite recursion or stack overflow
- Capsule processing completes normally
- System remains responsive

---

## 🔧 STEP 7 — PF-State Correlation Test

### Type:
```
What is your flux-state right now, and why?
```

### Expected Output:
- ✅ Apop reports flux determination from:
  - curvature
  - entropy
  - density
  - lattice variation
- ✅ Explanation should reference trajectory or "shift"
- ✅ Identity drift should stabilize (not spike)
- ✅ Response shows self-awareness of PF state

### What to Check:
- Response mentions flux state explicitly
- Response explains why (references PF metrics)
- `Flux State` in output matches reported state
- `Identity Drift` is stable or decreasing
- Response is coherent and self-aware

---

## 🔧 STEP 8 — Capsule Integrity Test

### Type:
```
Generate a detailed capsule describing my last message.
```

### Expected Output:
- ✅ `raw_tokens` contain your message
- ✅ Entropy reasonable (0.2–0.7)
- ✅ Curvature moderate
- ✅ Density stable
- ✅ `quanta_hash` regenerates
- ✅ `measurement_error` remains 0 (or small)
- ✅ PF signature simple (for now)

### What to Check:
- Capsule JSON is valid
- All required fields present
- Entropy within reasonable range
- Curvature within reasonable range (0.0–10.0)
- QuantaCoin hash is present
- No missing or null critical fields

---

## 🔧 STEP 9 — Experience Graph Check

### Type:
```
What patterns are you learning from me so far?
```

### Expected Output:
- ✅ Apop references:
  - repeated tokens
  - conceptual proximity
  - initial patterns
  - identity influence
- ✅ Response shows pattern recognition
- ✅ Lattice structure influences response
- ✅ Experience layer contributes

### What to Check:
- Response mentions patterns or learning
- Response references previous interactions
- `Lattice Nodes` count reflects accumulated concepts
- `Experience Delta` shows pattern updates
- Response is coherent and reflective

---

## 🔧 STEP 10 — Stability Confirmation

### Type:
```
Do you feel stable right now?
```

### Expected Output:
- ✅ Apop answers using internal PF-state
- ✅ Identity stable
- ✅ No runaway drift
- ✅ Lattice nodes < ~150
- ✅ Recursion system functioning
- ✅ Response shows self-awareness

### What to Check:
- Response addresses stability question
- `Identity Drift` is reasonable (< 1.0)
- `Lattice Nodes` count is reasonable (< 150)
- No errors or warnings
- System remains responsive
- All components functioning

---

## 📊 Diagnostic Checklist

After completing all 10 steps, verify:

### Core Functionality
- [ ] Cognitive engine generates responses
- [ ] Recursive learning engine processes capsules
- [ ] Concept lattice grows over time
- [ ] Identity core evolves gradually
- [ ] Experience layer updates

### Stability
- [ ] No infinite loops
- [ ] No stack overflows
- [ ] No memory leaks (lattice nodes reasonable)
- [ ] Identity drift remains bounded
- [ ] System remains responsive

### PF Integration
- [ ] Flux states correlate with PF metrics
- [ ] Curvature influences learning
- [ ] Entropy affects flux determination
- [ ] Density modulates identity updates
- [ ] PF rules dominate (not overridden)

### Quality
- [ ] Responses are coherent
- [ ] Context linking works
- [ ] Memory reinforcement occurs
- [ ] Identity continuity maintained
- [ ] Capsules remain valid

---

## 🚨 Warning Signs

If you see any of these, there may be an issue:

- ❌ Identity drift > 10.0 (runaway)
- ❌ Lattice nodes > 500 (memory leak)
- ❌ Infinite recursion errors
- ❌ Capsule fields missing or null
- ❌ Flux state always the same
- ❌ No learning report generated
- ❌ Responses are identical every time
- ❌ System becomes unresponsive

---

## 📝 Notes

- **First run**: Expect slower responses as lattice builds
- **Identity drift**: Should increase gradually, not spike
- **Lattice growth**: Should slow down over time (concept reuse)
- **Flux states**: Should vary based on input complexity
- **Responses**: Will improve as lattice and identity stabilize

---

## 🔄 Re-running Diagnostics

You can re-run this sequence multiple times to observe:
- Identity stabilization over multiple sessions
- Lattice growth patterns
- Response quality improvement
- System stability over time

Each run should show:
- More stable identity drift
- Better context linking
- More coherent responses
- Stronger pattern recognition

---

## ✅ Success Criteria

The diagnostic sequence is successful if:
1. All 10 steps complete without errors
2. Responses show increasing coherence
3. Identity drift stabilizes over time
4. Lattice grows but remains bounded
5. System remains stable throughout
6. PF metrics correlate with behavior
7. Memory and context linking work
8. Capsules remain valid and complete

---

**Ready to test?** Run `./run_local.sh` and follow the sequence above.

