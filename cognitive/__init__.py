"""
ApopToSiS Cognitive Engine (Limited Mode).

PF-inspired proto-mind:
- PF-based embeddings
- Semantic synthesis
- Concept lattice
- Flux reinforcement
- Identity regulation
- Oscillation dynamics

No ML. Pure heuristics + PF structure.
"""

from .engine import CognitiveEngine
from .embeddings import PFEmbeddingSpace
# SemanticSynthesizer not implemented yet
# # SemanticSynthesizer not implemented yet - commented out
# from .semantics import SemanticSynthesizer
from .concept_lattice import ConceptLattice
from .flux_reinforcement import FluxReinforcement
from .identity_regulator import IdentityRegulator
from .oscillation import OscillationDynamics

__all__ = [
    "CognitiveEngine",
    "PFEmbeddingSpace",
    # "SemanticSynthesizer",  # Not implemented yet
    "ConceptLattice",
    "FluxReinforcement",
    "IdentityRegulator",
    "OscillationDynamics",
]

