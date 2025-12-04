"""
Tests for ICM and LCM modules.
"""

from apop.core.icm import ICM, ICMState
from apop.core.lcm import LCM, LCMState


def test_icm_initialization() -> None:
    """Test ICM can be initialized."""
    icm = ICM()
    assert icm.state is not None
    assert isinstance(icm.state, ICMState)


def test_icm_update() -> None:
    """Test ICM update functionality."""
    icm = ICM()
    initial_len = len(icm.state.values)
    icm.update([1.0, 2.0, 3.0])
    assert len(icm.state.values) == initial_len + 3


def test_icm_curvature() -> None:
    """Test ICM curvature computation."""
    icm = ICM()
    curvature = icm.curvature()
    assert isinstance(curvature, float)


def test_lcm_initialization() -> None:
    """Test LCM can be initialized."""
    lcm = LCM()
    assert lcm.state is not None
    assert isinstance(lcm.state, LCMState)


def test_lcm_integrate_text() -> None:
    """Test LCM text integration."""
    lcm = LCM()
    initial_len = len(lcm.state.tokens)
    lcm.integrate_text("hello world")
    assert len(lcm.state.tokens) == initial_len + 2


def test_lcm_curvature() -> None:
    """Test LCM curvature computation."""
    lcm = LCM()
    curvature = lcm.curvature()
    assert isinstance(curvature, float)

