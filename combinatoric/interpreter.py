"""
Combinatoric Interpreter Layer (CIL).

Converts ANY textual input into PF primitives by extracting combinatoric patterns,
not semantic meanings. This makes Apop language-agnostic.

The CIL sits ABOVE raw strings and BELOW LCM's PF-distinction computations.
"""

from __future__ import annotations

import re
import math
from dataclasses import dataclass, field
from typing import Any
from collections import Counter
from ApopToSiS.core.pf_core import PFShell
from ApopToSiS.core.triplets import TripletType


@dataclass
class CombinatoricDistinctionPacket:
    """
    Packet containing combinatoric patterns extracted from input.
    
    This is what LCM ingests - language-agnostic distinction events.
    """
    raw: str
    tokens: list[str] = field(default_factory=list)
    adjacency_pairs: list[tuple[str, str]] = field(default_factory=list)
    triplets: list[tuple[str, str, str]] = field(default_factory=list)
    shell_suggestions: list[int] = field(default_factory=list)  # 0, 2, 3, 4
    error_deltas: list[float] = field(default_factory=list)
    curvature_deltas: list[float] = field(default_factory=list)
    entropy_delta: float = 0.0
    collapse_points: list[int] = field(default_factory=list)  # Token indices
    metadata: dict[str, Any] = field(default_factory=dict)


class CombinatoricInterpreter:
    """
    Language-agnostic combinatoric pattern extractor.
    
    Extracts:
    - Adjacency pairs
    - Triads (triplets)
    - Repetitions
    - Contrast markers
    - Branching markers
    - Recursion/loop markers
    - Assignment/collapse markers
    - Presence anchors
    """

    # Contrast markers (measurement/duality)
    CONTRAST_PATTERNS = [
        r'\b(but|vs|versus|versus|!=|<>|≠|else|otherwise|difference|diff|contrast)\b',
        r'[!=<>≠]',  # Operators
        r'\b(not|no|without|except)\b',
    ]

    # Branching markers (flux)
    BRANCHING_PATTERNS = [
        r'\b(if|or|match|switch|case|when|then)\b',
        r'[?|&]',  # Conditional operators
        r'\b(choose|select|pick)\b',
    ]

    # Recursion/loop markers (curvature)
    RECURSION_PATTERNS = [
        r'\b(for|while|loop|repeat|recurse|recursive|iterate)\b',
        r'[{}]',  # Braces often indicate loops/blocks
        r'\b(call|invoke|apply)\b',
    ]
    
    def _detect_self_recursion(self, tokens: list[str]) -> list[int]:
        """
        Detect self-recursion (function calling itself).
        
        Args:
            tokens: List of tokens
            
        Returns:
            List of token indices where self-recursion occurs
        """
        recursion_indices = []
        
        # Look for function definition followed by same name in body
        for i in range(len(tokens) - 1):
            # Check for "def name" pattern
            if tokens[i] == "def" and i + 1 < len(tokens):
                func_name = tokens[i + 1].split("(")[0]  # Extract function name
                
                # Look for same name later (self-call)
                for j in range(i + 2, len(tokens)):
                    if tokens[j] == func_name or tokens[j].startswith(func_name + "("):
                        recursion_indices.append(j)
        
        return recursion_indices

    # Assignment/collapse markers (Shell 4)
    COLLAPSE_PATTERNS = [
        r'[=:]',  # Assignment
        r'\b(return|yield|result|output|final|conclude|therefore)\b',
        r'\.',  # Period (conclusion)
        r'\b(end|finish|complete|done)\b',
    ]

    # Presence anchors (Shell 0)
    PRESENCE_PATTERNS = [
        r'\b(I|main|this|here|now|current|present|exists)\b',
        r'\b(create|new|init|start|begin)\b',
        r'^',  # Start of input
    ]

    def interpret(self, text: str) -> CombinatoricDistinctionPacket:
        """
        Interpret any string input into combinatoric patterns.

        Args:
            text: Input text (any language)

        Returns:
            CombinatoricDistinctionPacket with extracted patterns
        """
        # 1. Structural tokenization
        tokens = self._tokenize(text)
        
        # 2. Extract combinatoric patterns
        adjacency_pairs = self._extract_adjacency_pairs(tokens)
        triplets = self._extract_triplets(tokens)
        repetitions = self._extract_repetitions(tokens)
        
        # 3. Extract structural markers
        contrast_markers = self._extract_markers(text, self.CONTRAST_PATTERNS)
        branching_markers = self._extract_markers(text, self.BRANCHING_PATTERNS)
        recursion_markers = self._extract_markers(text, self.RECURSION_PATTERNS)
        
        # Also detect self-recursion (function calling itself)
        self_recursion_indices = self._detect_self_recursion(tokens)
        for idx in self_recursion_indices:
            # Add to recursion markers
            current_pos = sum(len(tokens[i]) for i in range(min(idx, len(tokens))))
            recursion_markers.append((current_pos, "self_recursion"))
        
        collapse_markers = self._extract_markers(text, self.COLLAPSE_PATTERNS)
        presence_markers = self._extract_markers(text, self.PRESENCE_PATTERNS)
        
        # 4. Compute shell suggestions
        shell_suggestions = self._compute_shell_suggestions(
            tokens, contrast_markers, branching_markers, recursion_markers,
            collapse_markers, presence_markers
        )
        
        # 5. Compute error deltas
        error_deltas = self._compute_error_deltas(tokens, adjacency_pairs)
        
        # 6. Compute curvature deltas
        curvature_deltas = self._compute_curvature_deltas(
            tokens, triplets, recursion_markers
        )
        
        # 7. Compute entropy delta
        entropy_delta = self._compute_entropy_delta(tokens, triplets)
        
        # 8. Identify collapse points
        collapse_points = self._identify_collapse_points(
            tokens, collapse_markers
        )
        
        return CombinatoricDistinctionPacket(
            raw=text,
            tokens=tokens,
            adjacency_pairs=adjacency_pairs,
            triplets=triplets,
            shell_suggestions=shell_suggestions,
            error_deltas=error_deltas,
            curvature_deltas=curvature_deltas,
            entropy_delta=entropy_delta,
            collapse_points=collapse_points,
            metadata={
                "repetitions": repetitions,
                "contrast_count": len(contrast_markers),
                "branching_count": len(branching_markers),
                "recursion_count": len(recursion_markers),
                "collapse_count": len(collapse_markers),
                "presence_count": len(presence_markers),
            }
        )

    def _tokenize(self, text: str) -> list[str]:
        """
        Perform structural tokenization (language-agnostic).

        Splits via:
        - whitespace
        - punctuation
        - indentation (for code)
        - brackets
        - operators
        - line breaks

        Args:
            text: Input text

        Returns:
            List of tokens
        """
        # Split on whitespace, punctuation, brackets, operators
        # Keep separators as separate tokens for combinatoric analysis
        tokens = []
        
        # Pattern: word characters, operators, brackets, punctuation
        pattern = r'(\w+|[^\w\s]|\s+)'
        matches = re.findall(pattern, text)
        
        for match in matches:
            match = match.strip()
            if match:  # Skip empty strings
                tokens.append(match)
        
        # Also split on line breaks and indentation
        lines = text.split('\n')
        for line in lines:
            # Extract indentation
            indent_match = re.match(r'^(\s+)', line)
            if indent_match:
                indent = indent_match.group(1)
                if indent not in tokens:
                    tokens.append(indent)
        
        return tokens

    def _extract_adjacency_pairs(self, tokens: list[str]) -> list[tuple[str, str]]:
        """
        Extract adjacency pairs (combinatoric structure).

        Args:
            tokens: List of tokens

        Returns:
            List of (token1, token2) pairs
        """
        pairs = []
        for i in range(len(tokens) - 1):
            pairs.append((tokens[i], tokens[i + 1]))
        return pairs

    def _extract_triplets(self, tokens: list[str]) -> list[tuple[str, str, str]]:
        """
        Extract triplets (triads) from tokens.

        Args:
            tokens: List of tokens

        Returns:
            List of (token1, token2, token3) triplets
        """
        triplets = []
        for i in range(len(tokens) - 2):
            triplets.append((tokens[i], tokens[i + 1], tokens[i + 2]))
        return triplets

    def _extract_repetitions(self, tokens: list[str]) -> dict[str, int]:
        """
        Extract repetition patterns.

        Args:
            tokens: List of tokens

        Returns:
            Dictionary of token -> count
        """
        return dict(Counter(tokens))

    def _extract_markers(self, text: str, patterns: list[str]) -> list[tuple[int, str]]:
        """
        Extract markers matching patterns.

        Args:
            text: Input text
            patterns: List of regex patterns

        Returns:
            List of (position, match) tuples
        """
        markers = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                markers.append((match.start(), match.group()))
        return markers

    def _compute_shell_suggestions(
        self,
        tokens: list[str],
        contrast_markers: list[tuple[int, str]],
        branching_markers: list[tuple[int, str]],
        recursion_markers: list[tuple[int, str]],
        collapse_markers: list[tuple[int, str]],
        presence_markers: list[tuple[int, str]]
    ) -> list[int]:
        """
        Compute shell suggestions for each token.

        Shell assignment:
        - 0 (Presence): presence anchors, start
        - 2 (Measurement): contrast markers, duality
        - 3 (Flux): branching, recursion
        - 4 (Collapse): assignment, return, conclusion

        Args:
            tokens: List of tokens
            contrast_markers: Contrast marker positions
            branching_markers: Branching marker positions
            recursion_markers: Recursion marker positions
            collapse_markers: Collapse marker positions
            presence_markers: Presence marker positions

        Returns:
            List of shell suggestions (0, 2, 3, 4)
        """
        suggestions = []
        
        # Create position map
        position_map = {}
        current_pos = 0
        for i, token in enumerate(tokens):
            position_map[i] = current_pos
            current_pos += len(token)
        
        for i, token in enumerate(tokens):
            pos = position_map.get(i, 0)
            shell = 0  # Default to presence
            
            # Priority order: presence < measurement < flux < collapse
            # But flux (branching/recursion) can coexist with collapse
            
            # Check for presence markers (lowest priority)
            for marker_pos, _ in presence_markers:
                if abs(marker_pos - pos) < len(token):
                    shell = 0
                    break
            
            # Check for measurement markers (contrast/duality)
            for marker_pos, _ in contrast_markers:
                if abs(marker_pos - pos) < len(token):
                    shell = 2
                    break
            
            # Check for flux markers (branching/recursion) - higher priority
            for marker_pos, _ in branching_markers + recursion_markers:
                if abs(marker_pos - pos) < len(token):
                    shell = 3
                    break
            
            # Check for collapse markers (highest priority, but don't override flux if both present)
            for marker_pos, _ in collapse_markers:
                if abs(marker_pos - pos) < len(token):
                    # Only set to collapse if not already flux
                    if shell != 3:
                        shell = 4
                    break
            
            suggestions.append(shell)
        
        return suggestions

    def _compute_error_deltas(
        self,
        tokens: list[str],
        adjacency_pairs: list[tuple[str, str]]
    ) -> list[float]:
        """
        Compute error deltas (difference from adjacency expectation).

        Args:
            tokens: List of tokens
            adjacency_pairs: Adjacency pairs

        Returns:
            List of error delta values
        """
        error_deltas = []
        
        # Compute expected adjacency patterns
        pair_counts = Counter(adjacency_pairs)
        total_pairs = len(adjacency_pairs)
        
        for i, token in enumerate(tokens):
            if i == 0:
                error_delta = 0.0  # First token has no expectation
            else:
                # Error = how unexpected this adjacency is
                prev_token = tokens[i - 1]
                pair = (prev_token, token)
                expected_freq = pair_counts.get(pair, 0) / max(total_pairs, 1)
                # Low frequency = high error (unexpected)
                error_delta = 1.0 - expected_freq
            
            error_deltas.append(error_delta)
        
        return error_deltas

    def _compute_curvature_deltas(
        self,
        tokens: list[str],
        triplets: list[tuple[str, str, str]],
        recursion_markers: list[tuple[int, str]]
    ) -> list[float]:
        """
        Compute curvature deltas (change in combinatoric pattern).

        Args:
            tokens: List of tokens
            triplets: Extracted triplets
            recursion_markers: Recursion marker positions

        Returns:
            List of curvature delta values
        """
        curvature_deltas = []
        
        # Recursion increases curvature
        recursion_positions = {pos for pos, _ in recursion_markers}
        
        # Compute triplet variance (curvature indicator)
        triplet_variance = 0.0
        if triplets:
            # Count unique triplets
            unique_triplets = len(set(triplets))
            total_triplets = len(triplets)
            triplet_variance = unique_triplets / max(total_triplets, 1)
        
        current_pos = 0
        for i, token in enumerate(tokens):
            # Check if near recursion marker
            near_recursion = any(
                abs(pos - current_pos) < len(token)
                for pos in recursion_positions
            )
            
            # Curvature delta based on:
            # - Recursion presence
            # - Triplet variance
            # - Position in sequence
            curvature_delta = 0.0
            if near_recursion:
                curvature_delta += 0.3
            curvature_delta += triplet_variance * 0.2
            curvature_delta += (i / max(len(tokens), 1)) * 0.1  # Position effect
            
            curvature_deltas.append(curvature_delta)
            current_pos += len(token)
        
        return curvature_deltas

    def _compute_entropy_delta(
        self,
        tokens: list[str],
        triplets: list[tuple[str, str, str]]
    ) -> float:
        """
        Compute entropy delta (distributional spread).

        Args:
            tokens: List of tokens
            triplets: Extracted triplets

        Returns:
            Entropy delta value
        """
        if not tokens:
            return 0.0
        
        # Token distribution entropy
        token_counts = Counter(tokens)
        total = len(tokens)
        token_entropy = 0.0
        
        for count in token_counts.values():
            if count > 0:
                p = count / total
                token_entropy -= p * math.log2(p) if p > 0 else 0.0
        
        # Triplet distribution entropy
        triplet_counts = Counter(triplets)
        total_triplets = len(triplets)
        triplet_entropy = 0.0
        
        if total_triplets > 0:
            for count in triplet_counts.values():
                if count > 0:
                    p = count / total_triplets
                    triplet_entropy -= p * math.log2(p) if p > 0 else 0.0
        
        # Combined entropy delta
        entropy_delta = (token_entropy + triplet_entropy) / 2.0
        
        return entropy_delta

    def _identify_collapse_points(
        self,
        tokens: list[str],
        collapse_markers: list[tuple[int, str]]
    ) -> list[int]:
        """
        Identify collapse points (token indices).

        Args:
            tokens: List of tokens
            collapse_markers: Collapse marker positions

        Returns:
            List of token indices where collapse occurs
        """
        collapse_points = []
        
        # Map positions to token indices
        current_pos = 0
        position_to_index = {}
        for i, token in enumerate(tokens):
            position_to_index[current_pos] = i
            current_pos += len(token)
        
        # Find tokens near collapse markers
        for marker_pos, _ in collapse_markers:
            # Find closest token index
            closest_index = None
            min_distance = float('inf')
            
            for pos, index in position_to_index.items():
                distance = abs(pos - marker_pos)
                if distance < min_distance:
                    min_distance = distance
                    closest_index = index
            
            if closest_index is not None and closest_index not in collapse_points:
                collapse_points.append(closest_index)
        
        return sorted(collapse_points)

