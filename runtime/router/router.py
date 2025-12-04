"""
Router — PF-based agent selection.

Full routing mathematics using:
- curvature-based routing
- entropy-based routing
- dual-rail interference routing
- distinction density routing
- flux amplitude routing
- triplet-oscillation routing
- PF Hamiltonian collapse routing
- superposition-based routing
- QuantaCoin entropy-drop routing
"""

from __future__ import annotations

from typing import Any
import math
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.icm import ICM
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.math.shells import Shell, shell_curvature
from ApopToSiS.core.math.hamiltonians import hamiltonian, collapse_energy
from ApopToSiS.core.math.lattice import rail_interaction
from ApopToSiS.core.math.superposition import shell_from_superposition
from ApopToSiS.core.math.quanta_math import compression_ratio
# TrigTriplet not needed for routing


def compute_agent_scores(
    state: PFState,
    agents: list[Any],
    icm: ICM,
    lcm: LCM
) -> dict[Any, float]:
    """
    Compute scores for each agent based on PF metrics.
    
    Uses weighted sum:
    score(agent) = w1*curvature + w2*entropy + w3*density + w4*flux +
                  w5*rail + w6*triplet_osc + w7*hamiltonian + w8*psi + w9*quanta

    Args:
        state: Current PF state
        agents: List of agents
        icm: ICM instance
        lcm: LCM instance

    Returns:
        Dictionary mapping agents to scores
    """
    scores = {}
    
    # Get PF metrics
    curvature = state.curvature
    entropy = state.entropy
    density = state.density
    psi = state.psi
    H = state.hamiltonian
    
    # Compute distinction density
    distinction_density = icm.distinction_density()
    
    # Compute flux amplitude (from distinction chain)
    flux_amplitude = 0.0
    if lcm.state.distinction_chain:
        last_event = lcm.state.distinction_chain[-1]
        flux_amplitude = abs(last_event.get("curvature_after", 0.0) - last_event.get("curvature_before", 0.0))
    
    # Compute triplet oscillation
    triplet_oscillation = _compute_triplet_oscillation(lcm)
    
    # Compute rail interference (from combinatoric triplets)
    rail_interference = _compute_rail_interference(lcm)
    
    # Compute QuantaCoin compression
    quanta_compression = _compute_quanta_compression(lcm)
    
    # Weights
    w1, w2, w3, w4 = 0.25, 0.15, 0.10, 0.10
    w5, w6, w7, w8, w9 = 0.05, 0.10, 0.15, 0.05, 0.05
    
    for agent in agents:
        base_score = 0.0
        
        # 1. Curvature-based routing
        curvature_term = _curvature_routing_term(curvature, agent)
        base_score += w1 * curvature_term
        
        # 2. Entropy-based routing
        entropy_term = _entropy_routing_term(entropy, agent)
        base_score += w2 * entropy_term
        
        # 3. Distinction density routing
        density_term = _density_routing_term(density, distinction_density, agent)
        base_score += w3 * density_term
        
        # 4. Flux amplitude routing
        flux_term = _flux_routing_term(flux_amplitude, agent)
        base_score += w4 * flux_term
        
        # 5. Dual-rail interference routing
        rail_term = _rail_routing_term(rail_interference, agent)
        base_score += w5 * rail_term
        
        # 6. Triplet-oscillation routing
        triplet_term = _triplet_oscillation_term(triplet_oscillation, agent)
        base_score += w6 * triplet_term
        
        # 7. PF Hamiltonian collapse routing
        hamiltonian_term = _hamiltonian_routing_term(H, agent)
        base_score += w7 * hamiltonian_term
        
        # 8. Superposition-based routing
        psi_term = _superposition_routing_term(psi, agent)
        base_score += w8 * psi_term
        
        # 9. QuantaCoin entropy-drop routing
        quanta_term = _quanta_routing_term(quanta_compression, agent)
        base_score += w9 * quanta_term
        
        # Agent-specific adjustments from flux/entropy signatures
        if hasattr(agent, 'flux_signature'):
            flux_sig = agent.flux_signature()
            base_score += abs(flux_sig.get('amplitude', 0.0)) * 0.1
        
        if hasattr(agent, 'entropy_signature'):
            entropy_sig = agent.entropy_signature()
            entropy_range = entropy_sig.get('entropy_range', (0.0, 1.0))
            if entropy_range[0] <= entropy <= entropy_range[1]:
                base_score += 0.2
        
        # Experience factor (from experience layer if available)
        experience_factor = 0.0
        if hasattr(lcm, 'experience_manager') and lcm.experience_manager:
            experience_factor = lcm.experience_manager.get_experience_factor()
            base_score += 0.10 * experience_factor  # w_exp = 0.10
        
        scores[agent] = base_score
    
    return scores


def _curvature_routing_term(curvature: float, agent: Any) -> float:
    """
    Curvature-based routing term.
    
    Higher curvature → needs Praxis
    Low curvature → Aegis
    Chaotic curvature → Eidos
    
    Args:
        curvature: Current curvature
        agent: Agent
        
    Returns:
        Routing term
    """
    SQRT2 = math.sqrt(2)
    PHI = (1 + math.sqrt(5)) / 2
    PI = math.pi
    
    kappa2 = SQRT2  # Shell 2
    kappa3 = PI / PHI  # Shell 3
    
    agent_type = _get_agent_type(agent)
    
    if curvature < kappa2:
        # Low curvature → Aegis
        return 1.0 if agent_type == "aegis" else 0.3
    elif curvature < kappa3:
        # Medium curvature → Eidos
        return 1.0 if agent_type == "eidos" else 0.5
    else:
        # High curvature → Praxis
        return 1.0 if agent_type == "praxis" else 0.3


def _entropy_routing_term(entropy: float, agent: Any) -> float:
    """
    Entropy-based routing term.
    
    High entropy → Eidos
    Medium entropy → Praxis
    Low entropy → Aegis
    
    Args:
        entropy: Current entropy
        agent: Agent
        
    Returns:
        Routing term
    """
    agent_type = _get_agent_type(agent)
    
    if entropy > 1.5:
        # High entropy → Eidos
        return 1.0 if agent_type == "eidos" else 0.3
    elif entropy > 0.8:
        # Medium entropy → Praxis
        return 1.0 if agent_type == "praxis" else 0.5
    else:
        # Low entropy → Aegis
        return 1.0 if agent_type == "aegis" else 0.3


def _density_routing_term(density: float, distinction_density: float, agent: Any) -> float:
    """
    Distinction density routing term.
    
    Density rising → Praxis
    Density falling → Aegis
    Density spike → Eidos
    
    Args:
        density: Current density
        distinction_density: Distinction density
        agent: Agent
        
    Returns:
        Routing term
    """
    agent_type = _get_agent_type(agent)
    
    # Use distinction density trend
    if distinction_density > 0.5:
        # High density → Praxis
        return 1.0 if agent_type == "praxis" else 0.4
    elif distinction_density < 0.2:
        # Low density → Aegis
        return 1.0 if agent_type == "aegis" else 0.4
    else:
        # Medium density → Eidos
        return 1.0 if agent_type == "eidos" else 0.5


def _flux_routing_term(flux_amplitude: float, agent: Any) -> float:
    """
    Flux amplitude routing term.
    
    High flux → Praxis
    Low flux → Aegis
    Oscillatory flux → Eidos
    
    Args:
        flux_amplitude: Flux amplitude
        agent: Agent
        
    Returns:
        Routing term
    """
    agent_type = _get_agent_type(agent)
    
    if flux_amplitude > 0.5:
        # High flux → Praxis
        return 1.0 if agent_type == "praxis" else 0.3
    elif flux_amplitude < 0.1:
        # Low flux → Aegis
        return 1.0 if agent_type == "aegis" else 0.3
    else:
        # Medium flux → Eidos
        return 1.0 if agent_type == "eidos" else 0.5


def _rail_routing_term(rail_interference: float, agent: Any) -> float:
    """
    Dual-rail interference routing term.
    
    Different rails → boost Eidos
    Same rail → boost Aegis
    
    Args:
        rail_interference: Rail interference value
        agent: Agent
        
    Returns:
        Routing term
    """
    agent_type = _get_agent_type(agent)
    
    if rail_interference > 0.5:
        # High interference → Eidos
        return 0.3 if agent_type == "eidos" else 0.1
    else:
        # Low interference → Aegis
        return 0.2 if agent_type == "aegis" else 0.1


def _triplet_oscillation_term(triplet_oscillation: float, agent: Any) -> float:
    """
    Triplet-oscillation routing term.
    
    sin ↔ cos → curvature neutral → Praxis
    tan → curvature unstable → Eidos
    1-state or 2-state dual → Aegis
    
    Args:
        triplet_oscillation: Triplet oscillation value
        agent: Agent
        
    Returns:
        Routing term
    """
    agent_type = _get_agent_type(agent)
    
    if triplet_oscillation > 0.5:
        # High oscillation → Eidos
        return 1.0 if agent_type == "eidos" else 0.3
    elif triplet_oscillation < 0.2:
        # Low oscillation → Aegis
        return 1.0 if agent_type == "aegis" else 0.3
    else:
        # Medium oscillation → Praxis
        return 1.0 if agent_type == "praxis" else 0.5


def _hamiltonian_routing_term(H: float, agent: Any) -> float:
    """
    PF Hamiltonian collapse routing term.
    
    If H > φ² → collapse → Aegis
    After collapse → reset → Eidos
    
    Args:
        H: Hamiltonian value
        agent: Agent
        
    Returns:
        Routing term
    """
    PHI = (1 + math.sqrt(5)) / 2
    collapse_threshold = PHI ** 2
    
    agent_type = _get_agent_type(agent)
    
    if H > collapse_threshold:
        # Collapse → Aegis
        return 1.5 if agent_type == "aegis" else 0.2
    else:
        # Normal routing
        return 0.5


def _superposition_routing_term(psi: float, agent: Any) -> float:
    """
    Superposition-based routing term.
    
    |ψ| < 0.6 → Eidos
    |ψ| ≈ 1 → Praxis
    |ψ| > 1.3 → Aegis
    
    Args:
        psi: Superposition magnitude
        agent: Agent
        
    Returns:
        Routing term
    """
    agent_type = _get_agent_type(agent)
    
    if psi < 0.6:
        # Low superposition → Eidos
        return 1.0 if agent_type == "eidos" else 0.3
    elif 0.8 <= psi <= 1.2:
        # Stable superposition → Praxis
        return 1.0 if agent_type == "praxis" else 0.5
    else:
        # High superposition → Aegis
        return 1.0 if agent_type == "aegis" else 0.3


def _quanta_routing_term(quanta_compression: float, agent: Any) -> float:
    """
    QuantaCoin entropy-drop routing term.
    
    Compression rate increases → Praxis
    Compression rate decreases → Eidos
    
    Args:
        quanta_compression: Compression ratio
        agent: Agent
        
    Returns:
        Routing term
    """
    agent_type = _get_agent_type(agent)
    
    if quanta_compression > 1.2:
        # High compression → Praxis
        return 0.3 if agent_type == "praxis" else 0.1
    elif quanta_compression < 0.8:
        # Low compression → Eidos
        return 0.3 if agent_type == "eidos" else 0.1
    else:
        return 0.1


def _compute_triplet_oscillation(lcm: LCM) -> float:
    """
    Compute triplet oscillation.
    
    Args:
        lcm: LCM instance
        
    Returns:
        Oscillation value
    """
    if not lcm.state.triplets:
        return 0.0
    
    # Get last 5 triplets
    recent_triplets = lcm.state.triplets[-5:]
    
    if len(recent_triplets) < 2:
        return 0.0
    
    # Compute variance in triplet values
    values = []
    for triplet in recent_triplets:
        values.append(triplet.a + triplet.b + triplet.c)
    
    if len(values) < 2:
        return 0.0
    
    mean_val = sum(values) / len(values)
    variance = sum((v - mean_val) ** 2 for v in values) / len(values)
    
    return math.sqrt(variance)


def _compute_rail_interference(lcm: LCM) -> float:
    """
    Compute rail interference from combinatoric triplets.
    
    Args:
        lcm: LCM instance
        
    Returns:
        Rail interference value
    """
    if not lcm.state.triplets:
        return 0.0
    
    total_interference = 0.0
    count = 0
    
    for triplet in lcm.state.triplets:
        if triplet.triplet_type.value == "combinatoric":
            p = int(triplet.a)
            q = int(triplet.c)
            interference = rail_interaction(p, q)
            total_interference += interference
            count += 1
    
    return total_interference / count if count > 0 else 0.0


def _compute_quanta_compression(lcm: LCM) -> float:
    """
    Compute QuantaCoin compression from entropy history.
    
    Args:
        lcm: LCM instance
        
    Returns:
        Compression ratio
    """
    if len(lcm.state.entropy_history) < 2:
        return 1.0
    
    # Compute compression from entropy reduction
    entropy_before = lcm.state.entropy_history[-2]
    entropy_after = lcm.state.entropy_history[-1]
    
    if entropy_after == 0:
        return 1.0
    
    return entropy_before / entropy_after


def _get_agent_type(agent: Any) -> str:
    """
    Get agent type from agent instance.
    
    Args:
        agent: Agent instance
        
    Returns:
        Agent type string
    """
    if hasattr(agent, 'flux_signature'):
        sig = agent.flux_signature()
        return sig.get('type', 'unknown')
    
    # Fallback to class name
    class_name = agent.__class__.__name__.lower()
    if 'eidos' in class_name:
        return "eidos"
    elif 'praxis' in class_name:
        return "praxis"
    elif 'aegis' in class_name:
        return "aegis"
    
    return "unknown"


def select_agent(scores: dict[Any, float], agents: list[Any]) -> Any:
    """
    Select the best agent based on scores.

    Args:
        scores: Dictionary of agent scores
        agents: List of agents

    Returns:
        Selected agent
    """
    if not scores:
        return agents[0] if agents else None
    
    # Select agent with highest score
    best_agent = max(scores.items(), key=lambda x: x[1])[0]
    return best_agent


def compute_flux_interference(agent_outputs: list[dict[str, Any]]) -> float:
    """
    Compute flux interference between agent outputs.
    
    Disagreement = flux amplitude, which drives routing.
    Disagreement is NOT conflict - it's informational potential.

    Args:
        agent_outputs: List of agent output dictionaries

    Returns:
        Flux interference measure (amplitude)
    """
    if len(agent_outputs) < 2:
        return 0.0
    
    # Compute variance in outputs as flux amplitude
    entropies = [out.get('entropy', 0.0) for out in agent_outputs]
    curvatures = [out.get('curvature', 0.0) for out in agent_outputs]
    flux_amplitudes = [out.get('flux_amplitude', 0.0) for out in agent_outputs]
    
    if not entropies:
        return 0.0
    
    # Variance in entropy
    mean_entropy = sum(entropies) / len(entropies)
    entropy_variance = sum((e - mean_entropy) ** 2 for e in entropies) / len(entropies)
    
    # Variance in curvature
    mean_curvature = sum(curvatures) / len(curvatures) if curvatures else 0.0
    curvature_variance = sum((c - mean_curvature) ** 2 for c in curvatures) / len(curvatures) if curvatures else 0.0
    
    # Flux amplitude = combination of variances
    flux_amplitude = math.sqrt(entropy_variance + curvature_variance)
    
    return flux_amplitude
