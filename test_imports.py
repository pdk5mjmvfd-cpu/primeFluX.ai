#!/usr/bin/env python3
"""Quick test to verify all imports work."""

import sys
import os

# Setup path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)

if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

print("Testing imports...")

try:
    from ApopToSiS.runtime.state.state import PFState
    print("✓ PFState")
    
    from ApopToSiS.core.lcm import LCM
    print("✓ LCM")
    
    from ApopToSiS.core.icm import ICM
    print("✓ ICM")
    
    from ApopToSiS.runtime.supervisor.supervisor import Supervisor
    print("✓ Supervisor")
    
    from ApopToSiS.runtime.capsules import Capsule
    print("✓ Capsule")
    
    from ApopToSiS.runtime.context.context import Context
    print("✓ Context")
    
    from ApopToSiS.quanta.quanta import QuantaCompressor
    print("✓ QuantaCompressor")
    
    from ApopToSiS.agents.registry.registry import AgentRegistry
    print("✓ AgentRegistry")
    
    from ApopToSiS.agents.eidos.eidos import EidosAgent
    print("✓ EidosAgent")
    
    from ApopToSiS.agents.praxis.praxis import PraxisAgent
    print("✓ PraxisAgent")
    
    from ApopToSiS.agents.aegis.aegis import AegisAgent
    print("✓ AegisAgent")
    
    print("\n✅ All imports successful!")
    
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

