# Fix: "pip: command not found"

## The Issue

On macOS, `pip` might not be in your PATH. Use one of these instead:

## Solution 1: Use `pip3` (Most Common)

```bash
pip3 install llama-cpp-python
```

## Solution 2: Use `python3 -m pip` (Always Works)

```bash
python3 -m pip install llama-cpp-python
```

## Solution 3: Check What You Have

Run this to see what's available:

```bash
which pip3
which python3
python3 -m pip --version
```

## Recommended Command

Use this (it always works):

```bash
python3 -m pip install llama-cpp-python
```

Then run Apop:

```bash
python3 runtime/offline_llm_bridge.py
```

---

**TL;DR**: Use `python3 -m pip` instead of just `pip`
