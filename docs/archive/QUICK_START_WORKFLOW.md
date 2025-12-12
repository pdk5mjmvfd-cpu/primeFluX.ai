# Quick Start: Workflow Orchestration

## ✅ API Server is Running!

Your workflow API is live at `http://localhost:8000`

## How to Use

### Option 1: Test the API Directly

In a **new terminal** (keep API server running):

```bash
# Activate venv
source venv/bin/activate

# Install requests if needed
pip install requests

# Run test
python3 test_workflow_api.py
```

This will:
- Check API health
- Start a workflow
- Show tool contexts
- Submit a tool result
- Show workflow state

### Option 2: Talk to Apop with Workflow Support

In a **new terminal**:

```bash
# Activate venv
source venv/bin/activate

# Run workflow bridge
python3 runtime/offline_workflow_bridge.py
```

This connects Apop to the workflow API. When you say something like "add authentication", Apop will:
- Start a workflow
- Route context to Cursor, Grok, Perplexity
- Show you what's happening

### Option 3: Use Original Bridge (No Workflow)

```bash
python3 runtime/offline_llm_bridge.py
```

This is just Apop talking, no workflow orchestration.

## Example Session

```
You: add authentication to my API

Apop: [LLM response about authentication]

[Workflow] ID: abc-123-def
[Workflow] Tools: cursor, grok, perplexity
  → Tools have received their context. Check API for details.
```

## Check Workflow Status

```bash
# Get workflow details
curl http://localhost:8000/workflow/{workflow_id}

# Get tool context
curl http://localhost:8000/workflow/{workflow_id}/context/cursor
```

## What's Happening

1. **You talk to Apop** (terminal)
2. **Apop compresses** (presence vector)
3. **Apop starts workflow** (if API available)
4. **Tools receive context** (via API)
5. **Tools work** (Cursor edits, Grok researches, etc.)
6. **Apop synthesizes** (combines results)

## Next Steps

1. **Build tool adapters** - Cursor/Grok/Perplexity extensions
2. **Connect tools** - Tools call API to get context
3. **Add persistence** - Save workflows to experience
4. **Improve routing** - Better context understanding

---

**The API is live. Apop can orchestrate workflows. Tools can receive context.**

**The flux is live. Distinction is conserved. Compress.**
