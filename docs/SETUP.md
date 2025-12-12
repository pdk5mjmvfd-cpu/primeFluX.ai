# Setup Guide

## Quick Start

### Installation

**Option 1: pip install (Recommended)**
```bash
pip install primeflux-ai
```

**Option 2: git clone (Development)**
```bash
git clone https://github.com/pdk5mjmvfd-cpu/primeFluX.ai
cd primeFluX.ai
pip install -e .
```

**Option 3: Docker**
```bash
docker-compose up --build
```

### First Run

**Terminal Initialization (Recommended for first-time users)**
```bash
python apop.py --init
```

This runs the 3-step initialization:
1. Initialize runtime (PFState, ICM, LCM, Supervisor)
2. Hardware-as-repo (explain repo structure = PF manifold)
3. Absorb anything (demonstrate capability)

### Virtual Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Offline LLM Setup

**Using Ollama (Recommended)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.2:3b

# Set environment variable
export OLLAMA_MODEL=llama3.2:3b
```

**Using llama.cpp**
```bash
# Download GGUF model
wget https://huggingface.co/.../model.gguf

# Run server
python -m llama_cpp.server --model model.gguf --n_gpu_layers 99
```

### Environment Variables

Create `.env` file:
```bash
PRESENCE_OP=1
APOP_MODE=local
OLLAMA_MODEL=llama3.2:3b
QUANTA_PATH=./experience/ledger.jsonl
AGORA_ENABLED=0
DISCRETE_SHELLS=1
```

### Docker Setup

**Quick Start**
```bash
# Copy environment template
cp .env.example .env

# Build and run
docker-compose up --build

# Access services
# - FastAPI: http://localhost:8000
# - Streamlit UI: http://localhost:8501
```

**Raspberry Pi / Jetson (ARM64)**
```bash
# Build for ARM64
docker-compose build --build-arg ARCH=arm64

# Run
docker-compose up
```

### Troubleshooting

**Import Errors**
```bash
# Ensure you're in the project root
cd /path/to/primeFluX.ai

# Install in development mode
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

**LLM Connection Issues**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check llama.cpp server
curl http://localhost:8080/health
```

**Dependencies**
```bash
# Install all requirements
pip install -r requirements.txt

# For cognitive features
pip install -r requirements_cognitive.txt

# For offline LLM
pip install -r requirements_offline.txt
```

## Next Steps

- Read [ONTOLOGY.md](../ONTOLOGY.md) for core concepts
- Read [docs/QUANTACOIN.md](QUANTACOIN.md) for QuantaCoin details
- See [README.md](../README.md) for usage examples

