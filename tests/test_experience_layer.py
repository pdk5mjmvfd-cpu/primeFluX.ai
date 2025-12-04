"""
Test Experience Layer — cognitive memory tests.

Tests:
- All experience subsystems update
- No module missing
- Experience factor computation
"""

import pytest
import time
from ApopToSiS.experience.manager import ExperienceManager
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.math.shells import Shell


def test_experience_update():
    """Test experience manager updates from capsule."""
    manager = ExperienceManager()
    state = PFState(
        shell=Shell.MEASUREMENT,
        curvature=1.1,
        entropy=0.5,
        density=0.4
    )
    
    capsule = Capsule(
        raw_tokens=["experience", "test"],
        triplets=[],
        entropy=0.5,
        curvature=1.1,
        shell=2,
        density=0.4,
        psi=1.0,
        hamiltonian=1.2,
        reptend_entropy=0.1,
        rail_interference=1.0,
        timestamp=time.time()
    )
    
    manager.update(capsule, state)
    summary = manager.summarize()
    
    assert "habits" in summary
    assert "shortcuts" in summary
    assert "objects" in summary
    assert "skills" in summary
    assert "experience_graph" in summary


def test_experience_factor():
    """Test experience factor computation."""
    manager = ExperienceManager()
    
    factor = manager.get_experience_factor()
    
    assert isinstance(factor, float)
    assert factor >= 0.0


def test_habits_update():
    """Test habits update from capsule."""
    from experience.habits.habits import HabitManager
    
    habit_manager = HabitManager()
    state = PFState(curvature=1.0, entropy=0.5, density=0.3)
    
    capsule = Capsule(
        raw_tokens=["habit", "test"],
        entropy=0.5,
        curvature=1.0,
        shell=2,
        timestamp=time.time()
    )
    
    habit_manager.update_from_capsule(capsule, state)
    
    summary = habit_manager.summary()
    assert isinstance(summary, dict)


def test_shortcuts_update():
    """Test shortcuts update from capsule."""
    from experience.shortcuts.shortcuts import ShortcutManager
    
    shortcut_manager = ShortcutManager()
    state = PFState(curvature=0.5, entropy=0.3, density=0.2)
    
    capsule = Capsule(
        raw_tokens=["shortcut", "test"],
        entropy=0.3,
        curvature=0.5,
        shell=2,
        timestamp=time.time()
    )
    
    shortcut_manager.update_from_capsule(capsule, state)
    
    summary = shortcut_manager.summary()
    assert isinstance(summary, dict)

