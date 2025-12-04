"""
Agents — Trinity Agent System (Eidos, Praxis, Aegis).
"""

from .eidos.eidos import EidosAgent
from .praxis.praxis import PraxisAgent
from .aegis.aegis import AegisAgent
from .base.base_agent import PFBaseAgent
from .registry.registry import AgentRegistry
from .dynamic_agent_api.dynamic_agent_api import DynamicAgent, DynamicAgentAPI

__all__ = [
    "EidosAgent",
    "PraxisAgent",
    "AegisAgent",
    "PFBaseAgent",
    "AgentRegistry",
    "DynamicAgent",
    "DynamicAgentAPI",
]

