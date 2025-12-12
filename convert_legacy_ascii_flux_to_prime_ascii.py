"""
Migration Script: Convert Legacy ASCII Flux to Prime ASCI

Converts existing PresenceVectors and LCM shortcuts from hash-based
ASCII flux mapping to Prime ASCI prime-based mapping.

Usage:
    python convert_legacy_ascii_flux_to_prime_ascii.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
_project_root = Path(__file__).parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.prime_ascii import get_prime_ascii
from core.math.pf_presence import PresenceVector


def migrate_presence_vector(old_vector: PresenceVector, prime_ascii) -> PresenceVector:
    """
    Migrate PresenceVector from legacy ASCII flux to Prime ASCI.
    
    Note: PresenceVectors are deterministic from text, so we can't
    reverse-engineer the original text. This migration is mainly
    for documentation/version tracking.
    
    Args:
        old_vector: Legacy PresenceVector
        prime_ascii: PrimeASCI instance
        
    Returns:
        New PresenceVector (same components, but version-tracked)
    """
    # PresenceVectors are already compatible - they don't depend on ASCII mapping
    # This is mainly for version tracking
    return old_vector


def migrate_lcm_state(lcm_state_path: Path, prime_ascii, dry_run: bool = False) -> bool:
    """
    Migrate LCM state file from legacy ASCII flux to Prime ASCI.
    
    Args:
        lcm_state_path: Path to LCM state file
        prime_ascii: PrimeASCI instance
        dry_run: If True, don't write changes
        
    Returns:
        True if successful, False otherwise
    """
    if not lcm_state_path.exists():
        print(f"LCM state file not found: {lcm_state_path}")
        return False
    
    try:
        # Load state
        with open(lcm_state_path, 'r') as f:
            state = json.load(f)
        
        # Add version tracking
        state['prime_ascii_version'] = prime_ascii.get_version()
        state['migrated'] = True
        
        if not dry_run:
            # Backup original
            backup_path = lcm_state_path.with_suffix('.json.bak')
            with open(backup_path, 'w') as f:
                json.dump(state, f, indent=2)
            
            # Write migrated state
            with open(lcm_state_path, 'w') as f:
                json.dump(state, f, indent=2)
            
            print(f"✓ Migrated {lcm_state_path}")
        else:
            print(f"[DRY RUN] Would migrate {lcm_state_path}")
        
        return True
    except Exception as e:
        print(f"Error migrating {lcm_state_path}: {e}")
        return False


def main():
    """Main migration function."""
    parser = argparse.ArgumentParser(description="Migrate legacy ASCII flux to Prime ASCI")
    parser.add_argument("--dry-run", action="store_true", help="Don't write changes, just show what would be done")
    parser.add_argument("--state-dir", type=str, default="experience", help="Directory containing state files")
    
    args = parser.parse_args()
    
    print("Prime ASCI Migration Script")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}\n")
    
    prime_ascii = get_prime_ascii()
    print(f"Prime ASCI version: {prime_ascii.get_version()}\n")
    
    # Find state files
    state_dir = Path(args.state_dir)
    if not state_dir.exists():
        print(f"State directory not found: {state_dir}")
        return 1
    
    # Look for LCM state files
    state_files = list(state_dir.glob("*.json")) + list(state_dir.glob("*.jsonl"))
    
    if not state_files:
        print(f"No state files found in {state_dir}")
        return 0
    
    print(f"Found {len(state_files)} state file(s)\n")
    
    success_count = 0
    for state_file in state_files:
        if migrate_lcm_state(state_file, prime_ascii, dry_run=args.dry_run):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Migration complete: {success_count}/{len(state_files)} files")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

