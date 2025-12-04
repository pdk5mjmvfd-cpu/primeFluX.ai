"""
Message API — LLM-facing capsule gateway.

LLM receives text from user, converts to tokens, passes to LCM,
returns encoded capsule. Capsule becomes the LLM's memory interface.

LLM output is then wrapped again into capsules for the Supervisor.
"""

from __future__ import annotations

from typing import Any
from .user_interface import UserInterface
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.combinatoric.interpreter import CombinatoricInterpreter


class MessageAPI:
    """
    Message API — LLM-facing capsule gateway.
    
    Purpose:
    - LLM receives text from user
    - Converts to tokens
    - Passes to LCM
    - Returns encoded capsule
    - Capsule becomes the LLM's memory interface
    
    LLM output is then wrapped again into capsules for the Supervisor.
    """

    def __init__(self, user_interface: UserInterface | None = None) -> None:
        """
        Initialize Message API.

        Args:
            user_interface: Optional UserInterface instance
        """
        self.ui = user_interface or UserInterface()
        self.combinatoric_interpreter = CombinatoricInterpreter()

    def process_message(self, text: str) -> dict[str, Any]:
        """
        Process a message through the full pipeline.
        
        Returns encoded capsule.

        Args:
            text: Input text message

        Returns:
            Encoded capsule dictionary
        """
        # Process through UserInterface
        result = self.ui.run_apop(text)
        
        # Return encoded capsule
        return result.get("capsule", {})

    def process_input(self, text: str) -> dict[str, Any]:
        """
        Process input text (alias for process_message).
        
        This is the entry point that uses combinatoric interpreter.

        Args:
            text: Input text

        Returns:
            Processing result with capsule
        """
        # Use combinatoric interpreter
        packet = self.combinatoric_interpreter.interpret(text)
        
        # Process through LCM
        self.ui.lcm.update_from_combinatorics(packet)
        
        # Get capsule from LCM
        capsule_dict = self.ui.lcm.generate_capsule()
        
        # Create capsule
        capsule = Capsule.decode(capsule_dict) if isinstance(capsule_dict, dict) else Capsule(raw_tokens=packet.tokens)
        
        # Compress and hash
        quanta_hash = self.ui.quanta_compressor.hash_capsule(capsule)
        
        # Process through Supervisor
        state = PFState()
        state.update(capsule.to_dict())
        
        selected_agent = self.ui.supervisor.route(state, self.ui.agents)
        
        if selected_agent:
            processed_capsule = selected_agent.transform(capsule)
        else:
            processed_capsule = capsule
        
        # Update experience
        self.ui.experience_manager.update(processed_capsule, state)
        
        return {
            "capsule": processed_capsule.encode(),
            "quanta_hash": quanta_hash,
            "routed_agent": selected_agent.__class__.__name__ if selected_agent else None,
        }
