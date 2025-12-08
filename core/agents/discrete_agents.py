# core/agents/discrete_agents.py
"""Workflow-specific agents: code/data/ledger. Tracks discrete QuantaCoin flows."""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.quanta.proof import CompressionProof

class DiscreteAgent:
    """Spawn per workflow: code/data/quanta. Tracks discrete QuantaCoin flows."""
    
    AGENT_TYPES = {
        "code": "Praxis",      # Builds/optimizes code
        "data": "Eidos",       # Explores/expands data
        "ledger": "Aegis"      # Validates QuantaCoin proofs
    }
    
    def __init__(self, agent_type: str, user_id: str, task: str):
        """
        Initialize discrete agent.
        
        Args:
            agent_type: One of "code", "data", "ledger"
            user_id: Salted wallet ID from RepoLogin
            task: Task description
        """
        self.agent_type = DiscreteAgent.AGENT_TYPES.get(agent_type, "Eidos")
        self.user_id = user_id
        self.task = task
        self.proofs: List[Dict[str, Any]] = []  # Discrete QuantaCoin proofs
    
    def execute(self, input_data: str) -> Dict[str, Any]:
        """
        Run workflow-specific logic and mint QuantaCoin.
        
        Args:
            input_data: Input text to process
            
        Returns:
            Result dict with agent_type, user_id, task_output, quanta_minted, proof_hash
        """
        # Create compression proof (the repo brain does the work)
        proof = CompressionProof(input_data)
        quanta = proof.quanta
        
        # Store proof
        self.proofs.append(proof.serialize())
        
        # Generate task output based on agent type
        if self.agent_type == "Praxis":
            task_output = f"Praxis optimized: {input_data[:50]}..."
        elif self.agent_type == "Eidos":
            task_output = f"Eidos explored: {input_data[:50]}..."
        elif self.agent_type == "Aegis":
            task_output = f"Aegis validated: {input_data[:50]}..."
        else:
            task_output = f"{self.agent_type} processed: {input_data[:50]}..."
        
        return {
            "agent_type": self.agent_type,
            "user_id": self.user_id,
            "task_output": task_output,
            "quanta_minted": quanta,
            "proof_hash": proof.proof_hash
        }
    
    def track_workflow(self) -> Dict[str, Any]:
        """Audit discrete QuantaCoin for this agent/workflow."""
        total_quanta = sum(p.get("quanta_minted", 0) for p in self.proofs)
        return {
            "user_id": self.user_id,
            "agent_type": self.agent_type,
            "total_quanta": total_quanta,
            "proof_count": len(self.proofs)
        }
