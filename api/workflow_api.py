"""
Workflow API — Context Orchestration for Multi-Tool Workflows.

Apop manages context across:
- Cursor (code editing)
- Grok (research/synthesis)
- Perplexity (real-time information)
- Other desktop tools

Each tool receives context it needs to understand its role in the workflow.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import Apop core
import sys
from pathlib import Path as PathLib
_project_root = PathLib(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.math.pf_presence import PresenceVector
from core.math.pf_trig_osc import Oscillator
from core.math.pf_quanta import mint_quanta


# Pydantic models for API
class WorkflowRequest(BaseModel):
    """Request to start/route a workflow."""
    user_input: str
    context: Optional[Dict[str, Any]] = None
    target_tools: Optional[List[str]] = None  # ["cursor", "grok", "perplexity"]


class ToolContext(BaseModel):
    """Context for a specific tool."""
    tool: str
    task: str
    context: Dict[str, Any]
    workflow_step: str
    workflow_id: str


class ToolResult(BaseModel):
    """Result from a tool."""
    tool: str
    workflow_id: str
    result: Dict[str, Any]
    next_steps: Optional[List[str]] = None


class WorkflowState(BaseModel):
    """Current workflow state."""
    workflow_id: str
    user_input: str
    status: str  # "pending", "in_progress", "complete"
    tool_contexts: Dict[str, ToolContext]
    tool_results: Dict[str, ToolResult]
    synthesized_result: Optional[str] = None
    created_at: str
    updated_at: str


# FastAPI app
app = FastAPI(title="PrimeFlux Workflow API", version="1.0.0")

# CORS middleware (allow desktop apps to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory workflow storage (v2: use database)
workflows: Dict[str, WorkflowState] = {}


class WorkflowOrchestrator:
    """
    Orchestrates workflows across multiple tools.
    
    Understands:
    - What each tool can do
    - What context each tool needs
    - How to route workflow steps
    - How to synthesize results
    """
    
    def __init__(self):
        """Initialize orchestrator."""
        self.tool_capabilities = {
            "cursor": {
                "capabilities": ["edit_code", "create_files", "refactor", "analyze_code"],
                "context_format": "cursor_v1",
                "needs": ["file_paths", "code_context", "task_description"]
            },
            "grok": {
                "capabilities": ["research", "synthesize", "analyze", "explain"],
                "context_format": "grok_v1",
                "needs": ["research_topic", "focus_areas", "synthesis_goal"]
            },
            "perplexity": {
                "capabilities": ["real_time_search", "latest_info", "fact_check"],
                "context_format": "perplexity_v1",
                "needs": ["search_query", "info_type", "time_sensitivity"]
            }
        }
    
    def analyze_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input to determine workflow needs.
        
        Returns:
            Analysis with suggested tools and context
        """
        # Compress to presence for analysis
        pv = PresenceVector.from_text(user_input)
        
        # Simple keyword-based routing (v2: use LLM for better understanding)
        analysis = {
            "needs_code": any(word in user_input.lower() for word in 
                            ["code", "implement", "create", "edit", "file", "function", "class"]),
            "needs_research": any(word in user_input.lower() for word in 
                                ["research", "learn", "understand", "how", "what", "why"]),
            "needs_realtime": any(word in user_input.lower() for word in 
                                ["latest", "current", "now", "today", "recent", "2025"]),
            "suggested_tools": []
        }
        
        if analysis["needs_code"]:
            analysis["suggested_tools"].append("cursor")
        if analysis["needs_research"]:
            analysis["suggested_tools"].append("grok")
        if analysis["needs_realtime"]:
            analysis["suggested_tools"].append("perplexity")
        
        if not analysis["suggested_tools"]:
            # Default: all tools if unclear
            analysis["suggested_tools"] = ["cursor", "grok", "perplexity"]
        
        return analysis
    
    def create_tool_context(
        self, 
        tool: str, 
        user_input: str, 
        workflow_id: str,
        analysis: Dict[str, Any]
    ) -> ToolContext:
        """
        Create context for a specific tool.
        
        Each tool gets context it needs to understand its role.
        """
        if tool == "cursor":
            return ToolContext(
                tool="cursor",
                task="code_implementation",
                context={
                    "user_request": user_input,
                    "workflow_step": "code_implementation",
                    "needs_code": analysis.get("needs_code", True),
                    "file_context": "Determine from user_input",
                    "code_patterns": "Follow repository conventions"
                },
                workflow_step="code_implementation",
                workflow_id=workflow_id
            )
        
        elif tool == "grok":
            return ToolContext(
                tool="grok",
                task="research_synthesis",
                context={
                    "user_request": user_input,
                    "workflow_step": "research_synthesis",
                    "research_topic": user_input,
                    "focus_areas": "Extract from user_input",
                    "synthesis_goal": "Provide actionable insights"
                },
                workflow_step="research_synthesis",
                workflow_id=workflow_id
            )
        
        elif tool == "perplexity":
            return ToolContext(
                tool="perplexity",
                task="real_time_info",
                context={
                    "user_request": user_input,
                    "workflow_step": "real_time_info",
                    "search_query": user_input,
                    "info_type": "latest_standards",
                    "time_sensitivity": "high"
                },
                workflow_step="real_time_info",
                workflow_id=workflow_id
            )
        
        else:
            # Generic context
            return ToolContext(
                tool=tool,
                task="generic_task",
                context={"user_request": user_input},
                workflow_step="generic",
                workflow_id=workflow_id
            )
    
    def synthesize_results(
        self, 
        workflow_id: str,
        tool_results: Dict[str, ToolResult]
    ) -> str:
        """
        Synthesize results from multiple tools into coherent response.
        
        This is what Apop tells the user.
        """
        synthesis_parts = []
        
        for tool, result in tool_results.items():
            if tool == "cursor":
                synthesis_parts.append(f"**Code (Cursor)**: {result.result.get('summary', 'Code changes made')}")
            elif tool == "grok":
                synthesis_parts.append(f"**Research (Grok)**: {result.result.get('summary', 'Research completed')}")
            elif tool == "perplexity":
                synthesis_parts.append(f"**Latest Info (Perplexity)**: {result.result.get('summary', 'Information gathered')}")
        
        return "\n\n".join(synthesis_parts) if synthesis_parts else "Workflow completed."


orchestrator = WorkflowOrchestrator()


@app.post("/workflow/start")
async def start_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """
    Start a new workflow.
    
    Apop receives user input, analyzes it, and routes context to tools.
    """
    workflow_id = str(uuid.uuid4())
    
    # Analyze user input
    analysis = orchestrator.analyze_user_input(request.user_input)
    
    # Determine target tools
    target_tools = request.target_tools or analysis["suggested_tools"]
    
    # Create tool contexts
    tool_contexts = {}
    for tool in target_tools:
        tool_contexts[tool] = orchestrator.create_tool_context(
            tool, request.user_input, workflow_id, analysis
        )
    
    # Create workflow state
    workflow = WorkflowState(
        workflow_id=workflow_id,
        user_input=request.user_input,
        status="in_progress",
        tool_contexts={tool: ctx.dict() for tool, ctx in tool_contexts.items()},
        tool_results={},
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    workflows[workflow_id] = workflow
    
    # Compress to presence and log
    pv = PresenceVector.from_text(request.user_input)
    osc = Oscillator(pv, max_steps=8)
    final = osc.run()
    quanta = mint_quanta(pv, final, osc.nat_error)
    
    # Log to experience
    log_dir = Path(_project_root) / "experience_log"
    log_dir.mkdir(exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "workflow_id": workflow_id,
        "user_input": request.user_input,
        "target_tools": target_tools,
        "quanta": round(quanta, 3),
        "type": "workflow_start"
    }
    with open(log_dir / "workflow_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return {
        "workflow_id": workflow_id,
        "status": "started",
        "tool_contexts": {tool: ctx.dict() for tool, ctx in tool_contexts.items()},
        "message": "Workflow started. Tools have received their context."
    }


@app.get("/workflow/{workflow_id}/context/{tool}")
async def get_tool_context(workflow_id: str, tool: str) -> Dict[str, Any]:
    """
    Get context for a specific tool.
    
    Tools call this to understand what they need to do.
    """
    if workflow_id not in workflows:
        return {"error": "Workflow not found"}
    
    workflow = workflows[workflow_id]
    
    if tool not in workflow.tool_contexts:
        return {"error": f"Tool {tool} not in workflow"}
    
    return workflow.tool_contexts[tool]


@app.post("/workflow/result")
async def submit_tool_result(result: ToolResult) -> Dict[str, Any]:
    """
    Tool submits its result.
    
    Tools call this when they've completed their work.
    """
    if result.workflow_id not in workflows:
        return {"error": "Workflow not found"}
    
    workflow = workflows[result.workflow_id]
    workflow.tool_results[result.tool] = result.dict()
    workflow.updated_at = datetime.now().isoformat()
    
    # Check if all tools are done
    all_tools = set(workflow.tool_contexts.keys())
    completed_tools = set(workflow.tool_results.keys())
    
    if all_tools == completed_tools:
        # Synthesize results
        workflow.synthesized_result = orchestrator.synthesize_results(
            result.workflow_id,
            {tool: ToolResult(**r) for tool, r in workflow.tool_results.items()}
        )
        workflow.status = "complete"
    
    return {
        "status": "received",
        "workflow_status": workflow.status,
        "synthesized": workflow.synthesized_result if workflow.status == "complete" else None
    }


@app.get("/workflow/{workflow_id}")
async def get_workflow_state(workflow_id: str) -> Dict[str, Any]:
    """Get current workflow state."""
    if workflow_id not in workflows:
        return {"error": "Workflow not found"}
    
    return workflows[workflow_id].dict()


@app.websocket("/workflow/stream")
async def workflow_stream(websocket: WebSocket):
    """
    WebSocket for real-time workflow updates.
    
    Tools can connect to receive context updates.
    """
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "subscribe":
                workflow_id = data.get("workflow_id")
                # Send workflow updates
                if workflow_id in workflows:
                    await websocket.send_json(workflows[workflow_id].dict())
            
            elif data.get("type") == "update":
                # Handle tool updates
                pass
                
    except WebSocketDisconnect:
        pass


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "PrimeFlux Workflow API",
        "workflows_active": len([w for w in workflows.values() if w.status == "in_progress"])
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
