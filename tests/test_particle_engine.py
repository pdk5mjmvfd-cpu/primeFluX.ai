"""
Tests for Particle Engine.
"""

import pytest
import math
from core.particle_engine import (
    PFParticle,
    ParticleEngine,
    ParticleSimulator,
    BoundaryMapper
)


def test_particle_initialization():
    """Test particle initialization."""
    particle = PFParticle(
        position=(1.0, 2.0, 3.0),
        momentum=(0.1, 0.2, 0.3),
        prime=7
    )
    
    assert particle.position == (1.0, 2.0, 3.0)
    assert particle.momentum == (0.1, 0.2, 0.3)
    assert particle.prime == 7
    assert particle.energy > 0.0


def test_particle_update_position():
    """Test position update."""
    particle = PFParticle(
        position=(0.0, 0.0, 0.0),
        momentum=(1.0, 0.0, 0.0),
        prime=2,
        mass=1.0
    )
    
    initial_pos = particle.position
    particle.update_position(dt=0.1)
    
    # Position should change
    assert particle.position[0] > initial_pos[0]
    assert particle.position[0] == pytest.approx(0.1)


def test_particle_update_momentum():
    """Test momentum update."""
    particle = PFParticle(
        position=(0.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3,
        mass=1.0
    )
    
    initial_energy = particle.energy
    particle.update_momentum(force=(1.0, 0.0, 0.0), dt=0.1)
    
    # Momentum should change
    assert particle.momentum[0] > 0.0
    assert particle.momentum[0] == pytest.approx(0.1)
    
    # Energy should increase
    assert particle.energy > initial_energy


def test_particle_engine_init():
    """Test engine initialization."""
    engine = ParticleEngine(mode='refinement', presence_on=True)
    
    assert engine.mode == 'refinement'
    assert engine.presence_on is True
    assert len(engine.particles) == 0


def test_particle_engine_presence_operator():
    """Test presence operator."""
    engine = ParticleEngine(mode='research', presence_on=True)
    
    phase = math.pi / 4
    g_pf = engine.presence_operator(phase)
    
    assert g_pf == pytest.approx(math.sin(phase))
    
    # Test with presence off
    engine.presence_on = False
    g_pf_off = engine.presence_operator(phase)
    assert g_pf_off == 0.0


def test_particle_engine_add_particle():
    """Test adding particles."""
    engine = ParticleEngine()
    
    particle = PFParticle(
        position=(0.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=5
    )
    
    engine.add_particle(particle)
    assert len(engine.particles) == 1
    assert engine.particles[0].prime == 5


def test_particle_engine_step():
    """Test engine step."""
    engine = ParticleEngine(mode='refinement', presence_on=True)
    
    particle = PFParticle(
        position=(1.0, 0.0, 0.0),
        momentum=(0.0, 0.0, 0.0),
        prime=7
    )
    engine.add_particle(particle)
    
    initial_pos = particle.position
    initial_energy = engine.get_total_energy()
    
    # Step simulation
    engine.step(dt=0.01, curvature=1.0)
    
    # Position should change
    assert particle.position != initial_pos
    
    # Energy may change (force applied)
    # But should be reasonable
    final_energy = engine.get_total_energy()
    assert final_energy >= 0.0


def test_particle_simulator_run():
    """Test simulator run_simulation."""
    simulator = ParticleSimulator(mode='refinement', presence_on=True)
    
    result = simulator.run_simulation(prime=7, steps=10, dt=0.01, curvature=1.0)
    
    assert result['prime'] == 7
    assert result['steps'] == 10
    assert result['particle_count'] > 0
    assert 'initial_energy' in result
    assert 'final_energy' in result
    assert 'energy_conservation' in result


def test_particle_simulator_conservation():
    """Test energy conservation."""
    simulator = ParticleSimulator(mode='refinement', presence_on=True)
    
    result = simulator.run_simulation(prime=5, steps=100, dt=0.01, curvature=1.0)
    
    # Energy conservation should be reasonable (< 10% drift)
    assert result['energy_conservation'] < 0.1


def test_boundary_mapper():
    """Test boundary mapper."""
    mapper = BoundaryMapper(bounds=(10.0, 10.0, 10.0))
    
    particle = PFParticle(
        position=(15.0, 5.0, -12.0),
        momentum=(0.0, 0.0, 0.0),
        prime=3
    )
    
    mapped = mapper.apply_boundary(particle)
    
    # Should be within bounds
    assert -10.0 <= mapped.position[0] <= 10.0
    assert -10.0 <= mapped.position[1] <= 10.0
    assert -10.0 <= mapped.position[2] <= 10.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
