#!/usr/bin/env python3
"""
Example: How to Test Experience Merge

Experience deltas are extracted and merged from capsules.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.experience_merge import ExperienceMerge
from ApopToSiS.experience.manager import ExperienceManager
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.math.shells import Shell
import time


def test_experience_merge():
    """Test experience merge."""
    print("=== Testing Experience Merge ===\n")
    
    # Create experience manager
    experience_manager = ExperienceManager()
    
    # Create capsules
    print("1. Creating capsules with experience...")
    capsules = []
    for i in range(3):
        capsule = Capsule(
            raw_tokens=[f"experience", f"test{i}"],
            shell=2,
            entropy=0.5 + i * 0.1,
            curvature=1.0 + i * 0.2,
            timestamp=time.time() + i,
            compression_ratio=1.5 + i * 0.1,
        )
        
        # Update experience from capsule
        state = PFState(shell=Shell.MEASUREMENT, curvature=capsule.curvature, entropy=capsule.entropy)
        experience_manager.update(capsule, state)
        capsules.append(capsule)
        print(f"   Created capsule {i+1}")
    
    # Extract experience deltas
    print("\n2. Extracting experience deltas...")
    merge = ExperienceMerge()
    deltas = []
    
    for capsule in capsules:
        delta = merge.extract_experience_delta(capsule, experience_manager)
        deltas.append(delta)
        print(f"   Delta {len(deltas)}: {len(delta.get('habits', []))} habits, {len(delta.get('shortcuts', []))} shortcuts")
    
    # Test delta structure
    print("\n3. Testing delta structure...")
    for i, delta in enumerate(deltas):
        assert delta is not None, f"Delta {i+1} is None"
        assert isinstance(delta, dict), f"Delta {i+1} is not a dict"
        assert 'capsule_id' in delta, f"Delta {i+1} missing capsule_id"
        assert 'compression_ratio' in delta, f"Delta {i+1} missing compression_ratio"
        print(f"   ✓ Delta {i+1} structure valid")
    
    # Merge deltas into new experience manager
    print("\n4. Merging experience deltas...")
    new_experience = ExperienceManager()
    merge.merge_experience_deltas(deltas, new_experience)
    
    summary = new_experience.summarize()
    print(f"   Merged experience:")
    print(f"     Habits: {len(summary.get('habits', {}))}")
    print(f"     Shortcuts: {len(summary.get('shortcuts', {}))}")
    print(f"     Objects: {len(summary.get('objects', {}))}")
    print(f"     Skills: {len(summary.get('skills', {}))}")
    
    print("\n✓ Experience merge tests complete!")
    return deltas, new_experience


if __name__ == "__main__":
    deltas, experience = test_experience_merge()

