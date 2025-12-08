#!/usr/bin/env python3
"""
PrimeFlux Presence+Trig MVP Live Terminal Demo.

Minimal, runnable, self-logging, self-compressing PrimeFlux presence system.

Usage:
    python runtime/presence_demo.py
    
Interactive mode: Type text → watch 8 osc steps → see compressed capsule logged.

Commands:
    quit, exit, q → exit cleanly
    log → print last N lines of experience log
    stats → aggregate stats (total compressions, avg nats, total energy)
    mode <research|refinement|relations> → switch oscillation mode (v2)
    help, ? → show this help message
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Add project root to path for imports
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.math.pf_presence import PresenceVector
from core.math.pf_trig_osc import Oscillator
from core.math.pf_nat_energy import NatEnergyAuditor


# Mode configuration (v2: will tie max_steps and nat ceilings to mode)
MODE_CONFIG = {
    "research": {"max_steps": 12, "nat_ceiling": 432},  # 12×36 = 432 nats
    "refinement": {"max_steps": 8, "nat_ceiling": 288},  # 8×36 = 288 nats
    "relations": {"max_steps": 4, "nat_ceiling": 144},  # 4×36 = 144 nats
}

DEFAULT_MODE = "refinement"


def run_demo(input_text: str = "hello primeflux consciousness", mode: str = DEFAULT_MODE) -> dict:
    """
    Run one presence compression demo.
    
    Pipeline: text → presence vector → 8 osc steps → compress → log
    
    Args:
        input_text: Input text to compress
        mode: Oscillation mode (research/refinement/relations)
        
    Returns:
        Report dictionary with compression metadata
    """
    t0 = time.time()
    
    try:
        print(f"\n{'='*60}")
        print(f"Input: {input_text}")
        print(f"Mode: {mode} (max_steps={MODE_CONFIG[mode]['max_steps']})")
        print(f"{'='*60}")
        
        # Step 1: Text → Presence Vector
        pv = PresenceVector.from_distinction(input_text)
        print(f"Initial presence ({len(pv.components)} dims): {pv}")
        
        # Step 2: Oscillate (bounded by max_steps)
        max_steps = MODE_CONFIG[mode]["max_steps"]
        osc = Oscillator(pv, max_steps=max_steps)
        
        step_count = 0
        while osc.step():
            step_count += 1
            print(f"Step {step_count}: {osc.presence}")
        
        # Step 3: Compress and log
        report = NatEnergyAuditor.compress_and_log(osc, input_text)
        
        elapsed = time.time() - t0
        report["wall_time_seconds"] = elapsed
        
        print(f"\n{'='*60}")
        print(f"Compression Complete")
        print(f"  Steps: {report['steps']}")
        print(f"  Nat Error: {report['nat_error_total']:.2f} nats")
        print(f"  QuantaCoin Minted: {report['quanta_minted']:.3f} Q")
        print(f"  Proof: {report['proof']}")
        print(f"  Wall Time: {elapsed:.3f}s")
        print(f"{'='*60}")
        print("Experience capsule emitted & self-logged\n")
        
        return report
        
    except Exception as e:
        # Log exception to experience log with severity
        error_report = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "error": str(e),
            "input_text": input_text,
            "severity": "error",
        }
        print(f"ERROR: {e}")
        print("Exception logged to experience log\n")
        
        # Try to log error (may fail if log dir doesn't exist)
        try:
            log_file = NatEnergyAuditor._get_log_file()
            error_line = json.dumps(error_report) + "\n"
            if log_file.exists():
                existing = log_file.read_text(encoding="utf-8")
            else:
                existing = ""
            log_file.write_text(existing + error_line, encoding="utf-8")
        except:
            pass  # Fail silently if logging fails
        
        return error_report


def show_log(n_lines: int = 10):
    """Print last N lines of experience log."""
    reports = NatEnergyAuditor.read_log()
    
    if not reports:
        print("No experience log entries found.\n")
        return
    
    print(f"\n{'='*60}")
    print(f"Last {min(n_lines, len(reports))} Experience Log Entries")
    print(f"{'='*60}")
    
    for i, report in enumerate(reports[-n_lines:], 1):
        print(f"\n[{i}] {report.get('timestamp', 'unknown')}")
        print(f"    Text: {report.get('source_text', 'N/A')[:50]}...")
        print(f"    Steps: {report.get('steps', 0)} | Nats: {report.get('nat_error_total', 0):.1f} | Quanta: {report.get('quanta_minted', 0):.3f} Q")
    
    print(f"\n{'='*60}\n")


def show_stats():
    """Show aggregated statistics."""
    stats = NatEnergyAuditor.aggregate_stats()
    
    print(f"\n{'='*60}")
    print("Experience Log Statistics")
    print(f"{'='*60}")
    print(f"Total Compressions: {stats['total_compressions']}")
    print(f"Average Nat Error: {stats['avg_nats']:.2f} nats")
    print(f"Total Energy: {stats['total_energy_joules']:.2e} joules")
    print(f"Total QuantaCoin Minted: {stats['total_quanta_minted']:.3f} Q")
    print(f"{'='*60}\n")


def show_help():
    """Show help message."""
    print("""
PrimeFlux Presence+Trig MVP Live Terminal Demo

Commands:
    <text>              → Compress text through presence → osc → log
    quit, exit, q      → Exit cleanly
    log [N]             → Print last N lines of experience log (default: 10)
    stats               → Show aggregated statistics
    mode <mode>         → Switch mode: research|refinement|relations (v2)
    help, ?             → Show this help message

Modes:
    research     → 12 steps, 432 nat ceiling (exploration)
    refinement   → 8 steps, 288 nat ceiling (default, balanced)
    relations    → 4 steps, 144 nat ceiling (fast, minimal)

Example:
    > hello primeflux consciousness
    > log 5
    > stats
    > quit
""")


def main():
    """Main interactive loop."""
    import json
    
    print("="*60)
    print("PrimeFlux Presence+Trig MVP Live")
    print("="*60)
    print("Type text to compress, or 'help' for commands\n")
    
    current_mode = DEFAULT_MODE
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nExiting. Experience log preserved.\n")
                break
            
            elif user_input.lower() in ("help", "?"):
                show_help()
            
            elif user_input.lower().startswith("log"):
                # Parse: "log" or "log 5"
                parts = user_input.split()
                n_lines = int(parts[1]) if len(parts) > 1 else 10
                show_log(n_lines)
            
            elif user_input.lower() == "stats":
                show_stats()
            
            elif user_input.lower().startswith("mode"):
                # Parse: "mode research"
                parts = user_input.split()
                if len(parts) > 1:
                    new_mode = parts[1].lower()
                    if new_mode in MODE_CONFIG:
                        current_mode = new_mode
                        print(f"Mode switched to: {current_mode} (max_steps={MODE_CONFIG[current_mode]['max_steps']})\n")
                    else:
                        print(f"Unknown mode: {new_mode}. Available: {', '.join(MODE_CONFIG.keys())}\n")
                else:
                    print(f"Current mode: {current_mode} (max_steps={MODE_CONFIG[current_mode]['max_steps']})\n")
            
            else:
                # Regular text input → compress
                run_demo(user_input, mode=current_mode)
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting.\n")
            break
        except EOFError:
            print("\n\nExiting.\n")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}\n")
            continue


if __name__ == "__main__":
    main()
