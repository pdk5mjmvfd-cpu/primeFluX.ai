"""
Concept Lattice — ApopToSiS v3

Emergent structure for semantic drift, identity shaping, and recursive learning.

This is the runtime concept lattice (separate from cognitive/concept_lattice.py).
"""

from __future__ import annotations

from typing import List, Dict, Any
from ApopToSiS.core.numpy_fallback import np


class ConceptLattice:
    """
    Concept Lattice — Runtime version.
    
    Emergent structure for semantic drift, identity shaping, and recursive learning.
    Uses naive drift for embedding updates.
    """

    def __init__(self) -> None:
        """Initialize concept lattice."""
        self.nodes: Dict[str, Any] = {}  # token -> embedding vector (list or np.ndarray)
        self.strength: Dict[str, float] = {}  # token -> reinforcement strength

    def update_from_capsule(
        self,
        tokens: List[str],
        entropy: float,
        curvature: float
    ) -> None:
        """
        Update concept embeddings using naive drift.
        
        Args:
            tokens: List of tokens from capsule
            entropy: Entropy value
            curvature: Curvature value
        """
        for token in tokens:
            if token not in self.nodes:
                # Initialize new node
                # Generate random vector (64 dimensions)
                self.nodes[token] = np.random_normal(0, 1, 64) if hasattr(np, 'random_normal') else [0.0] * 64
                self.strength[token] = 1.0
            else:
                # Update existing node with drift
                drift = (entropy + curvature * 0.1)
                # Add random drift based on PF metrics
                # Generate drift vector
                drift_vector = np.random_normal(0, drift, 64) if hasattr(np, 'random_normal') else [0.0] * 64
                self.nodes[token] = self.nodes[token] + drift_vector
                # Update strength
                self.strength[token] += 0.05 * drift

    def get_embedding(self, token: str) -> np.ndarray | None:
        """
        Get embedding for a token.
        
        Args:
            token: Token string
            
        Returns:
            Embedding vector or None if not found
        """
        return self.nodes.get(token)

    def get_strength(self, token: str) -> float:
        """
        Get reinforcement strength for a token.
        
        Args:
            token: Token string
            
        Returns:
            Strength value (0.0 if not found)
        """
        return self.strength.get(token, 0.0)

    def export(self) -> Dict[str, Any]:
        """
        Export lattice state.
        
        Returns:
            Dictionary with nodes and strength
        """
        # Handle both numpy arrays and lists
        nodes_dict = {}
        for k, v in self.nodes.items():
            if hasattr(v, 'tolist'):
                nodes_dict[k] = v.tolist()
            elif isinstance(v, (list, tuple)):
                nodes_dict[k] = list(v)
            else:
                nodes_dict[k] = v
        
        return {
            "nodes": nodes_dict,
            "strength": self.strength,
            "node_count": len(self.nodes)
        }

    def summary(self) -> Dict[str, Any]:
        """
        Get lattice summary.
        
        Returns:
            Summary dictionary
        """
        return {
            "nodes": len(self.nodes),
            "total_strength": sum(self.strength.values()),
            "avg_strength": sum(self.strength.values()) / max(1, len(self.strength))
        }

