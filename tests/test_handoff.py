"""
Tests for handoff manager and supervisor.
"""

from apop.runtime.handoff_manager import HandoffManager, HandoffManagerConfig
from apop.runtime.apop_supervisor import ApopSupervisor
from apop.runtime.context_capsule import ContextCapsule
from apop.core.icm import ICMState
from apop.core.lcm import LCMState


def test_handoff_manager_initialization() -> None:
    """Test HandoffManager can be initialized."""
    manager = HandoffManager()
    assert manager.eidos is not None
    assert manager.praxis is not None
    assert manager.aegis is not None


def test_handoff_manager_run_cycle() -> None:
    """Test HandoffManager can run a cycle."""
    manager = HandoffManager()
    capsule = ContextCapsule(
        icm_state=ICMState(),
        lcm_state=LCMState(),
    )
    result = manager.run_cycle(capsule)
    assert isinstance(result, ContextCapsule)


def test_apop_supervisor_initialization() -> None:
    """Test ApopSupervisor can be initialized."""
    supervisor = ApopSupervisor()
    assert supervisor.icm is not None
    assert supervisor.lcm is not None
    assert supervisor.handoff_manager is not None


def test_apop_supervisor_new_session() -> None:
    """Test ApopSupervisor new_session resets state."""
    supervisor = ApopSupervisor()
    supervisor.new_session()
    assert supervisor.icm is not None
    assert supervisor.lcm is not None


def test_apop_supervisor_process_input() -> None:
    """Test ApopSupervisor can process input."""
    supervisor = ApopSupervisor()
    capsule = supervisor.process_input("hello world")
    assert isinstance(capsule, ContextCapsule)

