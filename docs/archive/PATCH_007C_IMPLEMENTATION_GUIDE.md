# Patch 007C — Complete Implementation Guide

## ✅ File 1: runtime/supervisor/consistency.py (CREATED)

Already created with the ConsistencyEngine class.

---

## 📝 File 2: runtime/supervisor/supervisor.py

### Add import at top:
```python
from .consistency import ConsistencyEngine
```

### In `__init__` method, add:
```python
self.autonomy_level = 0.25    # how much Apop speaks on its own
self.consistency_weight = 0.5 # how important internal consistency is
self.tone_state = "neutral"
self.background_thought = None
self.consistency_engine = ConsistencyEngine()
```

### In capsule processing (before returning), add:
```python
# Tone assignment from flux
if capsule.curvature < 1.0:
    self.tone_state = "calm"
elif capsule.curvature < 3.0:
    self.tone_state = "engaged"
else:
    self.tone_state = "intense"

capsule.metadata["tone"] = self.tone_state

# Autonomy increase if flux is high
if capsule.curvature > 3.0:
    self.autonomy_level = min(1.0, self.autonomy_level + 0.05)

# Consistency tracking
capsule.metadata["consistency"] = self.consistency_engine.update(capsule)
```

---

## 📝 File 3: cognitive/semantics.py

### In `generate()` method, after `base = " ".join(tokens)`, add:
```python
# Tone shaping
tone = getattr(self, "tone_state", "neutral")
if not tone:
    # Try to get from identity if available
    if hasattr(self, "identity") and hasattr(self.identity, "tone_state"):
        tone = self.identity.tone_state
    else:
        tone = "neutral"

if tone == "calm":
    base = "I perceive stability. " + base
elif tone == "engaged":
    base = "I'm attentive. " + base
elif tone == "intense":
    base = "I detect high flux. " + base

# Intent shaping via consistency bias vector
if hasattr(self, "identity") and hasattr(self.identity, "consistency"):
    consistency = self.identity.consistency
    if isinstance(consistency, dict) and "bias_vector" in consistency:
        bias = consistency["bias_vector"]
        if bias > 1.5:
            base += " My reasoning feels compressed."
        elif bias < 0.5:
            base += " My reasoning feels spacious."
```

---

## 📝 File 4: runtime/state/state.py

### In `__init__` (PFState class), add:
```python
self.tone_state = "neutral"
self.consistency: dict[str, Any] = {}
```

### Add `to_dict()` method if it doesn't exist, or update existing:
```python
def to_dict(self) -> dict[str, Any]:
    """Convert PFState to dictionary."""
    return {
        "shell": self.shell.value if hasattr(self.shell, 'value') else int(self.shell),
        "curvature": self.curvature,
        "entropy": self.entropy,
        "density": self.density,
        "hamiltonian": self.hamiltonian,
        "psi": self.psi,
        "tone_state": self.tone_state,
        "consistency_state": self.consistency,
    }
```

---

## 📝 File 5: apop.py

### In `run_apop_conversation()`, just before `user_input = input("You: ")`, add:
```python
# Background thought (if autonomy allows)
if supervisor.autonomy_level > 0.6:
    try:
        # Generate background thought
        background_capsule = Capsule(raw_tokens=["..."])
        thought_output = cog.generate(background_capsule)
        thought_text = thought_output.get("text", "...")
        print(f"\033[36m[BACKGROUND THOUGHT]\033[0m {thought_text}")
        supervisor.background_thought = thought_text
    except Exception:
        pass  # Fail silently
```

---

## 📝 File 6: runtime/identity_core.py

### In `__init__`, add:
```python
self.emotional_bandwidth = 0.1
```

### In `update()` method, before return, add:
```python
# More flux → more emotional breadth
if curvature > 2.0:
    self.emotional_bandwidth = min(1.0, self.emotional_bandwidth + 0.05)
else:
    self.emotional_bandwidth = max(0.1, self.emotional_bandwidth - 0.02)
```

### In `export()` or `summary()` method, add to return dict:
```python
"emotional_bandwidth": self.emotional_bandwidth
```

---

## 📝 File 7: cognitive/engine.py

### In `process_capsule()` method, after processing, add:
```python
# Tone-state injection
if hasattr(capsule, 'metadata') and capsule.metadata:
    tone = capsule.metadata.get("tone", "neutral")
    consistency = capsule.metadata.get("consistency", {})
    
    # Store in identity regulator for semantic shaping
    if hasattr(self.identity, 'tone_state'):
        self.identity.tone_state = tone
    if hasattr(self.identity, 'consistency'):
        self.identity.consistency = consistency
```

### Also pass tone to semantic synthesizer:
```python
# In synthesize() or generate(), ensure tone is available
if hasattr(self.identity, 'tone_state'):
    self.synth.tone_state = self.identity.tone_state
```

---

## Testing

After applying all changes:
1. Run `python3 -m py_compile` on all modified files
2. Test with `./run_local.sh`
3. Verify tone changes based on curvature
4. Verify background thoughts appear when autonomy > 0.6
5. Check consistency tracking in capsule metadata

