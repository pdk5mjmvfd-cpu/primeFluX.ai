# FluxAI Quick Reference

**One-page reference for the FluxAI Runtime refinement project**

---

## 📋 The 7 Refinement Directions

1. **FluxAI.Local** — Offline LLM (2B-8B parameters, runs on consumer hardware)
2. **FluxAI.Memory** — Integer-based memory (reversible PrimeFlux operators)
3. **FluxAI.OperatorCore** — Domain ↔ Range reversible transforms
4. **FluxAI.Trinity** — STEM/LANG/SAFE agents (domain roles, not cognitive modes)
5. **FluxAI.Runtime** — Unified runtime (Trinity + LCM + Local LLM)
6. **FluxAI.Evolution** — Compression-based learning (sessions → LCM packets → training)
7. **FluxAI.LedgerSync** — Grok/X network layer (pub-sub, distinctions only)

---

## 🎯 Priority Order

1. **Memory** (Critical) — Foundation
2. **OperatorCore** (Critical) — Needed for memory
3. **Trinity** (High) — Agent system
4. **Local** (High) — Offline operation
5. **Runtime** (Medium) — Integration
6. **Evolution** (Medium) — Learning
7. **LedgerSync** (Low) — Future

---

## 📁 Key Documents

- **`FLUXAI_REFINEMENT_ROADMAP.md`** — Full roadmap and code review
- **`AI_COLLABORATION_GUIDE.md`** — Guide for AI assistants
- **`IMPLEMENTATION_STATUS.md`** — Progress tracker
- **`REPOSITORY_SETUP_SUMMARY.md`** — Setup summary

---

## 🏗️ Current Architecture

**✅ Strong:**
- ICM (Information Curvature Manifold)
- LCM (Language Context Manifold)
- Capsules (JSON-Flux transport)
- Experience Layer
- PrimeFlux math

**⚠️ Needs Work:**
- Memory (JSON → integers)
- Agents (Eidos/Praxis/Aegis → STEM/LANG/SAFE)
- LLM (remote → local)
- Network (Grok/X integration)

---

## 🚀 Quick Start

**For Humans:**
1. Read `FLUXAI_REFINEMENT_ROADMAP.md`
2. Review `ARCHITECTURE.md`
3. Start Phase 1 (Memory + OperatorCore)

**For AI Assistants:**
1. Read `AI_COLLABORATION_GUIDE.md`
2. Check `IMPLEMENTATION_STATUS.md`
3. Follow existing patterns
4. Test with `python apop.py`

---

## 📝 Key Principles

**DO:**
- ✅ Preserve capsule protocol
- ✅ Maintain offline-first
- ✅ Use reversible operators
- ✅ Follow boot sequence

**DON'T:**
- ❌ Break capsule encode/decode
- ❌ Add network deps to core
- ❌ Modify PF math without understanding
- ❌ Store JSON when integers possible

---

## 🔧 Implementation Phases

**Phase 1 (Weeks 1-2):** Memory + OperatorCore  
**Phase 2 (Weeks 3-4):** Trinity + Local LLM  
**Phase 3 (Weeks 5-6):** Runtime + Evolution  
**Phase 4 (Weeks 7-8):** LedgerSync (future)

---

## 📊 Status

**Completion:** 0% (0/7 directions)  
**In Progress:** 0  
**Next:** Start FluxAI.Memory

---

**See full details in `FLUXAI_REFINEMENT_ROADMAP.md`**

