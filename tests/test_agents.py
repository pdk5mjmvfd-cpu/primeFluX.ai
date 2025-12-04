"""
Test Agents — Trinity agent tests.

Tests:
- Each agent returns a correct capsule
- Structural integrity
- Flux and entropy signatures
"""

import pytest
import time
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent
from ApopToSiS.runtime.capsules import Capsule


def test_agent_transforms():
    """Test each agent transforms capsules correctly."""
    capsule = Capsule(
        raw_tokens=["alpha"],
        triplets=[],
        entropy=0.1,
        curvature=0.2,
        shell=0,
        density=0.05,
        psi=0.7,
        hamiltonian=0.9,
        reptend_entropy=0.1,
        rail_interference=0.0,
        timestamp=time.time()
    )
    
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    for agent in agents:
        out = agent.transform(capsule)
        assert isinstance(out, Capsule)
        assert out.raw_tokens is not None


def test_agent_flux_signatures():
    """Test agent flux signatures."""
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    for agent in agents:
        flux_sig = agent.flux_signature()
        assert isinstance(flux_sig, dict)
        assert "type" in flux_sig or "amplitude" in flux_sig


def test_agent_entropy_signatures():
    """Test agent entropy signatures."""
    agents = [EidosAgent(), PraxisAgent(), AegisAgent()]
    
    for agent in agents:
        entropy_sig = agent.entropy_signature()
        assert isinstance(entropy_sig, dict)
        assert "type" in entropy_sig or "entropy_range" in entropy_sig


def test_eidos_expansion():
    """Test Eidos agent expands entropy."""
    capsule = Capsule(
        raw_tokens=["test"],
        entropy=0.5,
        curvature=1.0,
        shell=2,
        timestamp=time.time()
    )
    
    eidos = EidosAgent()
    transformed = eidos.transform(capsule)
    
    # Eidos should increase entropy
    assert transformed.entropy >= capsule.entropy or transformed.entropy_snapshot >= capsule.entropy_snapshot


def test_aegis_collapse():
    """Test Aegis agent collapses entropy."""
    capsule = Capsule(
        raw_tokens=["test"],
        entropy=1.5,
        curvature=1.5,
        shell=3,
        timestamp=time.time()
    )
    
    aegis = AegisAgent()
    transformed = aegis.transform(capsule)
    
    # Aegis should decrease entropy
    assert transformed.entropy <= capsule.entropy or transformed.entropy_snapshot <= capsule.entropy_snapshot
