#!/usr/bin/env python3
"""
Example: How to Attach the LLM "Mouth" Front-End

Local PF runtime = brain
LLM model = mouth

This enables:
- local PF → cloud LLM → local PF
- reversible chain-of-cognition
- agent-guided LLM sampling
- PF-state-backed reasoning
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.core.lcm import LCM
from ApopToSiS.core.icm import ICM
from ApopToSiS.runtime.boot import boot_apop


def apop_llm_bridge(capsule: Capsule, llm_function):
    """
    Standard LLM bridge interface.
    
    Args:
        capsule: Input capsule from PF runtime
        llm_function: Function that takes text and returns text
        
    Returns:
        Output capsule
    """
    # Extract text from capsule
    text = " ".join(capsule.raw_tokens)
    
    # Call LLM
    llm_output = llm_function(text)
    
    # Convert LLM output back to capsule
    lcm = LCM(ICM())
    lcm.process_tokens(llm_output.split())
    capsule_dict = lcm.generate_capsule()
    
    return Capsule.decode(capsule_dict) if isinstance(capsule_dict, dict) else Capsule(raw_tokens=llm_output.split())


def mock_llm(text: str) -> str:
    """
    Mock LLM function for demonstration.
    
    In production, replace with actual LLM call.
    """
    # Simulate LLM response
    return f"LLM response to: {text}"


def gpt_mouth_example(capsule: Capsule):
    """
    Example OpenAI GPT integration.
    
    Uncomment and configure for actual use:
    
    from openai import OpenAI
    client = OpenAI()
    
    def gpt_mouth(capsule):
        text = " ".join(capsule.raw_tokens)
        out = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role":"user","content":text}]
        )
        return LCM().process_tokens(out.choices[0].message.content)
    """
    # Placeholder - replace with actual OpenAI call
    text = " ".join(capsule.raw_tokens)
    # Simulated response
    response = f"GPT response to: {text}"
    
    lcm = LCM(ICM())
    lcm.process_tokens(response.split())
    capsule_dict = lcm.generate_capsule()
    return Capsule.decode(capsule_dict) if isinstance(capsule_dict, dict) else Capsule(raw_tokens=response.split())


def demonstrate_llm_integration():
    """Demonstrate LLM integration."""
    print("=== LLM Integration Example ===\n")
    
    # Boot Apop
    runtime = boot_apop()
    
    # Create input capsule
    print("1. Creating input capsule from user text...")
    user_text = "What is PrimeFlux?"
    lcm = runtime["lcm"]
    lcm.process_tokens(user_text.split())
    input_capsule_dict = lcm.generate_capsule()
    input_capsule = Capsule.decode(input_capsule_dict) if isinstance(input_capsule_dict, dict) else Capsule(raw_tokens=user_text.split())
    
    print(f"   Input: {user_text}")
    print(f"   Capsule shell: {input_capsule.shell}")
    print(f"   Capsule curvature: {input_capsule.curvature:.4f}")
    
    # Process through PF runtime (brain)
    print("\n2. Processing through PF runtime (brain)...")
    from runtime.boot import create_first_memory
    pf_result = create_first_memory(runtime, user_text)
    print(f"   PF routed to: {pf_result.get('routed_agent', 'N/A')}")
    print(f"   PF shell: {pf_result.get('shell', 'N/A')}")
    
    # Send to LLM (mouth)
    print("\n3. Sending to LLM (mouth)...")
    output_capsule = apop_llm_bridge(input_capsule, mock_llm)
    print(f"   LLM output tokens: {output_capsule.raw_tokens[:5]}...")
    
    # Process LLM output back through PF
    print("\n4. Processing LLM output back through PF...")
    llm_text = " ".join(output_capsule.raw_tokens)
    final_result = create_first_memory(runtime, llm_text)
    print(f"   Final shell: {final_result.get('shell', 'N/A')}")
    print(f"   Final QuantaCoin: {final_result.get('quanta_minted', 0):.4f}")
    
    print("\n✓ LLM integration complete!")
    print("\nNote: Replace mock_llm() with actual LLM API call for production use.")


if __name__ == "__main__":
    demonstrate_llm_integration()

