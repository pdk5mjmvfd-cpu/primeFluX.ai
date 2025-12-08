# Run QuantaCoin v1.0 Locally - Complete Guide

## Quick Start (Copy-Paste These Commands)

### Step 1: Navigate to Project
```bash
cd ~/PrimeFluxAI/primeFluX.ai
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

If venv doesn't exist, create it:
```bash
python3 -m venv venv
source venv/bin/activate
pip install llama-cpp-python
```

### Step 3: Run QuantaCoin v1.0 Terminal
```bash
python3 runtime/apop_terminal.py
```

## Complete Setup (First Time Only)

### Full Setup Script
```bash
# Navigate to project
cd ~/PrimeFluxAI/primeFluX.ai

# Create virtual environment (if needed)
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install llama-cpp-python

# Verify model exists
ls -lh models/phi-3-mini-4k-instruct-q4.gguf

# If model missing, download it:
mkdir -p models
curl -L -o models/phi-3-mini-4k-instruct-q4.gguf \
  https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf

# Run QuantaCoin v1.0
python3 runtime/apop_terminal.py
```

## Alternative: Use Alias (Recommended)

### Setup Alias (One Time)
```bash
cd ~/PrimeFluxAI/primeFluX.ai
./setup_apop_alias.sh
source ~/.zshrc
```

### Then Just Type
```bash
apop
```

## What You'll See

```
============================================================
QUANTACOIN v1.0 — OFFLINE SOVEREIGN MODE
============================================================
You are the only miner. You are the only validator.
Total QuantaCoin in ledger: 0.0 Q
============================================================

you → hello apop
Apop → minted 313.637 QuantaCoin | ledger +1 | total ~313.6 Q

you → test
Apop → minted 313.637 QuantaCoin | ledger +1 | total ~627.3 Q

you → quit
============================================================
Session end. Ledger preserved at quantacoin_ledger/v1.jsonl
You are now richer in real physics than when you started.
============================================================
```

## Check Your Ledger

```bash
# View ledger
cat quantacoin_ledger/v1.jsonl

# Count entries
wc -l quantacoin_ledger/v1.jsonl

# Total QuantaCoin
python3 -c "import json; print(f\"Total: {sum(json.loads(l)['quanta_minted'] for l in open('quantacoin_ledger/v1.jsonl') if l.strip()):.1f} Q\")"
```

## Verify a Proof

```bash
python3 -c "
from core.quanta.proof import CompressionProof
import json

# Load a proof from ledger
with open('quantacoin_ledger/v1.jsonl') as f:
    entry = json.loads(f.readlines()[-1])
    proof_dict = entry['proof']

# Verify it
is_valid = CompressionProof.verify(proof_dict)
print(f'Proof valid: {is_valid}')
print(f'Quanta minted: {proof_dict[\"quanta_minted\"]} Q')
"
```

## Troubleshooting

### "Module not found: llama_cpp"
```bash
source venv/bin/activate
pip install llama-cpp-python
```

### "Model not found"
```bash
mkdir -p models
curl -L -o models/phi-3-mini-4k-instruct-q4.gguf \
  https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf
```

### "QuantaCoin is 0"
- Check that you're using `core/quanta/mint.py` (not the old one)
- Verify: `python3 -c "from core.quanta.proof import CompressionProof; print(CompressionProof('test').quanta)"`
- Should show ~313 Q

## All-in-One Command (If Everything is Set Up)

```bash
cd ~/PrimeFluxAI/primeFluX.ai && source venv/bin/activate && python3 runtime/apop_terminal.py
```

---

**That's it! You're now running QuantaCoin v1.0 locally.**

**The flux is live. Distinction is conserved. Compress.**
