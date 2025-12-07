"""
Capsule Validator - Validates ecosystem capsule structure.

Validates ECOSYSTEM_CAPSULE.json structure and generates fingerprints
for integrity checking.
"""

from __future__ import annotations

import json
import hashlib
import warnings
from typing import Any, Dict, Optional
from pathlib import Path


class CapsuleValidator:
    """
    Validates ecosystem capsule structure.
    
    Checks for required keys (ecosystem, workflow) and warns on
    missing sub-keys like apop.
    """
    
    def __init__(self, capsule_dict: Dict[str, Any]):
        """
        Initialize validator with capsule dictionary.
        
        Args:
            capsule_dict: Capsule dictionary to validate
        """
        self.capsule_dict = capsule_dict
        self._fingerprint_cache: Optional[str] = None
    
    def fingerprint(self) -> str:
        """
        Generate SHA256 fingerprint of sorted JSON.
        
        Returns:
            Hex string of SHA256 hash (64 characters)
        """
        if self._fingerprint_cache is not None:
            return self._fingerprint_cache
        
        # Sort keys and convert to JSON string
        sorted_json = json.dumps(self.capsule_dict, sort_keys=True)
        
        # Generate SHA256 hash
        hash_obj = hashlib.sha256(sorted_json.encode('utf-8'))
        fingerprint = hash_obj.hexdigest()
        
        self._fingerprint_cache = fingerprint
        return fingerprint
    
    def validate(self) -> bool:
        """
        Validate capsule structure.
        
        Checks for required keys: ecosystem, workflow
        Warns on missing sub-keys like apop.
        
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["ecosystem", "workflow"]
        
        # Check required top-level keys
        for key in required_keys:
            if key not in self.capsule_dict:
                warnings.warn(f"Missing required key: {key}", UserWarning)
                return False
        
        # Check ecosystem sub-keys
        ecosystem = self.capsule_dict.get("ecosystem", {})
        expected_ecosystem_keys = ["apop", "primeflux", "quanta", "agora"]
        
        for key in expected_ecosystem_keys:
            if key not in ecosystem:
                warnings.warn(
                    f"Missing ecosystem sub-key: {key}",
                    UserWarning
                )
        
        # Check workflow structure
        workflow = self.capsule_dict.get("workflow", {})
        if "modes" not in workflow:
            warnings.warn("Missing workflow.modes", UserWarning)
        
        if "repo_handoffs" not in workflow:
            warnings.warn("Missing workflow.repo_handoffs", UserWarning)
        
        return True
    
    @classmethod
    def from_file(cls, file_path: str) -> "CapsuleValidator":
        """
        Load validator from JSON file.
        
        Args:
            file_path: Path to capsule JSON file
            
        Returns:
            CapsuleValidator instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Capsule file not found: {file_path}")
        
        with open(path, 'r') as f:
            capsule_dict = json.load(f)
        
        return cls(capsule_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert validator to dictionary."""
        return {
            "fingerprint": self.fingerprint(),
            "valid": self.validate(),
            "capsule_version": self.capsule_dict.get("capsule_version", "unknown")
        }
