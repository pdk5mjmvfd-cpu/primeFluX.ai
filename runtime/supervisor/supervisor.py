"""
Supervisor — PF routing and capsule integration engine.

The Supervisor:
- Routes capsules to appropriate agents based on PF metrics
- Integrates capsules back into state
- Maintains consistency via ConsistencyEngine
- Coordinates with Experience Manager
"""

from __future__ import annotations

from typing import Any, Optional
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.core.icm import ICM
from ApopToSiS.core.lcm import LCM
from ApopToSiS.runtime.supervisor.consistency import ConsistencyEngine
from ApopToSiS.runtime.router.router import (
    compute_agent_scores,
    select_agent,
)
# CoSy and PrimeFS imports
from ApopToSiS.core.consensus import CoSyBridgeMain
from ApopToSiS.pf_json import PFJsonGenerator, PFExpander

# QuantaCoin integration (optional)
try:
    from fluxai.quanta.quanta_core import QuantaCoin
    QUANTA_AVAILABLE = True
except ImportError:
    QUANTA_AVAILABLE = False
    QuantaCoin = None

# Agora integration (optional)
try:
    from fluxai.agora.agora_core import AgoraEcosystem
    from fluxai.agora.grokepedia import GrokEpedia
    AGORA_AVAILABLE = True
except ImportError:
    AGORA_AVAILABLE = False
    AgoraEcosystem = None
    GrokEpedia = None


class Supervisor:
    """
    Supervisor — PF routing and capsule integration engine.
    
    Routes capsules to agents and integrates results back into state.
    """

    def __init__(
        self,
        icm: Optional[ICM] = None,
        lcm: Optional[LCM] = None,
        experience_manager: Any = None
    ) -> None:
        """
        Initialize Supervisor.
        
        Args:
            icm: ICM instance
            lcm: LCM instance
            experience_manager: Optional ExperienceManager instance
        """
        self.icm = icm or ICM()
        self.lcm = lcm or LCM(icm=self.icm)
        self.experience_manager = experience_manager
        self.consistency_engine = ConsistencyEngine()
        # Initialize consensus engine
        self.cosy = CoSyBridgeMain()
        self._last_capsule: Optional[Capsule] = None
        # Initialize QuantaCoin (optional)
        self.quanta_coin: Optional[QuantaCoin] = None
        if QUANTA_AVAILABLE and QuantaCoin:
            self.quanta_coin = QuantaCoin()
        # Initialize Agora Ecosystem (optional)
        self.agora: Optional[AgoraEcosystem] = None
        self.grokepedia: Optional[GrokEpedia] = None
        if AGORA_AVAILABLE and AgoraEcosystem:
            self.agora = AgoraEcosystem()
            if self.quanta_coin:
                self.agora.quanta_coin = self.quanta_coin
                self.agora.operator_core = None  # Will be set if available
            if GrokEpedia:
                self.grokepedia = GrokEpedia(
                    operator_core=None,  # Will be set if available
                    quanta_coin=self.quanta_coin
                )

    def route(
        self,
        state: PFState,
        agents: list[Any]
    ) -> Any:
        """
        Route capsule to appropriate agent based on PF metrics.
        
        Uses PF-based routing with consistency bias.
        
        Args:
            state: Current PF state
            agents: List of available agents
            
        Returns:
            Selected agent (or None if no agents)
        """
        if not agents:
            return None
        
        # Compute base agent scores
        scores = compute_agent_scores(state, agents, self.icm, self.lcm)
        
        # Apply consistency bias if we have a last capsule
        if self._last_capsule:
            consistency_metrics = self.consistency_engine.update(self._last_capsule)
            bias = consistency_metrics.get("bias_vector", 0.0)
            
            # Apply bias as soft weight (modulate scores, don't block)
            for agent in scores:
                # Slight boost for agents that align with consistency
                scores[agent] *= (1.0 + bias * 0.1)
        
        # Select best agent
        selected = select_agent(scores, agents)
        return selected

    def integrate_capsule(self, capsule: Capsule) -> None:
        """
        Integrate capsule into Supervisor state.
        
        Updates:
        - LCM state
        - ICM state
        - Experience Manager (if available)
        - Consistency Engine
        
        Args:
            capsule: Capsule to integrate
        """
        # Update LCM with capsule data
        if capsule.raw_tokens:
            self.lcm.process_tokens(capsule.raw_tokens)
        
        # Update ICM from capsule PF metrics
        self.icm.update_curvature(
            capsule.raw_tokens,
            [t for t in self.lcm.state.triplets if hasattr(t, 'a')]
        )
        self.icm.update_entropy(
            capsule.raw_tokens,
            [t for t in self.lcm.state.triplets if hasattr(t, 'a')]
        )
        
        # Update experience manager if available
        if self.experience_manager and hasattr(self.experience_manager, 'update'):
            # We need state, but we can create a minimal one
            state = PFState()
            state.update_from_capsule(capsule)
            self.experience_manager.update(capsule, state)
        
        # Update consistency engine
        self.consistency_engine.update(capsule)
        
        # Store as last capsule
        self._last_capsule = capsule

    def update_state(self, capsule: Capsule) -> PFState:
        """
        Update PF state from capsule.
        
        Args:
            capsule: Capsule to extract state from
            
        Returns:
            Updated PF state
        """
        state = PFState()
        state.update_from_capsule(capsule)
        return state

    def process_capsule(
        self,
        capsule: Capsule,
        agents: list[Any]
    ) -> dict[str, Any]:
        """
        Process capsule through full supervisor pipeline.
        
        This is a convenience method that:
        1. Routes to agent
        2. Transforms capsule
        3. Integrates capsule
        4. Returns processing result
        
        Args:
            capsule: Input capsule
            agents: List of available agents
            
        Returns:
            Processing result dictionary
        """
        # Create state from capsule
        state = PFState()
        state.update_from_capsule(capsule)
        
        # Route to agent
        selected_agent = self.route(state, agents)
        agent_sequence = []
        
        if selected_agent:
            agent_sequence.append(selected_agent.__class__.__name__)
            capsule = selected_agent.transform(capsule)
            capsule.agent_trace.append(selected_agent.__class__.__name__)
        
        # Integrate capsule
        self.integrate_capsule(capsule)
        
        # Update state again
        final_state = self.update_state(capsule)
        
        # Compute flux metrics
        flux_metrics = {
            "entropy": capsule.entropy,
            "curvature": capsule.curvature,
            "density": capsule.density,
            "psi": capsule.psi,
            "hamiltonian": capsule.hamiltonian,
        }
        
        # Quanta metrics
        quanta_minted = {
            "quanta_hash": capsule.quanta_hash,
            "compression_ratio": capsule.compression_ratio,
        }
        
        return {
            "final_capsule": capsule,
            "state": final_state,
            "agent_sequence": agent_sequence,
            "flux_metrics": flux_metrics,
            "quanta_minted": quanta_minted,
        }

    def integrate_experience(self, experience_manager: Any) -> None:
        """
        Attach experience manager to supervisor.
        
        Args:
            experience_manager: ExperienceManager instance
        """
        self.experience_manager = experience_manager
    
    def quanta_router(
        self,
        txn_data: dict[str, Any],
        salt: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Route transaction through QuantaCoin system.
        
        Detects transactions (e.g., Scheels POS: 2FA pin + thermal salt),
        routes to QuantaCoin.burn_txn, stakes via stake_balance.
        
        Args:
            txn_data: Transaction data (e.g., {"amount": 250.0, "merchant": "scheels"})
            salt: Optional thermal salt (generates if None)
            
        Returns:
            Transaction result with burn/stake details
        """
        if not QUANTA_AVAILABLE or not self.quanta_coin:
            # Fallback: return simple response
            return {
                "status": "quanta_unavailable",
                "message": "QuantaCoin not available"
            }
        
        # Generate salt if not provided
        if salt is None:
            import time
            salt = int(time.time() * 1000) % (2**32)
        
        # Extract transaction details
        amount = txn_data.get("amount", 0.0)
        merchant = txn_data.get("merchant", "unknown")
        holder_prime = txn_data.get("holder_prime", 2)  # Default prime
        
        # Create event space for transaction
        import time
        event_space_data = {
            "amount": amount,
            "merchant": merchant,
            "timestamp": time.time(),
            "salt": salt
        }
        
        # Encode event space as polyform
        try:
            from fluxai.memory.polyform_int import PrimeFluxInt
            event_space = PrimeFluxInt(salt=salt)
            event_space.encode(event_space_data, salt=salt)
        except Exception:
            event_space = None
        
        # Burn transaction (partial burn)
        burn_result = self.quanta_coin.burn_txn(amount, event_space, salt)
        
        # Calculate unused balance (28% of amount)
        unused = amount * 0.28
        
        # Stake unused balance
        staked_amount = self.quanta_coin.stake_balance(
            unused,
            holder_prime,
            ttl_epochs=30
        )
        
        # Calculate yield
        yield_info = self.quanta_coin.agora_yield_calc(holder_prime, epoch=0)
        
        return {
            "status": "success",
            "amount": amount,
            "burned": amount * 0.72,  # 72% burned
            "staked": unused,
            "staked_with_yield": staked_amount,
            "yield": yield_info,
            "merchant": merchant,
            "salt": salt,
            "holder_prime": holder_prime
        }
    
    def agora_router(
        self,
        command: str,
        data: dict[str, Any],
        agent_prime: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Route Agora commands: txn/query/mining.
        
        Routes to agora_core.process_event; burn/stake via quanta;
        agent reg for new entities.
        
        Args:
            command: Command type ("txn", "query", "mining")
            data: Command data
            agent_prime: Optional agent prime ID (auto-registered if None)
            
        Returns:
            Command result
        """
        if not AGORA_AVAILABLE or not self.agora:
            return {
                "status": "error",
                "message": "Agora ecosystem not available"
            }
        
        # Ensure operator_core is set
        if self.agora.operator_core is None:
            try:
                from fluxai.operator_core.polyform_ops import ReversiblePolyformOps
                self.agora.operator_core = ReversiblePolyformOps(salt=self.agora.salt)
            except ImportError:
                pass
        
        # Ensure GrokEpedia operator_core is set
        if self.grokepedia and self.grokepedia.operator_core is None:
            self.grokepedia.operator_core = self.agora.operator_core
        
        if command == "txn":
            # Transaction: budget 250 scheels
            amount = data.get("amount", 0.0)
            merchant = data.get("merchant", "unknown")
            
            # Register agent if needed
            if agent_prime is None:
                agent_prime = self.agora.register_agent("user")
            
            # Create event vector: x=(T,M,A,I,R,C)
            # T=timestamp, M=merchant, A=amount, I=agent, R=rewards, C=category
            import time
            event_vector = [
                time.time() % 1.0,  # T: normalized timestamp
                0.5 if merchant == "scheels" else 0.3,  # M: merchant type
                amount / 1000.0,  # A: normalized amount
                agent_prime / 100.0,  # I: normalized agent
                0.0,  # R: rewards (will be calculated)
                0.0  # C: category
            ]
            
            # Process event (π-lift encapsulation)
            event_pfi = self.agora.process_event(event_vector, agent_prime)
            
            # Burn and stake
            unused = amount * 0.28  # 28% unused
            burn_stake_result = self.agora.burn_and_stake(amount, unused, agent_prime)
            
            return {
                "status": "success",
                "command": "txn",
                "amount": amount,
                "merchant": merchant,
                "agent_prime": agent_prime,
                "event_polyform": event_pfi.to_dict() if hasattr(event_pfi, 'to_dict') else str(event_pfi),
                "burn_stake": burn_stake_result
            }
        
        elif command == "query":
            # Query: GrokEpedia
            query = data.get("query", "")
            sources = data.get("sources", None)
            
            # Register agent if needed
            if agent_prime is None:
                agent_prime = self.agora.register_agent("user")
            
            # Query GrokEpedia
            if self.grokepedia:
                result = self.grokepedia.query(query, sources, agent_prime)
                return {
                    "status": "success",
                    "command": "query",
                    "query": query,
                    "agent_prime": agent_prime,
                    "grokepedia_result": result
                }
            else:
                return {
                    "status": "error",
                    "message": "GrokEpedia not available"
                }
        
        elif command == "mining":
            # Mining: Compress telemetry logs
            telemetry_data = data.get("telemetry", {})
            
            # Register agent if needed
            if agent_prime is None:
                agent_prime = self.agora.register_agent("miner")
            
            # Create event vector for mining
            event_vector = [
                time.time() % 1.0,  # T
                0.8,  # M: mining type
                telemetry_data.get("hashrate", 0) / 1000.0,  # A: normalized hashrate
                agent_prime / 100.0,  # I
                0.0,  # R
                1.0  # C: mining category
            ]
            
            # Process event
            import time
            event_pfi = self.agora.process_event(event_vector, agent_prime)
            
            # Mint from compression
            if self.quanta_coin:
                compression_ratio = 0.50  # Target 50% compression
                quanta_minted = self.quanta_coin.mint_work(telemetry_data, compression_ratio)
            else:
                quanta_minted = 0
            
            return {
                "status": "success",
                "command": "mining",
                "agent_prime": agent_prime,
                "event_polyform": event_pfi.to_dict() if hasattr(event_pfi, 'to_dict') else str(event_pfi),
                "quanta_minted": quanta_minted
            }
        
        else:
            return {
                "status": "error",
                "message": f"Unknown agora command: {command}"
            }

