# core/quanta/proof.py
# Verifiable Proof-of-Compression (anyone can check)

import hashlib
import json
from ..math.pf_trig_osc import Oscillator
from ..math.pf_presence import PresenceVector
from .mint import mint_quanta


class CompressionProof:
    """
    Anyone on Earth can verify you actually did the work.
    
    This creates an immutable, verifiable proof of compression work.
    The proof can be verified by anyone with the same code.
    """
    
    def __init__(self, input_text: str, steps: int = 8):
        """
        Create a compression proof.
        
        Args:
            input_text: Input text to compress
            steps: Number of oscillation steps (default 8)
        """
        self.input = input_text
        self.steps = steps
        self.initial = PresenceVector.from_text(input_text)
        osc = Oscillator(self.initial, max_steps=steps)
        self.final = osc.run()
        self.nat_error = osc.nat_error
        self.quanta = mint_quanta(self.initial, self.final, self.nat_error)
        self.proof_hash = self._hash()
    
    def _hash(self) -> str:
        """
        Generate proof hash.
        
        Hash includes all critical data to ensure proof integrity.
        """
        payload = f"{self.input}|{self.initial.components}|{self.final.components}|{self.nat_error:.1f}|{self.steps}"
        return hashlib.sha256(payload.encode()).hexdigest()
    
    def serialize(self) -> dict:
        """
        Serialize proof to dictionary.
        
        Returns:
            Dictionary with all proof data
        """
        return {
            "proof_hash": self.proof_hash,
            "input": self.input,
            "initial_nonzero": sum(1 for x in self.initial.components if x != 0),
            "final_nonzero": sum(1 for x in self.final.components if x != 0),
            "nat_error": round(self.nat_error, 1),
            "quanta_minted": self.quanta,
            "steps": self.steps
        }
    
    @classmethod
    def verify(cls, proof_dict: dict) -> bool:
        """
        Verify a proof.
        
        Anyone can call this to verify that the proof is valid.
        Recreates the proof and checks if it matches.
        
        Args:
            proof_dict: Serialized proof dictionary
            
        Returns:
            True if proof is valid, False otherwise
        """
        try:
            temp = cls(proof_dict["input"], proof_dict["steps"])
            return (temp.proof_hash == proof_dict["proof_hash"] and
                    abs(temp.quanta - proof_dict["quanta_minted"]) < 0.1)
        except:
            return False
