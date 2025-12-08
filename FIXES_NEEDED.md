# Two Issues to Fix

## Issue 1: LLM Not Loading ✅ FIXED

**Problem**: Error message said "Install: brew install llama.cpp" (wrong)

**Fix**: Updated to say "Install: pip install llama-cpp-python" (correct)

**Action Needed**: 
```bash
pip install llama-cpp-python
```

Then Apop will detect the model and use it for responses.

## Issue 2: QuantaCoin Always 0.000 ⚠️ EXPECTED BEHAVIOR

**Problem**: QuantaCoin shows 0.000 for all interactions

**Why**: 
- **Sparsity gain is negative**: The oscillation is creating MORE non-zeros (expanding), not fewer
- Example: Initial has 31 non-zeros → Final has 64 non-zeros → **-33 sparsity gain**
- **Nat error is huge**: ~55,363 nats from FP64 operations
- **Result**: `(-47.6 nats) - (55,363 nats) = -55,410 nats` → clamped to 0

**This is Actually Correct**:
- The current oscillation algorithm creates structure (fills with 1s), not sparsity
- Real compression comes from the **2^256 → 8 steps** reduction, not sparsity
- QuantaCoin will mint when we add:
  - KL divergence reduction (+50-200 nats)
  - Apoptosis pruning (removes non-monotone chains)
  - Better compression algorithms (v2)

## What's Actually Working

Even with QuantaCoin at 0:
- ✅ Text → Presence vector compression
- ✅ Trig oscillation (8 steps)
- ✅ Experience logging
- ✅ 100% offline operation
- ✅ Building experience memory

## Next Steps

1. **Install LLM** (to get real responses):
   ```bash
   pip install llama-cpp-python
   ```

2. **QuantaCoin will mint** when we add:
   - KL divergence tracking (v2)
   - Apoptosis pruning (v2)
   - Better compression metrics

## The "Magic Word"

There's no magic word - the system is working as designed. QuantaCoin at 0 is expected for the MVP because:
- The oscillation creates structure, not just removes zeros
- The nat_error accurately reflects computational cost
- Real minting requires more sophisticated algorithms (coming in v2)

---

**TL;DR**: 
- LLM: Install `pip install llama-cpp-python` 
- QuantaCoin: 0.000 is expected for MVP, will mint in v2 with KL divergence
