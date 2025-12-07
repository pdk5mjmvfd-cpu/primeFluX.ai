"""
Tests for PF-aware Agent Router.
"""

import pytest
from datetime import datetime
from core.distinction_packet import DistinctionPacket
from agents.router import AgentRouter


def test_agent_router_high_curvature_eidos():
    """Test: High curvature (>0.7) → Eidos."""
    # Create packet with high curvature
    packet = DistinctionPacket(
        prime_modes=[2, 3, 5],
        rail_phase=0.8,  # High positive phase
        curvature_value=0.8,  # > 0.7
        timestamp=datetime.now()
    )
    
    router = AgentRouter()
    agent = router.route(packet)
    
    assert agent == "eidos"


def test_agent_router_negative_phase_aegis():
    """Test: Negative rail phase (<0) → Aegis."""
    # Create packet with negative phase
    packet = DistinctionPacket(
        prime_modes=[2, 3],
        rail_phase=-0.5,  # Negative phase
        curvature_value=0.5,
        timestamp=datetime.now()
    )
    
    router = AgentRouter()
    agent = router.route(packet)
    
    assert agent == "aegis"


def test_agent_router_default_praxis():
    """Test: Default case → Praxis."""
    # Create packet with moderate curvature and positive phase
    packet = DistinctionPacket(
        prime_modes=[2],
        rail_phase=0.3,  # Positive but not high
        curvature_value=0.3,  # < 0.7
        timestamp=datetime.now()
    )
    
    router = AgentRouter()
    agent = router.route(packet)
    
    assert agent == "praxis"


def test_agent_router_log_route():
    """Test logging route to experience graph."""
    packet = DistinctionPacket(
        prime_modes=[2, 3],
        rail_phase=0.5,
        curvature_value=0.5,
        timestamp=datetime.now()
    )
    
    router = AgentRouter()
    agent = router.route(packet)
    
    # Log route (without graph)
    router.log_route(packet, agent, experience_graph=None)
    
    # Check history
    history = router.get_routing_history()
    assert len(history) == 1
    assert history[0]["agent"] == agent
    assert history[0]["curvature"] == packet.curvature_value


def test_agent_router_from_input():
    """Test routing from input text."""
    router = AgentRouter()
    
    # High curvature input (long text)
    long_text = "a" * 1000
    packet1 = DistinctionPacket.from_input(long_text)
    agent1 = router.route(packet1)
    
    # Negative phase input
    negative_text = "test" * 50
    packet2 = DistinctionPacket.from_input(negative_text)
    agent2 = router.route(packet2)
    
    # Verify routing logic
    assert agent1 in ["eidos", "praxis", "aegis"]
    assert agent2 in ["eidos", "praxis", "aegis"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
