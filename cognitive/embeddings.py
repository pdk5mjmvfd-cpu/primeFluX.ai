"""
PF-inspired embedding space.

No ML. Pure mathematical structure.
"""

from __future__ import annotations

from ApopToSiS.core.numpy_fallback import np
from typing import Any


class PFEmbeddingSpace:
    """
    PF-inspired embedding space.
    
    No ML. Pure mathematical structure.
    Uses:
    - character ord sums
    - prime modulations
    - trig triplet oscillations
    """

    def __init__(self, dim: int = 32) -> None:
        """
        Initialize embedding space.
        
        Args:
            dim: Embedding dimension (default: 32)
        """
        self.dim = dim

    def encode(self, tokens: list[str]) -> np.ndarray:
        """
        Convert tokens → numeric vector using:
        - character ord sums
        - prime modulations
        - trig triplet oscillations
        
        Args:
            tokens: List of token strings
            
        Returns:
            Normalized embedding vector
        """
        vec = np.zeros(self.dim)
        
        for i, tok in enumerate(tokens):
            # Character ord sum
            h = sum(ord(c) for c in tok)
            # Prime modulation (97 is prime)
            vec[i % self.dim] += (h % 97) / 97.0
        
        # Normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        
        return vec

    def similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors.
        
        Args:
            vec1: First embedding vector
            vec2: Second embedding vector
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

