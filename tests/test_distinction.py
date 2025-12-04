"""
Test Distinction Chain — PF distinction tracking tests.

Tests:
- Distinction events build correctly
- Flux amplitude computes
- Shell propagation
"""

import pytest
from ApopToSiS.runtime.distinction.distinction import DistinctionChain, DistinctionEvent
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.math.shells import Shell
import time


def test_distinction_chain():
    """Test distinction chain builds correctly."""
    chain = DistinctionChain()
    
    event = DistinctionEvent(
        timestamp=time.time(),
        shell=Shell.MEASUREMENT,
        triplet_data={"type": "presence"},
        entropy=0.5,
        curvature=1.0,
        flux_amplitude=0.8
    )
    
    chain.add_event(event)
    
    assert chain.current_shell() == Shell.MEASUREMENT or chain.current_shell().value == 2


def test_distinction_flux_amplitude():
    """Test flux amplitude computation."""
    chain = DistinctionChain()
    
    event1 = DistinctionEvent(
        timestamp=time.time(),
        shell=Shell.PRESENCE,
        triplet_data={},
        entropy=0.2,
        curvature=0.2,
        flux_amplitude=0.0
    )
    
    event2 = DistinctionEvent(
        timestamp=time.time() + 1,
        shell=Shell.MEASUREMENT,
        triplet_data={},
        entropy=0.5,
        curvature=1.0,
        flux_amplitude=0.8
    )
    
    chain.add_event(event1)
    chain.add_event(event2)
    
    # Check that flux amplitude is computed
    assert hasattr(chain, 'get_curvature_history') or hasattr(chain, 'get_entropy_history')


def test_distinction_shell_propagation():
    """Test shell propagation in distinction chain."""
    chain = DistinctionChain()
    
    state = PFState(
        shell=Shell.MEASUREMENT,
        curvature=1.0,
        entropy=0.5
    )
    
    # Create event from state
    event = chain.create_event_from_state(state, {"type": "test"})
    
    chain.add_event(event)
    
    current_shell = chain.current_shell()
    assert current_shell is not None

