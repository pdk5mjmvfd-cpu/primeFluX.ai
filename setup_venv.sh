#!/bin/bash
# Setup virtual environment and install dependencies

echo "============================================================"
echo "Setting up PrimeFlux AI Virtual Environment"
echo "============================================================"

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate venv
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install llama-cpp-python
echo ""
echo "Installing llama-cpp-python (this may take a few minutes)..."
pip install llama-cpp-python

# Install any other dependencies if needed
echo ""
echo "Checking for other dependencies..."
if [ -f "requirements_offline.txt" ]; then
    echo "Installing from requirements_offline.txt..."
    pip install -r requirements_offline.txt
elif [ -f "requirements.txt" ]; then
    echo "Installing from requirements.txt..."
    pip install -r requirements.txt
fi

echo ""
echo "============================================================"
echo "✅ Setup complete!"
echo "============================================================"
echo ""
echo "To activate the venv in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "Then run Apop:"
echo "  python3 runtime/offline_llm_bridge.py"
echo ""
