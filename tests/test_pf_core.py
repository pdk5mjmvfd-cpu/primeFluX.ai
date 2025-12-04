"""
Tests for PrimeFlux core operations.
"""

from apop.core.pf_core import is_rail_plus, is_rail_minus, compute_flux, compute_curvature


def test_pf_core_stubs() -> None:
    """Test that PF core stub functions work correctly."""
    assert isinstance(is_rail_plus(5), bool)
    assert isinstance(is_rail_minus(5), bool)
    
    result = compute_flux(1.0)
    assert hasattr(result, "value")
    assert hasattr(result, "rail")
    assert hasattr(result, "metadata")
    
    curvature = compute_curvature([1.0, 2.0, 3.0])
    assert isinstance(curvature, float)

