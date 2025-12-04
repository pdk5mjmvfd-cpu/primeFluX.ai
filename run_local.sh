#!/bin/bash

echo "🌐 Starting ApopToSiS v3 Local Runtime..."

# ensure virtual env
if [ ! -d ".venv" ]; then
    echo "Creating venv..."
    python3 -m venv .venv
fi

# Activate virtual environment (must exist)
source .venv/bin/activate

# Install cognitive engine dependencies if needed
if ! python3 -c "import numpy" 2>/dev/null; then
    echo "Installing cognitive engine dependencies..."
    .venv/bin/pip install -q numpy==1.24.3 requests fastapi uvicorn
fi

# Get the parent directory (where ApopToSiS package should be found)
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(dirname "$PROJECT_ROOT")"

# Set PYTHONPATH so Python can find ApopToSiS as a package
export PYTHONPATH="$PARENT_DIR:$PROJECT_ROOT"
export APOPTOSIS_ENV="local"

python3 apop.py

