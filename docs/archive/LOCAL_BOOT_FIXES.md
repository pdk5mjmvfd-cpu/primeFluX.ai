# Local Boot Script - Fixes Applied

## Overview
Fixed the local boot script (`local_boot.py`) to properly integrate with the ApopToSiS v3 runtime architecture.

## Key Fixes

### 1. **Proper Component Initialization**
- Added ICM initialization (geometric interior)
- Added LCM initialization (linguistic cortex)
- Added Experience Manager initialization
- Properly linked LCM with Experience Manager
- Properly linked Supervisor with Experience Manager

### 2. **Capsule Creation**
- **Fixed**: `Capsule.from_tokens()` doesn't exist
- **Solution**: Use LCM to process tokens and generate capsule via `lcm.process_tokens()` → `lcm.generate_capsule()`
- Properly decode capsule dictionary to Capsule object

### 3. **Agent Registry**
- **Fixed**: `AgentRegistry.load_core_agents()` doesn't exist
- **Solution**: Manually instantiate and register Trinity agents:
  - `EidosAgent()`
  - `PraxisAgent()`
  - `AegisAgent()`

### 4. **State Serialization**
- **Fixed**: `state.to_dict()` doesn't exist
- **Solution**: Create manual dictionary with state fields:
  - shell, curvature, entropy, density, hamiltonian, psi
  - distinction_chain_length, history_length

### 5. **QuantaCoin Compression**
- **Fixed**: `QuantaCompressor.compression_ratio()` is an instance method, not static
- **Solution**: Use `quanta_compressor.compute_quanta(capsule)` for QuantaCoin value
- Use `quanta_compressor.hash_capsule(capsule)` for hashing

### 6. **Agent Transform Method**
- **Fixed**: `transform()` only takes `capsule`, not `state`
- **Solution**: Call `selected_agent.transform(capsule)` without state parameter

### 7. **Context Methods**
- **Fixed**: `context.update_state()` doesn't exist
- **Solution**: Use `context.add_capsule(capsule)` which internally calls `update()`

### 8. **Experience Delta Extraction**
- **Fixed**: `ExperienceMerge.extract_experience_delta()` requires `experience_manager` parameter
- **Solution**: Pass `experience_manager` as second argument

### 9. **Device Identity**
- **Fixed**: `DeviceIdentity.get_device_id()` and `get_instance_id()` are instance methods
- **Solution**: Use `get_device_identity()` global function to get singleton instance

## Complete Dataflow

```
User Input
  ↓
Tokenize (split)
  ↓
LCM.process_tokens() → Updates LCM state
  ↓
LCM.generate_capsule() → Creates capsule dictionary
  ↓
Capsule.decode() → Creates Capsule object
  ↓
Add device_id, session_id
  ↓
QuantaCompressor.hash_capsule() → QuantaCoin hash
  ↓
QuantaCompressor.compute_quanta() → QuantaCoin value
  ↓
State.update() → Updates PFState
  ↓
Context.add_capsule() → Updates context
  ↓
Supervisor.route() → Selects agent
  ↓
Agent.transform() → Processes capsule
  ↓
ExperienceManager.update() → Updates experience
  ↓
ExperienceMerge.extract_experience_delta() → Extracts delta
  ↓
Supervisor.integrate_capsule() → Final integration
  ↓
Save to local files
  ↓
Return result
```

## Usage

```bash
# Make executable (already done)
chmod +x local_boot.py

# Run
python3 local_boot.py

# Or directly
./local_boot.py
```

## Local Storage

All data is stored in `~/.apoptosis/`:
- `local_capsules/` - JSON capsule files
- `local_state/` - PFState snapshots
- `local_experience/` - Experience summaries

## Testing

The script includes error handling and will print stack traces if something goes wrong. This helps with debugging during initial runs.

## Next Steps

1. Test the script with simple inputs
2. Verify capsule generation
3. Verify agent routing
4. Verify experience layer updates
5. Verify QuantaCoin computation
6. Verify local file storage

