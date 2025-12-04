"""
Device & Instance Identity Model.

Each device is assigned:
- device_id = SHA256(public_key) - permanent
- instance_id = UUID + boot_timestamp - new each boot

Capsules must include both.
PFState uses device_id precedence.
"""

from __future__ import annotations

import hashlib
import uuid
import time
from typing import Optional


class DeviceIdentity:
    """
    Device and instance identity management.
    
    Device ID = permanent (SHA256 of public key)
    Instance ID = new each boot (UUID + boot_timestamp)
    """

    def __init__(self, public_key: Optional[str] = None, device_id: Optional[str] = None) -> None:
        """
        Initialize device identity.

        Args:
            public_key: Optional public key (if None, generates from hostname)
            device_id: Optional existing device ID
        """
        if device_id:
            self.device_id = device_id
        else:
            # Generate device_id from public_key or hostname
            if public_key:
                key_data = public_key.encode('utf-8')
            else:
                import socket
                key_data = socket.gethostname().encode('utf-8')
            
            self.device_id = hashlib.sha256(key_data).hexdigest()
        
        # Generate instance_id (new each boot)
        self.instance_id = self._generate_instance_id()
        self.boot_timestamp = time.time()

    def _generate_instance_id(self) -> str:
        """
        Generate instance ID (UUID + boot_timestamp).

        Returns:
            Instance ID string
        """
        instance_uuid = str(uuid.uuid4())
        boot_ts = str(int(time.time()))
        return f"{instance_uuid}_{boot_ts}"

    def get_device_id(self) -> str:
        """
        Get permanent device ID.

        Returns:
            Device ID (SHA256 hex)
        """
        return self.device_id

    def get_instance_id(self) -> str:
        """
        Get current instance ID.

        Returns:
            Instance ID
        """
        return self.instance_id

    def to_dict(self) -> dict[str, str]:
        """
        Convert to dictionary.

        Returns:
            Dictionary with device and instance IDs
        """
        return {
            "device_id": self.device_id,
            "instance_id": self.instance_id,
            "boot_timestamp": self.boot_timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "DeviceIdentity":
        """
        Create from dictionary.

        Args:
            data: Dictionary with device_id and instance_id

        Returns:
            DeviceIdentity instance
        """
        instance = cls(device_id=data.get("device_id"))
        instance.instance_id = data.get("instance_id", instance.instance_id)
        instance.boot_timestamp = data.get("boot_timestamp", time.time())
        return instance


# Global device identity (singleton)
_device_identity: Optional[DeviceIdentity] = None


def get_device_identity() -> DeviceIdentity:
    """
    Get global device identity (creates if needed).

    Returns:
        DeviceIdentity instance
    """
    global _device_identity
    if _device_identity is None:
        _device_identity = DeviceIdentity()
    return _device_identity


def set_device_identity(identity: DeviceIdentity) -> None:
    """
    Set global device identity.

    Args:
        identity: DeviceIdentity instance
    """
    global _device_identity
    _device_identity = identity

