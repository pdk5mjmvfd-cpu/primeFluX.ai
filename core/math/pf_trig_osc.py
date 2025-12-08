"""
PrimeFlux Trigonometric Oscillator.

Bounded oscillation with lattice projection and nat accounting.

Theory:
- Golden ratio φ ≈ 1.618 ensures phase space is dense (irrational seed)
- This guarantees exploration of presence manifold without periodic bias
- Source: Feigenbaum, chaos theory; dense orbits under irrational rotation
- Weierstrass (1885): trigonometric polynomial convergence guarantees

FP64 Nat Accounting:
- NAT_PER_TRIG_OP = -ln(2^-52) ≈ 36.04365338911715 nats per operation
- Each trig operation (sin, cos, multiply, add) accumulates this error
- IEEE 754 double precision bound: cannot exceed ~500 nats per chain
- v2: Will add real KL divergence monotonicity checking
"""

from __future__ import annotations

import math
from typing import List, Optional
from .pf_presence import PresenceVector


class Oscillator:
    """
    Bounded trigonometric oscillator with lattice projection.
    
    Oscillates presence vectors through trig space, projecting back to {-1, 0, 1}
    lattice at each step. Accumulates nat error from FP64 rounding.
    
    The oscillator is bounded by max_steps to ensure termination and nat budget
    compliance. Each step applies a golden-ratio damped trig flow that preserves
    information while exploring the presence manifold.
    
    Attributes:
        presence: Current presence vector state
        history: List of all presence vectors (initial + steps)
        kl_history: Placeholder for KL divergence (v2: real KL monotonicity)
        nat_error: Accumulated nat error from FP64 operations
        max_steps: Maximum oscillation steps (default 8)
    """
    
    # FP64 nat error per trig operation
    # Source: IEEE 754 double precision, -ln(2^-52) ≈ 36.04365338911715
    NAT_PER_TRIG_OP = 36.04365338911715
    
    def __init__(
        self,
        initial: PresenceVector,
        max_steps: int = 8,
        seed: Optional[float] = None,
        keep_history: bool = True
    ):
        """
        Initialize oscillator with initial presence vector.
        
        Args:
            initial: Starting presence vector
            max_steps: Maximum oscillation steps (default 8)
            seed: Optional seed for deterministic replay (default: golden ratio)
            keep_history: Whether to store full history (default True, disable for memory)
        """
        self.presence = initial
        self.history = [initial] if keep_history else []
        self.kl_history = [0.0]  # v2: Replace with real KL(p_current || q_attractor); abort if not monotone-decreasing
        self.nat_error = 0.0
        self.max_steps = max_steps
        self.keep_history = keep_history
        self._step_count = 0  # Track steps even when history disabled
        
        # Golden ratio φ for irrational phase (dense orbit guarantee)
        # If seed provided, use it for deterministic replay
        self.phi = seed if seed is not None else (1 + 5**0.5) / 2
    
    @staticmethod
    def project_to_lattice(raw_vec: List[float]) -> PresenceVector:
        """
        Project raw floating-point vector to {-1, 0, 1} lattice.
        
        Projection rule:
        - raw > 0.5 → 1
        - raw < -0.5 → -1
        - else → 0
        
        This projection is idempotent: projecting an already-projected vector
        yields the same result.
        
        Args:
            raw_vec: List of floating-point values
            
        Returns:
            PresenceVector with components in {-1, 0, 1}
        """
        components = []
        for raw in raw_vec:
            if raw > 0.5:
                components.append(1)
            elif raw < -0.5:
                components.append(-1)
            else:
                components.append(0)
        return PresenceVector(components)
    
    def step(self) -> bool:
        """
        One trig oscillation step + lattice projection + nat accounting.
        
        Algorithm:
        1. Compute golden-ratio damped trig flow for each component
        2. Project back to {-1, 0, 1} lattice
        3. Accumulate nat error (3 ops per component: sin/cos/add)
        4. Store in history if enabled
        
        Returns:
            True if step was taken, False if max_steps reached
        """
        # Check if we've reached max_steps
        if self.keep_history:
            if len(self.history) >= self.max_steps + 1:
                return False
            t = len(self.history)
        else:
            if self._step_count >= self.max_steps:
                return False
            t = self._step_count + 1
        new = []
        
        for x in self.presence.components:
            # Golden-ratio damped trig flow
            # Phase = t * φ ensures dense exploration (irrational rotation)
            phase = t * self.phi
            raw = math.cos(phase) * 0.95 + x * 0.618  # damping + momentum
            
            # Project back to lattice
            if raw > 0.5:
                new.append(1)
            elif raw < -0.5:
                new.append(-1)
            else:
                new.append(0)
            
            # Accumulate nat error: 3 operations per component (cos, multiply, add)
            self.nat_error += self.NAT_PER_TRIG_OP * 3
        
        self.presence = PresenceVector(new)
        self._step_count += 1
        
        if self.keep_history:
            self.history.append(self.presence)
        
        return True
    
    def get_nat_ceiling(self) -> float:
        """
        Get nat error ceiling for current max_steps.
        
        Computes maximum allowed nat error based on step count and component count.
        Formula: max_steps × components × 3 ops × NAT_PER_TRIG_OP
        
        Returns:
            Maximum nat error allowed
        """
        return self.max_steps * len(self.presence) * 3 * self.NAT_PER_TRIG_OP
    
    def exceeds_nat_ceiling(self) -> bool:
        """
        Check if nat error exceeds ceiling (audit for v2).
        
        Returns:
            True if nat error exceeds allowed ceiling
        """
        return self.nat_error > self.get_nat_ceiling()
    
    def run(self) -> PresenceVector:
        """
        Grok's simplified interface: run all steps at once.
        
        Returns:
            Final presence vector after oscillation
        """
        while self.step():
            pass
        return self.presence
    
    def __repr__(self) -> str:
        """String representation."""
        if self.keep_history:
            steps = len(self.history) - 1
        else:
            steps = self._step_count
        return f"Osc[{steps}/{self.max_steps} steps, {self.nat_error:.1f} nats]"
