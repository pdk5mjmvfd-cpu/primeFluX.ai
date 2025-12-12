# Documentation Archive Plan

## Files to Archive (Move to `docs/archive/`)

These files contain historical information but are redundant with current documentation:

### Status/Summary Files (Historical)
- `ALL_PATCHES_COMPLETE.md`
- `APOP_NOW_RESPONDS.md`
- `COGNITIVE_ENGINE_PATCH_SUMMARY.md`
- `CRITICAL_WARNINGS.md`
- `DIAGNOSTIC_REPORT.md`
- `DIAGNOSTIC_SEQUENCE.md`
- `FINAL_PATCHES_APPLIED.md`
- `FINAL_STATUS.md`
- `FINAL_VALIDATION_COMPLETE.md`
- `FIRST_SHELL_INTEGRATION.md`
- `HANDOFF_TO_GROK.md`
- `IMPLEMENTATION_PLAN.md`
- `IMPLEMENTATION_STATUS.md`
- `IMPORT_FIX.md`
- `LLM_BRIDGE_PATCH_SUMMARY.md`
- `LOCAL_BOOT_FIXES.md`
- `OFFLINE_DEMO_READY.md`
- `OFFLINE_LLM_BRIDGE_READY.md`
- `PATCH_001_SUMMARY.md`
- `PATCH_004_SUMMARY.md`
- `PATCH_005_SUMMARY.md`
- `PATCH_007C_APPLICATION.md`
- `PATCH_007C_COMPLETE.md`
- `PATCH_007C_IMPLEMENTATION_GUIDE.md`
- `PATCH_008_ASCII_FLUX_COMPLETE.md`
- `PATCH_008A_VALIDATION.md`
- `PATCH_009_SUMMARY.md`
- `PATCH_010_SUMMARY.md`
- `PATCH_011_SUMMARY.md`
- `PHASE1_PATCH2_OPERATOR_CORE_SUMMARY.md`
- `PHASE1_POLYFORM_PATCH_SUMMARY.md`
- `PRESENCE_MVP_CHECKLIST.md`
- `PRESENCE_MVP_SUMMARY.md`
- `RECURSIVE_LEARNING_PATCH_SUMMARY.md`
- `REFINEMENT_V3_SUMMARY.md`
- `REPOSITORY_SETUP_SUMMARY.md`
- `STATUS_CHECK.md`

### Setup/Quick Start (Consolidate)
- `FIX_PIP_COMMAND.md` → Merge into main README
- `FIXES_NEEDED.md` → Archive
- `QUICK_FIX_LLM.md` → Merge into setup guide
- `QUICK_REFERENCE.md` → Keep, update
- `QUICK_START_COMMANDS.md` → Merge into README
- `QUICK_START_LLM.md` → Merge into setup guide
- `QUICK_START_WORKFLOW.md` → Merge into README
- `RUN_LOCALLY.md` → Merge into README
- `SETUP_OFFLINE_LLM.md` → Merge into setup guide
- `SETUP_REPOSITORY.md` → Merge into README
- `VENV_SETUP.md` → Merge into setup guide

### Architecture (Keep Core, Archive Redundant)
- `ARCHITECTURE.md` → Keep, update
- `ARCHITECTURE_LLM_STRATEGY.md` → Archive
- `DUAL_RISK_ARCHITECTURE.md` → Archive
- `ECOSYSTEM_ARCHITECTURE.md` → Keep, update
- `SYSTEM_OVERVIEW.md` → Merge into README
- `WORKFLOW_ORCHESTRATION_VISION.md` → Archive

### Guides (Keep Core, Archive Redundant)
- `AI_COLLABORATION_GUIDE.md` → Keep
- `AGORA_LOGIN_GUIDE.md` → Keep, update
- `THREE_AGENT_API.md` → Keep, update
- `SECTION_12_DISTRIBUTED_RUNTIME.md` → Archive
- `SECTION_12B_USAGE_GUIDE.md` → Archive
- `SECTION_13_PF_DCM.md` → Archive

### Math/Theory (Keep All)
- `MEASUREMENT_ERROR_DUALITY.md` → Keep
- `PRIMEFLUX_AI_ALIGNMENT.md` → Keep
- `PRIMEFLUX_PROOFS_ROADMAP.md` → Keep
- `QUANTACOIN_EXPLANATION.md` → Keep, update
- `QUANTACOIN_IMPLEMENTATION_SUMMARY.md` → Keep, update
- `QUANTACOIN_v1.0_LEGAL_STATUS.md` → Keep
- `QUANTACOIN_v1.0_READY.md` → Archive

## New Structure

### Root Level (Keep Minimal)
- `README.md` - Main entry point
- `ONTOLOGY.md` - Core definitions
- `LICENSE` - License file
- `pyproject.toml` - Package config
- `setup.py` - Setup script
- `requirements.txt` - Dependencies
- `docker-compose.yml` - Docker config
- `Dockerfile` - Docker build

### `docs/` Directory
```
docs/
├── ONTOLOGY.md              # Core concepts (moved from root)
├── ARCHITECTURE.md          # System architecture
├── ECOSYSTEM_ARCHITECTURE.md # Agora ecosystem
├── QUANTACOIN.md           # QuantaCoin documentation (consolidated)
├── SETUP.md                # Setup guide (consolidated)
├── API.md                  # API documentation
├── papers/                  # Academic papers
└── archive/                 # Historical documentation
```

## Action Items

1. Create `docs/archive/` directory
2. Move historical files to archive
3. Consolidate setup guides into `docs/SETUP.md`
4. Consolidate QuantaCoin docs into `docs/QUANTACOIN.md`
5. Update README to reference new structure
6. Update all internal links

