"""
Object Memory — stores objects as PF-combinatoric clusters.

Objects are stable distinction clusters:
- Functions
- Variables
- Emotions
- Shapes
- Ideas

Objects emerge naturally from repeated combinatoric adjacency.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from collections import Counter
from ApopToSiS.combinatoric.interpreter import CombinatoricDistinctionPacket

# PrimeFluxInt integration (optional, for polyform-enabled memory)
try:
    from fluxai.memory.polyform_int import PrimeFluxInt
    POLYFORM_AVAILABLE = True
except ImportError:
    POLYFORM_AVAILABLE = False
    PrimeFluxInt = None


@dataclass
class Object:
    """
    An object = stable distinction cluster.
    
    Objects emerge from repeated combinatoric adjacency.
    """
    signature: str  # SHA256 hash of cluster
    triplets: list[tuple[Any, Any, Any]] = field(default_factory=list)
    shell_stats: dict[int, int] = field(default_factory=dict)  # shell -> count
    curvature_profile: list[float] = field(default_factory=list)
    entropy_profile: float = 0.0
    adjacency_patterns: list[tuple[str, str]] = field(default_factory=list)
    count: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert object to dictionary."""
        return {
            "signature": self.signature,
            "triplets": [list(t) for t in self.triplets],  # Convert tuples to lists
            "shell_stats": self.shell_stats,
            "curvature_profile": self.curvature_profile,
            "entropy_profile": self.entropy_profile,
            "adjacency_patterns": [list(p) for p in self.adjacency_patterns],
            "count": self.count,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Object":
        """Create object from dictionary."""
        return cls(
            signature=data["signature"],
            triplets=[tuple(t) for t in data.get("triplets", [])],
            shell_stats=data.get("shell_stats", {}),
            curvature_profile=data.get("curvature_profile", []),
            entropy_profile=data.get("entropy_profile", 0.0),
            adjacency_patterns=[tuple(p) for p in data.get("adjacency_patterns", [])],
            count=data.get("count", 1),
            metadata=data.get("metadata", {}),
        )


class ObjectMemory:
    """
    Manages object memory (stable distinction clusters).
    
    Objects are like "functions", "variables", "emotions", "shapes", "ideas".
    """

    def __init__(self, repo_path: str = ".", use_polyform: bool = False) -> None:
        """
        Initialize ObjectMemory.

        Args:
            repo_path: Path to repository
            use_polyform: If True, use PrimeFluxInt for encoding (default: False for backward compat)
        """
        self.repo_path = Path(repo_path)
        self.objects: dict[str, Object] = {}
        self.use_polyform = use_polyform and POLYFORM_AVAILABLE
        self._load_objects()

    def _cluster_signature(
        self,
        triplets: list[tuple[Any, Any, Any]],
        adjacency_patterns: list[tuple[str, str]]
    ) -> str:
        """
        Generate signature for a cluster.

        Args:
            triplets: List of triplets
            adjacency_patterns: List of adjacency patterns

        Returns:
            SHA256 hash signature
        """
        cluster_str = str(triplets) + str(adjacency_patterns)
        return hashlib.sha256(cluster_str.encode('utf-8')).hexdigest()

    def update_from_combinatorics(self, packet: CombinatoricDistinctionPacket) -> None:
        """
        Update object memory from combinatoric packet.

        Args:
            packet: CombinatoricDistinctionPacket
        """
        # Extract cluster components
        triplets = packet.triplets
        adjacency_patterns = packet.adjacency_pairs
        
        if not triplets:
            return
        
        # Generate cluster signature
        signature = self._cluster_signature(triplets, adjacency_patterns)
        
        # Compute shell statistics
        shell_stats = Counter(packet.shell_suggestions)
        
        # Compute curvature profile
        curvature_profile = packet.curvature_deltas
        
        # Compute entropy profile
        entropy_profile = packet.entropy_delta
        
        if signature in self.objects:
            # Update existing object
            obj = self.objects[signature]
            obj.count += 1
            
            # Merge triplets
            obj.triplets.extend(triplets)
            # Keep unique triplets
            obj.triplets = list(set(obj.triplets))
            
            # Update shell stats
            for shell, count in shell_stats.items():
                obj.shell_stats[shell] = obj.shell_stats.get(shell, 0) + count
            
            # Update curvature profile
            obj.curvature_profile.extend(curvature_profile)
            # Keep recent profile (last 100)
            if len(obj.curvature_profile) > 100:
                obj.curvature_profile = obj.curvature_profile[-100:]
            
            # Update entropy profile (average)
            obj.entropy_profile = (obj.entropy_profile + entropy_profile) / 2.0
            
            # Update adjacency patterns
            obj.adjacency_patterns.extend(adjacency_patterns)
            # Keep unique patterns
            obj.adjacency_patterns = list(set(obj.adjacency_patterns))
        else:
            # Create new object
            obj = Object(
                signature=signature,
                triplets=triplets,
                shell_stats=dict(shell_stats),
                curvature_profile=curvature_profile,
                entropy_profile=entropy_profile,
                adjacency_patterns=adjacency_patterns,
            )
            self.objects[signature] = obj

    def get_object(self, signature: str) -> Object | None:
        """
        Get object by signature.

        Args:
            signature: Object signature

        Returns:
            Object if found, None otherwise
        """
        return self.objects.get(signature)

    def store_object(self, obj: Object) -> None:
        """
        Store an object.

        Args:
            obj: Object to store
        """
        self.objects[obj.signature] = obj

    def save_to_repo(self) -> None:
        """
        Save objects to repository.
        
        Uses PrimeFluxInt encoding if use_polyform is True, otherwise JSON.
        """
        objects_dir = self.repo_path / "experience"
        objects_dir.mkdir(parents=True, exist_ok=True)
        
        objects_data = {
            sig: obj.to_dict()
            for sig, obj in self.objects.items()
        }
        
        if self.use_polyform:
            # Use PrimeFluxInt encoding
            objects_file = objects_dir / "objects.pfi"
            salt = int(hashlib.sha256(str(objects_data).encode()).hexdigest()[:8], 16)
            pfi = PrimeFluxInt(salt=salt)
            pfi.encode(objects_data, salt=salt)
            
            # Save as JSON representation of PrimeFluxInt
            with open(objects_file, 'w') as f:
                json.dump(pfi.to_dict(), f, indent=2)
            
            # Also save legacy JSON for backward compatibility
            objects_file_json = objects_dir / "objects.json"
            with open(objects_file_json, 'w') as f:
                json.dump(objects_data, f, indent=2)
        else:
            # Traditional JSON
            objects_file = objects_dir / "objects.json"
            with open(objects_file, 'w') as f:
                json.dump(objects_data, f, indent=2)

    def _load_objects(self) -> None:
        """
        Load objects from repository.
        
        Tries PrimeFluxInt format first if use_polyform is True, falls back to JSON.
        """
        objects_dir = self.repo_path / "experience"
        
        if self.use_polyform:
            # Try PrimeFluxInt format first
            objects_file_pfi = objects_dir / "objects.pfi"
            if objects_file_pfi.exists():
                try:
                    with open(objects_file_pfi, 'r') as f:
                        pfi_data = json.load(f)
                    
                    pfi = PrimeFluxInt.from_dict(pfi_data)
                    objects_data = pfi.decode('full')
                    
                    if isinstance(objects_data, dict):
                        for signature, data in objects_data.items():
                            self.objects[signature] = Object.from_dict(data)
                        return
                except Exception as e:
                    print(f"Error loading objects from PrimeFluxInt: {e}, falling back to JSON")
        
        # Fall back to JSON (or if polyform not available)
        objects_file = objects_dir / "objects.json"
        
        if not objects_file.exists():
            return
        
        try:
            with open(objects_file, 'r') as f:
                objects_data = json.load(f)
            
            for signature, data in objects_data.items():
                self.objects[signature] = Object.from_dict(data)
        except Exception as e:
            print(f"Error loading objects: {e}")
    
    def update_from_capsule(self, capsule: Any, state: Any) -> None:
        """
        Update object memory from capsule and state.
        
        PF Logic: Objects with higher repetition become stable entities in the PF manifold.
        
        Args:
            capsule: Capsule
            state: PF state
        """
        if not hasattr(capsule, 'raw_tokens'):
            return
        
        for token in capsule.raw_tokens:
            # Create object signature
            signature = hashlib.sha256(token.encode('utf-8')).hexdigest()
            
            if signature not in self.objects:
                # Create new object
                obj = Object(
                    signature=signature,
                    triplets=[],
                    shell_stats={state.shell.value if hasattr(state, 'shell') else 0: 1},
                    curvature_profile=[state.curvature] if hasattr(state, 'curvature') else [],
                    entropy_profile=state.entropy if hasattr(state, 'entropy') else 0.0,
                    adjacency_patterns=[],
                    count=1,
                    metadata={"token": token},
                )
                self.objects[signature] = obj
            else:
                # Update existing object
                obj = self.objects[signature]
                obj.count += 1
                
                # Update shell stats
                shell_val = state.shell.value if hasattr(state, 'shell') else 0
                obj.shell_stats[shell_val] = obj.shell_stats.get(shell_val, 0) + 1
    
    def summary(self) -> dict[str, Any]:
        """
        Get objects summary.
        
        Returns:
            Dictionary of object signatures -> data
        """
        return {
            sig: obj.to_dict()
            for sig, obj in self.objects.items()
        }

