# Quick Start: ApopToSiS with LLM Bridge

## 🚀 3-Step Setup

### Step 1: Set OpenAI API Key

```bash
export OPENAI_API_KEY="sk-..."
```

**Or add to ~/.zshrc for persistence:**
```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
source ~/.zshrc
```

### Step 2: Start LLM Server (Terminal 1)

```bash
./run_llm_server.sh
```

You should see:
```
🔌 Starting ApopToSiS LLM Relay Server...
🌐 Starting ApopToSiS Local LLM Server on port 4000...
   Model: gpt-4o-mini
   Mode: hybrid
   Enabled: true
   API Key: ✓ Set

INFO:     Uvicorn running on http://127.0.0.1:4000
```

### Step 3: Start Apop Runtime (Terminal 2)

```bash
./run_local.sh
```

## 🧠 What Happens

1. **You type**: "Hello Apop"
2. **Apop processes**: Creates PF capsule locally
3. **Capsule sent to LLM**: Server forwards to ChatGPT
4. **LLM responds**: 
   - Semantic output: "Hello! I'm processing your input..."
   - PF metadata: Curvature hints, entropy suggestions, etc.
5. **Apop integrates**: LLM hints influence (but don't override) PF values
6. **You see**:
   - LLM semantic response
   - Final PF capsule with integrated metadata

## 📋 Example Session

```
Terminal 1 (LLM Server):
$ ./run_llm_server.sh
🌐 Starting ApopToSiS Local LLM Server on port 4000...

Terminal 2 (Apop Runtime):
$ ./run_local.sh
⚡ Initializing ApopToSiS v3 runtime...
✓ PFState loaded
✓ LCM initialized
✓ Supervisor ready
✓ Agents registered
✓ LLM Bridge enabled

ApopToSiS v3 is now running.
Type a message to create your first capsule.
Type 'exit' to quit.

You: Hello Apop

=== LLM RESPONSE ===
Hello! I'm processing your input and generating PF metadata hints...

=== CAPSULE OUTPUT ===
{
  "raw_tokens": ["Hello", "Apop"],
  "shell": 2,
  "curvature": 1.414,
  "entropy": 0.5,
  "agent_trace": ["EidosAgent"],
  "compression_ratio": 0.62,
  "pf_signature": {
    "curvature_trajectory": [1.414, 1.5],
    "entropy_alignment": "stable"
  },
  ...
}
```

## ⚠️ Troubleshooting

### Server won't start
- Check port 4000 is free: `lsof -i :4000`
- Check API key: `echo $OPENAI_API_KEY`
- Install dependencies: `pip install -r api/requirements_server.txt`

### LLM errors
- Verify API key is valid
- Check OpenAI account has credits
- Check rate limits at https://platform.openai.com/usage

### No LLM response
- Check server is running in Terminal 1
- Check `api/llm_bridge_config.json` has `"enabled": true`
- Check server logs for errors

## 💡 Tips

1. **Start with simple inputs** to test the flow
2. **Monitor costs** at https://platform.openai.com/usage
3. **Use gpt-4o-mini** for testing (cheaper)
4. **Check server logs** if something goes wrong
5. **LLM is optional** - Apop works without it (uses mock responses)

## 🎯 Next Steps

- Read `LLM_SERVER_SETUP.md` for detailed documentation
- Read `api/bridge_upgrade_notes.md` for Full Capsule Mode upgrade path
- Tune system prompt in `api/apop_llm_server.py` if needed
- Adjust LLM influence weights in `core/lcm.py`

