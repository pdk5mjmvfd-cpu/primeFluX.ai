"""
Mining Pilot - S19 XP Integration for Proof-of-Compression.

Simulates Bitmain Antminer S19 XP setup:
- 141 TH/s hashrate
- 3.01 kW power consumption
- 72 kWh daily draw
- Compress telemetry logs (50% via polyform)
- Mint ΦQ as "proof-of-compression"
"""

from __future__ import annotations

import json
import time
import math
from typing import Dict, Any, Optional
from .quanta_core import QuantaCoin

# S19 XP Specifications
S19_XP_HASHRATE = 141.0  # TH/s
S19_XP_POWER = 3010.0  # W
S19_XP_DAILY_KWH = 72.0  # kWh/day


class MiningPilot:
    """
    Mining Pilot - S19 XP simulation for proof-of-compression.
    
    Compresses telemetry logs and mints ΦQ as proof-of-compression.
    """
    
    def __init__(self, quanta_coin: Optional[QuantaCoin] = None):
        """
        Initialize Mining Pilot.
        
        Args:
            quanta_coin: Optional QuantaCoin instance
        """
        self.quanta_coin = quanta_coin or QuantaCoin()
        self.hashrate = S19_XP_HASHRATE
        self.power_consumption = S19_XP_POWER
        self.daily_kwh = S19_XP_DAILY_KWH
        self.telemetry_logs: list[Dict[str, Any]] = []
    
    def generate_telemetry(self) -> Dict[str, Any]:
        """
        Generate telemetry data for S19 XP.
        
        Returns:
            Telemetry data dictionary
        """
        current_time = time.time()
        
        telemetry = {
            "timestamp": current_time,
            "hashrate_th_s": self.hashrate,
            "power_w": self.power_consumption,
            "temperature_c": 65.0 + (math.sin(current_time / 100) * 5),  # Simulated temp
            "fan_speed_rpm": 3000 + int(math.sin(current_time / 50) * 500),
            "voltage_v": 220.0,
            "current_a": self.power_consumption / 220.0,
            "daily_kwh": self.daily_kwh,
            "uptime_hours": (current_time % 86400) / 3600.0,
            "blocks_found": int(current_time / 600) % 100,  # Simulated
            "errors": 0
        }
        
        return telemetry
    
    def compress_telemetry(
        self,
        telemetry_data: Dict[str, Any]
    ) -> tuple[float, int]:
        """
        Compress telemetry data and mint ΦQ.
        
        Target: 50% compression via polyform.
        
        Args:
            telemetry_data: Telemetry data to compress
            
        Returns:
            Tuple of (compression_ratio, quanta_minted)
        """
        # Original size
        original_json = json.dumps(telemetry_data, sort_keys=True)
        original_size = len(original_json.encode('utf-8'))
        
        # Compress using QuantaCoin mint_work
        # This uses polyform encoding internally
        compression_ratio = 0.50  # Target 50% compression
        quanta_minted = self.quanta_coin.mint_work(
            telemetry_data,
            compression_ratio
        )
        
        # Calculate actual compression ratio
        # (QuantaCoin stores compressed data in ledger)
        if hasattr(self.quanta_coin, 'ledger') and self.quanta_coin.ledger:
            # Get last mint event
            last_event = list(self.quanta_coin.ledger.values())[-1]
            if last_event.get("type") == "mint":
                actual_ratio = last_event.get("compression_ratio", compression_ratio)
            else:
                actual_ratio = compression_ratio
        else:
            actual_ratio = compression_ratio
        
        # Store telemetry log
        self.telemetry_logs.append(telemetry_data)
        
        return actual_ratio, quanta_minted
    
    def simulate_mining_day(self) -> Dict[str, Any]:
        """
        Simulate a full day of mining operations.
        
        Returns:
            Summary of mining day
        """
        # Generate telemetry every hour (24 samples)
        samples = []
        total_quanta = 0
        
        for hour in range(24):
            telemetry = self.generate_telemetry()
            compression_ratio, quanta = self.compress_telemetry(telemetry)
            
            samples.append({
                "hour": hour,
                "quanta_minted": quanta,
                "compression_ratio": compression_ratio
            })
            
            total_quanta += quanta
        
        # Calculate daily stats
        total_kwh = self.daily_kwh
        cost_per_kwh = 0.075  # Average: $0.05-$0.10/kWh
        daily_cost = total_kwh * cost_per_kwh
        
        return {
            "date": time.strftime("%Y-%m-%d"),
            "total_quanta_minted": total_quanta,
            "total_kwh": total_kwh,
            "daily_cost_usd": daily_cost,
            "samples": samples,
            "avg_compression_ratio": sum(s["compression_ratio"] for s in samples) / len(samples),
            "hashrate_th_s": self.hashrate,
            "power_w": self.power_consumption
        }
    
    def get_power_estimate(self, hours: float = 24.0) -> Dict[str, Any]:
        """
        Get power consumption estimate.
        
        Args:
            hours: Number of hours
            
        Returns:
            Power consumption details
        """
        kwh = (self.power_consumption / 1000.0) * hours
        cost_low = kwh * 0.05  # $0.05/kWh
        cost_high = kwh * 0.10  # $0.10/kWh
        
        return {
            "hours": hours,
            "kwh": kwh,
            "cost_range_usd": {
                "low": cost_low,
                "high": cost_high
            },
            "power_w": self.power_consumption
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "hashrate_th_s": self.hashrate,
            "power_consumption_w": self.power_consumption,
            "daily_kwh": self.daily_kwh,
            "telemetry_logs_count": len(self.telemetry_logs),
            "quanta_coin": self.quanta_coin.to_dict()
        }
