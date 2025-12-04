# Upgrade Path to Full Capsule Mode (Option B)

## Current State: Hybrid Mode (Option C)

In Hybrid Mode:
- Local Apop sends capsule → LLM
- LLM returns semantic output + PF metadata hints
- Local runtime generates the actual capsule
- LLM metadata influences but does not dominate (PF rules)

## Upgrade to Full Capsule Mode (Option B)

When ready to upgrade, implement the following:

### 1. Full Capsule Return Format

LLM should return a complete PF capsule structure:
```json
{
    "capsule": {
        "raw_tokens": [...],
        "triplets": [...],
        "shell": 2,
        "curvature": 1.414,
        "entropy": 0.5,
        "density": 0.3,
        "psi": 0.8,
        "hamiltonian": 2.1,
        ...
    },
    "semantic_output": "...",
    "pf_metadata": {...}
}
```

### 2. Permit LLM to Set Curvature

In `core/lcm.py`, modify `integrate_llm_feedback()`:
- Remove curvature override protection
- Allow LLM to set absolute curvature (with validation)
- Add validation layer to ensure curvature is within PF bounds

### 3. Permit LLM to Set Shell (with Validation)

In `runtime/distributed_safety.py`:
- Add `validate_llm_shell()` method
- Check shell transitions are valid (0→2→3→4→0)
- Allow LLM to suggest shell transitions

### 4. Allow LLM to Generate Distinction Events

In `runtime/distinction/distinction.py`:
- Add `create_from_llm_metadata()` method
- Allow LLM-provided distinction events
- Validate distinction events follow PF rules

### 5. Allow PFState to Ingest Remote Curvature

In `runtime/state/state.py`:
- Modify `update()` to accept remote curvature
- Add curvature merge logic (weighted average)
- Ensure local PF computation still dominates

### 6. Introduce Distributed Curvature Merging

In `runtime/state_merge.py`:
- Add `merge_remote_curvature()` method
- Implement weighted average based on QuantaCoin trust
- Ensure PF consistency is maintained

## Migration Checklist

- [ ] Update `RemoteLLMBridge` to handle full capsule returns
- [ ] Modify `LLMAdapter` to extract full capsules
- [ ] Update `LCM.integrate_llm_feedback()` to accept full capsules
- [ ] Add validation for LLM-generated capsules
- [ ] Update `DistributedSafety` to validate LLM capsules
- [ ] Implement curvature merging logic
- [ ] Add shell transition validation for LLM suggestions
- [ ] Update documentation

## Compatibility

Hybrid Mode is forward-compatible with Full Capsule Mode:
- Existing Hybrid Mode code will continue to work
- Full Capsule Mode can be enabled via configuration
- Both modes can coexist (different endpoints)

## Safety Considerations

When upgrading to Full Capsule Mode:
1. **Always validate LLM-generated capsules** using `DistributedSafety`
2. **Maintain PF rule dominance** - LLM suggestions are hints, not commands
3. **Use QuantaCoin trust scores** to weight LLM contributions
4. **Monitor curvature consistency** - reject capsules with invalid transitions
5. **Preserve local PF computation** - LLM enhances, does not replace

## Testing

Before enabling Full Capsule Mode in production:
1. Test with mock LLM responses
2. Validate all safety checks pass
3. Verify PF consistency is maintained
4. Test curvature merging logic
5. Test shell transition validation
6. Test with various LLM response formats

## Configuration

Add to `api/llm_bridge_config.json`:
```json
{
    "mode": "full_capsule",
    "validate_llm_capsules": true,
    "curvature_merge_weight": 0.3,
    "allow_llm_shell_transitions": true
}
```

