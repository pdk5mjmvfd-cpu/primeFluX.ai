#!/bin/bash
# Quick setup script to get Apop running with LLM voice

echo "============================================================"
echo "Setting up Apop with LLM Voice"
echo "============================================================"

# Step 1: Install llama-cpp-python
echo ""
echo "Step 1: Installing llama-cpp-python..."
pip install llama-cpp-python

# Step 2: Verify model exists
echo ""
echo "Step 2: Checking for model..."
if [ -f "models/phi-3-mini-4k-instruct-q4.gguf" ]; then
    echo "✅ Model found: models/phi-3-mini-4k-instruct-q4.gguf"
    ls -lh models/phi-3-mini-4k-instruct-q4.gguf
else
    echo "⚠️  Model not found. Downloading..."
    mkdir -p models
    curl -L -o models/phi-3-mini-4k-instruct-q4.gguf \
      https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf
fi

# Step 3: Run Apop
echo ""
echo "============================================================"
echo "Step 3: Starting Apop..."
echo "============================================================"
echo ""
python3 runtime/offline_llm_bridge.py
