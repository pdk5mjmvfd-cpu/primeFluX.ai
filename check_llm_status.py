#!/usr/bin/env python3
"""Check LLM setup status."""

import os
from pathlib import Path

print("="*60)
print("LLM Setup Status Check")
print("="*60)

# Check model
model_path = Path("models/phi-3-mini-4k-instruct-q4.gguf")
if model_path.exists():
    size_gb = model_path.stat().st_size / (1024**3)
    print(f"✅ Model downloaded: {size_gb:.1f}GB")
else:
    print("❌ Model not found")

# Check Python package
try:
    from llama_cpp import Llama
    print("✅ llama-cpp-python is installed")
    
    # Try to load the model
    if model_path.exists():
        try:
            llm = Llama(model_path=str(model_path), n_ctx=512, n_threads=4, verbose=False)
            print("✅ Model can be loaded successfully!")
            print("\n🎉 Everything is ready! Run: python3 runtime/offline_llm_bridge.py")
        except Exception as e:
            print(f"⚠️  Model found but can't load: {e}")
    else:
        print("⚠️  Package installed but model not found")
        
except ImportError:
    print("❌ llama-cpp-python NOT installed")
    print("   Run: pip install llama-cpp-python")

print("="*60)
