"""
Offline → Online Sync Queue.

Offline queue: ~/.apoptosis/sync_queue/

On reconnection:
- Capsules stream in timestamp order
- PFState rebuilds
- Experience merges from deltas
- Quanta recomputed

Offline Apop = full fidelity.
Online Apop = aggregation of capsules.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from ApopToSiS.runtime.capsules import Capsule


class SyncQueue:
    """
    Offline sync queue manager.
    
    Stores capsules for later synchronization.
    """

    def __init__(self, queue_dir: str = ".apoptosis/sync_queue") -> None:
        """
        Initialize sync queue.

        Args:
            queue_dir: Directory for sync queue
        """
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def enqueue_capsule(self, capsule: Capsule) -> None:
        """
        Add capsule to sync queue.
        
        Stores capsule for later network sync.

        Args:
            capsule: Capsule to queue
        """
        # Create filename from capsule ID and timestamp
        filename = f"{capsule.capsule_id}_{int(capsule.timestamp)}.json"
        filepath = self.queue_dir / filename
        
        # Write capsule
        with open(filepath, 'w') as f:
            json.dump(capsule.encode(), f, indent=2)

    def dequeue_capsules(self, max_count: int = 100) -> list[Capsule]:
        """
        Get capsules from sync queue.
        
        Returns capsules in timestamp order.

        Args:
            max_count: Maximum capsules to return

        Returns:
            List of capsules
        """
        capsules = []
        
        # Get all queue files
        queue_files = sorted(self.queue_dir.glob("*.json"))
        
        for filepath in queue_files[:max_count]:
            try:
                with open(filepath, 'r') as f:
                    capsule_data = json.load(f)
                
                capsule = Capsule.decode(capsule_data)
                capsules.append(capsule)
                
            except Exception:
                # Skip invalid files
                continue
        
        # Sort by timestamp
        capsules.sort(key=lambda c: c.timestamp)
        
        return capsules

    def clear_processed(self, capsule_ids: list[str]) -> None:
        """
        Remove processed capsules from queue.
        
        Args:
            capsule_ids: List of capsule IDs to remove
        """
        for filepath in self.queue_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    capsule_data = json.load(f)
                
                if capsule_data.get("capsule_id") in capsule_ids:
                    filepath.unlink()
                    
            except Exception:
                continue

    def get_queue_size(self) -> int:
        """
        Get number of capsules in queue.

        Returns:
            Queue size
        """
        return len(list(self.queue_dir.glob("*.json")))

