"""
Capsules — PrimeFlux Cognitive State Transport Layer.

Capsules are the "atoms" of PrimeFlux cognition.
They transport information, measure curvature, encode distinctions,
record triplets, manage superposition ψ, transmit state between agents,
compress memory (QuantaCoin), express identity continuity,
integrate with the Experience Layer, and interface with the LLM front-end.

Capsules = JSON-Flux = transport layer of the PF manifold.
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
import json
import time
import uuid
from ApopToSiS.core.math.shells import Shell
from ApopToSiS.runtime.device_identity import get_device_identity


@dataclass
class Capsule:
    """
    Capsule — PrimeFlux cognitive state container.
    
    Capsules are containers of PF state, not linguistic entities.
    They are the fundamental PrimeFlux unit.
    
    Everything in ApopToSiS v3 reduces to:
    Distinction → Triplet → Capsule → Flux → Collapse → Capsule → Identity
    """
    
    # Required PF fields
    raw_tokens: list[str] = field(default_factory=list)
    triplets: list[dict[str, Any]] = field(default_factory=list)
    entropy: float = 0.0
    curvature: float = 0.0
    shell: int = 0  # PF shell (0, 2, 3, 4)
    density: float = 0.0
    psi: float = 0.0  # Superposition magnitude
    hamiltonian: float = 0.0
    reptend_entropy: float = 0.0
    rail_interference: float = 0.0
    timestamp: float = field(default_factory=time.time)
    quanta_hash: str | None = None
    
    # Network/distributed fields (Section 12)
    device_id: str = ""
    session_id: str = ""
    capsule_id: str = ""
    prev_capsule_id: str = ""
    compression_ratio: float = 1.0
    experience_delta: dict[str, Any] = field(default_factory=dict)
    agent_trace: list[str] = field(default_factory=list)
    
    # Legacy fields for backward compatibility
    triplet_summary: dict[str, Any] = field(default_factory=dict)
    shell_state: int = 0
    entropy_snapshot: float = 0.0
    curvature_snapshot: float = 0.0
    pf_signature: dict[str, Any] = field(default_factory=dict)
    compression_hash: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    measurement_error: float = 0.0
    
    # PrimeFS fields (Patch 008A)
    salt_2: str = ""
    salt_5: str = ""
    pf_json_type: str = "pf_capsule"
    pf_json_version: str = "3.0"
    dimensions: int = 0
    
    # ASCII-Flux fields (Patch 008)
    ascii_flux: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Initialize derived fields."""
        # Sync legacy fields if not provided
        if self.entropy_snapshot == 0.0:
            self.entropy_snapshot = self.entropy
        if self.curvature_snapshot == 0.0:
            self.curvature_snapshot = self.curvature
        if self.shell_state == 0:
            self.shell_state = self.shell
        if self.compression_hash is None:
            self.compression_hash = self.quanta_hash
        
        # Initialize network fields if not provided
        if not self.device_id:
            device_identity = get_device_identity()
            self.device_id = device_identity.get_device_id()
        
        if not self.capsule_id:
            self.capsule_id = str(uuid.uuid4())
        
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
    
    def encode(self) -> dict[str, Any]:
        """
        Encode capsule to JSON-Flux format (distributed format).
        
        Capsules = JSON-Flux = transport layer of the PF manifold.
        This is the canonical distributed format.
        
        Returns:
            Dictionary with all PF fields including network fields
        """
        capsule_dict = {
            "type": "pf_capsule",
            "version": "3.0",
            # PrimeFS fields
            "salt_2": self.salt_2 or "TODO_placeholder_2_salt",
            "salt_5": self.salt_5 or "TODO_placeholder_5_salt",
            "pf_json_type": self.pf_json_type,
            "pf_json_version": self.pf_json_version,
            "dimensions": self.dimensions,
            # Standard fields
            "raw_tokens": self.raw_tokens,
            "triplets": self.triplets,
            "shell": self.shell,
            "entropy": self.entropy,
            "curvature": self.curvature,
            "density": self.density,
            "psi": self.psi,
            "hamiltonian": self.hamiltonian,
            "reptend_entropy": self.reptend_entropy,
            "rail_interference": self.rail_interference,
            "timestamp": self.timestamp,
            "device_id": self.device_id,
            "session_id": self.session_id,
            "capsule_id": self.capsule_id,
            "prev_capsule_id": self.prev_capsule_id,
            "quanta_hash": self.quanta_hash,
            "compression_ratio": self.compression_ratio,
            "experience_delta": self.experience_delta,
            "agent_trace": self.agent_trace,
            "pf_signature": self.pf_signature,
            # Legacy fields for compatibility
            "triplet_summary": self.triplet_summary,
            "shell_state": self.shell_state,
            "entropy_snapshot": self.entropy_snapshot,
            "curvature_snapshot": self.curvature_snapshot,
            "compression_hash": self.compression_hash,
            "metadata": self.metadata,
            "measurement_error": self.measurement_error,
            # ASCII-Flux field
            "ascii_flux": self.ascii_flux or {},
        }
        exp_delta = capsule_dict.get("experience_delta")
        if exp_delta:
            entropy_boost = len(exp_delta) * 0.01
            capsule_dict["entropy"] = round(capsule_dict.get("entropy", 0.0) + entropy_boost, 4)
        pf_signature_block = {}
        if isinstance(self.pf_signature, dict):
            pf_signature_block.update(self.pf_signature)
        pf_signature_block.update({
            "shell_suggestion": capsule_dict.get("shell"),
            "curvature_confidence": round(capsule_dict.get("curvature", 0.0) * 0.12, 3),
            "entropy_estimate": round(capsule_dict.get("entropy", 0.0), 3),
        })
        capsule_dict["pf_signature"] = pf_signature_block
        capsule_dict["continuity"] = {
            "tokens": len(capsule_dict.get("raw_tokens", [])),
            "identity_depth": capsule_dict.get("metadata", {}).get("cog_response", {}).get("identity_state", {}).get("interactions", 0),
        }
        return capsule_dict
    
    @staticmethod
    def decode(data: dict[str, Any]) -> "Capsule":
        """
        Decode capsule from JSON-Flux format (distributed format).
        
        Args:
            data: Dictionary with capsule fields
            
        Returns:
            Capsule instance
        """
        return Capsule(
            raw_tokens=data.get("raw_tokens", []),
            triplets=data.get("triplets", []),
            entropy=data.get("entropy", 0.0),
            curvature=data.get("curvature", 0.0),
            shell=data.get("shell", 0),
            density=data.get("density", 0.0),
            psi=data.get("psi", 0.0),
            hamiltonian=data.get("hamiltonian", 0.0),
            reptend_entropy=data.get("reptend_entropy", 0.0),
            rail_interference=data.get("rail_interference", 0.0),
            timestamp=data.get("timestamp", time.time()),
            quanta_hash=data.get("quanta_hash"),
            # Network fields
            device_id=data.get("device_id", ""),
            session_id=data.get("session_id", ""),
            capsule_id=data.get("capsule_id", ""),
            prev_capsule_id=data.get("prev_capsule_id", ""),
            compression_ratio=data.get("compression_ratio", 1.0),
            experience_delta=data.get("experience_delta", {}),
            agent_trace=data.get("agent_trace", []),
            # Legacy fields
            triplet_summary=data.get("triplet_summary", {}),
            shell_state=data.get("shell_state", 0),
            entropy_snapshot=data.get("entropy_snapshot", 0.0),
            curvature_snapshot=data.get("curvature_snapshot", 0.0),
            pf_signature=data.get("pf_signature", {}),
            compression_hash=data.get("compression_hash"),
            metadata=data.get("metadata", {}),
            measurement_error=data.get("measurement_error", 0.0),
            # PrimeFS fields
            salt_2=data.get("salt_2", ""),
            salt_5=data.get("salt_5", ""),
            pf_json_type=data.get("pf_json_type", "pf_capsule"),
            pf_json_version=data.get("pf_json_version", "3.0"),
            dimensions=data.get("dimensions", 0),
            # ASCII-Flux field
            ascii_flux=data.get("ascii_flux", {}) or {},
        )
    
    @classmethod
    def from_tokens(cls, tokens: list[str], **kwargs: Any) -> "Capsule":
        """
        Convenience constructor to build a capsule from raw tokens.
        
        Args:
            tokens: Token sequence to embed inside the capsule
            **kwargs: Optional overrides for capsule fields
            
        Returns:
            Capsule instance
        """
        return cls(raw_tokens=list(tokens), **kwargs)
    
    def merge(self, other: "Capsule") -> "Capsule":
        """
        Merge two capsules.
        
        Agent transformations become capsule synthesis.
        This is Apop's combinatoric "thought merging".
        
        Args:
            other: Other capsule to merge with
            
        Returns:
            New merged capsule
        """
        # Merge tokens (append)
        merged_tokens = self.raw_tokens + other.raw_tokens
        
        # Merge triplets (append)
        merged_triplets = self.triplets + other.triplets
        
        # Average scalar fields
        merged_entropy = (self.entropy + other.entropy) / 2.0
        merged_curvature = (self.curvature + other.curvature) / 2.0
        merged_density = (self.density + other.density) / 2.0
        merged_psi = (self.psi + other.psi) / 2.0
        merged_reptend_entropy = (self.reptend_entropy + other.reptend_entropy) / 2.0
        merged_measurement_error = (self.measurement_error + other.measurement_error) / 2.0
        
        # Take maximum for shell, hamiltonian, rail_interference
        merged_shell = max(self.shell, other.shell)
        merged_hamiltonian = max(self.hamiltonian, other.hamiltonian)
        merged_rail_interference = max(self.rail_interference, other.rail_interference)
        
        # Merge metadata
        merged_metadata = {**self.metadata, **other.metadata}
        merged_metadata["merged_from"] = [self.timestamp, other.timestamp]
        
        # Merge triplet summaries
        merged_triplet_summary = {**self.triplet_summary, **other.triplet_summary}
        merged_triplet_summary["merged"] = True
        
        # Merge PF signatures
        merged_pf_signature = {**self.pf_signature, **other.pf_signature}
        
        # Use later timestamp
        merged_timestamp = max(self.timestamp, other.timestamp)
        
        # Quanta hash will be recomputed after merge
        merged_quanta_hash = None
        
        return Capsule(
            raw_tokens=merged_tokens,
            triplets=merged_triplets,
            entropy=merged_entropy,
            curvature=merged_curvature,
            shell=merged_shell,
            density=merged_density,
            psi=merged_psi,
            hamiltonian=merged_hamiltonian,
            reptend_entropy=merged_reptend_entropy,
            rail_interference=merged_rail_interference,
            timestamp=merged_timestamp,
            quanta_hash=merged_quanta_hash,
            triplet_summary=merged_triplet_summary,
            shell_state=merged_shell,
            entropy_snapshot=merged_entropy,
            curvature_snapshot=merged_curvature,
            pf_signature=merged_pf_signature,
            metadata=merged_metadata,
            measurement_error=merged_measurement_error,
        )
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert capsule to dictionary (alias for encode).
        
        Returns:
            Dictionary representation
        """
        return self.encode()
    
    def __str__(self) -> str:
        """String representation of capsule."""
        return f"Capsule(shell={self.shell}, curvature={self.curvature:.4f}, entropy={self.entropy:.4f}, tokens={len(self.raw_tokens)})"
    
    def __repr__(self) -> str:
        """Representation of capsule."""
        return self.__str__()
