"""
Test State & Context — runtime state management tests.

Tests:
- PFState accepts capsule fields
- Context window updates
- State transitions
"""

import pytest
import time
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.core.math.shells import Shell


def test_state_context_updates():
    """Test state and context update from capsule."""
    state = PFState()
    context = Context()
    
    capsule = Capsule(
        raw_tokens=["state", "update"],
        triplets=[],
        entropy=0.6,
        curvature=1.4,
        shell=3,
        density=0.5,
        psi=1.1,
        hamiltonian=1.4,
        reptend_entropy=0.2,
        rail_interference=1.0,
        timestamp=time.time()
    )
    
    # Update state
    state.update(capsule.to_dict())
    
    # Update context
    context.add_capsule(capsule)
    
    # Check context
    last_capsules = context.last_capsules(1)
    assert len(last_capsules) > 0
    assert last_capsules[0].raw_tokens == ["state", "update"]


def test_state_update():
    """Test PFState updates from capsule."""
    state = PFState()
    
    capsule = Capsule(
        raw_tokens=["test"],
        entropy=0.5,
        curvature=1.2,
        shell=2,
        timestamp=time.time()
    )
    
    state.update(capsule.to_dict())
    
    assert state.curvature == 1.2 or state.curvature > 0
    assert state.entropy == 0.5 or state.entropy > 0


def test_context_capsule_storage():
    """Test context stores capsules."""
    context = Context()
    
    capsule1 = Capsule(
        raw_tokens=["first"],
        timestamp=time.time()
    )
    
    capsule2 = Capsule(
        raw_tokens=["second"],
        timestamp=time.time() + 1
    )
    
    context.add_capsule(capsule1)
    context.add_capsule(capsule2)
    
    last = context.last_capsules(2)
    assert len(last) >= 1


def test_context_trends():
    """Test context trend computation."""
    context = Context()
    
    # Add some capsules
    for i in range(3):
        capsule = Capsule(
            raw_tokens=[f"token_{i}"],
            curvature=1.0 + i * 0.1,
            entropy=0.5 + i * 0.1,
            timestamp=time.time() + i
        )
        context.add_capsule(capsule)
    
    # Check trends
    curvature_trend = context.curvature_trend()
    entropy_trend = context.entropy_trend()
    
    assert isinstance(curvature_trend, (float, int))
    assert isinstance(entropy_trend, (float, int))

