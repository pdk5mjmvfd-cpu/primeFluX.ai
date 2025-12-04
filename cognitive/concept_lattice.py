"""
Self-growing concept lattice.

Each token integrates as a node.
Edges grow by co-occurrence and PF-distance.
"""

from __future__ import annotations

from ApopToSiS.core.numpy_fallback import np
from collections import defaultdict
from typing import Any


class ConceptLattice:
    """
    Self-growing concept lattice.
    
    Each token integrates as a node.
    Edges grow by co-occurrence and PF-distance.
    """

    def __init__(self) -> None:
        """Initialize concept lattice."""
        self.nodes: dict[str, np.ndarray] = {}
        self.edges: dict[tuple[str, str], float] = defaultdict(float)
        self.node_counts: dict[str, int] = defaultdict(int)

    def integrate(self, tokens: list[str], vec: np.ndarray) -> None:
        """
        Integrate embeddings into lattice.
        
        Args:
            tokens: List of tokens
            vec: Embedding vector for these tokens
        """
        # Update nodes
        for tok in tokens:
            self.node_counts[tok] += 1
            
            if tok not in self.nodes:
                self.nodes[tok] = vec.copy()
            else:
                # Update existing node (moving average)
                self.nodes[tok] = 0.9 * self.nodes[tok] + 0.1 * vec
        
        # Connect all pairs (strengthen edges)
        for i, a in enumerate(tokens):
            for b in tokens[i+1:]:
                if a != b:
                    self.edges[(a, b)] += 0.1  # Strengthens over time
                    # Also add reverse edge
                    self.edges[(b, a)] += 0.1

        # Lattice pruning for stability
        self._prune_low_importance(max_nodes=200)

    def get_related_concepts(self, token: str, top_k: int = 5) -> list[tuple[str, float]]:
        """
        Get related concepts for a token.
        
        Args:
            token: Input token
            top_k: Number of related concepts to return
            
        Returns:
            List of (concept, strength) tuples
        """
        related = []
        for (a, b), strength in self.edges.items():
            if a == token:
                related.append((b, strength))
        
        # Sort by strength
        related.sort(key=lambda x: x[1], reverse=True)
        return related[:top_k]

    def summary(self) -> dict[str, Any]:
        """
        Get lattice summary.
        
        Returns:
            Dictionary with lattice statistics
        """
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "total_interactions": sum(self.node_counts.values()),
            "unique_concepts": len(self.node_counts),
        }

    def _prune_low_importance(self, max_nodes: int) -> None:
        """Prune least important nodes to keep lattice bounded."""
        if len(self.nodes) <= max_nodes:
            return

        # Sort nodes by usage count (ascending)
        sorted_nodes = sorted(self.node_counts.items(), key=lambda item: item[1])
        remove_count = len(self.nodes) - max_nodes
        tokens_to_remove = [token for token, _ in sorted_nodes[:remove_count]]

        for token in tokens_to_remove:
            self.nodes.pop(token, None)
            self.node_counts.pop(token, None)

        # Remove edges referencing pruned tokens
        self.edges = defaultdict(
            float,
            {
                (a, b): strength
                for (a, b), strength in self.edges.items()
                if a not in tokens_to_remove and b not in tokens_to_remove
            },
        )

