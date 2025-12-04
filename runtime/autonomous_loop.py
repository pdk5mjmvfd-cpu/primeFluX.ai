"""
Background autonomous cognition loop for ApopToSiS.

Runs the cognitive engine + recursive learning engine without user input
to keep PF-state, identity, and experience evolving continuously.
"""

from __future__ import annotations

import time
import uuid
from threading import Thread, Event
from typing import Any, Optional

from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.cognitive.engine import CognitiveEngine
from ApopToSiS.runtime.recursive_engine import RecursiveLearningEngine

try:  # Optional import to avoid circular reference during tests
    from ApopToSiS.core.lcm import LCM
except Exception:  # pragma: no cover - optional during bootstrap
    LCM = None  # type: ignore


class AutonomousCognitionLoop:
    """
    Background autonomous cognition loop.

    Runs the cognitive engine autonomously to allow PF-state growth,
    identity formation, and experience accumulation without user input.
    """

    def __init__(
        self,
        state: PFState,
        context: Context,
        lcm: Optional["LCM"] = None,
        rle: Optional[RecursiveLearningEngine] = None,
        interval: float = 2.0,
    ) -> None:
        self.state = state
        self.context = context
        self.lcm = lcm
        self.interval = max(interval, 0.5)
        self.cog = CognitiveEngine()
        self.rle = rle
        self.running = False
        self.thread: Optional[Thread] = None
        self.stop_event = Event()
        self.last_cog_output: dict[str, Any] = {}
        self.last_learning_report: dict[str, Any] = {}

    def _generate_internal_tokens(self) -> list[str]:
        """
        Autonomous 'internal thoughts' tokens.

        Currently simple placeholders; can be expanded with PF cues later.
        """
        shell = getattr(self.state.current_shell, "name", "presence").lower()
        return ["...", "internal", "flux", f"shell_{shell}"]

    def _build_capsule(self, tokens: list[str]) -> Capsule:
        """Create a capsule either via LCM or via direct construction."""
        capsule: Capsule
        if self.lcm is not None:
            try:
                self.lcm.process_tokens(tokens)
                capsule_dict = self.lcm.generate_capsule()
                capsule = (
                    Capsule.decode(capsule_dict)
                    if isinstance(capsule_dict, dict)
                    else Capsule.from_tokens(tokens)
                )
            except Exception:
                capsule = Capsule.from_tokens(tokens)
        else:
            capsule = Capsule.from_tokens(tokens)

        # Ensure basic PF fields exist for downstream engines
        shell_value = getattr(self.state.current_shell, "value", 0)
        capsule.shell = capsule.shell or shell_value
        capsule.shell_state = capsule.shell
        if capsule.entropy <= 0:
            capsule.entropy = max(0.05, self.state.entropy * 0.9 + 0.05)
        if capsule.curvature <= 0:
            capsule.curvature = max(0.05, self.state.curvature * 0.9 + 0.05)
        if capsule.density <= 0:
            capsule.density = 0.1 + 0.05 * len(tokens)
        capsule.psi = capsule.psi or (capsule.entropy / (capsule.curvature + 1e-3))
        capsule.hamiltonian = capsule.hamiltonian or (capsule.curvature * 0.5 + capsule.entropy)
        capsule.timestamp = time.time()
        capsule.metadata.setdefault("source", "autonomous_loop")
        capsule.metadata["background_run_id"] = str(uuid.uuid4())
        capsule.agent_trace.append("AutonomousLoop")
        return capsule

    def _loop(self) -> None:
        """Internal worker loop."""
        while self.running and not self.stop_event.is_set():
            tokens = self._generate_internal_tokens()
            capsule = self._build_capsule(tokens)

            try:
                # Cognitive Engine
                cog_output = self.cog.process_capsule(capsule, self.state, self.context)
                enriched_output = {
                    "engine_output": cog_output.get("engine_output", cog_output.get("text", "")),
                    "flux_state": cog_output.get("flux_state"),
                    **cog_output,
                }
                capsule.metadata["background_cog"] = enriched_output
                self.state.last_cognitive_trace = enriched_output
                self.last_cog_output = enriched_output

                # Recursive Learning Engine (if provided)
                if self.rle is not None:
                    self.last_learning_report = self.rle.process(capsule, self.state)

                # Update PF State & context
                self.state.update_from_capsule(capsule)
                self.context.add_capsule(capsule)
            except Exception:
                # Background cognition should never interrupt the main runtime
                pass

            # Respect interval
            self.stop_event.wait(self.interval)

    def start(self) -> None:
        """Start the background cognition loop."""
        if self.running:
            return
        self.running = True
        self.stop_event.clear()
        self.thread = Thread(target=self._loop, name="AutonomousCognitionLoop", daemon=True)
        self.thread.start()

    def stop(self) -> None:
        """Stop the background cognition loop."""
        if not self.running:
            return
        self.running = False
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        self.thread = None

