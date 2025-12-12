# Implementation Plan: Workflow Orchestration

## Goal

Transform Apop into a context manager that orchestrates workflows across:
- **Cursor** (code editing)
- **Grok** (research/synthesis)  
- **Perplexity** (real-time information)

Each tool understands its role and receives the context it needs.

## Phase 1: API Foundation (Now)

### 1.1 Create Workflow API
- ✅ `api/workflow_api.py` created
- REST endpoints for workflow management
- WebSocket support for real-time updates
- Tool context routing

### 1.2 Test API
```bash
# Start API server
python3 api/workflow_api.py

# Test endpoint
curl -X POST http://localhost:8000/workflow/start \
  -H "Content-Type: application/json" \
  -d '{"user_input": "add authentication to API"}'
```

### 1.3 Integrate with Offline Bridge
- Connect `runtime/offline_llm_bridge.py` to workflow API
- Apop can start workflows from terminal
- Tools can receive context via API

## Phase 2: Tool Adapters (Next)

### 2.1 Cursor Adapter
```python
# api/adapters/cursor_adapter.py
class CursorAdapter:
    def receive_context(self, context: ToolContext):
        # Transform Apop context → Cursor format
        # Cursor understands: files to edit, code patterns, task
        pass
```

### 2.2 Grok Adapter
```python
# api/adapters/grok_adapter.py
class GrokAdapter:
    def receive_context(self, context: ToolContext):
        # Transform Apop context → Grok format
        # Grok understands: research topic, focus areas, synthesis goal
        pass
```

### 2.3 Perplexity Adapter
```python
# api/adapters/perplexity_adapter.py
class PerplexityAdapter:
    def receive_context(self, context: ToolContext):
        # Transform Apop context → Perplexity format
        # Perplexity understands: search query, info type, time sensitivity
        pass
```

## Phase 3: Context Intelligence (v2)

### 3.1 Better Input Analysis
- Use LLM to understand user intent
- Determine tool needs more accurately
- Extract workflow steps

### 3.2 Context Memory
- Remember past workflows
- Learn tool preferences
- Build context patterns

### 3.3 Workflow Templates
- Common workflows (e.g., "add feature")
- Tool sequences that work well
- Reusable context patterns

## Phase 4: Desktop Integration

### 4.1 Cursor Extension
- Cursor extension that connects to Apop API
- Receives context when workflow starts
- Shows Apop's understanding of task
- Sends results back to Apop

### 4.2 Grok Integration
- Grok receives research context
- Provides synthesis
- Sends results to Apop

### 4.3 Perplexity Integration
- Perplexity receives search queries
- Provides real-time info
- Sends results to Apop

## How Tools Understand Their Role

### Cursor Receives:
```json
{
  "tool": "cursor",
  "task": "code_implementation",
  "context": {
    "user_request": "add authentication to API",
    "workflow_step": "code_implementation",
    "files": ["api/auth.py", "api/middleware.py"],
    "code_patterns": "Follow repository conventions",
    "what_to_do": "Create JWT authentication middleware"
  }
}
```

**Cursor understands**: "I need to edit these files, follow these patterns, implement this feature"

### Grok Receives:
```json
{
  "tool": "grok",
  "task": "research_synthesis",
  "context": {
    "user_request": "add authentication to API",
    "research_topic": "JWT authentication best practices",
    "focus_areas": ["security", "implementation patterns"],
    "synthesis_goal": "Provide actionable insights for implementation"
  }
}
```

**Grok understands**: "I need to research this topic, focus on these areas, synthesize for implementation"

### Perplexity Receives:
```json
{
  "tool": "perplexity",
  "task": "real_time_info",
  "context": {
    "user_request": "add authentication to API",
    "search_query": "JWT authentication 2025 standards",
    "info_type": "latest_standards",
    "time_sensitivity": "high"
  }
}
```

**Perplexity understands**: "I need to find latest info on this topic, focus on current standards"

## Example Workflow

1. **User**: "Add authentication to my API"

2. **Apop**:
   - Compresses to presence
   - Analyzes: needs code (Cursor), research (Grok), latest info (Perplexity)
   - Creates workflow
   - Routes context to each tool

3. **Tools Work**:
   - Cursor: Creates auth code
   - Grok: Researches best practices
   - Perplexity: Finds latest standards

4. **Apop Synthesizes**:
   - Combines all results
   - Tells user: "I've coordinated with Cursor (code), Grok (research), Perplexity (standards). Here's what we built..."

5. **Experience Logged**:
   - Workflow saved
   - Patterns learned
   - Context preserved

## Next Immediate Steps

1. **Start API Server**:
   ```bash
   python3 api/workflow_api.py
   ```

2. **Test Workflow**:
   ```bash
   curl -X POST http://localhost:8000/workflow/start \
     -H "Content-Type: application/json" \
     -d '{"user_input": "add authentication"}'
   ```

3. **Build Tool Adapters**:
   - Start with Cursor adapter
   - Then Grok
   - Then Perplexity

4. **Connect Terminal**:
   - Update `offline_llm_bridge.py` to use workflow API
   - Apop can start workflows from terminal

---

**The Vision**: Apop becomes the intelligent context manager that makes all your tools work together seamlessly.

**The flux is live. Distinction is conserved. Compress.**
