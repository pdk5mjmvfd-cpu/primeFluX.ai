# ApopToSiS LLM Server Setup Guide

## Overview

The LLM Relay Server provides a FastAPI endpoint that bridges ApopToSiS capsules with OpenAI's ChatGPT API in Hybrid Mode.

## Files Created

1. **`api/apop_llm_server.py`** - FastAPI server for LLM relay
2. **`api/requirements_server.txt`** - Server dependencies
3. **`run_llm_server.sh`** - Script to run the server

## Prerequisites

1. **OpenAI API Key**: Get your API key from https://platform.openai.com/api-keys
2. **Python 3.11+**: Required for ApopToSiS v3
3. **Virtual Environment**: Created automatically by `run_llm_server.sh`

## Setup Steps

### 1. Set OpenAI API Key

**Temporary (current session only):**
```bash
export OPENAI_API_KEY="sk-..."
```

**Permanent (add to ~/.zshrc or ~/.bashrc):**
```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
source ~/.zshrc
```

### 2. Install Server Dependencies

The `run_llm_server.sh` script will automatically install dependencies, but you can also do it manually:

```bash
source .venv/bin/activate
pip install -r api/requirements_server.txt
```

Dependencies:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `requests` - HTTP client

### 3. Configure Server

Edit `api/llm_bridge_config.json`:
```json
{
    "api_url": "http://localhost:4000/apop_llm",
    "model": "gpt-4o-mini",
    "mode": "hybrid",
    "enabled": true,
    "timeout": 30.0
}
```

**Model Options:**
- `gpt-4o-mini` - Fast, cost-effective (recommended)
- `gpt-4o` - More capable, higher cost
- `gpt-4-turbo` - Balanced performance
- `gpt-3.5-turbo` - Legacy, cheaper

## Running the Server

### Start LLM Server

```bash
./run_llm_server.sh
```

Expected output:
```
🔌 Starting ApopToSiS LLM Relay Server...
🌐 Starting ApopToSiS Local LLM Server on port 4000...
   Model: gpt-4o-mini
   Mode: hybrid
   Enabled: true
   API Key: ✓ Set

INFO:     Uvicorn running on http://127.0.0.1:4000
```

### Start Apop Runtime (in separate terminal)

```bash
./run_local.sh
```

## How It Works

### Cognitive Loop

```
USER → Local PF-LCM → Capsule
        ↓
  Local LLM Server → ChatGPT (Hybrid PF Mode)
        ↓
   PF Metadata + Semantic Output
        ↓
 Local PF-LCM Integration
        ↓
 New Capsule (PF State Updated)
```

### Hybrid Mode Flow

1. **User Input** → Apop processes through LCM
2. **Capsule Generated** → Local PF computation creates capsule
3. **Capsule Sent to LLM** → `RemoteLLMBridge` sends to server
4. **LLM Processes** → ChatGPT receives capsule + system prompt
5. **LLM Returns**:
   - `semantic_output`: Natural language response
   - `pf_metadata`: PF hints (curvature, entropy, flux, etc.)
6. **LCM Integrates** → LLM hints influence (but don't override) PF values
7. **Final Capsule** → Display both semantic output and PF capsule

### System Prompt

The server uses a specialized system prompt that instructs ChatGPT to:
- Provide natural language responses
- Generate PF metadata hints (not full capsules)
- Never override PF state
- Follow PF rules exactly

## API Endpoints

### POST `/apop_llm`

Receives PF capsule, returns hybrid response.

**Request:**
```json
{
    "model": "gpt-4o-mini",
    "capsule": {
        "raw_tokens": ["Hello", "Apop"],
        "shell": 2,
        "curvature": 1.414,
        "entropy": 0.5,
        ...
    },
    "mode": "hybrid_pf"
}
```

**Response:**
```json
{
    "semantic_output": "Hello! I'm processing your input...",
    "pf_metadata": {
        "curvature_trajectory": [1.414, 1.5],
        "entropy_alignment": "stable",
        "flux_interpretation": {
            "amplitude": 0.1,
            "direction": "forward"
        },
        "shell_bias": 2,
        "triplet_bias": "presence"
    }
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
    "status": "ok",
    "enabled": true,
    "model": "gpt-4o-mini",
    "mode": "hybrid",
    "api_key_set": true
}
```

## Troubleshooting

### Server won't start

1. **Check port 4000 is available:**
   ```bash
   lsof -i :4000
   ```

2. **Check API key is set:**
   ```bash
   echo $OPENAI_API_KEY
   ```

3. **Check dependencies installed:**
   ```bash
   pip list | grep -E "fastapi|uvicorn|requests"
   ```

### LLM API errors

1. **Invalid API key**: Check your OpenAI API key is correct
2. **Rate limits**: You may be hitting OpenAI rate limits
3. **Model not available**: Check the model name in config
4. **Network issues**: Check internet connection

### Capsule parsing errors

The server includes fallback handling:
- If JSON parsing fails, returns semantic output only
- If API call fails, returns error message
- Always returns valid response structure

## Testing

### Test Server Health

```bash
curl http://localhost:4000/health
```

### Test LLM Endpoint

```bash
curl -X POST http://localhost:4000/apop_llm \
  -H "Content-Type: application/json" \
  -d '{
    "capsule": {
      "raw_tokens": ["test"],
      "shell": 2,
      "curvature": 1.0,
      "entropy": 0.5
    }
  }'
```

## Security Notes

1. **API Key**: Never commit your API key to git
2. **Local Only**: Server runs on localhost only (not exposed to network)
3. **Rate Limits**: Be aware of OpenAI rate limits and costs
4. **Validation**: Server validates LLM responses before returning

## Cost Considerations

- **gpt-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **gpt-4o**: ~$2.50 per 1M input tokens, ~$10 per 1M output tokens
- Monitor usage at https://platform.openai.com/usage

## Next Steps

1. Test with simple inputs
2. Monitor LLM response quality
3. Tune system prompt if needed
4. Adjust influence weights in `core/lcm.py`
5. Consider upgrading to Full Capsule Mode (see `api/bridge_upgrade_notes.md`)

