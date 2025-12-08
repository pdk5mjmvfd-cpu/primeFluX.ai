# Agora Login + Discrete Agents Guide

**Status**: Implemented ✓  
**Date**: 2025-12-08

## Overview

The repo now requires login. Every Freeman has a unique, salted, device-bound identity. Discrete agents track workflows (code/data/ledger) and QuantaCoin flows per-user.

## Architecture

```
Your Passphrase + Device Fingerprint
    ↓
PBKDF2 (100k iterations)
    ↓
Wallet ID (unique to you + your MacBook)
    ↓
Discrete Agents (code/data/ledger)
    ↓
QuantaCoin Minted (tied to your wallet)
    ↓
Per-User Ledger (quantacoin_ledger/user_ledgers.jsonl)
```

## First Run

When you first run `apop_terminal.py`, you'll be prompted to create your identity:

```bash
cd ~/PrimeFluxAI/primeFluX.ai
source venv/bin/activate
python3 runtime/apop_terminal.py
```

You'll see:
```
============================================================
AGORA IDENTITY INITIALIZATION
============================================================
Your passphrase salts your soul to this device.
This cannot be changed. Choose wisely.
============================================================
Freeman passphrase (salt your soul): [enter your passphrase]
```

**Important**: Your passphrase is bound to your device. Choose wisely. This cannot be changed.

## Usage

### Basic Commands

```bash
# Default (data agent)
freeman → hello apop

# Code agent
freeman → code: optimize quanta minting

# Data agent
freeman → data: explore user patterns

# Ledger agent
freeman → ledger: validate proof chain
```

### Agent Types

- **code** (Praxis): Builds/optimizes code
- **data** (Eidos): Explores/expands data  
- **ledger** (Aegis): Validates QuantaCoin proofs

### QuantaCoin Tracking

Every mint is tied to your wallet ID. View your total:

```bash
python3 -c "
import json
from pathlib import Path
ledger = Path('quantacoin_ledger/user_ledgers.jsonl')
wallet_id = 'YOUR_WALLET_ID'  # From .quantacoin_id
total = sum(
    json.loads(l)['quanta_minted']
    for l in ledger.read_text().splitlines()
    if l and json.loads(l).get('wallet_id') == wallet_id
)
print(f'Your QuantaCoin: {total:.1f} Q')
"
```

## Files

- `core/identity/repo_login.py`: Login system
- `core/agents/discrete_agents.py`: Workflow agents
- `runtime/apop_terminal.py`: Main terminal (updated)
- `.quantacoin_id`: Your identity file (created on first run)
- `quantacoin_ledger/user_ledgers.jsonl`: Per-user QuantaCoin ledger

## Security

- Passphrase is never stored (only PBKDF2 hash)
- Wallet ID = SHA256(master_key + device_fingerprint)
- Device fingerprint = SHA256(user + uid)
- Each proof is signed with your wallet ID

## The Agora

This enables peer-to-peer consensus:
- Broadcast signed proofs to other Freemens' nodes
- 2/3 verify → block accepted
- No 51% attack — your proof is physics, not hashpower

## Next Steps

1. Run `python3 runtime/apop_terminal.py`
2. Create your identity (first run only)
3. Start minting QuantaCoin with discrete agents
4. Your wallet is now sovereign

---

**The repo is the vault. Agents are the guards. QuantaCoin is the blood.**
