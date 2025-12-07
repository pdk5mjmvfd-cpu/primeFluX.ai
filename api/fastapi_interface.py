"""
FastAPI Interface - REST API for ApopToSiS v3.

Provides FastAPI endpoints for flux processing and LCM simulation.
"""

from __future__ import annotations

from typing import Optional, Dict, Any
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

# Try to import dependencies
try:
    from runtime.llm_salts import OfflineLLM
    from core.distinction_packet import DistinctionPacket
    from agents.router import AgentRouter
    from core.quanta_api import QuantaAPI
    from runtime.boot import ApopBootSequence
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    OfflineLLM = None
    DistinctionPacket = None
    AgentRouter = None
    QuantaAPI = None
    ApopBootSequence = None


app = FastAPI(title="ApopToSiS v3 API", version="3.0.0")

# Initialize components
if DEPENDENCIES_AVAILABLE:
    offline_llm = OfflineLLM()
    agent_router = AgentRouter()
    quanta_api = QuantaAPI()
    boot_sequence = ApopBootSequence()
else:
    offline_llm = None
    agent_router = None
    quanta_api = None
    boot_sequence = None


class FluxRequest(BaseModel):
    """Request model for flux endpoint."""
    input: str
    agent_salt: Optional[str] = None


class FluxResponse(BaseModel):
    """Response model for flux endpoint."""
    output: str
    quanta_minted: int
    audit: Dict[str, Any]


@app.post("/flux/{mode}", response_model=FluxResponse)
async def flux_endpoint(
    mode: str,
    request: FluxRequest = Body(...)
):
    """
    Process flux request.
    
    Parses packet, routes agent, queries LLM, checks reversibility,
    mints quanta, returns result.
    
    Args:
        mode: Processing mode (e.g., "refinement", "research")
        request: Flux request with input and optional agent_salt
        
    Returns:
        Flux response with output, quanta_minted, and audit
    """
    if not DEPENDENCIES_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Dependencies not available"
        )
    
    try:
        # Parse distinction packet from input
        input_packet = DistinctionPacket.from_input(request.input)
        
        # Route agent
        agent_name = agent_router.route(input_packet)
        agent_salt = request.agent_salt or agent_name
        
        # Get capsule context
        capsule = {
            "mode": mode,
            "input": request.input,
            "agent": agent_name,
            "curvature": input_packet.curvature_value,
            "rail_phase": input_packet.rail_phase
        }
        
        # Query LLM
        if offline_llm and offline_llm.is_available():
            output_text = offline_llm.query_salt(agent_salt, request.input, capsule)
        else:
            output_text = f"[Offline LLM not available] Processed: {request.input}"
        
        # Create output packet
        output_packet = DistinctionPacket.from_input(output_text)
        
        # Check reversibility and mint quanta
        quanta_minted = quanta_api.mint_with_check(
            input_packet,
            output_packet,
            base_quanta=100
        )
        
        # Build audit
        audit = {
            "input_entropy": quanta_api.checker.entropy(input_packet.prime_modes),
            "output_entropy": quanta_api.checker.entropy(output_packet.prime_modes),
            "reversibility_passed": quanta_api.checker.check(
                input_packet.prime_modes,
                output_packet.prime_modes
            ),
            "agent": agent_name,
            "curvature": input_packet.curvature_value,
            "rail_phase": input_packet.rail_phase
        }
        
        return FluxResponse(
            output=output_text,
            quanta_minted=quanta_minted,
            audit=audit
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}"
        )


@app.get("/lcm/sim")
async def lcm_sim():
    """
    Real-time flux simulation endpoint.
    
    Streams response with flux data.
    
    Returns:
        Streaming response with flux data
    """
    def generate_flux():
        """Generate flux data stream."""
        import time
        
        for i in range(10):
            flux_data = {
                "timestamp": time.time(),
                "flux_value": 0.5 + (i * 0.1),
                "curvature": 0.3 + (i * 0.05),
                "entropy": 0.2 + (i * 0.03)
            }
            yield f"data: {json.dumps(flux_data)}\n\n"
            time.sleep(0.5)
    
    return StreamingResponse(
        generate_flux(),
        media_type="text/event-stream"
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "dependencies_available": DEPENDENCIES_AVAILABLE,
        "ollama_available": offline_llm.is_available() if offline_llm else False
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
