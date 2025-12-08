#!/bin/bash
# Run Apop with virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Run ./setup_venv.sh first"
    exit 1
fi

# Run Apop
python3 runtime/offline_llm_bridge.py
