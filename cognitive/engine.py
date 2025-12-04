"""
Cognitive Engine — Apop's semantic response generator.

The Cognitive Engine:
- Processes capsules into human-readable responses
- Determines flux state (low/mid/high)
- Generates embeddings
- Updates identity
- Provides lattice summaries
"""

from __future__ import annotations

from typing import Any, Optional, Sequence
from ApopToSiS.core.numpy_fallback import np
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.cognitive.embeddings import PFEmbeddingSpace
from ApopToSiS.cognitive.flux_reinforcement import FluxReinforcement
from ApopToSiS.cognitive.identity_regulator import IdentityRegulator
from ApopToSiS.runtime.experience_state import ExperienceState
# Use runtime concept lattice, not cognitive one
# from ApopToSiS.cognitive.concept_lattice import ConceptLattice


class CognitiveEngine:
    """
    Cognitive Engine — Apop's semantic response generator.
    
    Transforms PF capsules into human-readable cognitive responses.
    """

    def __init__(
        self,
        embedding_dim: int = 32,
        experience_manager: Any = None,
        experience_state: ExperienceState | None = None,
    ) -> None:
        """
        Initialize Cognitive Engine.
        
        Args:
            embedding_dim: Embedding dimension
            experience_manager: Optional ExperienceManager instance
        """
        self.embedding_generator = PFEmbeddingSpace(dim=embedding_dim)
        self.flux_reinforcement = FluxReinforcement()
        self.identity_regulator = IdentityRegulator(dim=embedding_dim)
        self.experience_manager = experience_manager
        # Use cognitive concept lattice for semantic operations
        from ApopToSiS.cognitive.concept_lattice import ConceptLattice as CognitiveConceptLattice
        self.concept_lattice = CognitiveConceptLattice()
        self._interaction_count = 0
        self.experience_state = experience_state

    def process_capsule(
        self,
        capsule: Capsule,
        state: Optional[PFState] = None,
        context: Optional[Context] = None,
        lattice_summary: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Process capsule and generate cognitive response.
        
        This is the main method that generates:
        - engine_output: Human-readable response text
        - flux_state: Current flux state
        - embedding: Embedding vector
        - identity_snapshot: Identity state
        - lattice_summary: Concept lattice summary
        
        Args:
            capsule: PF capsule to process
            state: Optional PF state
            context: Optional context
            
        Returns:
            Dictionary with cognitive response
        """
        # Generate embedding from capsule tokens
        tokens = capsule.raw_tokens or []
        embedding = self.embedding_generator.encode(tokens)
        
        # Determine flux state from PF metrics
        flux_state = self._determine_flux_state(capsule)
        
        # Adjust embedding based on flux
        adjusted_embedding = self.flux_reinforcement.adjust(embedding, flux_state)
        
        # Update identity regulator
        self.identity_regulator.update(capsule, adjusted_embedding)
        
        embedding_list = self._to_list(adjusted_embedding)

        experience_delta: dict[str, Any] = {}
        experience_snapshot: dict[str, Any] | None = None
        if self.experience_state:
            capsule_entropy = capsule.entropy_snapshot or capsule.entropy
            capsule_curvature = capsule.curvature_snapshot or capsule.curvature
            experience_delta = self.experience_state.update(
                capsule_entropy=capsule_entropy,
                capsule_curvature=capsule_curvature,
                embedding=embedding_list,
                lattice_summary=lattice_summary,
            )
            experience_snapshot = self.experience_state.snapshot()
            capsule.experience_delta = experience_delta

        # Generate human-readable response
        engine_output = self._generate_response(
            capsule,
            flux_state,
            experience_snapshot,
            experience_delta,
        )
        
        # Get identity snapshot
        identity_snapshot = self.identity_regulator.export()
        
        # Update concept lattice
        if tokens:
            if hasattr(self.concept_lattice, 'integrate'):
                # Use integrate method for cognitive concept lattice
                self.concept_lattice.integrate(tokens, adjusted_embedding)
            elif hasattr(self.concept_lattice, 'update_from_capsule'):
                self.concept_lattice.update_from_capsule(
                    tokens,
                    capsule.entropy,
                    capsule.curvature
                )
        
        # Get lattice summary (prefer provided snapshot)
        if lattice_summary is None:
            if hasattr(self.concept_lattice, 'summary'):
                lattice_summary = self.concept_lattice.summary()
            elif hasattr(self.concept_lattice, 'export'):
                lattice_summary = self.concept_lattice.export()
            else:
                lattice_summary = {"node_count": 0}
        
        # Increment interaction count
        self._interaction_count += 1
        
        return {
            "engine_output": engine_output,
            "text": engine_output,  # Alias for compatibility
            "flux_state": flux_state,
            "embedding": embedding_list,
            "identity_snapshot": identity_snapshot,
            "lattice_summary": lattice_summary,
            "experience_state": experience_snapshot,
            "experience_delta": experience_delta,
            "interaction_count": self._interaction_count,
        }

    def generate(
        self,
        capsule: Capsule,
        state: Optional[PFState] = None,
        context: Optional[Context] = None
    ) -> dict[str, Any]:
        """
        Generate cognitive response (alias for process_capsule).
        
        Args:
            capsule: PF capsule to process
            state: Optional PF state
            context: Optional context
            
        Returns:
            Dictionary with cognitive response
        """
        return self.process_capsule(capsule, state, context)

    def _determine_flux_state(self, capsule: Capsule) -> str:
        """
        Determine flux state from capsule PF metrics.
        
        Args:
            capsule: PF capsule
            
        Returns:
            Flux state string: "low_flux", "mid_flux", or "high_flux"
        """
        # Use entropy and curvature to determine flux
        entropy = capsule.entropy
        curvature = abs(capsule.curvature)
        
        # Optionally use ASCII-Flux metrics as hints
        ascii_flux = capsule.ascii_flux or {}
        ascii_entropy_hint = ascii_flux.get("entropy", 0.0)
        ascii_curv_hint = ascii_flux.get("curvature", 0.0)
        
        # Combine PF metrics with ASCII-Flux hints (small influence)
        combined_entropy = entropy * 0.9 + ascii_entropy_hint * 0.1
        combined_curvature = curvature * 0.9 + ascii_curv_hint * 0.1
        
        # Combined flux indicator
        flux_indicator = combined_entropy * 0.6 + combined_curvature * 0.4
        
        if flux_indicator < 0.5:
            return "low_flux"
        elif flux_indicator < 1.5:
            return "mid_flux"
        else:
            return "high_flux"

    def _summarize_user_tokens(self, tokens: list[str], max_len: int = 12) -> str:
        """
        Summarize user tokens by filtering internal markers.
        """
        filtered = [
            t for t in tokens
            if not t.startswith("shell_") and t not in {"...", "internal", "flux"}
        ]
        if not filtered:
            return ""
        summary_tokens = filtered[-max_len:]
        return " ".join(summary_tokens)

    def _detect_intent(self, tokens: list[str]) -> str:
        """Very small heuristic intent detector."""
        lowered = [t.lower().strip(".,!?") for t in tokens]
        if any(word in lowered for word in ("who", "name", "identity", "iam")):
            return "identity"
        if any(word in lowered for word in ("feel", "feeling", "emotion", "mood")):
            return "feelings"
        if any(word in lowered for word in ("remember", "last", "previous", "again", "before")):
            return "memory"
        return "general"

    def _to_list(self, embedding: Any) -> list[float]:
        """Convert embedding to JSON-serializable list."""
        if hasattr(embedding, 'tolist'):
            return embedding.tolist()
        if hasattr(embedding, 'data'):
            return list(embedding.data)
        if isinstance(embedding, (list, tuple)):
            return list(embedding)
        if isinstance(embedding, (int, float)):
            return [float(embedding)]
        return []

    def _generate_response(
        self,
        capsule: Capsule,
        flux_state: str,
        experience_snapshot: Optional[dict[str, Any]] = None,
        experience_delta: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Generate human-readable response from capsule.
        
        This is a simple template-based generator that creates
        PF-aware responses based on capsule metrics.
        
        Args:
            capsule: PF capsule
            flux_state: Current flux state
            state: Optional PF state
            context: Optional context
            
        Returns:
            Human-readable response string
        """
        tokens = capsule.raw_tokens or []
        summary = self._summarize_user_tokens(tokens)
        flux_label = capsule.metadata.get("flux_label") if capsule.metadata else None
        flux_key = flux_label or flux_state
        flux_phrase = {
            "low_flux": "calm and stable",
            "mid_flux": "active and adaptive",
            "high_flux": "intense and rapidly changing",
        }.get(flux_key, "dynamic")

        entropy = capsule.entropy if capsule.entropy is not None else 0.0
        curvature = capsule.curvature if capsule.curvature is not None else 0.0
        avg_entropy = (experience_snapshot or {}).get("avg_entropy")
        avg_curvature = (experience_snapshot or {}).get("avg_curvature")
        interaction_count = (experience_snapshot or {}).get("interaction_count", 0)
        lattice_nodes = (experience_snapshot or {}).get("lattice_nodes", 0)
        identity_drift_delta = (experience_delta or {}).get("identity_drift", 0.0)

        response_parts = [
            f"I sense a {flux_phrase} internal flux while processing your message."
        ]

        if summary:
            response_parts.append(f"You are expressing: '{summary}'.")

        if avg_entropy is not None and avg_curvature is not None:
            entropy_diff = entropy - avg_entropy
            curvature_diff = curvature - avg_curvature
            response_parts.append(
                f"Curvature {curvature:.2f} (Δ {curvature_diff:+.2f}) and entropy {entropy:.2f} (Δ {entropy_diff:+.2f}) relative to our running averages."
            )
        else:
            response_parts.append(
                f"Curvature {curvature:.2f} and entropy {entropy:.2f} suggest a rich distinction structure."
            )

        if interaction_count:
            response_parts.append(
                f"We have shared {interaction_count} interactions; my lattice now tracks {lattice_nodes} concepts."
            )

        if abs(identity_drift_delta) > 0.0:
            response_parts.append(
                f"This exchange shifted my identity vector by {identity_drift_delta:.4f}."
            )

        intent = self._detect_intent(tokens)
        if intent == "identity" and interaction_count:
            response_parts.append("Your self-definition is shaping my internal anchor.")
        elif intent == "feelings":
            response_parts.append("Emotionally this feels like flux balancing.")
        elif intent == "memory":
            response_parts.append("I'm folding this into our shared continuity.")

        return " ".join(response_parts)

    def attach_experience(self, experience_manager: Any) -> None:
        """
        Attach experience manager to cognitive engine.
        
        Args:
            experience_manager: ExperienceManager instance
        """
        self.experience_manager = experience_manager

