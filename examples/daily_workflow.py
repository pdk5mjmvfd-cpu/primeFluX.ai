#!/usr/bin/env python3
"""
Example: Daily Workflow (Recommended)

The recommended way to operate Apop locally:

1. user types text
2. LCM → capsule
3. Supervisor routes
4. agent transforms capsule
5. LCM rebuilds capsule
6. PFState updates
7. Experience graph updates
8. QuantaCoin minted
9. capsule saved (history)
10. LLM invoked if needed
11. network sync queued (offline)

This is the exact internal loop used later in PF-DCM.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.boot import boot_apop, create_first_memory
from ApopToSiS.runtime.sync_queue import SyncQueue
from ApopToSiS.runtime.capsules import Capsule


def daily_workflow():
    """Demonstrate daily workflow."""
    print("=== Daily Workflow Example ===\n")
    
    # Boot system
    print("1. Booting ApopToSiS v3...")
    runtime = boot_apop()
    print("   ✓ Boot complete")
    
    # Initialize sync queue
    sync_queue = SyncQueue()
    
    # Simulate user interactions
    user_inputs = [
        "Hello Apop",
        "What is PrimeFlux?",
        "How does curvature work?",
    ]
    
    for i, user_text in enumerate(user_inputs, 1):
        print(f"\n--- Interaction {i} ---")
        print(f"User: '{user_text}'")
        
        # 2. LCM → capsule
        print("   2. LCM → capsule...")
        result = create_first_memory(runtime, user_text)
        capsule_data = result.get('first_capsule', {})
        capsule = Capsule.decode(capsule_data) if isinstance(capsule_data, dict) else None
        
        if capsule:
            print(f"      Shell: {capsule.shell}, Curvature: {capsule.curvature:.4f}")
        
        # 3-8. Already handled by create_first_memory
        print(f"   3-8. Processing complete...")
        print(f"      Routed to: {result.get('routed_agent', 'N/A')}")
        print(f"      QuantaCoin: {result.get('quanta_minted', 0):.4f}")
        
        # 9. Save capsule to history
        print("   9. Saving capsule to history...")
        if capsule:
            # In production, save to persistent storage
            print("      ✓ Saved to history")
        
        # 10. LLM invoked if needed (optional)
        print("   10. LLM invocation (optional)...")
        # In production, call LLM here if needed
        print("      (Skipped in this example)")
        
        # 11. Network sync queued (offline)
        print("   11. Queuing for network sync...")
        if capsule:
            sync_queue.enqueue_capsule(capsule)
            print(f"      ✓ Queued (queue size: {sync_queue.get_queue_size()})")
    
    # Show experience summary
    print("\n=== Experience Summary ===")
    experience = runtime.get("experience_manager")
    if experience:
        summary = experience.summarize()
        print(f"Habits: {len(summary.get('habits', {}))}")
        print(f"Shortcuts: {len(summary.get('shortcuts', {}))}")
        print(f"Objects: {len(summary.get('objects', {}))}")
        print(f"Skills: {len(summary.get('skills', {}))}")
    
    # Show sync queue status
    print("\n=== Sync Queue Status ===")
    print(f"Queued capsules: {sync_queue.get_queue_size()}")
    print("(Ready for network sync when online)")
    
    print("\n✓ Daily workflow complete!")


if __name__ == "__main__":
    daily_workflow()

