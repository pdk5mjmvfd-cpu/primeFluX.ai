"""
QuantaCoin Core - Utility token for compressed, reversible work.

Core Concept: ΦQ = "quantum of meaningful work" — minted via PrimeFlux ops
(e.g., 𝓐(x)=exp{−β𝓥(x)} for decay-invariant scaling). Agora = colony of agents
sharing yields (Z=∏_p exp{λ_p ṡ_p} for multiplicative independence).

Incorporates:
- Minting via proof-of-compression (telemetry compression)
- Burning for transactions (partial burns with thermal salt)
- Staking for yields (EMA updates, 2-5% APY)
- Ledger compression via β-decays and Z-partitions
- PrimeFlux math: exponential epochs, Z-partition for yields, β-decays for scaling
"""

from __future__ import annotations

import json
import math
import time
import hashlib
from typing import Any, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

# Try to import PrimeFluxInt and operator_core
try:
    from fluxai.memory.polyform_int import PrimeFluxInt
    from fluxai.operator_core.polyform_ops import ReversiblePolyformOps
    POLYFORM_AVAILABLE = True
except ImportError:
    POLYFORM_AVAILABLE = False
    PrimeFluxInt = None
    ReversiblePolyformOps = None


@dataclass
class Lease:
    """Epoch lease for staked balances."""
    holder: int  # Prime number representing agent/user
    epoch: int   # Current epoch
    ttl: int     # Time-to-live in epochs
    amount: float  # Staked amount
    yield_rate: float  # APY rate (0.02-0.05)


@dataclass
class Transaction:
    """Transaction event space (composite)."""
    amount: float
    burned: float
    staked: float
    event_space: Any  # PrimeFluxInt composite
    salt: int
    timestamp: float


class QuantaCoin:
    """
    QuantaCoin (ΦQ) - Utility token for reversible work compression.
    
    Primes = agent IDs (users/families/orgs as classes via PrimeFlux duality)
    Composites = event spaces (transactions hashed into polyforms)
    Ledger compresses exponentially via β-decays and Z-partitions
    """
    
    def __init__(self, salt: int = 0):
        """
        Initialize QuantaCoin.
        
        Args:
            salt: Salt for encryption
        """
        self.salt = salt
        self.ledger: Dict[str, Any] = {}  # Polyform dict for compressed events
        self.dao_pool: float = 0.0  # Yield accumulator
        self.stakes: Dict[int, Lease] = {}  # holder_prime -> Lease
        self.transactions: list[Transaction] = []
        self.operator_core: Optional[ReversiblePolyformOps] = None
        
        if POLYFORM_AVAILABLE and ReversiblePolyformOps:
            self.operator_core = ReversiblePolyformOps(salt=salt)
    
    def mint_work(
        self,
        telemetry_data: Dict[str, Any],
        compression_ratio: float
    ) -> int:
        """
        Mint ΦQ quanta based on compression work.
        
        Uses PrimeFlux ops (pf_encode_poly from operator_core) + ZipNN Huffman
        for 33-50% savings; mint ΦQ quanta based on ratio.
        
        Args:
            telemetry_data: Telemetry data to compress
            compression_ratio: Compression ratio achieved (0.33-0.50)
            
        Returns:
            Minted quanta (e.g., quanta = floor(ratio * 1000))
        """
        if not POLYFORM_AVAILABLE or not self.operator_core:
            # Fallback: simple minting without polyform
            quanta = int(math.floor(compression_ratio * 1000))
            return quanta
        
        # Encode telemetry as polyform
        event_pfi = self.operator_core.pf_encode_poly(telemetry_data, salt=self.salt)
        
        # Calculate compression ratio
        # Original size estimate
        original_json = json.dumps(telemetry_data, sort_keys=True)
        original_size = len(original_json.encode('utf-8'))
        
        # Compressed size (from polyform payload)
        compressed_size = len(event_pfi.payload)
        
        # Actual compression ratio
        if original_size > 0:
            actual_ratio = compressed_size / original_size
        else:
            actual_ratio = compression_ratio
        
        # Mint quanta based on compression achieved
        # Formula: quanta = floor(compression_ratio * 1000)
        # Higher compression = more quanta
        quanta = int(math.floor(compression_ratio * 1000))
        
        # Store in ledger
        event_hash = hashlib.sha256(
            json.dumps(telemetry_data, sort_keys=True).encode('utf-8')
        ).hexdigest()[:16]
        
        self.ledger[event_hash] = {
            "type": "mint",
            "quanta": quanta,
            "compression_ratio": compression_ratio,
            "polyform": event_pfi.to_dict() if hasattr(event_pfi, 'to_dict') else None,
            "timestamp": time.time()
        }
        
        return quanta
    
    def burn_txn(
        self,
        amount: float,
        event_space: Any,
        salt: int
    ) -> PrimeFluxInt:
        """
        Burn quanta for transaction (partial burn).
        
        Example: $250 txn → burn $180, stake $70
        
        Args:
            amount: Total transaction amount
            event_space: PrimeFluxInt composite for event space
            salt: Thermal salt for encryption
            
        Returns:
            Burned quanta as PrimeFluxInt
        """
        # Calculate partial burn (e.g., 72% of amount)
        burn_ratio = 0.72  # 72% burn, 28% stake
        burned_amount = amount * burn_ratio
        
        # Hash to composite event using Z-partition
        # Z-partition: exp{Σ λ_p ṡ_p} for multiplicative independence
        if isinstance(event_space, PrimeFluxInt) and POLYFORM_AVAILABLE:
            # Decode event space
            event_data = self.operator_core.pf_decode_poly(event_space, mode='full')
            
            # Create burn event
            burn_event = {
                "amount": amount,
                "burned": burned_amount,
                "staked": amount - burned_amount,
                "salt": salt,
                "timestamp": time.time()
            }
            
            # Encode burn event as polyform
            burn_pfi = self.operator_core.pf_encode_poly(burn_event, salt=salt)
            
            # Store transaction
            txn = Transaction(
                amount=amount,
                burned=burned_amount,
                staked=amount - burned_amount,
                event_space=burn_pfi,
                salt=salt,
                timestamp=time.time()
            )
            self.transactions.append(txn)
            
            return burn_pfi
        else:
            # Fallback: simple burn without polyform
            burn_event = {
                "amount": amount,
                "burned": burned_amount,
                "staked": amount - burned_amount,
                "salt": salt,
                "timestamp": time.time()
            }
            
            # Create simple PrimeFluxInt if available
            if POLYFORM_AVAILABLE:
                burn_pfi = PrimeFluxInt(salt=salt)
                burn_pfi.encode(burn_event, salt=salt)
                return burn_pfi
            else:
                # Return a simple dict representation
                return burn_event
    
    def stake_balance(
        self,
        unused: float,
        holder_prime: int,
        ttl_epochs: int
    ) -> float:
        """
        Stake unused balance for yields.
        
        EMA update (m⁺=m+η(y−m)); accrue yield (2-5% APY via dao_pool fees);
        tie to legal (log USD FMV for tax).
        
        Args:
            unused: Unused balance to stake
            holder_prime: Prime number representing holder (agent/user)
            ttl_epochs: Time-to-live in epochs
            
        Returns:
            Staked amount with yield accrued
        """
        # Calculate yield rate (2-5% APY)
        base_yield = 0.02  # 2% base
        dao_bonus = min(0.03, self.dao_pool / 10000.0)  # Up to 3% bonus from DAO pool
        yield_rate = base_yield + dao_bonus
        
        # Create or update lease
        if holder_prime in self.stakes:
            lease = self.stakes[holder_prime]
            # EMA update: m⁺ = m + η(y - m)
            eta = 0.1  # Learning rate
            old_amount = lease.amount
            new_amount = old_amount + eta * (unused - old_amount)
            lease.amount = new_amount
            lease.epoch += 1
            lease.ttl = ttl_epochs
            lease.yield_rate = yield_rate
        else:
            lease = Lease(
                holder=holder_prime,
                epoch=0,
                ttl=ttl_epochs,
                amount=unused,
                yield_rate=yield_rate
            )
            self.stakes[holder_prime] = lease
        
        # Accrue yield
        # Yield = amount * yield_rate * (epochs / 365) for APY
        epochs_per_year = 365
        yield_amount = lease.amount * yield_rate * (ttl_epochs / epochs_per_year)
        
        # Update DAO pool (10% of yield goes to pool)
        pool_contribution = yield_amount * 0.1
        self.dao_pool += pool_contribution
        
        # Log USD FMV for tax (legal compliance)
        usd_fmv = unused  # Assume 1:1 for now
        self._log_tax_event(holder_prime, usd_fmv, yield_amount)
        
        return lease.amount + yield_amount
    
    def agora_yield_calc(
        self,
        prime: int,
        epoch: int
    ) -> Dict[str, Any]:
        """
        Calculate Agora yield for a prime (agent).
        
        Uses β-decay (exp{−β𝓥(x)}) for scaling.
        
        Args:
            prime: Prime number representing agent
            epoch: Current epoch
            
        Returns:
            Dictionary with yield, rewards, etc.
        """
        if prime not in self.stakes:
            return {
                "yield": 0.0,
                "rewards": [],
                "epoch": epoch
            }
        
        lease = self.stakes[prime]
        
        # β-decay for scaling: exp{−β𝓥(x)}
        beta = 0.1  # Decay parameter
        potential = lease.amount  # 𝓥(x)
        decay_factor = math.exp(-beta * potential)
        
        # Calculate yield with decay
        base_yield = lease.amount * lease.yield_rate * (lease.ttl / 365.0)
        scaled_yield = base_yield * decay_factor
        
        # Rewards (merch credits, etc.)
        rewards = []
        if scaled_yield > 10.0:
            rewards.append("merch_credits")
        if scaled_yield > 50.0:
            rewards.append("premium_access")
        
        return {
            "yield": scaled_yield,
            "rewards": rewards,
            "epoch": epoch,
            "decay_factor": decay_factor,
            "base_yield": base_yield
        }
    
    def _log_tax_event(self, holder_prime: int, usd_fmv: float, yield_amount: float):
        """
        Log USD FMV for tax compliance (W-2/1099 income).
        
        Args:
            holder_prime: Prime number representing holder
            usd_fmv: USD fair market value
            yield_amount: Yield amount
        """
        # Store tax event in ledger
        tax_event = {
            "type": "tax_log",
            "holder": holder_prime,
            "usd_fmv": usd_fmv,
            "yield": yield_amount,
            "timestamp": time.time()
        }
        
        event_hash = hashlib.sha256(
            json.dumps(tax_event, sort_keys=True).encode('utf-8')
        ).hexdigest()[:16]
        
        self.ledger[event_hash] = tax_event
    
    def get_balance(self, holder_prime: int) -> float:
        """
        Get balance for a holder.
        
        Args:
            holder_prime: Prime number representing holder
            
        Returns:
            Total balance (staked + available)
        """
        if holder_prime not in self.stakes:
            return 0.0
        
        lease = self.stakes[holder_prime]
        return lease.amount
    
    def compress_ledger(self) -> float:
        """
        Compress ledger using β-decay.
        
        Returns:
            Compression ratio achieved
        """
        # Original ledger size
        original_json = json.dumps(self.ledger, sort_keys=True)
        original_size = len(original_json.encode('utf-8'))
        
        # Apply β-decay to old transactions
        # Remove transactions older than threshold
        current_time = time.time()
        threshold = 86400 * 30  # 30 days
        
        compressed_ledger = {}
        for key, value in self.ledger.items():
            timestamp = value.get("timestamp", current_time)
            age = current_time - timestamp
            
            # β-decay: exp{−βt} - older entries decay more
            beta = 0.0001  # Decay rate
            decay_factor = math.exp(-beta * age)
            
            # Keep if recent or high importance
            if age < threshold or decay_factor > 0.5:
                compressed_ledger[key] = value
        
        # Compressed size
        compressed_json = json.dumps(compressed_ledger, sort_keys=True)
        compressed_size = len(compressed_json.encode('utf-8'))
        
        # Update ledger
        self.ledger = compressed_ledger
        
        # Calculate compression ratio
        if original_size > 0:
            ratio = compressed_size / original_size
        else:
            ratio = 1.0
        
        return ratio
    
    def __add__(self, other: Any) -> QuantaCoin:
        """
        Overload add for agent transactions.
        
        Decode primes to classes, exec burn/stake, re-encode ledger.
        
        Args:
            other: Other QuantaCoin or transaction data
            
        Returns:
            Updated QuantaCoin
        """
        # This is a simplified version - in full implementation,
        # would decode primes to agent classes and execute transactions
        if isinstance(other, dict):
            # Transaction data
            amount = other.get("amount", 0.0)
            holder_prime = other.get("holder", 2)  # Default prime
            salt = other.get("salt", self.salt)
            
            # Burn transaction
            event_space = PrimeFluxInt(salt=salt) if POLYFORM_AVAILABLE else None
            if event_space:
                event_space.encode(other, salt=salt)
            
            self.burn_txn(amount, event_space, salt)
            
            # Stake unused
            unused = amount * 0.28  # 28% unused
            self.stake_balance(unused, holder_prime, ttl_epochs=30)
        
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "salt": self.salt,
            "dao_pool": self.dao_pool,
            "stakes": {str(k): asdict(v) for k, v in self.stakes.items()},
            "ledger_size": len(self.ledger),
            "transactions_count": len(self.transactions)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> QuantaCoin:
        """Create from dictionary."""
        quanta = cls(salt=data.get("salt", 0))
        quanta.dao_pool = data.get("dao_pool", 0.0)
        
        # Restore stakes
        stakes_data = data.get("stakes", {})
        for k, v in stakes_data.items():
            prime = int(k)
            lease = Lease(**v)
            quanta.stakes[prime] = lease
        
        return quanta
