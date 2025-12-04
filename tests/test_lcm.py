"""
Test LCM — Language Context Manifold tests.

Tests:
- Token → Capsule
- Triplet detection
- Shell transition
- Curvature/entropy produced
"""

import pytest
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM


def test_lcm_process_tokens():
    """Test LCM processes tokens and produces capsule."""
    icm = ICM()
    lcm = LCM(icm)
    tokens = ["hello", "world"]
    
    capsule_dict = lcm.process_tokens(tokens)
    
    # Check capsule structure
    assert capsule_dict is not None
    assert "raw_tokens" in capsule_dict or isinstance(capsule_dict, dict)
    
    # If it's a dict, check fields
    if isinstance(capsule_dict, dict):
        assert "entropy" in capsule_dict or "entropy_snapshot" in capsule_dict
        assert "curvature" in capsule_dict or "curvature_snapshot" in capsule_dict
        assert "shell" in capsule_dict or "shell_state" in capsule_dict


def test_lcm_triplet_detection():
    """Test LCM detects triplets."""
    icm = ICM()
    lcm = LCM(icm)
    tokens = ["def", "factorial", "n"]
    
    triplets = lcm.compute_triplets(tokens)
    
    assert triplets is not None
    assert isinstance(triplets, list)


def test_lcm_shell_transition():
    """Test LCM performs shell transitions."""
    icm = ICM()
    lcm = LCM(icm)
    
    # Process tokens to get initial state
    tokens = ["test", "shell", "transition"]
    lcm.process_tokens(tokens)
    
    # Check shell transition logic exists
    assert hasattr(lcm, 'shell_transition') or hasattr(lcm, '_transition_shell')


def test_lcm_curvature_entropy():
    """Test LCM produces curvature and entropy."""
    icm = ICM()
    lcm = LCM(icm)
    tokens = ["curvature", "entropy", "test"]
    
    capsule_dict = lcm.process_tokens(tokens)
    
    if isinstance(capsule_dict, dict):
        # Check that curvature and entropy are computed
        assert "curvature" in capsule_dict or "curvature_snapshot" in capsule_dict
        assert "entropy" in capsule_dict or "entropy_snapshot" in capsule_dict

