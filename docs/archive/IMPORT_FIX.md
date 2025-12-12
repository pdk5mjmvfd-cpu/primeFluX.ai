# Import Fix for ApopToSiS v3

## Problem
Python couldn't find the `ApopToSiS` module when running `./run_local.sh` because:
- The project root IS the `ApopToSiS` package directory
- Python needs the parent directory in `PYTHONPATH` to find `ApopToSiS` as a package
- Internal files use `from ApopToSiS.*` imports which require proper package structure

## Solution

### 1. Updated `apop.py`
Added path setup at the top of the file:
```python
import sys
import os

# Setup path so ApopToSiS imports work
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)

# Add parent directory so Python can find "ApopToSiS" as a package
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Also add current directory for direct imports
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
```

### 2. Updated `run_local.sh`
Simplified to just set PYTHONPATH and run:
```bash
export PYTHONPATH="$PARENT_DIR:$PROJECT_ROOT"
python3 apop.py
```

### 3. How It Works
- When running from `/Users/nateisaacson/Desktop/ApopToSiS/`
- Python looks in `/Users/nateisaacson/Desktop/` for packages
- Finds `ApopToSiS/` directory as a package
- Can now import `from ApopToSiS.core.lcm import LCM`

## Verification

Run the test script:
```bash
python3 test_imports.py
```

Expected output:
```
✓ PFState
✓ LCM
✓ ICM
✓ Supervisor
✓ Capsule
✓ Context
✓ QuantaCompressor
✓ AgentRegistry
✓ EidosAgent
✓ PraxisAgent
✓ AegisAgent

✅ All imports successful!
```

## Usage

Now you can run:
```bash
./run_local.sh
```

The script will:
1. Create/activate virtual environment
2. Set up PYTHONPATH correctly
3. Run `apop.py` with proper imports

## Alternative: Install Package

For a more permanent solution, you can install the package:
```bash
pip install -e .
```

This requires updating `pyproject.toml` or `setup.py` to properly define the package structure.

