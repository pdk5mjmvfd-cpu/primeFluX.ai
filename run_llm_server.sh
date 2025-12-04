#!/bin/bash

echo "🔌 Starting ApopToSiS LLM Relay Server..."

# Activate the main venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "✓ Virtual environment created"
fi

# Install server dependencies if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing server dependencies..."
    pip install -q -r api/requirements_server.txt
fi

# Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY not set!"
    echo "   Set it with: export OPENAI_API_KEY='sk-...'"
    echo "   Or add to ~/.zshrc for persistence"
    echo ""
fi

# Navigate to api directory
cd api

# Run server
python apop_llm_server.py

