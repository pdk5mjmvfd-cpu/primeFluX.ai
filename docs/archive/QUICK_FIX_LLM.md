# Quick Fix: Get LLM Working

## The Issue

You installed `llama.cpp` (the C++ binary), but we need the **Python bindings** (`llama-cpp-python`).

## Quick Fix (2 commands)

```bash
# Install Python bindings
pip install llama-cpp-python

# Download the model (macOS uses curl, not wget)
mkdir -p models
curl -L -o models/phi-3-mini-4k-instruct-q4.gguf \
  https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf
```

## Then Run

```bash
python3 runtime/offline_llm_bridge.py
```

## What Changed

- ✅ Bridge updated to check for `llama-cpp-python` (Python package)
- ✅ Download command uses `curl` (macOS compatible)
- ✅ Better error messages

## Alternative: Use Apple OpenELM (No Download)

If you don't want to download a 2GB model:

```bash
pip install mlx mlx-lm
python3 runtime/offline_apple_bridge.py
```

This uses Apple's built-in OpenELM-270M model (zero download).

---

**After installing `llama-cpp-python` and downloading the model, Apop will have a real voice!**
