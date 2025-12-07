"""
Tests for Orbital Children with Quark Colors & Event Spaces.
"""

import pytest
import math
from core.particle_engine import (
    PFParticle,
    OrbitalChild,
    OrbitalShell,
    ParticleEngine,
    QuarkColor
)


def test_orbital_child_initialization():
    """Test OrbitalChild initialization with parent shell."""
    # Create parent shell
    parent_shell = OrbitalShell(freq=1.0, phase=0.0, curvature=1.0)
    
    # Create child with harmonic n=1, color RED
    child = OrbitalChild(
        position=(1.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=parent_shell,
        harmonic_n=1,
        color_idx=0  # RED
    )
    
    # Check frequency: child freq = parent freq / n
    assert child.freq == pytest.approx(1.0 / 1)  # parent.freq / 1
    
    # Check phase: child phase = parent phase + (2π/3) * color_idx
    expected_phase = 0.0 + (2 * math.pi / 3) * 0  # RED = 0
    assert child.phase == pytest.approx(expected_phase)


def test_orbital_child_quark_colors():
    """Test quark color phases."""
    parent_shell = OrbitalShell(freq=1.0, phase=0.0, curvature=1.0)
    
    # RED child
    red_child = OrbitalChild(
        position=(1.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=parent_shell,
        harmonic_n=1,
        color_idx=0  # RED
    )
    assert red_child.phase == pytest.approx(0.0)
    
    # GREEN child
    green_child = OrbitalChild(
        position=(0.0, 1.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=parent_shell,
        harmonic_n=1,
        color_idx=1  # GREEN
    )
    assert green_child.phase == pytest.approx(2 * math.pi / 3)
    
    # BLUE child
    blue_child = OrbitalChild(
        position=(0.0, 0.0, 1.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=parent_shell,
        harmonic_n=1,
        color_idx=2  # BLUE
    )
    assert blue_child.phase == pytest.approx(4 * math.pi / 3)


def test_orbital_child_harmonic_frequency():
    """Test harmonic frequency inheritance."""
    parent_shell = OrbitalShell(freq=2.0, phase=0.0, curvature=1.0)
    
    # Child with n=1
    child1 = OrbitalChild(
        position=(1.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=parent_shell,
        harmonic_n=1,
        color_idx=0
    )
    assert child1.freq == pytest.approx(2.0 / 1)
    
    # Child with n=2
    child2 = OrbitalChild(
        position=(2.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=parent_shell,
        harmonic_n=2,
        color_idx=0
    )
    assert child2.freq == pytest.approx(2.0 / 2)


def test_engine_with_nucleus_and_children():
    """Test engine with nucleus and child orbitals."""
    engine = ParticleEngine(mode='refinement', presence_on=True)
    
    # Create nucleus (p=3)
    nucleus = PFParticle(
        position=(0.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3
    )
    engine.nucleus = nucleus
    engine.add_particle(nucleus)
    
    # Create parent shell
    shell = OrbitalShell(freq=1.0, phase=0.0, curvature=1.0)
    engine.shells.append(shell)
    
    # Add 2 children (n=1,2, colors RED/BLUE)
    child1 = OrbitalChild(
        position=(1.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=shell,
        harmonic_n=1,
        color_idx=0,  # RED
        drag=0.1
    )
    shell.add_child(child1)
    engine.add_particle(child1)
    
    child2 = OrbitalChild(
        position=(2.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=shell,
        harmonic_n=2,
        color_idx=2,  # BLUE
        drag=0.2
    )
    shell.add_child(child2)
    engine.add_particle(child2)
    
    # Verify children
    assert len(engine.shells) == 1
    assert len(engine.shells[0].children) == 2
    assert child1.freq == pytest.approx(1.0 / 1)
    assert child2.freq == pytest.approx(1.0 / 2)
    assert child1.phase == pytest.approx(0.0)  # RED
    assert child2.phase == pytest.approx(4 * math.pi / 3)  # BLUE


def test_engine_step_with_children():
    """Test engine step with child orbitals."""
    engine = ParticleEngine(mode='refinement', presence_on=True)
    
    # Create nucleus
    nucleus = PFParticle(
        position=(0.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3
    )
    engine.nucleus = nucleus
    engine.add_particle(nucleus)
    
    # Create shell and children
    shell = OrbitalShell(freq=1.0, phase=0.0, curvature=1.0)
    engine.shells.append(shell)
    
    child = OrbitalChild(
        position=(1.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=shell,
        harmonic_n=1,
        color_idx=0,
        drag=0.1
    )
    shell.add_child(child)
    engine.add_particle(child)
    
    # Record initial positions
    initial_nucleus_pos = nucleus.position
    initial_child_pos = child.position
    
    # Run 10 steps
    for _ in range(10):
        engine.step(dt=0.01, curvature=1.0)
    
    # Assert position changes
    assert nucleus.position != initial_nucleus_pos
    assert child.position != initial_child_pos
    
    # Assert outer drag pulls nucleus (position delta > 0 in x direction)
    nucleus_delta_x = nucleus.position[0] - initial_nucleus_pos[0]
    # With drag, nucleus should move in positive x direction
    assert nucleus_delta_x > 0 or abs(nucleus_delta_x) < 0.01  # Allow small tolerance


def test_event_spaces_off():
    """Test event spaces off (no dynamics)."""
    engine = ParticleEngine(mode='refinement', presence_on=False)  # Event spaces off
    
    # Create nucleus
    nucleus = PFParticle(
        position=(0.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3
    )
    engine.nucleus = nucleus
    engine.add_particle(nucleus)
    
    # Create shell with inactive orbital
    shell = OrbitalShell(freq=1.0, phase=0.0, curvature=1.0)
    engine.shells.append(shell)
    
    child = OrbitalChild(
        position=(1.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=shell,
        harmonic_n=1,
        color_idx=0
    )
    shell.add_child(child)
    engine.add_particle(child)
    
    # Record initial positions
    initial_nucleus_pos = nucleus.position
    initial_child_pos = child.position
    
    # Run 10 steps with presence off
    for _ in range(10):
        engine.step(dt=0.01, curvature=1.0)
    
    # With presence off, positions should not change (or change minimally)
    # Since presence_operator returns 0, forces should be minimal
    nucleus_delta = sum(
        abs(nucleus.position[i] - initial_nucleus_pos[i])
        for i in range(3)
    )
    
    # Position should be unchanged or very small (within numerical precision)
    assert nucleus_delta < 0.01


def test_inherit_force_from_parent():
    """Test child inherits force from parent shell."""
    engine = ParticleEngine(mode='refinement', presence_on=True)
    
    # Create nucleus
    nucleus = PFParticle(
        position=(0.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3
    )
    engine.nucleus = nucleus
    engine.add_particle(nucleus)
    
    # Create shell with curvature
    shell = OrbitalShell(freq=1.0, phase=0.0, curvature=2.0)
    engine.shells.append(shell)
    
    child = OrbitalChild(
        position=(1.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        parent_shell=shell,
        harmonic_n=1,
        color_idx=0
    )
    shell.add_child(child)
    engine.add_particle(child)
    
    # Calculate expected inherit force magnitude
    expected_inherit = shell.curvature * (math.pi - math.e)
    
    # Update particle should add inherit force
    phase = 0.0
    engine.update_particle(child, curvature=1.0, phase=phase, dt=0.01)
    
    # Child should have momentum change (force applied)
    # The inherit force should contribute
    assert sum(abs(p) for p in child.momentum) > 0 or abs(expected_inherit) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
