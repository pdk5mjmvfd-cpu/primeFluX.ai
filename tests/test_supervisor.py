"""
Test Supervisor — PF routing engine tests.

Tests:
- Basic routing works
- Agents sequence without error
- State updates
"""

import pytest
from ApopToSiS.runtime.supervisor.supervisor import Supervisor
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.math.shells import Shell
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent


def test_supervisor_routing():
    """Test supervisor routing."""
    icm = ICM()
    lcm = LCM(icm)
    supervisor = Supervisor(icm=icm, lcm=lcm)
    
    # Create agents
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    # Create state
    state = PFState(
        shell=Shell.MEASUREMENT,
        curvature=1.5,
        entropy=1.0,
        density=0.5
    )
    
    # Route
    selected_agent = supervisor.route(state, agents)
    
    assert selected_agent is not None
    assert selected_agent in agents


def test_supervisor_process_capsule():
    """Test supervisor processes capsule."""
    from ApopToSiS.runtime.capsules import Capsule
    import time
    
    icm = ICM()
    lcm = LCM(icm)
    supervisor = Supervisor(icm=icm, lcm=lcm)
    
    # Create capsule
    capsule = Capsule(
        raw_tokens=["primeflux", "test"],
        entropy=0.5,
        curvature=1.2,
        shell=2,
        timestamp=time.time()
    )
    
    # Create agents
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    # Process capsule
    result = supervisor.process_capsule(capsule, agents)
    
    assert "final_capsule" in result
    assert "state" in result
    assert "agent_sequence" in result
    assert "flux_metrics" in result
    assert "quanta_minted" in result


def test_supervisor_integrate_capsule():
    """Test supervisor integrates capsule."""
    from ApopToSiS.runtime.capsules import Capsule
    import time
    
    icm = ICM()
    lcm = LCM(icm)
    supervisor = Supervisor(icm=icm, lcm=lcm)
    
    capsule = Capsule(
        raw_tokens=["integrate", "test"],
        entropy=0.5,
        curvature=1.0,
        shell=2,
        timestamp=time.time()
    )
    
    # Should not raise
    supervisor.integrate_capsule(capsule)
    
    assert True  # If we get here, integration worked

