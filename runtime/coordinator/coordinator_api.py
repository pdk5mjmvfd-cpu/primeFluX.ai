"""
Coordinator API - FastAPI endpoints for multi-agent coordinator.

Provides REST API for coordinating 3 LLMs and routing events.
"""

from __future__ import annotations

from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from runtime.coordinator.coordinator import MultiAgentCoordinator
from runtime.coordinator.ebb_flow import EbbFlow
from core.lcm import LCM
from runtime.supervisor.supervisor import Supervisor


app = FastAPI(title="PrimeFlux Multi-Agent Coordinator API")


class RouteRequest(BaseModel):
    """Request model for routing events."""
    user_input: str
    agent_name: Optional[str] = None  # Optional override


class RouteResponse(BaseModel):
    """Response model for routing events."""
    agent: str
    shortcut_used: bool
    llm_responses: Dict[str, str]
    merged_response: str
    new_pathway: bool
    quanta_minted: float


# Global coordinator instance
_coordinator: Optional[MultiAgentCoordinator] = None


def get_coordinator() -> MultiAgentCoordinator:
    """
    Get global coordinator instance (singleton).
    
    Returns:
        MultiAgentCoordinator instance
    """
    global _coordinator
    if _coordinator is None:
        # Initialize with default components
        lcm = LCM()
        supervisor = Supervisor(lcm=lcm)
        ebb_flow = EbbFlow()
        _coordinator = MultiAgentCoordinator(
            lcm=lcm,
            supervisor=supervisor,
            ebb_flow=ebb_flow
        )
    return _coordinator


@app.post("/route", response_model=RouteResponse)
async def route_event(request: RouteRequest) -> RouteResponse:
    """
    Route event through multi-agent system.
    
    Args:
        request: RouteRequest with user input
        
    Returns:
        RouteResponse with routing results
    """
    coordinator = get_coordinator()
    
    try:
        result = coordinator.route_event(request.user_input)
        return RouteResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    coordinator = get_coordinator()
    
    # Check LLM health
    llm_health = {}
    for llm in coordinator.llms:
        llm_health[llm.name] = llm.health_check()
    
    return {
        "status": "healthy",
        "llms": llm_health,
        "lcm_available": coordinator.lcm is not None,
        "supervisor_available": coordinator.supervisor is not None,
    }


@app.get("/shortcuts")
async def get_shortcuts() -> Dict[str, Any]:
    """
    Get all LCM shortcuts.
    
    Returns:
        Dictionary of shortcuts
    """
    coordinator = get_coordinator()
    
    if not coordinator.lcm:
        return {"shortcuts": []}
    
    shortcuts = []
    for presence_vector, shortcut in coordinator.lcm.state.lcm_map.items():
        shortcuts.append({
            "presence_vector": str(presence_vector),
            "reliability": shortcut.reliability_score,
            "success_count": shortcut.success_count,
            "total_attempts": shortcut.total_attempts,
        })
    
    return {"shortcuts": shortcuts}


@app.get("/event_space")
async def get_event_space() -> Dict[str, Any]:
    """
    Get event space nodes.
    
    Returns:
        Dictionary of event space nodes
    """
    coordinator = get_coordinator()
    
    if not coordinator.lcm:
        return {"nodes": []}
    
    nodes = []
    for node in coordinator.lcm.state.event_space:
        nodes.append({
            "node_id": node.node_id,
            "lcm_value": node.lcm_value,
            "timestamp": node.timestamp,
        })
    
    return {"nodes": nodes, "count": len(nodes)}

