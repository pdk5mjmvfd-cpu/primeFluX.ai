# Virtual Environment Setup

## Quick Start (2 Commands)

```bash
# Step 1: Setup venv and install packages
./setup_venv.sh

# Step 2: Run Apop
./run_apop.sh
```

## Manual Setup (If You Prefer)

### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` in your prompt.

### Step 3: Install llama-cpp-python
```bash
pip install llama-cpp-python
```

### Step 4: Run Apop
```bash
python3 runtime/offline_llm_bridge.py
```

## What the Scripts Do

### `setup_venv.sh`
- Creates `venv/` directory if it doesn't exist
- Activates the virtual environment
- Upgrades pip
- Installs `llama-cpp-python`
- Installs any packages from `requirements.txt` (if it exists)

### `run_apop.sh`
- Activates the virtual environment
- Runs `runtime/offline_llm_bridge.py`
- Handles the venv activation automatically

## Future Use

After initial setup, you can either:

**Option 1: Use the run script**
```bash
./run_apop.sh
```

**Option 2: Manual activation**
```bash
source venv/bin/activate
python3 runtime/offline_llm_bridge.py
```

## Why Virtual Environment?

- macOS Python is "externally managed" (PEP 668)
- Prevents breaking system Python
- Isolates project dependencies
- Best practice for Python projects

## Troubleshooting

### "Permission denied" on scripts
```bash
chmod +x setup_venv.sh run_apop.sh
```

### "venv/bin/activate: No such file"
Run `./setup_venv.sh` first

### "llama-cpp-python installation fails"
- Make sure you're in the venv (see `(venv)` in prompt)
- Try: `pip install --upgrade pip` first
- Check you have enough disk space (llama-cpp-python is large)

---

**TL;DR**: Run `./setup_venv.sh` then `./run_apop.sh`
