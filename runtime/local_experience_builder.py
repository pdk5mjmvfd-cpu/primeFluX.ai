"""
Local Experience Builder - Build experiences locally on the computer.

Offline-first runtime for building experiences using the Agora ecosystem.
Compresses knowledge, processes transactions, and generates yield-bearing
polyforms all locally without network dependencies.

Key Features:
- Offline-first: All processing happens locally
- Experience compression: Knowledge → polyform → yields
- Transaction processing: Burn/stake flows
- Mining integration: Proof-of-compression mints
- Local storage: Experiences saved to disk
"""

from __future__ import annotations

import json
import time
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

# Try to import dependencies
try:
    from fluxai.agora.agora_core import AgoraEcosystem
    from fluxai.agora.grokepedia import GrokEpedia
    from fluxai.quanta.quanta_core import QuantaCoin
    from fluxai.operator_core.polyform_ops import ReversiblePolyformOps
    AGORA_AVAILABLE = True
except ImportError:
    AGORA_AVAILABLE = False
    AgoraEcosystem = None
    GrokEpedia = None
    QuantaCoin = None
    ReversiblePolyformOps = None


class LocalExperienceBuilder:
    """
    Local Experience Builder - Build experiences locally.
    
    Offline-first runtime for compressing knowledge, processing transactions,
    and generating yield-bearing polyforms.
    """
    
    def __init__(self, data_dir: str = ".agora_data"):
        """
        Initialize Local Experience Builder.
        
        Args:
            data_dir: Directory for storing local data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize Agora ecosystem
        self.agora: Optional[AgoraEcosystem] = None
        self.grokepedia: Optional[GrokEpedia] = None
        
        if AGORA_AVAILABLE:
            self.agora = AgoraEcosystem()
            self.grokepedia = GrokEpedia(
                operator_core=self.agora.operator_core,
                quanta_coin=self.agora.quanta_coin
            )
        
        # Load existing data
        self._load_data()
    
    def _load_data(self):
        """Load existing data from disk."""
        ledger_file = self.data_dir / "ledger.json"
        agents_file = self.data_dir / "agents.json"
        
        if ledger_file.exists():
            try:
                with open(ledger_file, 'r') as f:
                    ledger_data = json.load(f)
                    if self.agora:
                        self.agora.ledger_poly = ledger_data
            except Exception:
                pass
        
        if agents_file.exists():
            try:
                with open(agents_file, 'r') as f:
                    agents_data = json.load(f)
                    if self.agora:
                        # Restore agents
                        for prime_str, agent_data in agents_data.items():
                            prime_id = int(prime_str)
                            from fluxai.agora.agora_core import Agent
                            agent = Agent(**agent_data)
                            self.agora.agent_registry[prime_id] = agent
            except Exception:
                pass
    
    def _save_data(self):
        """Save data to disk."""
        if not self.agora:
            return
        
        ledger_file = self.data_dir / "ledger.json"
        agents_file = self.data_dir / "agents.json"
        
        # Save ledger
        try:
            with open(ledger_file, 'w') as f:
                json.dump(self.agora.ledger_poly, f, indent=2)
        except Exception:
            pass
        
        # Save agents
        try:
            agents_data = {
                str(k): {
                    "prime_id": v.prime_id,
                    "entity_type": v.entity_type,
                    "registered_at": v.registered_at,
                    "metadata": v.metadata
                }
                for k, v in self.agora.agent_registry.items()
            }
            with open(agents_file, 'w') as f:
                json.dump(agents_data, f, indent=2)
        except Exception:
            pass
    
    def register_entity(
        self,
        entity_type: str,
        name: Optional[str] = None
    ) -> int:
        """
        Register a new entity (user/family/org).
        
        Args:
            entity_type: Type of entity
            name: Optional name for the entity
            
        Returns:
            Prime ID of registered agent
        """
        if not self.agora:
            return 0
        
        prime_id = self.agora.register_agent(entity_type)
        
        # Store name in metadata
        if name:
            agent = self.agora.get_agent(prime_id)
            if agent:
                agent.metadata["name"] = name
        
        self._save_data()
        return prime_id
    
    def process_transaction(
        self,
        amount: float,
        merchant: str,
        agent_prime: int
    ) -> Dict[str, Any]:
        """
        Process a transaction locally.
        
        Args:
            amount: Transaction amount
            merchant: Merchant name
            agent_prime: Prime ID of agent
            
        Returns:
            Transaction result
        """
        if not self.agora:
            return {
                "status": "error",
                "message": "Agora ecosystem not available"
            }
        
        # Create event vector
        import time
        event_vector = [
            time.time() % 1.0,  # T
            0.5 if merchant.lower() == "scheels" else 0.3,  # M
            amount / 1000.0,  # A
            agent_prime / 100.0,  # I
            0.0,  # R
            0.0  # C
        ]
        
        # Process event
        event_pfi = self.agora.process_event(event_vector, agent_prime)
        
        # Burn and stake
        unused = amount * 0.28
        burn_stake_result = self.agora.burn_and_stake(amount, unused, agent_prime)
        
        self._save_data()
        
        return {
            "status": "success",
            "amount": amount,
            "merchant": merchant,
            "agent_prime": agent_prime,
            "event_polyform": event_pfi.to_dict() if hasattr(event_pfi, 'to_dict') else str(event_pfi),
            "burn_stake": burn_stake_result
        }
    
    def compress_knowledge(
        self,
        query: str,
        sources: Optional[List[Dict[str, Any]]] = None,
        agent_prime: int = 2
    ) -> Dict[str, Any]:
        """
        Compress knowledge into yield-bearing polyform.
        
        Args:
            query: Query string
            sources: Optional sources
            agent_prime: Prime ID of agent
            
        Returns:
            Compression result
        """
        if not self.grokepedia:
            return {
                "status": "error",
                "message": "GrokEpedia not available"
            }
        
        result = self.grokepedia.query(query, sources, agent_prime)
        
        # Save knowledge base
        knowledge_file = self.data_dir / "knowledge.json"
        try:
            knowledge_data = self.grokepedia.to_dict()
            with open(knowledge_file, 'w') as f:
                json.dump(knowledge_data, f, indent=2)
        except Exception:
            pass
        
        return result
    
    def reconstruct_experience(
        self,
        query_hash: str
    ) -> Dict[str, Any]:
        """
        Reconstruct experience from compressed polyform.
        
        Args:
            query_hash: Hash of query to reconstruct
            
        Returns:
            Reconstructed experience
        """
        if not self.grokepedia:
            return {
                "status": "error",
                "message": "GrokEpedia not available"
            }
        
        return self.grokepedia.reconstruct_experience(query_hash, synthesize=True)
    
    def compress_ledger(self) -> float:
        """
        Compress the ledger.
        
        Returns:
            Compression ratio achieved
        """
        if not self.agora:
            return 1.0
        
        ratio = self.agora.compress_ledger()
        self._save_data()
        return ratio
    
    def get_agent_info(self, agent_prime: int) -> Dict[str, Any]:
        """
        Get information about an agent.
        
        Args:
            agent_prime: Prime ID of agent
            
        Returns:
            Agent information
        """
        if not self.agora:
            return {}
        
        agent = self.agora.get_agent(agent_prime)
        if not agent:
            return {}
        
        # Get quanta balance
        quanta_balance = 0.0
        if self.agora.quanta_coin:
            quanta_balance = self.agora.quanta_coin.get_balance(agent_prime)
        
        # Get yield info
        yield_info = {}
        if self.agora.quanta_coin:
            yield_info = self.agora.quanta_coin.agora_yield_calc(agent_prime, epoch=0)
        
        return {
            "prime_id": agent.prime_id,
            "entity_type": agent.entity_type,
            "registered_at": agent.registered_at,
            "metadata": agent.metadata,
            "quanta_balance": quanta_balance,
            "yield": yield_info
        }
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents."""
        if not self.agora:
            return []
        
        agents = []
        for agent in self.agora.list_agents():
            agent_info = self.get_agent_info(agent.prime_id)
            agents.append(agent_info)
        
        return agents
    
    def run_interactive(self):
        """Run interactive experience builder."""
        print("🌑 Local Experience Builder - Offline Agora Ecosystem")
        print("Type 'help' for commands, 'exit' to quit.\n")
        
        while True:
            try:
                user_input = input("Agora> ").strip()
                
                if user_input.lower() in ["exit", "quit"]:
                    print("Saving data...")
                    self._save_data()
                    print("Goodbye!")
                    break
                
                if user_input.lower() == "help":
                    print("\nCommands:")
                    print("  register <type> [name] - Register entity (user/family/org)")
                    print("  txn <amount> <merchant> <prime> - Process transaction")
                    print("  query <query> [prime] - Compress knowledge")
                    print("  agents - List all agents")
                    print("  info <prime> - Get agent info")
                    print("  compress - Compress ledger")
                    print("  exit - Exit and save")
                    print()
                    continue
                
                tokens = user_input.split()
                if not tokens:
                    continue
                
                command = tokens[0].lower()
                
                if command == "register":
                    if len(tokens) < 2:
                        print("Usage: register <type> [name]")
                        continue
                    entity_type = tokens[1]
                    name = tokens[2] if len(tokens) > 2 else None
                    prime_id = self.register_entity(entity_type, name)
                    print(f"Registered {entity_type} with prime ID: {prime_id}")
                
                elif command == "txn":
                    if len(tokens) < 4:
                        print("Usage: txn <amount> <merchant> <prime>")
                        continue
                    amount = float(tokens[1])
                    merchant = tokens[2]
                    prime = int(tokens[3])
                    result = self.process_transaction(amount, merchant, prime)
                    print(json.dumps(result, indent=2))
                
                elif command == "query":
                    if len(tokens) < 2:
                        print("Usage: query <query> [prime]")
                        continue
                    query = " ".join(tokens[1:-1]) if len(tokens) > 2 else tokens[1]
                    prime = int(tokens[-1]) if tokens[-1].isdigit() else 2
                    result = self.compress_knowledge(query, sources=None, agent_prime=prime)
                    print(json.dumps(result, indent=2))
                
                elif command == "agents":
                    agents = self.list_agents()
                    print(json.dumps(agents, indent=2))
                
                elif command == "info":
                    if len(tokens) < 2:
                        print("Usage: info <prime>")
                        continue
                    prime = int(tokens[1])
                    info = self.get_agent_info(prime)
                    print(json.dumps(info, indent=2))
                
                elif command == "compress":
                    ratio = self.compress_ledger()
                    print(f"Ledger compressed. Ratio: {ratio:.2%}")
                
                else:
                    print(f"Unknown command: {command}. Type 'help' for commands.")
            
            except KeyboardInterrupt:
                print("\nSaving data...")
                self._save_data()
                print("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    builder = LocalExperienceBuilder()
    builder.run_interactive()
