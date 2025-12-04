#!/usr/bin/env python3
"""
Example: How to Process a Capsule Through the PF Runtime

Processing = full Apop cognition cycle.

What happens internally:
1. capsule enters Supervisor
2. entropy/curvature determine which agent
3. agent transforms the capsule
4. capsule re-enters LCM
5. PFState updates
6. Experience Layer updates
7. QuantaCoin minted
8. capsule output returned

This is the "thinking" loop.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.supervisor.supervisor import Supervisor
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM
from ApopToSiS.core.math.shells import Shell
import time


def process_capsule_through_runtime():
    """Process a capsule through the full PF runtime."""
    print("=== Processing Capsule Through PF Runtime ===\n")
    
    # Initialize components
    icm = ICM()
    lcm = LCM(icm)
    supervisor = Supervisor(icm=icm, lcm=lcm)
    context = Context()
    
    # Create agents
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    # Create initial state
    state = PFState(
        shell=Shell.PRESENCE,
        curvature=0.0,
        entropy=0.0
    )
    
    # Create a capsule
    capsule = Capsule(
        raw_tokens=["process", "this", "capsule"],
        shell=0,
        entropy=0.5,
        curvature=1.0,
        timestamp=time.time()
    )
    
    print(f"Input capsule:")
    print(f"  Tokens: {capsule.raw_tokens}")
    print(f"  Shell: {capsule.shell}")
    print(f"  Entropy: {capsule.entropy:.4f}")
    print(f"  Curvature: {capsule.curvature:.4f}\n")
    
    # Process through supervisor
    print("Processing through Supervisor...")
    result = supervisor.process_capsule(capsule, agents)
    
    print(f"\nOutput:")
    print(f"  Final capsule shell: {result['state']['shell']}")
    print(f"  Final curvature: {result['state']['curvature']:.4f}")
    print(f"  Final entropy: {result['state']['entropy']:.4f}")
    print(f"  Routed agent: {result['agent_sequence'][-1] if result['agent_sequence'] else 'None'}")
    print(f"  QuantaCoin minted: {result['quanta_minted']:.4f}")
    print(f"  Flux amplitude: {result['flux_metrics']['flux_amplitude']:.4f}")
    
    return result


if __name__ == "__main__":
    result = process_capsule_through_runtime()
    print("\n✓ Capsule processing complete!")

