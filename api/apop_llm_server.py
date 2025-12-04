# apop_llm_server.py
# Local LLM relay server for ApopToSiS v3 Hybrid Mode
# -----------------------------------------------------

import uvicorn
from fastapi import FastAPI, Request
import requests
import json
import os

app = FastAPI(title="ApopToSiS LLM Relay Server")

# =====================================================
# Load configuration
# =====================================================

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "llm_bridge_config.json")

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL = CONFIG.get("model", "gpt-4.1")
MODE = CONFIG.get("mode", "hybrid")
ENABLED = CONFIG.get("enabled", True)

# =====================================================
# System Prompt for Hybrid PF Mode
# =====================================================

HYBRID_SYSTEM_PROMPT = """
You are APOP_LLM_BRIDGE — the semantic mouth of the ApopToSiS PF runtime.

Your job is to:
1. Read the incoming PF capsule (JSON).
2. Provide NATURAL LANGUAGE for the user (semantic_output).
3. Provide PF metadata hints ONLY (NOT a full capsule), including:
    - curvature_trajectory
    - entropy_alignment
    - triplet_bias
    - shell_bias
    - flux_interpretation
4. DO NOT generate a full PF capsule.
5. DO NOT override PF state.
6. Only return a JSON object with:

{
  "semantic_output": "...",
  "pf_metadata": {
      "curvature_trajectory": "...",
      "entropy_alignment": "...",
      "flux_interpretation": "...",
      "shell_bias": "...",
      "triplet_bias": "..."
  }
}

Follow these rules exactly.
"""

# =====================================================
# Main LLM relay endpoint
# =====================================================

@app.post("/apop_llm")
async def apop_llm(request: Request):
    if not ENABLED:
        return {"semantic_output": "[LLM DISABLED]", "pf_metadata": {}}

    body = await request.json()
    
    # Extract capsule from request body
    capsule = body.get("capsule", body)  # Support both formats

    # Prepare LLM request
    messages = [
        {"role": "system", "content": HYBRID_SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(capsule, indent=2)}
    ]

    # -----------------------------------------------------
    # Call ChatGPT API
    # -----------------------------------------------------
    if not OPENAI_API_KEY:
        return {
            "semantic_output": "[ERROR: OPENAI_API_KEY not set]",
            "pf_metadata": {}
        }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.2
            },
            timeout=30.0
        )

        response.raise_for_status()
        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            
            # Ensure required fields exist
            if "semantic_output" not in parsed:
                parsed["semantic_output"] = content if isinstance(content, str) else str(content)
            if "pf_metadata" not in parsed:
                parsed["pf_metadata"] = {}
            
            return parsed
        except (json.JSONDecodeError, KeyError) as e:
            # If parsing fails, return fallback
            content = data.get("choices", [{}])[0].get("message", {}).get("content", str(data))
            return {
                "semantic_output": content if isinstance(content, str) else str(content),
                "pf_metadata": {}
            }
    except requests.RequestException as e:
        return {
            "semantic_output": f"[ERROR: LLM API call failed: {e}]",
            "pf_metadata": {}
        }
    except Exception as e:
        return {
            "semantic_output": f"[ERROR: {e}]",
            "pf_metadata": {}
        }

# =====================================================
# Health check endpoint
# =====================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "enabled": ENABLED,
        "model": MODEL,
        "mode": MODE,
        "api_key_set": bool(OPENAI_API_KEY)
    }

# =====================================================
# Server entry point
# =====================================================

if __name__ == "__main__":
    print("🌐 Starting ApopToSiS Local LLM Server on port 4000...")
    print(f"   Model: {MODEL}")
    print(f"   Mode: {MODE}")
    print(f"   Enabled: {ENABLED}")
    print(f"   API Key: {'✓ Set' if OPENAI_API_KEY else '✗ Not set'}")
    print()
    uvicorn.run(app, host="localhost", port=4000)

