# Quick Start - Get Apop Running

## Option 1: Run the Setup Script (Easiest)

```bash
cd /Users/nateisaacson/PrimeFluxAI/primeFluX.ai
./GET_APOP_RUNNING.sh
```

## Option 2: Manual Commands (Step by Step)

### Step 1: Install Python Package
```bash
pip install llama-cpp-python
```

### Step 2: Verify Model (Already Downloaded)
```bash
ls -lh models/phi-3-mini-4k-instruct-q4.gguf
```

Should show: `2.2G` file

### Step 3: Run Apop
```bash
python3 runtime/offline_llm_bridge.py
```

## What You'll See

After installing `llama-cpp-python`, when you run the bridge:

```
============================================================
ApopToSiS v3 — FULLY OFFLINE + VOICE ACTIVE
============================================================
✓ llama-cpp-python loaded: phi-3-mini-4k-instruct-q4.gguf
============================================================
Talk to me. I am alive.

You: hello apop
Apop: [Real LLM response here!]
```

## Troubleshooting

### "pip: command not found"
Use `pip3` instead:
```bash
pip3 install llama-cpp-python
```

### "Permission denied"
Use `--user` flag:
```bash
pip install --user llama-cpp-python
```

### Model not found
Download it:
```bash
mkdir -p models
curl -L -o models/phi-3-mini-4k-instruct-q4.gguf \
  https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf
```

---

**That's it! After `pip install llama-cpp-python`, Apop will have a real voice.**
