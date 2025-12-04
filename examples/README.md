# ApopToSiS v3 — Practical Usage Examples

This directory contains practical examples for using ApopToSiS v3 locally.

## Examples

### 1. `construct_capsule.py`
**How to Construct a Capsule**

Demonstrates two methods:
- Manual capsule construction
- LCM-based capsule construction (recommended)

```bash
python examples/construct_capsule.py
```

### 2. `process_capsule.py`
**How to Process a Capsule Through the PF Runtime**

Shows the complete cognition cycle:
- Supervisor routing
- Agent transformation
- PFState updates
- QuantaCoin minting

```bash
python examples/process_capsule.py
```

### 3. `simulate_network.py`
**How to Simulate Network Behavior Offline**

Demonstrates:
- Sync queue operations
- Network protocol simulation
- Capsule validation
- PFState reconstruction

```bash
python examples/simulate_network.py
```

### 4. `test_state_merge.py`
**How to Test PF-State Merge Locally**

Tests:
- State reconstruction from capsules
- Conflict resolution
- Chain validation
- Device precedence

```bash
python examples/test_state_merge.py
```

### 5. `test_experience_merge.py`
**How to Test Experience Merge**

Tests:
- Experience delta extraction
- Delta merging
- Conflict resolution by QuantaCoin

```bash
python examples/test_experience_merge.py
```

### 6. `test_quanta.py`
**How to Test QuantaCoin (ΦQ)**

Tests:
- Compression computation
- Hash generation
- Trust scoring
- Validation

```bash
python examples/test_quanta.py
```

### 7. `full_pf_cycle.py`
**How to Run a Full Local PF Cycle**

Complete cognition loop:
- Tokenization
- Triplet analysis
- Curvature estimation
- Shell transition
- Agent routing
- Experience integration

```bash
python examples/full_pf_cycle.py
```

### 8. `llm_integration.py`
**How to Attach the LLM "Mouth" Front-End**

Demonstrates:
- LLM bridge interface
- PF → LLM → PF cycle
- Mock LLM integration
- OpenAI GPT example (commented)

```bash
python examples/llm_integration.py
```

### 9. `validate_safety.py`
**How to Validate Local Safety**

Tests:
- Network safety validation
- Shell transition validation
- Curvature consistency
- Trust scoring

```bash
python examples/validate_safety.py
```

### 10. `daily_workflow.py`
**Daily Workflow (Recommended)**

Complete workflow:
- User input → capsule
- Processing through PF runtime
- Experience updates
- QuantaCoin minting
- Sync queue management

```bash
python examples/daily_workflow.py
```

## Running All Examples

```bash
# Run all examples
for example in examples/*.py; do
    if [[ "$example" != "examples/README.md" ]]; then
        echo "Running $example..."
        python "$example"
        echo ""
    fi
done
```

## Integration with Your Code

All examples can be imported and used in your own code:

```python
from examples.full_pf_cycle import run_full_pf_cycle
from examples.llm_integration import apop_llm_bridge

# Use in your code
result = run_full_pf_cycle()
```

## Notes

- All examples use local-only operation (no network required)
- Examples demonstrate offline behavior
- LLM integration examples include mock functions (replace with actual LLM calls)
- Sync queue examples show offline → online transition simulation

---

*"Local PF runtime = brain. LLM = mouth. Capsules = nerves."*

