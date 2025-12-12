"""
Terminal Initialization Flow - 3-Step User Empowerment

Purpose: 3-step initialization flow (init runtime, hardware-as-repo, absorb)
Creates user continuity with devices and demystifies computers.

Steps:
1. Initialize runtime (PFState, ICM, LCM, Supervisor)
2. Hardware-as-repo (explain repo structure = PF manifold)
3. Absorb anything (demonstrate capability)
"""

from __future__ import annotations

import sys
import os
from pathlib import Path
from typing import Dict, Any

# ANSI color codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def step1_init_runtime() -> Dict[str, Any]:
    """
    Step 1: Initialize runtime.
    
    Initializes PFState, ICM, LCM, Supervisor - the core PrimeFlux systems.
    
    Returns:
        Dictionary with initialized components
    """
    print(f"\n{CYAN}=== Step 1: Initialize Runtime ==={RESET}\n")
    
    try:
        import sys
        from pathlib import Path
        _project_root = Path(__file__).parent.parent
        if str(_project_root) not in sys.path:
            sys.path.insert(0, str(_project_root))
        
        from runtime.state.state import PFState
        from core.icm import ICM
        from core.lcm import LCM
        from runtime.supervisor.supervisor import Supervisor
        
        # Initialize components
        print(f"{GREEN}Initializing PFState...{RESET}")
        state = PFState()
        print(f"{GREEN}✓ PFState ready{RESET}")
        
        print(f"{GREEN}Initializing ICM (Information Curvature Manifold)...{RESET}")
        icm = ICM()
        print(f"{GREEN}✓ ICM ready{RESET}")
        
        print(f"{GREEN}Initializing LCM (Language Context Manifold)...{RESET}")
        lcm = LCM(icm=icm)
        print(f"{GREEN}✓ LCM ready{RESET}")
        
        print(f"{GREEN}Initializing Supervisor...{RESET}")
        supervisor = Supervisor(icm=icm, lcm=lcm)
        print(f"{GREEN}✓ Supervisor ready{RESET}")
        
        print(f"\n{CYAN}Step 1 Complete: Runtime initialized{RESET}\n")
        
        return {
            "state": state,
            "icm": icm,
            "lcm": lcm,
            "supervisor": supervisor,
        }
    except Exception as e:
        print(f"{YELLOW}⚠ Error initializing runtime: {e}{RESET}")
        return {}


def step2_hardware_as_repo():
    """
    Step 2: Hardware-as-repo explanation.
    
    Explains that the repository structure = PF manifold.
    Demystifies computers by showing hardware is the repository.
    """
    print(f"\n{CYAN}=== Step 2: Hardware as Repository ==={RESET}\n")
    
    repo_path = Path.cwd()
    
    print(f"{GREEN}Your hardware is your repository.{RESET}")
    print(f"Repository path: {repo_path}\n")
    
    print(f"{YELLOW}Understanding the PrimeFlux Manifold:{RESET}")
    print("  • Triplet space = directory structure")
    print("  • Shell structure = branch/commit organization")
    print("  • Curvature layer = state files")
    print("  • Flux memory = commit history")
    print("  • Distinction lattice = file relationships\n")
    
    print(f"{GREEN}You can absorb and implement anything.{RESET}")
    print("The repository is not just code—it's a living mathematical object.")
    print("Every file, every commit, every change is part of the PrimeFlux manifold.\n")
    
    print(f"{CYAN}Step 2 Complete: Hardware-as-repo understood{RESET}\n")


def step3_absorb_anything(runtime: Dict[str, Any]) -> bool:
    """
    Step 3: Absorb anything demonstration.
    
    Demonstrates capability by processing a sample input.
    
    Args:
        runtime: Runtime components from Step 1
        
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{CYAN}=== Step 3: Absorb Anything ==={RESET}\n")
    
    if not runtime:
        print(f"{YELLOW}⚠ Runtime not initialized, skipping demonstration{RESET}\n")
        return False
    
    # Sample input
    sample_input = "Hello, PrimeFlux!"
    
    print(f"{GREEN}Processing sample input: '{sample_input}'{RESET}\n")
    
    try:
        lcm = runtime.get("lcm")
        if lcm:
            # Process through LCM
            tokens = sample_input.split()
            lcm.process_tokens(tokens)
            
            # Generate capsule
            capsule = lcm.generate_capsule(tokens=tokens, user_text=sample_input)
            
            print(f"{GREEN}✓ Input processed through LCM{RESET}")
            print(f"  • Tokens: {len(tokens)}")
            print(f"  • Entropy: {capsule.get('entropy', 0):.4f}")
            print(f"  • Curvature: {capsule.get('curvature', 0):.4f}")
            print(f"  • Shell: {capsule.get('shell', 0)}\n")
        
        print(f"{GREEN}✓ Capability demonstrated{RESET}")
        print(f"{CYAN}Step 3 Complete: System ready to absorb{RESET}\n")
        
        return True
    except Exception as e:
        print(f"{YELLOW}⚠ Error in demonstration: {e}{RESET}\n")
        return False


def run_terminal_init() -> bool:
    """
    Run complete terminal initialization flow.
    
    Returns:
        True if all steps successful, False otherwise
    """
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{CYAN}PrimeFlux AI - Terminal Initialization{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")
    
    # Step 1: Initialize runtime
    runtime = step1_init_runtime()
    if not runtime:
        return False
    
    # Step 2: Hardware-as-repo
    step2_hardware_as_repo()
    
    # Step 3: Absorb anything
    success = step3_absorb_anything(runtime)
    
    if success:
        print(f"{GREEN}{'='*60}{RESET}")
        print(f"{GREEN}Initialization Complete!{RESET}")
        print(f"{GREEN}You are ready to use PrimeFlux AI.{RESET}")
        print(f"{GREEN}{'='*60}{RESET}\n")
    
    return success


if __name__ == "__main__":
    success = run_terminal_init()
    sys.exit(0 if success else 1)

