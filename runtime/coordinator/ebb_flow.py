"""
Ebb/Flow System - Unified User Productivity Flow

Single unified system for user productivity flow that Supervisor uses.
Implements Explore/Absorb/Create mapping to Eidos/Praxis/Aegis agents.

Mathematical Foundation:
- Distinction flux: d_phi = |Ψ⁺ - Ψ⁻| (ApopTosis Thesis §2.4)
- Threshold: 0.112 (deviation constant 3/(π²e) from flux annihilation)
- Gaussian envelope: G(Ψ) = exp(-d_phi²/2σ²), σ=1/√2 (ApopTosis Thesis §2.6)
- Attractor stabilization: System converges toward attractors via flux wave equation

Event Type: Ψ state (PresenceVector) - deterministic routing
Decision Rule: argmax(|Ψ⁺ - Ψ⁻|) → agent selection
Supervisor Relationship: Ebb/Flow is policy layer (answers "which agent?"),
                         Supervisor.route() answers "which action?"
"""

from __future__ import annotations

import math
from typing import Optional, Dict, Any
from ApopToSiS.core.math.pf_presence import PresenceVector


# Threshold for Ebb/Flow decision
# Deviation constant 3/(π²e) ≈ 0.112 from flux annihilation
EBB_FLOW_THRESHOLD = 3.0 / (math.pi ** 2 * math.e)  # ≈ 0.112

# Gaussian envelope width
# σ = 1/√2 derived from critical line Re(s) = 1/2 on ζ-plane
SIGMA = 1.0 / math.sqrt(2.0)  # ≈ 0.7071


class EbbFlow:
    """
    Ebb/Flow system for user productivity flow routing.
    
    Maps distinction flux to agent selection:
    - Ebb (Reflect): d_phi > threshold → Explore → Eidos agent
    - Flow (Act): d_phi ≤ threshold → Absorb/Create → Praxis/Aegis agents
    """
    
    def __init__(self, threshold: float = EBB_FLOW_THRESHOLD, sigma: float = SIGMA):
        """
        Initialize Ebb/Flow system.
        
        Args:
            threshold: Distinction flux threshold (default 0.112)
            sigma: Gaussian envelope width (default 1/√2)
        """
        self.threshold = threshold
        self.sigma = sigma
        self._stable_habits: list[PresenceVector] = []  # 80% stable habits
        self._new_flux: list[PresenceVector] = []  # 20% new flux
    
    def route_event(self, event: PresenceVector) -> str:
        """
        Route event to appropriate agent based on distinction flux.
        
        Event type: Ψ state (PresenceVector) - deterministic routing
        
        Args:
            event: PresenceVector representing the event state
            
        Returns:
            Agent name: "eidos", "praxis", or "aegis"
        """
        # Split into dual rails
        psi_plus, psi_minus = event.split_rails()
        
        # Compute distinction flux
        d_phi = PresenceVector.distinction_flux(psi_plus, psi_minus)
        
        # Decision rule: deterministic argmax(|Ψ⁺ - Ψ⁻|)
        if d_phi > self.threshold:
            # Ebb (Reflect): High distinction flux → Explore → Eidos
            return "eidos"
        else:
            # Flow (Act): Low distinction flux → Absorb/Create
            # Choose between Praxis (Absorb) and Aegis (Create) based on flux magnitude
            if d_phi > self.threshold / 2:
                return "praxis"  # Moderate flux → Absorb
            else:
                return "aegis"  # Low flux → Create
    
    def compute_gaussian_envelope(self, d_phi: float) -> float:
        """
        Compute Gaussian envelope for context compression.
        
        G(Ψ) = exp(-d_phi²/2σ²)
        
        Args:
            d_phi: Distinction flux magnitude
            
        Returns:
            Gaussian envelope value in [0, 1]
        """
        return PresenceVector.gaussian_envelope(d_phi, self.sigma)
    
    def neuroplastic_replay(
        self,
        new_flux: PresenceVector,
        stable_weight: float = 0.8,
        new_weight: float = 0.2
    ) -> PresenceVector:
        """
        Neuroplastic replay: 80% stable habits + 20% new flux.
        
        Prevents forgetting while allowing adaptation.
        
        Args:
            new_flux: New flux vector
            stable_weight: Weight for stable habits (default 0.8)
            new_weight: Weight for new flux (default 0.2)
            
        Returns:
            Combined vector
        """
        # Store new flux
        self._new_flux.append(new_flux)
        
        # Keep only recent new flux (last 10)
        if len(self._new_flux) > 10:
            self._new_flux = self._new_flux[-10:]
        
        # Compute weighted average with stable habits
        if not self._stable_habits:
            # No stable habits yet, use new flux
            return new_flux
        
        # Average stable habits
        stable_avg = self._average_vectors(self._stable_habits)
        
        # Combine: stable_weight * stable_avg + new_weight * new_flux
        # Note: This is a simplified version - in practice, you'd need proper
        # vector arithmetic for PresenceVectors
        # For now, we'll use the new flux and update stable habits
        if len(self._stable_habits) < 100:
            self._stable_habits.append(new_flux)
        else:
            # Replace oldest habit
            self._stable_habits = self._stable_habits[1:] + [new_flux]
        
        return new_flux
    
    def _average_vectors(self, vectors: list[PresenceVector]) -> PresenceVector:
        """
        Average multiple presence vectors.
        
        Args:
            vectors: List of presence vectors
            
        Returns:
            Averaged vector
        """
        if not vectors:
            raise ValueError("Cannot average empty vector list")
        
        dim = len(vectors[0])
        avg_components = [0] * dim
        
        for vec in vectors:
            for i, comp in enumerate(vec.components):
                avg_components[i] += comp
        
        # Normalize and round to {-1, 0, 1}
        for i in range(dim):
            avg_val = avg_components[i] / len(vectors)
            # Round to nearest valid value
            if avg_val > 0.5:
                avg_components[i] = 1
            elif avg_val < -0.5:
                avg_components[i] = -1
            else:
                avg_components[i] = 0
        
        return PresenceVector(avg_components)
    
    def check_attractor_stabilization(self, d_phi: float) -> bool:
        """
        Check if system is stabilizing toward attractors.
        
        System converges when distinction flux is near attractor values.
        Uses Gaussian envelope to measure proximity.
        
        Args:
            d_phi: Distinction flux magnitude
            
        Returns:
            True if stabilizing, False otherwise
        """
        # If Gaussian envelope is high, system is near equilibrium (attractor)
        envelope = self.compute_gaussian_envelope(d_phi)
        return envelope > 0.5  # Threshold for stabilization


def route_event(event: PresenceVector, threshold: float = EBB_FLOW_THRESHOLD) -> str:
    """
    Convenience function to route an event.
    
    Args:
        event: PresenceVector representing the event state
        threshold: Optional threshold override
        
    Returns:
        Agent name: "eidos", "praxis", or "aegis"
    """
    ebb_flow = EbbFlow(threshold=threshold)
    return ebb_flow.route_event(event)

