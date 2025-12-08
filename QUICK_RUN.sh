#!/bin/bash
# Quick run script for QuantaCoin v1.0

cd "$(dirname "$0")"

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install llama-cpp-python
fi

# Check for model
if [ ! -f "models/phi-3-mini-4k-instruct-q4.gguf" ]; then
    echo "⚠️  Model not found. Downloading..."
    mkdir -p models
    curl -L -o models/phi-3-mini-4k-instruct-q4.gguf \
      https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf
fi

# Run QuantaCoin v1.0
python3 runtime/apop_terminal.py
