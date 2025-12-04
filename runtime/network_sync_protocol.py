"""
Network Sync Protocol (NSP) — governs how capsules move between devices.

NSP/1.0 — direct capsule push
NSP/1.1 — batch send
NSP/1.2 — capsule streaming
NSP/2.0 — PF-curvature routing (future)

Sequence:
1. Device sends capsule
2. Receiver authenticates
3. LCM integrates
4. Experience updates
5. Quanta verifies compression
6. Supervisor updates PFState

Network = Capsule Stream, not shared context.
"""

from __future__ import annotations

from typing import Any
from enum import Enum
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.device_identity import DeviceIdentity


class NSPVersion(Enum):
    """Network Sync Protocol versions."""
    V1_0 = "1.0"  # Direct capsule push
    V1_1 = "1.1"  # Batch send
    V1_2 = "1.2"  # Capsule streaming
    V2_0 = "2.0"  # PF-curvature routing (future)


class NSPSyncRequest:
    """
    NSP sync request.
    
    Used to request capsules from another device.
    """

    def __init__(
        self,
        device_id: str,
        from_timestamp: float = 0.0,
        to_timestamp: float | None = None,
        max_capsules: int = 100
    ) -> None:
        """
        Initialize sync request.

        Args:
            device_id: Target device ID
            from_timestamp: Start timestamp
            to_timestamp: End timestamp (None = now)
            max_capsules: Maximum capsules to return
        """
        self.device_id = device_id
        self.from_timestamp = from_timestamp
        self.to_timestamp = to_timestamp
        self.max_capsules = max_capsules
        self.version = NSPVersion.V1_2.value

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "device_id": self.device_id,
            "from_timestamp": self.from_timestamp,
            "to_timestamp": self.to_timestamp,
            "max_capsules": self.max_capsules,
        }


class NSPSyncResponse:
    """
    NSP sync response.
    
    Contains capsules and metadata.
    """

    def __init__(
        self,
        capsules: list[Capsule],
        device_id: str,
        total_count: int = 0
    ) -> None:
        """
        Initialize sync response.

        Args:
            capsules: List of capsules
            device_id: Source device ID
            total_count: Total capsules available
        """
        self.capsules = capsules
        self.device_id = device_id
        self.total_count = total_count
        self.version = NSPVersion.V1_2.value

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "device_id": self.device_id,
            "total_count": self.total_count,
            "capsules": [c.encode() for c in self.capsules],
        }


class NetworkSyncProtocol:
    """
    Network Sync Protocol handler.
    
    Manages capsule synchronization between devices.
    """

    def __init__(self, device_identity: DeviceIdentity) -> None:
        """
        Initialize NSP handler.

        Args:
            device_identity: Device identity
        """
        self.device_identity = device_identity
        self.version = NSPVersion.V1_2

    def validate_capsule(self, capsule: Capsule) -> tuple[bool, str]:
        """
        Validate incoming capsule.
        
        Checks:
        - Device ID present
        - Capsule ID present
        - Timestamp valid
        - Quanta hash present

        Args:
            capsule: Capsule to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not capsule.device_id:
            return False, "Missing device_id"
        
        if not capsule.capsule_id:
            return False, "Missing capsule_id"
        
        if capsule.timestamp <= 0:
            return False, "Invalid timestamp"
        
        if not capsule.quanta_hash:
            return False, "Missing quanta_hash"
        
        return True, ""

    def prepare_capsule_for_send(self, capsule: Capsule) -> dict[str, Any]:
        """
        Prepare capsule for network transmission.
        
        Ensures all network fields are set.

        Args:
            capsule: Capsule to prepare

        Returns:
            Encoded capsule dictionary
        """
        # Ensure network fields are set
        if not capsule.device_id:
            capsule.device_id = self.device_identity.get_device_id()
        
        # Encode with network fields
        encoded = capsule.encode()
        
        return encoded

    def receive_capsule(self, capsule_data: dict[str, Any]) -> Capsule | None:
        """
        Receive and decode capsule from network.
        
        Validates and decodes capsule.

        Args:
            capsule_data: Encoded capsule dictionary

        Returns:
            Decoded capsule or None if invalid
        """
        try:
            capsule = Capsule.decode(capsule_data)
            
            # Validate
            is_valid, error = self.validate_capsule(capsule)
            if not is_valid:
                return None
            
            return capsule
            
        except Exception:
            return None

