# QuantaCoin (ΦQ) Implementation Summary

## Overview

QuantaCoin (ΦQ) has been successfully integrated into the ApopToSiS v3 codebase as a utility token system for reversible work compression, powering agent interactions in the AI agora ecosystem.

## Core Concept

- **ΦQ = "quantum of meaningful work"** — minted via PrimeFlux operations
- **Primes = agent IDs** (users/families/orgs as classes via PrimeFlux duality)
- **Composites = event spaces** (transactions hashed into polyforms)
- **Ledger compresses exponentially** via β-decays and Z-partitions
- **Burns fuel spends** (e.g., partial $250 Scheels txn: 72% burned, 28% staked)
- **Unused balances stake for yields** (merch rewards/ΦQ APY: 2-5%)

## Files Created

### 1. `fluxai/quanta/__init__.py`
- Module initialization with QuantaCoin export

### 2. `fluxai/quanta/quanta_core.py`
- **QuantaCoin class**: Core utility token implementation
  - `mint_work()`: Mint ΦQ from compression work (proof-of-compression)
  - `burn_txn()`: Partial burn for transactions (72% burn, 28% stake)
  - `stake_balance()`: Stake unused balances with EMA updates
  - `agora_yield_calc()`: Calculate yields using β-decay (exp{−β𝓥(x)})
  - `compress_ledger()`: Compress ledger via β-decay (<50% size target)
  - Tax logging for W-2/1099 compliance

### 3. `fluxai/quanta/mining_pilot.py`
- **MiningPilot class**: S19 XP integration for proof-of-compression
  - Simulates Bitmain Antminer S19 XP (141 TH/s, 3.01 kW)
  - Generates telemetry data
  - Compresses telemetry logs (50% target via polyform)
  - Mints ΦQ as "proof-of-compression"
  - Daily mining simulation (72 kWh/day)

## Files Modified

### 1. `runtime/supervisor/supervisor.py`
- Added `quanta_coin` initialization
- Added `quanta_router()` method:
  - Detects transactions (e.g., Scheels POS: 2FA pin + thermal salt)
  - Routes to `QuantaCoin.burn_txn()`
  - Stakes via `stake_balance()`
  - Returns burn/stake/yield details

### 2. `experience/manager.py`
- Added `quanta_etch()` method:
  - Compresses experience delta to polyform lease
  - Creates lease structure: `{holder=p, epoch=e, ttl}`
  - Updates objects.json with ΦQ balances
  - Stores in ObjectMemory metadata

### 3. `apop.py`
- Added QuantaCoin imports (optional, graceful fallback)
- Added `handle_quanta_command()` function:
  - Parses quanta commands from user input
  - Commands supported:
    - `quanta txn: budget 250 scheels` — Process transaction
    - `quanta mint: telemetry` — Mint from compression
    - `quanta stake: 100` — Stake balance
    - `quanta yield: 2` — Calculate yield
- Integrated command handling in conversation loop

## Test Suite

### `tests/test_quanta.py`
Comprehensive test coverage:

1. **Mint/Burn Round-Trip Test**
   - $250 → burn $180 → stake $70 → yield >2%
   - Verifies complete transaction flow

2. **Ledger Compression Test**
   - 100 txns → <50% size via β-decay
   - Verifies exponential compression

3. **Integration Tests**
   - Supervisor.quanta_router() integration
   - ExperienceManager.quanta_etch() integration
   - Command parsing and execution

4. **Mining Pilot Tests**
   - Telemetry generation
   - Compression and minting
   - Full day simulation

5. **Legal Compliance Tests**
   - USD FMV logging for tax (W-2/1099)

## Key Features Implemented

### 1. PrimeFlux Math Integration
- **β-decay**: `exp{−β𝓥(x)}` for scaling
- **Z-partition**: `exp{Σ λ_p ṡ_p}` for multiplicative independence
- **Exponential epochs**: Lease structure with TTL
- **Polyform encoding**: Events compressed as PrimeFluxInt

### 2. Transaction Flow
```
$250 Transaction
  ├─ 72% burned ($180) → burn_txn()
  └─ 28% staked ($70) → stake_balance()
      └─ Yield accrued (2-5% APY)
          └─ Tax logged (USD FMV)
```

### 3. Proof-of-Compression
- Telemetry logs compressed via polyform (50% target)
- ΦQ minted based on compression ratio
- Mining pilot simulates S19 XP operations

### 4. Agora Ecosystem
- Agents share yields via multiplicative independence
- Staked balances accrue rewards
- DAO pool accumulates fees (10% of yields)

## Usage Examples

### Command Line
```bash
python apop.py
> quanta txn: budget 250 scheels
```

### Programmatic
```python
from fluxai.quanta.quanta_core import QuantaCoin

quanta = QuantaCoin()
# Mint from compression
quanta_minted = quanta.mint_work(telemetry_data, compression_ratio=0.50)

# Burn transaction
burn_result = quanta.burn_txn(250.0, event_space, salt)

# Stake balance
staked = quanta.stake_balance(70.0, holder_prime=2, ttl_epochs=30)

# Calculate yield
yield_info = quanta.agora_yield_calc(2, epoch=0)
```

## Backward Compatibility

- Optional imports (graceful fallback if unavailable)
- No breaking changes to existing code
- QuantaCoin initialized only if available
- Falls back to simple responses if polyform unavailable

## Legal Structure

- **Entity**: QuantaCoin DAO
- **Token**: ΦQ (Utility Token, non-security)
- **States**: Wyoming, Colorado (Series LLC + DAO)
- **Compliance**: DAO framework, no CFTC registration for compression work
- **Tax**: Logged as USD FMV for W-2/1099 income

## Mining Integration

- **Hardware**: Bitmain Antminer S19 XP (141 TH/s, 3.01 kW)
- **Power**: 72 kWh/day, $3.60-$7.20/day cost
- **Cooling**: Air-cooled (75-80 dB)
- **Firmware**: Braiiins OS (auto-tuning, dynamic frequency scaling)
- **Proof**: Compress telemetry logs → mint ΦQ

## Next Steps

1. **DAO Governance Stubs**: Add governance voting mechanisms
2. **Network Integration**: Connect to distributed ledger
3. **POS Integration**: Real-world point-of-sale integration
4. **Yield Optimization**: Advanced yield calculation algorithms
5. **Legal Compliance**: Full W-2/1099 reporting automation

## Validation

To validate the implementation:

```bash
# Run tests
pytest tests/test_quanta.py -v

# Test command line
python apop.py
> quanta txn: budget 250 scheels
> quanta mint: telemetry
> quanta yield: 2
```

Expected output for `quanta txn: budget 250 scheels`:
- Status: success
- Amount: 250.0
- Burned: 180.0 (72%)
- Staked: 70.0 (28%)
- Yield: >2% APY
- Polyform event with burn/stake log

## Summary

QuantaCoin (ΦQ) is now fully integrated into ApopToSiS v3, providing:
- ✅ Minting via proof-of-compression
- ✅ Partial burn transactions (72/28 split)
- ✅ Staking with yield accrual (2-5% APY)
- ✅ Ledger compression via β-decay
- ✅ Tax compliance logging
- ✅ Mining pilot integration
- ✅ Command-line interface
- ✅ Comprehensive test suite
- ✅ Backward compatibility

The Agora ecosystem is ready to hum! 🚀
