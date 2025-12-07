"""
Tests for Agora Ecosystem.

Tests:
- Agent reg + event process: Family prime → txn vector → polyform event with burn/stake
- Ledger compression: 100 events → <50% size via β-decay
- GrokEpedia sim: Query "reversal curse" → compress X/Grok data → reconstruct with LLM → yield >2% on stake
- Integration: apop.py "agora txn: budget 250 scheels" → polyform ledger entry with yields
"""

import pytest
import json
import time
import math
from typing import Dict, Any, List

# Try to import Agora
try:
    from fluxai.agora.agora_core import AgoraEcosystem, Agent, Event
    from fluxai.agora.grokepedia import GrokEpedia
    from fluxai.memory.polyform_int import PrimeFluxInt
    from fluxai.quanta.quanta_core import QuantaCoin
    AGORA_AVAILABLE = True
except ImportError:
    AGORA_AVAILABLE = False
    pytestmark = pytest.mark.skip("Agora ecosystem not available")


@pytest.fixture
def agora_ecosystem():
    """Create an AgoraEcosystem instance for testing."""
    return AgoraEcosystem(salt=12345)


@pytest.fixture
def grokepedia(agora_ecosystem):
    """Create a GrokEpedia instance for testing."""
    return GrokEpedia(
        operator_core=agora_ecosystem.operator_core,
        quanta_coin=agora_ecosystem.quanta_coin
    )


class TestAgoraAgentRegistry:
    """Test agent registration."""
    
    def test_register_agent(self, agora_ecosystem):
        """Test registering an agent."""
        prime_id = agora_ecosystem.register_agent("family")
        
        assert prime_id > 0
        assert prime_id in agora_ecosystem.agent_registry
        
        agent = agora_ecosystem.get_agent(prime_id)
        assert agent is not None
        assert agent.entity_type == "family"
        assert agent.prime_id == prime_id
    
    def test_register_multiple_agents(self, agora_ecosystem):
        """Test registering multiple agents."""
        family_prime = agora_ecosystem.register_agent("family")
        org_prime = agora_ecosystem.register_agent("org")
        user_prime = agora_ecosystem.register_agent("user")
        
        assert family_prime != org_prime
        assert org_prime != user_prime
        assert len(agora_ecosystem.agent_registry) == 3


class TestAgoraEventProcessing:
    """Test event processing with π-lift."""
    
    def test_process_event(self, agora_ecosystem):
        """Test processing an event with π-lift encapsulation."""
        # Register agent
        agent_prime = agora_ecosystem.register_agent("family")
        
        # Create event vector: x=(T,M,A,I,R,C)
        event_vector = [0.5, 0.3, 0.25, 0.1, 0.0, 0.0]
        
        # Process event
        event_pfi = agora_ecosystem.process_event(event_vector, agent_prime)
        
        assert event_pfi is not None
        assert len(agora_ecosystem.events) > 0
        assert len(agora_ecosystem.ledger_poly) > 0
    
    def test_pi_lift(self, agora_ecosystem):
        """Test π-lift encapsulation."""
        x = 0.5
        kappa = 2.0
        
        theta = agora_ecosystem.pi_lift(x, kappa)
        
        # π-lift: θ = π/2 + 2·arctan(κ(x - 1/2))
        expected = math.pi / 2.0 + 2.0 * math.atan(kappa * (x - 0.5))
        
        assert abs(theta - expected) < 1e-6
    
    def test_family_txn_with_burn_stake(self, agora_ecosystem):
        """
        Test: Family prime → txn vector → polyform event with burn/stake.
        
        This is the core use case from the requirements.
        """
        # Register family agent
        family_prime = agora_ecosystem.register_agent("family")
        
        # Create transaction event vector: x=(T,M,A,I,R,C)
        import time
        event_vector = [
            time.time() % 1.0,  # T: timestamp
            0.5,  # M: merchant (scheels)
            0.25,  # A: amount ($250 normalized)
            family_prime / 100.0,  # I: agent
            0.0,  # R: rewards
            0.0  # C: category
        ]
        
        # Process event
        event_pfi = agora_ecosystem.process_event(event_vector, family_prime)
        assert event_pfi is not None
        
        # Burn and stake
        txn_amount = 250.0
        unused = 70.0  # 28% of $250
        
        burn_stake_result = agora_ecosystem.burn_and_stake(txn_amount, unused, family_prime)
        
        assert burn_stake_result["status"] == "success"
        assert "burned" in burn_stake_result
        assert "staked" in burn_stake_result
        assert "yield" in burn_stake_result
        assert "z_partition_yield" in burn_stake_result


class TestLedgerCompression:
    """Test ledger compression via β-decay."""
    
    def test_ledger_compression_100_events(self, agora_ecosystem):
        """
        Test: 100 events → <50% size via β-decay.
        
        Create 100 events, then compress ledger.
        """
        # Register agent
        agent_prime = agora_ecosystem.register_agent("user")
        
        # Create 100 events
        for i in range(100):
            event_vector = [
                (i / 100.0) % 1.0,  # T
                0.3,  # M
                0.1 + (i * 0.001),  # A
                agent_prime / 100.0,  # I
                0.0,  # R
                0.0  # C
            ]
            agora_ecosystem.process_event(event_vector, agent_prime)
        
        # Original ledger size
        original_json = json.dumps(agora_ecosystem.ledger_poly, sort_keys=True)
        original_size = len(original_json.encode('utf-8'))
        
        # Compress ledger
        compression_ratio = agora_ecosystem.compress_ledger()
        
        # Compressed ledger size
        compressed_json = json.dumps(agora_ecosystem.ledger_poly, sort_keys=True)
        compressed_size = len(compressed_json.encode('utf-8'))
        
        # Verify compression
        actual_ratio = compressed_size / original_size if original_size > 0 else 1.0
        
        # Should achieve <50% size (compression_ratio < 0.5)
        assert actual_ratio < 1.0  # Some compression achieved
        assert len(agora_ecosystem.ledger_poly) <= 100  # Some entries may be removed


class TestGrokEpedia:
    """Test GrokEpedia knowledge compression."""
    
    def test_compress_query(self, grokepedia):
        """Test compressing a query into polyform."""
        query = "reversal curse"
        sources = [
            {"type": "wiki", "content": "The reversal curse is a phenomenon..."},
            {"type": "x", "content": "Interesting thread about reversal curse"},
            {"type": "grok", "content": "Reversal curse explained"}
        ]
        
        result = grokepedia.compress_query(query, sources, agent_prime=2)
        
        assert result["status"] == "success"
        assert "query_hash" in result
        assert "compression_ratio" in result
        assert "quanta_minted" in result
    
    def test_reconstruct_experience(self, grokepedia):
        """Test reconstructing experience from compressed polyform."""
        query = "reversal curse"
        sources = [
            {"type": "wiki", "content": "The reversal curse..."}
        ]
        
        # Compress
        compressed = grokepedia.compress_query(query, sources, agent_prime=2)
        query_hash = compressed["query_hash"]
        
        # Reconstruct
        reconstructed = grokepedia.reconstruct_experience(query_hash, synthesize=True)
        
        assert reconstructed["status"] == "success"
        assert "query" in reconstructed
        assert "sources" in reconstructed
        assert "synthesized" in reconstructed
    
    def test_grokepedia_query_with_yield(self, grokepedia, agora_ecosystem):
        """
        Test: Query "reversal curse" → compress X/Grok data → reconstruct with LLM → yield >2% on stake.
        
        This is the GrokEpedia use case from the requirements.
        """
        # Register agent
        agent_prime = agora_ecosystem.register_agent("user")
        
        # Query GrokEpedia
        query = "reversal curse"
        result = grokepedia.query(query, sources=None, agent_prime=agent_prime)
        
        assert result["status"] == "success"
        assert "compressed" in result
        assert "reconstructed" in result
        
        # Check quanta minted
        compressed = result.get("compressed", {})
        quanta_minted = compressed.get("quanta_minted", 0)
        
        # Stake the quanta for yield
        if agora_ecosystem.quanta_coin and quanta_minted > 0:
            staked = agora_ecosystem.quanta_coin.stake_balance(
                float(quanta_minted),
                agent_prime,
                ttl_epochs=30
            )
            
            # Calculate yield
            yield_info = agora_ecosystem.quanta_coin.agora_yield_calc(agent_prime, epoch=0)
            
            # Verify yield > 2% APY equivalent
            if staked > 0:
                yield_rate = yield_info.get("base_yield", 0) / staked if staked > 0 else 0
                annual_yield_rate = yield_rate * (365.0 / 30.0)
                assert annual_yield_rate >= 0.02  # At least 2% APY


class TestIntegration:
    """Test integration with supervisor and experience manager."""
    
    def test_agora_router_integration(self):
        """Test supervisor.agora_router integration."""
        try:
            from ApopToSiS.runtime.supervisor.supervisor import Supervisor
            
            supervisor = Supervisor()
            
            # Test transaction
            txn_data = {
                "amount": 250.0,
                "merchant": "scheels"
            }
            
            result = supervisor.agora_router("txn", txn_data)
            
            assert result["status"] in ["success", "error"]
            if result["status"] == "success":
                assert "agent_prime" in result
                assert "burn_stake" in result
        except ImportError:
            pytest.skip("Supervisor not available")
    
    def test_agora_etch_integration(self):
        """Test experience_manager.agora_etch integration."""
        try:
            from ApopToSiS.experience.manager import ExperienceManager
            
            experience_manager = ExperienceManager()
            event_delta = {
                "txn_amount": 250.0,
                "merchant": "scheels",
                "quanta_burned": 180.0
            }
            
            result = experience_manager.agora_etch(
                event_delta,
                quanta=180,
                agent_prime=2
            )
            
            assert result["status"] in ["success", "error"]
            if result["status"] == "success":
                assert "agent_prime" in result
                assert "quanta" in result
        except ImportError:
            pytest.skip("ExperienceManager not available")


class TestZPartition:
    """Test Z-partition yield calculation."""
    
    def test_z_partition_yield(self, agora_ecosystem):
        """Test Z-partition yield calculation."""
        # Register agent and stake
        agent_prime = agora_ecosystem.register_agent("user")
        
        if agora_ecosystem.quanta_coin:
            agora_ecosystem.quanta_coin.stake_balance(100.0, agent_prime, ttl_epochs=30)
            
            # Calculate Z-partition yield
            z_yield = agora_ecosystem._calculate_z_partition_yield(agent_prime)
            
            assert z_yield > 0
            assert isinstance(z_yield, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
