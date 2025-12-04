#!/usr/bin/env python3
"""
Example: How to Run a Full Local PF Cycle

This is the complete offline cognition loop:
1. tokenization
2. triplet analysis
3. curvature estimation
4. shell transition
5. agent routing
6. capsule rewrite
7. PFState update
8. QuantaCoin update
9. experience integration

This is Apop thinking.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.boot import boot_apop, create_first_memory


def run_full_pf_cycle():
    """Run a complete PF cognition cycle."""
    print("=== Running Full Local PF Cycle ===\n")
    
    # Boot the system
    print("Booting ApopToSiS v3...")
    runtime = boot_apop()
    print("✓ Boot complete\n")
    
    # Process input
    text = "Apop, what should I do today?"
    print(f"Input: '{text}'\n")
    
    print("Processing through PF cycle...")
    print("  1. Tokenization...")
    print("  2. Triplet analysis...")
    print("  3. Curvature estimation...")
    print("  4. Shell transition...")
    print("  5. Agent routing...")
    print("  6. Capsule rewrite...")
    print("  7. PFState update...")
    print("  8. QuantaCoin update...")
    print("  9. Experience integration...\n")
    
    result = create_first_memory(runtime, text)
    
    print("=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Shell: {result.get('shell', 'N/A')}")
    print(f"Curvature: {result.get('curvature', 0):.4f}")
    print(f"Entropy: {result.get('entropy', 0):.4f}")
    print(f"QuantaCoin: {result.get('quanta_minted', 0):.4f}")
    print(f"Routed Agent: {result.get('routed_agent', 'N/A')}")
    print("=" * 60)
    
    return result


def run_multiple_cycles():
    """Run multiple PF cycles to show experience accumulation."""
    print("\n=== Running Multiple PF Cycles ===\n")
    
    runtime = boot_apop()
    
    inputs = [
        "Hello Apop",
        "What is PrimeFlux?",
        "How does curvature work?",
    ]
    
    for i, text in enumerate(inputs, 1):
        print(f"\nCycle {i}: '{text}'")
        result = create_first_memory(runtime, text)
        print(f"  → Shell: {result.get('shell')}, "
              f"Curvature: {result.get('curvature', 0):.4f}, "
              f"Agent: {result.get('routed_agent', 'N/A')}")
    
    # Get experience summary
    print("\n=== Experience Summary ===")
    experience = runtime.get("experience_manager")
    if experience:
        summary = experience.summarize()
        print(f"Habits: {len(summary.get('habits', {}))}")
        print(f"Shortcuts: {len(summary.get('shortcuts', {}))}")
        print(f"Objects: {len(summary.get('objects', {}))}")
        print(f"Skills: {len(summary.get('skills', {}))}")


if __name__ == "__main__":
    # Single cycle
    result = run_full_pf_cycle()
    
    # Multiple cycles
    run_multiple_cycles()
    
    print("\n✓ Full PF cycle complete!")

