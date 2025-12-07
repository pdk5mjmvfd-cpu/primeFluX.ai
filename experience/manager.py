"""
Experience Manager — orchestrates all experience subsystems.

The Experience Layer is where Apop builds:
- habits
- shortcuts
- object memories
- skills
- user-specific preferences
- PF distinction continuity
- PF curvature reinforcement
- internal experience-graphs
- conceptual schemas
- manifold-level identity
"""

from __future__ import annotations

from typing import Any
from .habits.habits import HabitManager
from .shortcuts.shortcuts import ShortcutManager
from .objects.object_memory import ObjectMemory
from .skills.skills import SkillManager
from .pattern_recognition.pattern_recognition import (
    detect_repetition,
    detect_triplet_pattern,
    detect_flux_pattern,
    detect_entropy_trend,
    detect_curvature_pattern,
)
from .experience_graph.experience_graph import ExperienceGraph
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState

# PrimeFluxInt integration (optional)
try:
    from fluxai.memory.polyform_int import PrimeFluxInt
    POLYFORM_AVAILABLE = True
except ImportError:
    POLYFORM_AVAILABLE = False
    PrimeFluxInt = None

# QuantaCoin integration (optional)
try:
    from fluxai.quanta.quanta_core import QuantaCoin
    QUANTA_AVAILABLE = True
except ImportError:
    QUANTA_AVAILABLE = False
    QuantaCoin = None

# Agora integration (optional)
try:
    from fluxai.agora.agora_core import AgoraEcosystem
    AGORA_AVAILABLE = True
except ImportError:
    AGORA_AVAILABLE = False
    AgoraEcosystem = None


class ExperienceManager:
    """
    Experience Manager — orchestrates all experience subsystems.
    
    Updates after every Supervisor step.
    """

    def __init__(self, repo_path: str = ".", use_polyform: bool = False) -> None:
        """
        Initialize Experience Manager.

        Args:
            repo_path: Path to repository
            use_polyform: If True, enable PrimeFluxInt encoding for objects (default: False)
        """
        self.habits = HabitManager(repo_path=repo_path)
        self.shortcuts = ShortcutManager(repo_path=repo_path)
        self.objects = ObjectMemory(repo_path=repo_path, use_polyform=use_polyform)
        self.skills = SkillManager(
            repo_path=repo_path,
            habit_manager=self.habits,
            shortcut_manager=self.shortcuts,
            object_memory=self.objects
        )
        self.patterns = None  # Pattern recognition is functional
        self.graph = ExperienceGraph(repo_path=repo_path)
        # Lightweight reinforcement trackers (per Patch 007B spec)
        self.habit_counts: dict[str, int] = {}
        self.shortcut_counts: dict[tuple[str, str], int] = {}
        self.object_counts: dict[str, int] = {}
        # Back-compat aliases
        self.habit_signals = self.habit_counts
        self.shortcut_signals = self.shortcut_counts
        self.object_signals = self.object_counts
        self._last_state: PFState | None = None
        self.use_polyform = use_polyform and POLYFORM_AVAILABLE

    def update(self, capsule: Capsule, state: PFState) -> None:
        """
        Update all experience subsystems from capsule.
        
        All experience subsystems learn from capsule.

        Args:
            capsule: Capsule to learn from
            state: Current PF state
        """
        # Update habits
        self.habits.update_from_capsule(capsule, state)
        
        # Update shortcuts
        self.shortcuts.update_from_capsule(capsule, state)
        
        # Update object memory
        self.objects.update_from_capsule(capsule, state)
        
        # Update skills
        self.skills.update_from_capsule(capsule, state)
        
        # Update experience graph
        self.graph.update_from_capsule(capsule, state)

    def attach_state(self, state: PFState) -> None:
        """Attach a PF state reference for autonomous updates."""
        self._last_state = state

    def update_from_capsule(
        self,
        capsule: Capsule,
        state: PFState | None = None
    ) -> dict[str, int]:
        """
        Lightweight update used for reinforcement summaries.
        
        Args:
            capsule: Capsule to learn from
            state: Optional PF state
        
        Returns:
            Dictionary with habit/shortcut/object sizes
        """
        if state is not None:
            self._last_state = state
        active_state = state or self._last_state
        if active_state is not None:
            self.update(capsule, active_state)

        tokens = getattr(capsule, "raw_tokens", []) or []

        for token in tokens:
            self.habit_counts[token] = self.habit_counts.get(token, 0) + 1

        if len(tokens) >= 2:
            pair = (tokens[0], tokens[-1])
            self.shortcut_counts[pair] = self.shortcut_counts.get(pair, 0) + 1

        if len(tokens) > 3:
            obj = " ".join(tokens[:3])
            self.object_counts[obj] = self.object_counts.get(obj, 0) + 1

        summary = {
            "habits_size": len(self.habit_counts),
            "shortcuts_size": len(self.shortcut_counts),
            "objects_size": len(self.object_counts),
        }

        return summary

    def summarize(self) -> dict[str, Any]:
        """
        Get summary of all experience subsystems.

        Returns:
            Dictionary with summaries
        """
        return {
            "habits": self.habits.summary(),
            "shortcuts": self.shortcuts.summary(),
            "objects": self.objects.summary(),
            "skills": self.skills.summary(),
            "experience_graph": self.graph.summary(),
        }
    
    def get_experience_factor(self) -> float:
        """
        Compute experience factor for routing.
        
        experience_factor = (
            habit_strength
          + shortcut_density
          + object_stability
          + skill_curvature
          + graph_connectivity
        )
        
        Returns:
            Experience factor
        """
        # Habit strength
        habits_summary = self.habits.summary()
        habit_strength = sum(habits_summary.values()) / max(len(habits_summary), 1)
        
        # Shortcut density
        shortcuts_summary = self.shortcuts.summary()
        shortcut_density = len(shortcuts_summary) / 10.0  # Normalize
        
        # Object stability
        objects_summary = self.objects.summary()
        object_stability = sum(obj.get("count", 0) for obj in objects_summary.values()) / max(len(objects_summary), 1)
        
        # Skill curvature
        skills_summary = self.skills.summary()
        skill_curvature = sum(skill.get("curvature", 0.0) for skill in skills_summary.values()) / max(len(skills_summary), 1)
        
        # Graph connectivity
        graph_summary = self.graph.summary()
        graph_connectivity = len(graph_summary.get("edges", [])) / 10.0  # Normalize
        
        # Combined experience factor
        experience_factor = (
            habit_strength * 0.2 +
            shortcut_density * 0.2 +
            object_stability * 0.2 +
            skill_curvature * 0.2 +
            graph_connectivity * 0.2
        )
        
        return experience_factor
    
    def quanta_etch(
        self,
        experience_delta: dict[str, Any],
        quanta: int,
        holder_prime: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Compress experience delta to polyform lease.
        
        Creates lease {holder=p, epoch=e, ttl} and updates objects.json
        with ΦQ balances.
        
        Args:
            experience_delta: Experience delta to compress
            quanta: Quanta amount
            holder_prime: Optional prime number for holder (defaults to 2)
            
        Returns:
            Lease dictionary with polyform encoding
        """
        if not QUANTA_AVAILABLE or not QuantaCoin:
            # Fallback: return simple lease
            return {
                "holder": holder_prime or 2,
                "epoch": 0,
                "ttl": 30,
                "quanta": quanta,
                "polyform_enabled": False
            }
        
        if holder_prime is None:
            holder_prime = 2  # Default prime
        
        # Create lease structure
        import time
        lease_data = {
            "holder": holder_prime,
            "epoch": 0,  # Current epoch
            "ttl": 30,  # Time-to-live in epochs
            "quanta": quanta,
            "experience_delta": experience_delta,
            "timestamp": time.time()
        }
        
        # Encode as polyform if available
        lease_polyform = None
        if POLYFORM_AVAILABLE and PrimeFluxInt:
            try:
                salt = int(time.time() * 1000) % (2**32)
                lease_pfi = PrimeFluxInt(salt=salt)
                lease_pfi.encode(lease_data, salt=salt)
                lease_polyform = lease_pfi.to_dict() if hasattr(lease_pfi, 'to_dict') else {
                    "salt": lease_pfi.salt,
                    "payload": lease_pfi.payload
                }
            except Exception as e:
                # Fallback if polyform encoding fails
                lease_polyform = None
        
        # Update objects with ΦQ balance (store in metadata)
        try:
            # Create a signature for the quanta balance object
            import hashlib
            quanta_signature = hashlib.sha256(
                f"quanta_balance_{holder_prime}".encode('utf-8')
            ).hexdigest()
            
            # Try to get existing object
            existing_obj = self.objects.get_object(quanta_signature)
            
            if existing_obj:
                # Update existing object metadata
                existing_obj.metadata["quanta"] = existing_obj.metadata.get("quanta", 0) + quanta
                existing_obj.metadata["holder"] = holder_prime
                existing_obj.metadata["lease"] = lease_data
                existing_obj.metadata["polyform"] = lease_polyform
                existing_obj.count += 1
            else:
                # Create new object with quanta metadata
                from .objects.object_memory import Object
                quanta_obj = Object(
                    signature=quanta_signature,
                    triplets=[],
                    metadata={
                        "quanta": quanta,
                        "holder": holder_prime,
                        "lease": lease_data,
                        "polyform": lease_polyform,
                        "type": "quanta_balance"
                    }
                )
                self.objects.store_object(quanta_obj)
        except Exception as e:
            # Silently fail if objects update fails
            pass
        
        return {
            "holder": holder_prime,
            "epoch": 0,
            "ttl": 30,
            "quanta": quanta,
            "lease": lease_data,
            "polyform": lease_polyform,
            "polyform_enabled": lease_polyform is not None
        }
    
    def agora_etch(
        self,
        event_delta: dict[str, Any],
        quanta: int,
        agent_prime: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Compress event delta to polyform lease in Agora ecosystem.
        
        Updates objects.json with agent primes + yields.
        
        Args:
            event_delta: Event delta to compress
            quanta: Quanta amount
            agent_prime: Optional agent prime ID
            
        Returns:
            Agora etch result with polyform lease
        """
        if not AGORA_AVAILABLE or not AgoraEcosystem:
            return {
                "status": "error",
                "message": "Agora ecosystem not available"
            }
        
        if agent_prime is None:
            agent_prime = 2  # Default prime
        
        # Create lease structure
        import time
        lease_data = {
            "holder": agent_prime,
            "epoch": 0,
            "ttl": 30,
            "quanta": quanta,
            "event_delta": event_delta,
            "timestamp": time.time()
        }
        
        # Encode as polyform if available
        lease_polyform = None
        if POLYFORM_AVAILABLE and PrimeFluxInt:
            try:
                salt = int(time.time() * 1000) % (2**32)
                lease_pfi = PrimeFluxInt(salt=salt)
                lease_pfi.encode(lease_data, salt=salt)
                lease_polyform = lease_pfi.to_dict() if hasattr(lease_pfi, 'to_dict') else {
                    "salt": lease_pfi.salt,
                    "payload": lease_pfi.payload
                }
            except Exception:
                lease_polyform = None
        
        # Update objects with agent prime and yields
        try:
            import hashlib
            agent_signature = hashlib.sha256(
                f"agora_agent_{agent_prime}".encode('utf-8')
            ).hexdigest()
            
            existing_obj = self.objects.get_object(agent_signature)
            
            if existing_obj:
                # Update existing agent object
                existing_obj.metadata["agent_prime"] = agent_prime
                existing_obj.metadata["quanta"] = existing_obj.metadata.get("quanta", 0) + quanta
                existing_obj.metadata["lease"] = lease_data
                existing_obj.metadata["polyform"] = lease_polyform
                existing_obj.metadata["event_delta"] = event_delta
                existing_obj.count += 1
            else:
                # Create new agent object
                from .objects.object_memory import Object
                agent_obj = Object(
                    signature=agent_signature,
                    triplets=[],
                    metadata={
                        "agent_prime": agent_prime,
                        "quanta": quanta,
                        "lease": lease_data,
                        "polyform": lease_polyform,
                        "event_delta": event_delta,
                        "type": "agora_agent"
                    }
                )
                self.objects.store_object(agent_obj)
        except Exception:
            # Silently fail if objects update fails
            pass
        
        return {
            "status": "success",
            "agent_prime": agent_prime,
            "quanta": quanta,
            "lease": lease_data,
            "polyform": lease_polyform,
            "polyform_enabled": lease_polyform is not None
        }

