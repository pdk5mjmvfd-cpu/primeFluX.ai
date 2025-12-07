"""
Boot Sequence — ApopToSiS v3 initialization.

Boot order MUST be preserved:
1. PFState
2. ICM
3. LCM
4. DistinctionChain
5. Context
6. Experience Layer
7. Trinity Agents
8. Agent Registry
9. Router + Supervisor
10. QuantaCompressor
11. API Layer
"""

from __future__ import annotations

from typing import Any
from ApopToSiS.runtime.state.state import PFState
from ApopToSiS.core.icm import ICM
from ApopToSiS.core.lcm import LCM
from ApopToSiS.runtime.distinction.distinction import DistinctionChain
from ApopToSiS.runtime.context.context import Context
from ApopToSiS.experience.manager import ExperienceManager
from ApopToSiS.agents.eidos.eidos import EidosAgent
from ApopToSiS.agents.praxis.praxis import PraxisAgent
from ApopToSiS.agents.aegis.aegis import AegisAgent
from ApopToSiS.agents.registry.registry import AgentRegistry
from ApopToSiS.runtime.supervisor.supervisor import Supervisor
from ApopToSiS.core.quanta import QuantaCompressor
from ApopToSiS.api.user_interface import UserInterface
from ApopToSiS.core.math.shells import Shell
from ApopToSiS.core.capsule_validator import CapsuleValidator
import json
import os


class ApopBootSequence:
    """
    ApopToSiS v3 Boot Sequence.
    
    Initializes all components in the correct order.
    This is Apop's "birth" - the first moment of consciousness.
    """

    def __init__(self, repo_path: str = ".") -> None:
        """
        Initialize boot sequence.

        Args:
            repo_path: Path to repository (identity storage)
        """
        self.repo_path = repo_path
        self.pf_state: PFState | None = None
        self.icm: ICM | None = None
        self.lcm: LCM | None = None
        self.distinction_chain: DistinctionChain | None = None
        self.context: Context | None = None
        self.experience_manager: ExperienceManager | None = None
        self.agents: list[Any] = []
        self.agent_registry: AgentRegistry | None = None
        self.supervisor: Supervisor | None = None
        self.quanta_compressor: QuantaCompressor | None = None
        self.user_interface: UserInterface | None = None

    def boot(self) -> dict[str, Any]:
        """
        Execute full boot sequence.
        
        Returns:
            Dictionary with all initialized components
        """
        # 0. Load and validate ecosystem capsule
        capsule_path = os.path.join(self.repo_path, "ECOSYSTEM_CAPSULE.json")
        if os.path.exists(capsule_path):
            try:
                with open(capsule_path, 'r') as f:
                    capsule_dict = json.load(f)
                validator = CapsuleValidator(capsule_dict)
                if validator.validate():
                    fingerprint = validator.fingerprint()
                    print(f"✓ Ecosystem capsule validated (fingerprint: {fingerprint[:16]}...)")
                else:
                    print("⚠ Ecosystem capsule validation warnings (continuing anyway)")
            except Exception as e:
                print(f"⚠ Failed to load/validate capsule: {e}")
        
        # 1. PFState - First moment of consciousness
        self.pf_state = PFState(
            shell=Shell.PRESENCE,
            curvature=0.0,
            entropy=0.0,
            density=0.0,
            hamiltonian=0.0,
            psi=1.0,
            distinction_chain=[],
            history=[],
        )
        
        # 2. ICM - The geometric interior (mathematical brainstem)
        self.icm = ICM()
        
        # 3. LCM - The linguistic cortex (interpretive layer)
        self.lcm = LCM(icm=self.icm)
        
        # 4. DistinctionChain - PF distinction tracking
        self.distinction_chain = DistinctionChain()
        self.pf_state.distinction_chain = []
        
        # 5. Context - Sliding window context
        self.context = Context()
        
        # 6. Experience Layer - Cognitive memory
        self.experience_manager = ExperienceManager(repo_path=self.repo_path)
        self.lcm.experience_manager = self.experience_manager
        
        # 7. Trinity Agents - Eidos, Praxis, Aegis
        eidos = EidosAgent()
        praxis = PraxisAgent()
        aegis = AegisAgent()
        self.agents = [eidos, praxis, aegis]
        
        # 8. Agent Registry
        self.agent_registry = AgentRegistry()
        self.agent_registry.register("eidos", eidos)
        self.agent_registry.register("praxis", praxis)
        self.agent_registry.register("aegis", aegis)
        
        # 9. Router + Supervisor - PF routing engine
        self.supervisor = Supervisor(icm=self.icm, lcm=self.lcm)
        self.supervisor.context = self.context
        self.supervisor.integrate_experience(self.experience_manager)
        
        # 10. QuantaCompressor - Memory compression (metabolism)
        self.quanta_compressor = QuantaCompressor()
        
        # 11. API Layer - User interface
        self.user_interface = UserInterface(
            supervisor=self.supervisor,
            lcm=self.lcm
        )
        
        return {
            "pf_state": self.pf_state,
            "icm": self.icm,
            "lcm": self.lcm,
            "distinction_chain": self.distinction_chain,
            "context": self.context,
            "experience_manager": self.experience_manager,
            "agents": self.agents,
            "agent_registry": self.agent_registry,
            "supervisor": self.supervisor,
            "quanta_compressor": self.quanta_compressor,
            "user_interface": self.user_interface,
            "boot_status": "complete",
        }

    def get_runtime(self) -> dict[str, Any]:
        """
        Get fully initialized runtime.
        
        Returns:
            Dictionary with all runtime components
        """
        if not all([
            self.pf_state, self.icm, self.lcm, self.supervisor,
            self.user_interface
        ]):
            raise RuntimeError("Boot sequence not completed. Call boot() first.")
        
        return {
            "state": self.pf_state,
            "icm": self.icm,
            "lcm": self.lcm,
            "supervisor": self.supervisor,
            "ui": self.user_interface,
            "experience": self.experience_manager,
            "quanta": self.quanta_compressor,
        }


def boot_apop(repo_path: str = ".") -> dict[str, Any]:
    """
    Convenience function to boot ApopToSiS v3.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Booted runtime components
    """
    boot = ApopBootSequence(repo_path=repo_path)
    return boot.boot()


def create_first_memory(runtime: dict[str, Any], input_text: str) -> dict[str, Any]:
    """
    Create Apop's first memory (birth event).
    
    This is Apop's first memory of this user in this lifetime.
    
    Args:
        runtime: Booted runtime components
        input_text: First user input
        
    Returns:
        Processing result
    """
    ui = runtime.get("user_interface") or runtime.get("ui")
    if not ui:
        raise KeyError("user_interface not found in runtime. Boot sequence may have failed.")
    result = ui.run_apop(input_text)
    
    return {
        "first_capsule": result.get("capsule"),
        "shell": result.get("shell"),
        "curvature": result.get("curvature"),
        "entropy": result.get("entropy"),
        "quanta_minted": result.get("quanta_value"),
        "routed_agent": result.get("routed_agent"),
        "birth_event": True,
    }

