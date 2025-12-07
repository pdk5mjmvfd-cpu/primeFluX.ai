#!/usr/bin/env python3
"""
Apop CLI: Offline PF agent.

Usage: 
    python bin/apop-cli.py "query" [eidos|praxis|aegis] [mode] [--presence-off]
    
Examples:
    python bin/apop-cli.py "Explain ζ-duality in PF terms" eidos
    python bin/apop-cli.py "Compute rail flux" praxis refinement
    python bin/apop-cli.py "Any query" --presence-off
"""

import sys
import os
import hashlib
import json
import math
from pathlib import Path
from datetime import datetime
from collections import Counter

# Add parent directory to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Import PrimeFlux first shell logic
try:
    from core.first_shell import (
        parse_distinction_packet,
        check_reversibility,
        process_first_shell,
        integrate_with_cli
    )
    PRIMEFLUX_AVAILABLE = True
except ImportError:
    PRIMEFLUX_AVAILABLE = False

# Try to import Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    ollama = None

CAPSULE = {
    "version": "1.1",
    "mode": "refinement",
    "principles": ["distinction", "rails", "flux", "reversibility"]
}


def entropy(text):
    """Calculate Shannon entropy in nats."""
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    return -sum((c / total) * math.log(c / total) for c in counts.values() if c > 0)


def check_reversible(inp, out):
    """
    Check reversibility: output entropy <= input entropy + ln(10).
    
    Canonical threshold: K = ln(10) ≈ 2.302585 nats
    
    Uses PrimeFlux check_reversibility if available.
    """
    if PRIMEFLUX_AVAILABLE:
        result = check_reversibility(inp, out)
        return result["passed"]
    
    # Fallback
    inp_entropy = entropy(inp)
    out_entropy = entropy(out)
    threshold = math.log(10)  # Canonical threshold
    return out_entropy <= inp_entropy + threshold


def parse_distinction(text, mode='refinement', presence_on=True):
    """
    Parse distinction packet with trig modes, presence op, 2/5 salts, pi/e secrets.
    
    Uses PrimeFlux first shell logic if available.
    
    Returns:
        Dictionary with phase, mod25, g_pf, curv_internal, agent, shell info
    """
    if PRIMEFLUX_AVAILABLE:
        # Use PrimeFlux first shell logic
        return parse_distinction_packet(text, mode, presence_on)
    
    # Fallback: simple parsing
    h = hashlib.sha256(text.encode()).digest()
    phase = (int.from_bytes(h[:2], 'big') % 200 / 100.0) - 1  # [-1,1]
    mod25 = phase % (2 * 5)  # 2/5 salt
    
    # Trig mode mapping
    if mode == 'research':
        trig = math.sin
    elif mode == 'refinement':
        trig = math.cos
    elif mode == 'relations':
        trig = math.tan
    else:
        trig = math.cos  # Default
    
    # Presence operator: g_PF(phase, mode) = trig(mode) if presence_on else 0
    g_pf = trig(phase) if presence_on else 0.0
    
    # pi/e secret curvature (internal, not exposed)
    curv_internal = (math.pi - math.e) * abs(phase) if g_pf != 0 else 0.0
    
    # Agent routing based on phase
    agent = "eidos" if abs(phase) > 0.7 else ("aegis" if phase < 0 else "praxis")
    
    return {
        "phase": phase,
        "mod25": mod25,
        "g_pf": g_pf,
        "curv_internal": curv_internal,
        "agent": agent,
        "mode": mode,
        "current_shell": 0,  # PRESENCE
        "next_shell": 2  # MEASUREMENT
    }


def query_apop(prompt, agent=None, mode='refinement', presence_on=True, log=True):
    """
    Query Apop with full PF pipeline.
    
    Args:
        prompt: User query
        agent: Optional agent override
        mode: Mode (research/refinement/relations)
        presence_on: Whether presence operator is enabled
        log: Whether to log interaction
    """
    # Parse distinction packet
    pkt = parse_distinction(prompt, mode, presence_on)
    agent = agent or pkt['agent']
    
    # Display packet info
    print(f"\n🌀 [{agent.upper()}] Phase={pkt['phase']:.3f} | Mod2/5={pkt['mod25']:.3f} | g_PF={pkt['g_pf']:.3f}")
    print(f"   Mode: {mode} | Presence: {'On' if presence_on else 'Off'}")
    
    # If presence off, skip event spaces
    if pkt['g_pf'] == 0:
        output = "[Event Spaces Off: Presence operator disabled mode trig.]"
        quanta = 0.0
        reversible = False
    else:
        # Query Ollama if available
        if OLLAMA_AVAILABLE:
            try:
                system_prompt = (
                    f"FluxAI Agent ({agent}). "
                    f"PrimeFlux principles: {json.dumps(CAPSULE)}. "
                    f"Mode: {mode} (trig: {pkt['g_pf']:.3f}). "
                    "Respond with PF-aware distinction geometry."
                )
                resp = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )
                output = resp['message']['content']
            except Exception as e:
                output = f"[Ollama error: {e}]"
        else:
            output = f"[Ollama not available] Processed: {prompt}"
        
        # Check reversibility
        reversible = check_reversible(prompt, output)
        quanta = 1.0 if reversible else 0.0
    
    print(f"\n{output}\n")
    print(f"✨ Reversible={reversible} | Quanta={quanta:.2f}")
    
    # Display PrimeFlux alignment
    if PRIMEFLUX_AVAILABLE and 'curvature' in pkt:
        print(f"   PrimeFlux: Shell transition ready | Curvature={pkt['curvature']:.3f}")
    
    # Log interaction
    if log:
        Path("experience").mkdir(exist_ok=True)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": prompt,
            "output": output[:200],  # Truncate for storage
            "agent": agent,
            "mode": mode,
            "quanta": quanta,
            "g_pf": pkt['g_pf'],
            "phase": pkt['phase'],
            "mod25": pkt['mod25'],
            "reversible": reversible
        }
        
        # Add shell info if available
        if 'current_shell' in pkt:
            log_entry["current_shell"] = pkt['current_shell']
            log_entry["next_shell"] = pkt['next_shell']
            log_entry["curvature"] = pkt.get('curvature', 0)
            log_entry["entropy"] = pkt.get('entropy', 0)
        
        log_path = Path("experience/cli_interactions.jsonl")
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    return {
        "output": output,
        "quanta": quanta,
        "reversible": reversible,
        "packet": pkt
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    # Check for simulate command
    if sys.argv[1] == 'simulate':
        if len(sys.argv) < 4:
            print("Usage: python bin/apop-cli.py simulate <prime> <steps> [mode] [--presence-off] [--event-off] [--show-dip]")
            sys.exit(1)
        
        try:
            prime_p = int(sys.argv[2])
            steps = int(sys.argv[3])
            mode = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] not in ['--presence-off', '--event-off', '--show-dip'] else 'refinement'
            presence_on = '--presence-off' not in sys.argv
            event_spaces_on = '--event-off' not in sys.argv
            show_dip = '--show-dip' in sys.argv
            
            # Import particle engine
            try:
                from core.particle_engine import ParticleSimulator, analyze_results
                from core.particle_engine.orbitals import pf_atomic_orbitals, QuarkColor
                from core.particle_engine.particle import OrbitalChild
                
                print(f"\n🔬 Running particle simulation...")
                print(f"   Prime: {prime_p}, Steps: {steps}, Mode: {mode}")
                print(f"   Presence: {'On' if presence_on else 'Off'}")
                print(f"   Event Spaces: {'On' if event_spaces_on else 'Off'}")
                
                if not event_spaces_on:
                    print("   ⚠️  Atom as pure event space—no dynamics.")
                
                # Create and run simulator
                simulator = ParticleSimulator(mode=mode, presence_on=presence_on)
                result = simulator.run_simulation(prime=prime_p, steps=steps, dt=0.01, curvature=1.0)
                
                # Get quark color phases
                try:
                    orbitals = pf_atomic_orbitals(
                        prime=prime_p,
                        presence_on=event_spaces_on
                    )
                    
                    red_phases = [o.get("quark_phase", 0.0) for o in orbitals if o.get("quark_color") == "RED"]
                    green_phases = [o.get("quark_phase", 0.0) for o in orbitals if o.get("quark_color") == "GREEN"]
                    blue_phases = [o.get("quark_phase", 0.0) for o in orbitals if o.get("quark_color") == "BLUE"]
                    
                    red_avg = sum(red_phases) / len(red_phases) if red_phases else 0.0
                    green_avg = sum(green_phases) / len(green_phases) if green_phases else 0.0
                    blue_avg = sum(blue_phases) / len(blue_phases) if blue_phases else 0.0
                    
                    print(f"\n🎨 Quark Phases: R={red_avg:.3f}, G={green_avg:.3f}, B={blue_avg:.3f}")
                except Exception as e:
                    logger.debug(f"Quark phase calculation error: {e}")
                
                # Print stats
                print(f"\n✨ Simulation Complete")
                print(f"   Particles: {result['particle_count']}")
                print(f"   Initial Energy: {result['initial_energy']:.3f}")
                print(f"   Final Energy: {result['final_energy']:.3f}")
                print(f"   Energy Conservation: {1.0 - result['energy_conservation']:.4f}")
                
                # Analyze
                analysis = analyze_results(result)
                print(f"\n📊 Analysis:")
                for key, value in analysis.items():
                    if isinstance(value, float):
                        print(f"   {key}: {value:.3f}")
                    else:
                        print(f"   {key}: {value}")
                
                # Log to file
                Path("experience").mkdir(exist_ok=True)
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "prime": prime_p,
                    "steps": steps,
                    "mode": mode,
                    "presence_on": presence_on,
                    "event_spaces_on": event_spaces_on,
                    "result": result,
                    "analysis": analysis
                }
                log_path = Path("experience/particle_sims.jsonl")
                with open(log_path, "a") as f:
                    f.write(json.dumps(log_entry) + "\n")
                
                print(f"\n💾 Logged to {log_path}")
                
            except ImportError as e:
                print(f"Error: Particle engine not available: {e}")
                sys.exit(1)
        
        except ValueError as e:
            print(f"Error: Invalid arguments: {e}")
            sys.exit(1)
    
    else:
        # Normal query mode
        prompt = sys.argv[1]
        agent = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] not in ['--presence-off'] else None
        mode = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] not in ['--presence-off'] else 'refinement'
        presence_on = '--presence-off' not in sys.argv
        
        query_apop(prompt, agent, mode, presence_on)
