"""
Tests for Capsule Validator.
"""

import pytest
import json
from pathlib import Path
from core.capsule_validator import CapsuleValidator


def test_capsule_validator_load_v1_1():
    """Test loading v1.1 capsule and validating."""
    capsule_path = Path(__file__).parent.parent / "ECOSYSTEM_CAPSULE.json"
    
    if not capsule_path.exists():
        pytest.skip("ECOSYSTEM_CAPSULE.json not found")
    
    validator = CapsuleValidator.from_file(str(capsule_path))
    
    # Check version
    assert validator.capsule_dict.get("capsule_version") == "1.1"
    
    # Check fingerprint hex length is 64
    fingerprint = validator.fingerprint()
    assert len(fingerprint) == 64
    assert all(c in '0123456789abcdef' for c in fingerprint)
    
    # Validate
    assert validator.validate() is True


def test_capsule_validator_fingerprint():
    """Test fingerprint generation."""
    capsule_dict = {
        "capsule_version": "1.1",
        "ecosystem": {
            "apop": {"description": "test"}
        },
        "workflow": {
            "modes": []
        }
    }
    
    validator = CapsuleValidator(capsule_dict)
    fingerprint = validator.fingerprint()
    
    assert len(fingerprint) == 64
    assert isinstance(fingerprint, str)


def test_capsule_validator_validate():
    """Test validation logic."""
    # Valid capsule
    valid_capsule = {
        "capsule_version": "1.1",
        "ecosystem": {
            "apop": {"description": "test"}
        },
        "workflow": {
            "modes": [],
            "repo_handoffs": {}
        }
    }
    
    validator = CapsuleValidator(valid_capsule)
    assert validator.validate() is True
    
    # Invalid capsule (missing ecosystem)
    invalid_capsule = {
        "capsule_version": "1.1",
        "workflow": {}
    }
    
    validator = CapsuleValidator(invalid_capsule)
    assert validator.validate() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
