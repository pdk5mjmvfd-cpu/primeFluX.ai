"""
Unit tests for PrimeFlux Presence MVP.

Tests determinism, reversibility, nat accounting, and integration.
"""

import pytest
import json
import math
from pathlib import Path
import tempfile
import shutil

from core.math.pf_presence import PresenceVector
from core.math.pf_trig_osc import Oscillator
from core.math.pf_nat_energy import NatEnergyAuditor


class TestPresenceVector:
    """Test PresenceVector class."""
    
    def test_presence_determinism(self):
        """Same input → same vector always."""
        v1 = PresenceVector.from_distinction("hello")
        v2 = PresenceVector.from_distinction("hello")
        assert v1.components == v2.components
    
    def test_presence_different_inputs(self):
        """Different inputs → different vectors."""
        v1 = PresenceVector.from_distinction("hello")
        v2 = PresenceVector.from_distinction("world")
        assert v1.components != v2.components
    
    def test_flip_rail_involution(self):
        """Flipping twice returns original."""
        v = PresenceVector([1, 0, -1])
        v2 = v.flip_rail(0).flip_rail(0)
        assert v.components == v2.components
    
    def test_flip_rail_zero_component(self):
        """Flipping zero component does nothing."""
        v = PresenceVector([1, 0, -1])
        v2 = v.flip_rail(1)  # Flip zero component
        assert v.components == v2.components
    
    def test_presence_bounds(self):
        """Only {-1, 0, 1} allowed."""
        with pytest.raises(ValueError):
            PresenceVector([2, 0, -1])
    
    def test_to_bitstring_reversibility(self):
        """Presence → bitstring conversion works."""
        v = PresenceVector([1, 0, -1, 1])
        bits = v.to_bitstring(width=8)
        assert len(bits) == 8
        assert isinstance(bits, str)
        assert all(c in "01" for c in bits)
    
    def test_from_distinction_dimension(self):
        """Can specify dimension."""
        v1 = PresenceVector.from_distinction("test", dim=32)
        v2 = PresenceVector.from_distinction("test", dim=64)
        assert len(v1) == 32
        assert len(v2) == 64


class TestOscillator:
    """Test Oscillator class."""
    
    def test_osc_nat_accumulation(self):
        """Nat error accumulates per step."""
        pv = PresenceVector.from_distinction("test", dim=64)
        osc = Oscillator(pv, max_steps=8)
        
        # Run one step, check nat error is ~64 * 3 * 36.04
        osc.step()
        expected_nats = 64 * 3 * Oscillator.NAT_PER_TRIG_OP
        assert abs(osc.nat_error - expected_nats) < 100  # Allow tolerance
    
    def test_projection_idempotence(self):
        """Projecting an already-projected vector yields same result."""
        raw = [1.2, 0.1, -1.3, 0.0]
        proj1 = Oscillator.project_to_lattice(raw)
        # Project again using components as floats
        proj2 = Oscillator.project_to_lattice([float(x) for x in proj1.components])
        assert proj1.components == proj2.components
    
    def test_history_length(self):
        """History includes initial + steps."""
        pv = PresenceVector.from_distinction("test", dim=64)
        osc = Oscillator(pv, max_steps=3, keep_history=True)
        osc.step()
        osc.step()
        assert len(osc.history) == 3  # initial + 2 steps
    
    def test_max_steps_enforcement(self):
        """Oscillator stops at max_steps."""
        pv = PresenceVector.from_distinction("test", dim=64)
        osc = Oscillator(pv, max_steps=3)
        
        step_count = 0
        while osc.step():
            step_count += 1
        
        assert step_count == 3
        assert len(osc.history) == 4  # initial + 3 steps
    
    def test_deterministic_replay(self):
        """Same seed → same osc history."""
        pv1 = PresenceVector.from_distinction("test", dim=64)
        pv2 = PresenceVector.from_distinction("test", dim=64)
        
        osc1 = Oscillator(pv1, max_steps=5, seed=1.618)
        osc2 = Oscillator(pv2, max_steps=5, seed=1.618)
        
        while osc1.step():
            pass
        while osc2.step():
            pass
        
        assert osc1.history == osc2.history
        assert abs(osc1.nat_error - osc2.nat_error) < 1e-10
    
    def test_nat_ceiling(self):
        """Nat ceiling calculation is correct."""
        pv = PresenceVector.from_distinction("test", dim=64)
        osc = Oscillator(pv, max_steps=8)
        ceiling = osc.get_nat_ceiling()
        expected = 8 * 64 * 3 * Oscillator.NAT_PER_TRIG_OP
        assert abs(ceiling - expected) < 1e-6


class TestNatEnergyAuditor:
    """Test NatEnergyAuditor class."""
    
    @pytest.fixture
    def temp_log_dir(self):
        """Create temporary log directory."""
        temp_dir = Path(tempfile.mkdtemp())
        original_dir = NatEnergyAuditor.LOG_DIR
        NatEnergyAuditor.LOG_DIR = temp_dir
        yield temp_dir
        shutil.rmtree(temp_dir)
        NatEnergyAuditor.LOG_DIR = original_dir
    
    def test_log_jsonl_validity(self, temp_log_dir):
        """Each log line is valid JSON."""
        pv = PresenceVector.from_distinction("test", dim=64)
        osc = Oscillator(pv, max_steps=2)
        osc.step()
        osc.step()
        
        report = NatEnergyAuditor.compress_and_log(osc, "test")
        
        # Read back the log file
        log_files = list(temp_log_dir.glob("memory_*.jsonl"))
        assert len(log_files) > 0
        
        lines = log_files[0].read_text().strip().split("\n")
        for line in lines:
            if line.strip():
                json.loads(line)  # Should not raise
    
    def test_capsule_fields(self, temp_log_dir):
        """Report contains required fields for QuantaCoin integration."""
        pv = PresenceVector.from_distinction("test", dim=64)
        osc = Oscillator(pv, max_steps=2)
        osc.step()
        osc.step()
        
        report = NatEnergyAuditor.compress_and_log(osc, "test")
        
        required = [
            "timestamp",
            "source_text",
            "steps",
            "final_presence",
            "nat_error_total",
            "energy_joules_est",
            "quanta_minted",
            "sparsity_gain",
            "capsule_id",
            "reversible",
        ]
        for field in required:
            assert field in report
    
    def test_quanta_minting_formula(self, temp_log_dir):
        """QuantaCoin minting follows exact formula."""
        pv = PresenceVector.from_distinction("test", dim=64)
        osc = Oscillator(pv, max_steps=8)
        
        while osc.step():
            pass
        
        initial = osc.history[0]
        final = osc.history[-1]
        
        # Calculate manually
        initial_nonzero = sum(1 for x in initial.components if x != 0)
        final_nonzero = sum(1 for x in final.components if x != 0)
        sparsity_gain = initial_nonzero - final_nonzero
        nats_from_sparsity = sparsity_gain / math.log(2)
        nats_preserved = nats_from_sparsity - osc.nat_error
        
        # Compare with auditor
        report = NatEnergyAuditor.compress_and_log(osc, "test")
        
        # Allow small floating-point differences
        assert abs(report["quanta_minted"] - max(nats_preserved, 0)) < 0.1
    
    def test_aggregate_stats(self, temp_log_dir):
        """Aggregate stats computation works."""
        # Create multiple compressions
        for text in ["test1", "test2", "test3"]:
            pv = PresenceVector.from_distinction(text, dim=64)
            osc = Oscillator(pv, max_steps=3)
            while osc.step():
                pass
            NatEnergyAuditor.compress_and_log(osc, text)
        
        stats = NatEnergyAuditor.aggregate_stats()
        
        assert stats["total_compressions"] == 3
        assert stats["avg_nats"] > 0
        assert stats["total_quanta_minted"] >= 0


class TestIntegration:
    """End-to-end integration tests."""
    
    @pytest.fixture
    def temp_log_dir(self):
        """Create temporary log directory."""
        temp_dir = Path(tempfile.mkdtemp())
        original_dir = NatEnergyAuditor.LOG_DIR
        NatEnergyAuditor.LOG_DIR = temp_dir
        yield temp_dir
        shutil.rmtree(temp_dir)
        NatEnergyAuditor.LOG_DIR = original_dir
    
    def test_end_to_end_presence_flow(self, temp_log_dir):
        """Full MVP pipeline: text → presence → osc → log."""
        input_text = "the consciousness compresses itself"
        pv = PresenceVector.from_distinction(input_text)
        osc = Oscillator(pv, max_steps=8)
        
        # Run all 8 steps
        while osc.step():
            pass
        
        # Log and verify
        report = NatEnergyAuditor.compress_and_log(osc, input_text)
        
        assert report["steps"] == 8
        assert report["nat_error_total"] > 0
        assert len(report["final_presence"]) == 64
        
        # Verify log file exists and is JSONL
        log_files = list(temp_log_dir.glob("memory_*.jsonl"))
        assert len(log_files) > 0
        
        lines = log_files[0].read_text().strip().split("\n")
        for line in lines:
            if line.strip():
                json.loads(line)  # Must be valid JSON
    
    def test_deterministic_compression(self, temp_log_dir):
        """Same input always yields same compression."""
        input_text = "determinism is law"
        
        # Run 1
        pv1 = PresenceVector.from_distinction(input_text)
        osc1 = Oscillator(pv1, max_steps=8)
        while osc1.step():
            pass
        nat1 = osc1.nat_error
        
        # Run 2
        pv2 = PresenceVector.from_distinction(input_text)
        osc2 = Oscillator(pv2, max_steps=8)
        while osc2.step():
            pass
        nat2 = osc2.nat_error
        
        # Should be identical
        assert pv1.components == pv2.components
        assert abs(nat1 - nat2) < 1e-10
        assert osc1.history == osc2.history
    
    def test_imports_work(self):
        """All modules can be imported cleanly."""
        from core.math import PresenceVector, Oscillator, NatEnergyAuditor
        assert PresenceVector is not None
        assert Oscillator is not None
        assert NatEnergyAuditor is not None
