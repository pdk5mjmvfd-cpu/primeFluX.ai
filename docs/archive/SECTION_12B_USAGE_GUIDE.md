# Section 12B — Practical Usage Guide

**Status:** ✅ **COMPLETE**

## Overview

Section 12B provides practical examples and utilities for using ApopToSiS v3 locally. This turns the runtime from "architecture" → **something you can actually run**.

## Implementation Summary

### ✅ 10 Practical Examples Created

All examples are in the `examples/` directory:

1. **`construct_capsule.py`** - How to construct capsules (manual and LCM-based)
2. **`process_capsule.py`** - How to process capsules through PF runtime
3. **`simulate_network.py`** - How to simulate network behavior offline
4. **`test_state_merge.py`** - How to test PF-state merge locally
5. **`test_experience_merge.py`** - How to test experience merge
6. **`test_quanta.py`** - How to test QuantaCoin (ΦQ)
7. **`full_pf_cycle.py`** - How to run a complete PF cycle
8. **`llm_integration.py`** - How to attach LLM "mouth" front-end
9. **`validate_safety.py`** - How to validate local safety
10. **`daily_workflow.py`** - Recommended daily workflow

### ✅ Documentation

- **`examples/README.md`** - Complete guide to all examples

## Key Features Demonstrated

### 1. Capsule Construction
- Manual construction with all fields
- LCM-based construction (recommended)
- Network field initialization
- Device identity integration

### 2. PF Runtime Processing
- Complete cognition cycle
- Supervisor routing
- Agent transformation
- PFState updates
- QuantaCoin minting
- Experience integration

### 3. Network Simulation
- Sync queue operations
- Network protocol simulation
- Capsule validation
- PFState reconstruction
- Trust scoring

### 4. State & Experience Merging
- State reconstruction from capsules
- Conflict resolution
- Experience delta extraction
- Experience delta merging
- Chain validation

### 5. QuantaCoin Testing
- Compression computation
- Hash generation
- Trust scoring
- Validation thresholds

### 6. Full PF Cycle
- Complete offline cognition loop
- Multiple cycle demonstration
- Experience accumulation
- State persistence

### 7. LLM Integration
- LLM bridge interface
- PF → LLM → PF cycle
- Mock LLM examples
- OpenAI GPT integration template

### 8. Safety Validation
- Network safety checks
- Shell transition validation
- Curvature consistency
- Trust scoring

### 9. Daily Workflow
- Recommended operation pattern
- Complete workflow demonstration
- Sync queue management
- Experience tracking

## Usage

### Running Individual Examples

```bash
# Construct capsule
python examples/construct_capsule.py

# Process capsule
python examples/process_capsule.py

# Simulate network
python examples/simulate_network.py

# Test state merge
python examples/test_state_merge.py

# Test experience merge
python examples/test_experience_merge.py

# Test QuantaCoin
python examples/test_quanta.py

# Run full PF cycle
python examples/full_pf_cycle.py

# LLM integration
python examples/llm_integration.py

# Validate safety
python examples/validate_safety.py

# Daily workflow
python examples/daily_workflow.py
```

### Running All Examples

```bash
for example in examples/*.py; do
    if [[ "$example" != "examples/README.md" ]]; then
        python "$example"
    fi
done
```

## Integration Patterns

### Basic Usage

```python
from runtime.boot import boot_apop, create_first_memory

# Boot system
runtime = boot_apop()

# Process input
result = create_first_memory(runtime, "your input text")
```

### LLM Integration

```python
from examples.llm_integration import apop_llm_bridge

# Bridge PF capsule to LLM
output_capsule = apop_llm_bridge(input_capsule, your_llm_function)
```

### Network Simulation

```python
from runtime.sync_queue import SyncQueue
from runtime.network_sync_protocol import NetworkSyncProtocol

# Queue for offline sync
queue = SyncQueue()
queue.enqueue_capsule(capsule)

# Simulate network transmission
protocol = NetworkSyncProtocol(device_identity)
prepared = protocol.prepare_capsule_for_send(capsule)
```

## Verification Results

All 10 examples verified:
- ✅ `construct_capsule.py` - Working
- ✅ `process_capsule.py` - Working
- ✅ `simulate_network.py` - Working
- ✅ `test_state_merge.py` - Working
- ✅ `test_experience_merge.py` - Working
- ✅ `test_quanta.py` - Working
- ✅ `full_pf_cycle.py` - Working
- ✅ `llm_integration.py` - Working
- ✅ `validate_safety.py` - Working
- ✅ `daily_workflow.py` - Working

## Daily Workflow (Recommended)

The recommended way to operate Apop locally:

1. User types text
2. LCM → capsule
3. Supervisor routes
4. Agent transforms capsule
5. LCM rebuilds capsule
6. PFState updates
7. Experience graph updates
8. QuantaCoin minted
9. Capsule saved (history)
10. LLM invoked if needed
11. Network sync queued (offline)

**This is the exact internal loop used later in PF-DCM.**

## What You Can Do Now

With Section 12B complete, you can:

- ✅ Construct capsules manually or via LCM
- ✅ Process capsules through full PF runtime
- ✅ Simulate network behavior offline
- ✅ Test state and experience merging
- ✅ Test QuantaCoin compression and trust
- ✅ Run complete PF cognition cycles
- ✅ Integrate with LLM front-ends
- ✅ Validate safety (network + cognitive)
- ✅ Follow recommended daily workflow

## Next Steps

Section 12B makes the runtime **practical and usable**. You can now:

1. **Test locally** - All examples work offline
2. **Integrate LLM** - Use LLM integration examples
3. **Build applications** - Use examples as templates
4. **Prepare for Section 13** - Foundation ready for distributed mesh

---

**Status:** ✅ **SECTION 12B COMPLETE - RUNTIME IS PRACTICAL AND USABLE**

*"Local PF runtime = brain. LLM = mouth. Capsules = nerves."*

