"""
Agora Core - Living colony organism of AI-agent interactions.

Agora = decentralized AI colony where transactions/interactions are event spaces
etched into a shrinking ledger. Agents (primes) represent users/families/orgs;
ledger shrinks exponentially via β-decays and Z-partitions.

Key Features:
- Agent registry: Primes as agent IDs
- Event processing: π-lift encapsulation for event vectors
- Ledger compression: β-decay (𝓐(x)=exp{−β𝓥(x)}) and Z-partitions (Z=∏_p exp{λ_p ṡ_p})
- Irrational salts: π-lift (θ_i = π/2 + 2·arctan(κ(x_i - 1/2)))
- Always-compressed: Ledger shrinks, never grows
"""

from __future__ import annotations

import json
import math
import time
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Try to import dependencies
try:
    from fluxai.memory.polyform_int import PrimeFluxInt
    from fluxai.operator_core.polyform_ops import ReversiblePolyformOps
    from fluxai.quanta.quanta_core import QuantaCoin
    POLYFORM_AVAILABLE = True
    QUANTA_AVAILABLE = True
except ImportError:
    POLYFORM_AVAILABLE = False
    QUANTA_AVAILABLE = False
    PrimeFluxInt = None
    ReversiblePolyformOps = None
    QuantaCoin = None


@dataclass
class Agent:
    """Agent in the Agora ecosystem."""
    prime_id: int
    entity_type: str  # "user", "family", "org", etc.
    registered_at: float
    metadata: Dict[str, Any]


@dataclass
class Event:
    """Event in the Agora ecosystem."""
    event_vector: List[float]  # x=(T,M,A,I,R,C) or similar
    agent_prime: int
    salt: float
    polyform: Optional[Any] = None
    timestamp: float = 0.0


class AgoraEcosystem:
    """
    Agora Ecosystem - Living, always-compressed colony organism.
    
    Agents (primes) represent users/families/orgs; composites merge via
    Galois/Diffusion duality. Ledger shrinks exponentially via β-decays.
    """
    
    def __init__(self, salt: int = 0):
        """
        Initialize Agora Ecosystem.
        
        Args:
            salt: Salt for encryption
        """
        self.salt = salt
        self.ledger_poly: Dict[str, Any] = {}  # Polyform dict for compressed events
        self.agent_registry: Dict[int, Agent] = {}  # Primes as agent IDs
        self.events: List[Event] = []
        self.operator_core: Optional[ReversiblePolyformOps] = None
        self.quanta_coin: Optional[QuantaCoin] = None
        
        # Initialize operator core and quanta coin if available
        if POLYFORM_AVAILABLE and ReversiblePolyformOps:
            self.operator_core = ReversiblePolyformOps(salt=salt)
        
        if QUANTA_AVAILABLE and QuantaCoin:
            self.quanta_coin = QuantaCoin(salt=salt)
        
        # Prime number generator for agent IDs
        self._next_prime = 2
        self._primes_cache = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
        self._prime_index = 0
    
    def _get_next_prime(self) -> int:
        """Get next prime number for agent ID."""
        if self._prime_index < len(self._primes_cache):
            prime = self._primes_cache[self._prime_index]
            self._prime_index += 1
            return prime
        
        # Generate next prime (simple algorithm)
        candidate = self._primes_cache[-1] + 2
        while True:
            is_prime = True
            for p in self._primes_cache:
                if p * p > candidate:
                    break
                if candidate % p == 0:
                    is_prime = False
                    break
            if is_prime:
                self._primes_cache.append(candidate)
                self._prime_index += 1
                return candidate
            candidate += 2
    
    def register_agent(
        self,
        entity_type: str,
        prime_id: Optional[int] = None
    ) -> int:
        """
        Register an agent in the Agora ecosystem.
        
        Assigns a prime ID (e.g., family/org as class via pf_encode_poly)
        and etches to ledger.
        
        Args:
            entity_type: Type of entity ("user", "family", "org", etc.)
            prime_id: Optional prime ID (auto-assigned if None)
            
        Returns:
            Assigned prime ID
        """
        if prime_id is None:
            prime_id = self._get_next_prime()
        
        # Create agent
        agent = Agent(
            prime_id=prime_id,
            entity_type=entity_type,
            registered_at=time.time(),
            metadata={}
        )
        
        self.agent_registry[prime_id] = agent
        
        # Encode agent as polyform and etch to ledger
        if POLYFORM_AVAILABLE and self.operator_core:
            agent_data = {
                "prime_id": prime_id,
                "entity_type": entity_type,
                "registered_at": agent.registered_at,
                "metadata": agent.metadata
            }
            
            agent_pfi = self.operator_core.pf_encode_poly(agent_data, salt=self.salt)
            
            # Store in ledger
            agent_hash = hashlib.sha256(
                f"{prime_id}_{entity_type}".encode('utf-8')
            ).hexdigest()[:16]
            
            self.ledger_poly[agent_hash] = {
                "type": "agent",
                "prime_id": prime_id,
                "entity_type": entity_type,
                "polyform": agent_pfi.to_dict() if hasattr(agent_pfi, 'to_dict') else {
                    "salt": agent_pfi.salt,
                    "payload": agent_pfi.payload
                },
                "timestamp": agent.registered_at
            }
        
        return prime_id
    
    def pi_lift(
        self,
        x: float,
        kappa: float = 1.0
    ) -> float:
        """
        π-lift: Irrational salt encapsulation.
        
        θ_i = π/2 + 2·arctan(κ(x_i - 1/2))
        
        Args:
            x: Input value (normalized to [0, 1])
            kappa: Scaling parameter
            
        Returns:
            Lifted angle θ
        """
        # Normalize x to [0, 1] if needed
        if x < 0:
            x = 0.0
        elif x > 1:
            x = 1.0
        
        # π-lift formula
        theta = math.pi / 2.0 + 2.0 * math.atan(kappa * (x - 0.5))
        return theta
    
    def process_event(
        self,
        event_vector: List[float],
        agent_prime: int,
        salt: Optional[float] = None
    ) -> PrimeFluxInt:
        """
        Process an event in the Agora ecosystem.
        
        π-lift encapsulates event window; compress via ZipNN/Galois;
        return polyform.
        
        Args:
            event_vector: Event vector x=(T,M,A,I,R,C) or similar
            agent_prime: Prime ID of agent
            salt: Optional salt (uses π if None)
            
        Returns:
            Polyform-encoded event
        """
        if salt is None:
            salt = math.pi
        
        # Verify agent exists
        if agent_prime not in self.agent_registry:
            # Auto-register if not found
            self.register_agent("unknown", prime_id=agent_prime)
        
        # π-lift encapsulate event vector
        kappa = 2.0  # Default scaling
        lifted_vector = [self.pi_lift(x, kappa) for x in event_vector]
        
        # Create event data
        event_data = {
            "event_vector": event_vector,
            "lifted_vector": lifted_vector,
            "agent_prime": agent_prime,
            "salt": salt,
            "timestamp": time.time(),
            "entity_type": self.agent_registry[agent_prime].entity_type
        }
        
        # Encode as polyform
        if POLYFORM_AVAILABLE and self.operator_core:
            event_pfi = self.operator_core.pf_encode_poly(event_data, salt=int(salt * 1000) % (2**32))
            
            # Store event
            event = Event(
                event_vector=event_vector,
                agent_prime=agent_prime,
                salt=salt,
                polyform=event_pfi,
                timestamp=time.time()
            )
            self.events.append(event)
            
            # Etch to ledger
            event_hash = hashlib.sha256(
                json.dumps(event_data, sort_keys=True).encode('utf-8')
            ).hexdigest()[:16]
            
            self.ledger_poly[event_hash] = {
                "type": "event",
                "agent_prime": agent_prime,
                "polyform": event_pfi.to_dict() if hasattr(event_pfi, 'to_dict') else {
                    "salt": event_pfi.salt,
                    "payload": event_pfi.payload
                },
                "timestamp": event.timestamp
            }
            
            return event_pfi
        else:
            # Fallback: return simple dict
            event = Event(
                event_vector=event_vector,
                agent_prime=agent_prime,
                salt=salt,
                timestamp=time.time()
            )
            self.events.append(event)
            return event_data
    
    def burn_and_stake(
        self,
        txn_amount: float,
        unused: float,
        agent_prime: int
    ) -> Dict[str, Any]:
        """
        Burn partial amount and stake leftover.
        
        Uses quanta_core.burn_txn and stake_balance with β-decay scaling.
        Yield calculated via Z-partition.
        
        Args:
            txn_amount: Total transaction amount
            unused: Unused balance to stake
            agent_prime: Prime ID of agent
            
        Returns:
            Dictionary with burn/stake/yield details
        """
        if not self.quanta_coin:
            return {
                "status": "error",
                "message": "QuantaCoin not available"
            }
        
        # Verify agent exists
        if agent_prime not in self.agent_registry:
            self.register_agent("unknown", prime_id=agent_prime)
        
        # Burn transaction (partial)
        salt = int(time.time() * 1000) % (2**32)
        event_space_data = {
            "amount": txn_amount,
            "agent_prime": agent_prime,
            "timestamp": time.time(),
            "salt": salt
        }
        
        event_space = None
        if POLYFORM_AVAILABLE:
            event_space = PrimeFluxInt(salt=salt)
            event_space.encode(event_space_data, salt=salt)
        
        burn_result = self.quanta_coin.burn_txn(txn_amount, event_space, salt)
        
        # Stake unused balance
        staked_amount = self.quanta_coin.stake_balance(unused, agent_prime, ttl_epochs=30)
        
        # Calculate yield via Z-partition
        yield_info = self.quanta_coin.agora_yield_calc(agent_prime, epoch=0)
        
        # Z-partition: Z = ∏_p exp{λ_p ṡ_p} for multiplicative independence
        # Calculate Z-partition yield
        z_partition_yield = self._calculate_z_partition_yield(agent_prime)
        
        return {
            "status": "success",
            "txn_amount": txn_amount,
            "burned": txn_amount * 0.72,  # 72% burned
            "staked": unused,
            "staked_with_yield": staked_amount,
            "yield": yield_info,
            "z_partition_yield": z_partition_yield,
            "agent_prime": agent_prime
        }
    
    def _calculate_z_partition_yield(
        self,
        agent_prime: int
    ) -> float:
        """
        Calculate yield via Z-partition: Z = ∏_p exp{λ_p ṡ_p}.
        
        Multiplicative independence across agents.
        
        Args:
            agent_prime: Prime ID of agent
            
        Returns:
            Z-partition yield
        """
        if not self.quanta_coin or agent_prime not in self.quanta_coin.stakes:
            return 0.0
        
        lease = self.quanta_coin.stakes[agent_prime]
        
        # Z-partition: Z = ∏_p exp{λ_p ṡ_p}
        # For single agent: Z = exp{λ_p · ṡ_p}
        lambda_p = lease.yield_rate  # λ_p = yield rate
        s_p = lease.amount  # ṡ_p = staked amount
        
        z_yield = math.exp(lambda_p * s_p / 1000.0)  # Normalize for stability
        
        return z_yield
    
    def compress_ledger(self) -> float:
        """
        Compress ledger via β-decay and composite merging.
        
        Merge composites (∑1/n²=π²/6 sparsity); ensure <50% size on 100 events.
        
        Returns:
            Compression ratio achieved
        """
        # Original ledger size
        original_json = json.dumps(self.ledger_poly, sort_keys=True)
        original_size = len(original_json.encode('utf-8'))
        
        # Apply β-decay to old events
        # β-decay: 𝓐(x) = exp{−β𝓥(x)} for scaling
        beta = 0.0001  # Decay parameter
        current_time = time.time()
        threshold = 86400 * 30  # 30 days
        
        compressed_ledger = {}
        for key, value in self.ledger_poly.items():
            timestamp = value.get("timestamp", current_time)
            age = current_time - timestamp
            
            # β-decay factor
            potential = age  # 𝓥(x) = age
            decay_factor = math.exp(-beta * potential)
            
            # Keep if recent or high importance (decay_factor > 0.5)
            if age < threshold or decay_factor > 0.5:
                compressed_ledger[key] = value
        
        # Merge composites using sparsity (∑1/n² = π²/6)
        # This creates natural sparsity in the ledger
        pi_squared_over_6 = (math.pi ** 2) / 6.0
        
        # Apply sparsity: keep only top N entries where N ~ sqrt(total)
        if len(compressed_ledger) > 0:
            # Sort by timestamp (most recent first)
            sorted_entries = sorted(
                compressed_ledger.items(),
                key=lambda x: x[1].get("timestamp", 0),
                reverse=True
            )
            
            # Keep top sqrt(N) entries (sparsity)
            keep_count = int(math.sqrt(len(sorted_entries)) * pi_squared_over_6)
            compressed_ledger = dict(sorted_entries[:keep_count])
        
        # Compressed size
        compressed_json = json.dumps(compressed_ledger, sort_keys=True)
        compressed_size = len(compressed_json.encode('utf-8'))
        
        # Update ledger
        self.ledger_poly = compressed_ledger
        
        # Calculate compression ratio
        if original_size > 0:
            ratio = compressed_size / original_size
        else:
            ratio = 1.0
        
        return ratio
    
    def get_agent(self, prime_id: int) -> Optional[Agent]:
        """Get agent by prime ID."""
        return self.agent_registry.get(prime_id)
    
    def list_agents(self) -> List[Agent]:
        """List all registered agents."""
        return list(self.agent_registry.values())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "salt": self.salt,
            "agent_count": len(self.agent_registry),
            "event_count": len(self.events),
            "ledger_size": len(self.ledger_poly),
            "agents": {str(k): asdict(v) for k, v in self.agent_registry.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgoraEcosystem":
        """Create from dictionary."""
        agora = cls(salt=data.get("salt", 0))
        
        # Restore agents
        agents_data = data.get("agents", {})
        for k, v in agents_data.items():
            prime_id = int(k)
            agent = Agent(**v)
            agora.agent_registry[prime_id] = agent
        
        return agora
