"""Hostile regressions for the corrected G1 finite-probe driver."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from discovery import run_g1_atlas_v2 as engine  # noqa: E402


class G1AtlasEngineV2Tests(unittest.TestCase):
    def test_runtime_and_source_integrity_is_explicit(self) -> None:
        report = engine.integrity_report()
        self.assertEqual(report["runtime"], {
            "implementation": "CPython", "python": "3.12.3",
            "mpmath": "1.2.1", "optimization_level": 0,
        })
        self.assertEqual(report["screen_rows"], 588)
        self.assertEqual(report["finite_row_cap"], 660)

    def test_optimized_mode_fails_closed(self) -> None:
        command = [sys.executable, "-O", str(PROJECT / "discovery/run_g1_atlas_v2.py"), "--check-integrity"]
        result = subprocess.run(command, cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("optimization mode", result.stderr)

    def test_unexpected_exception_is_sanitized_and_retained(self) -> None:
        spec = engine.base.canonical_screen_specs()[1]
        message = f"bad pointer 0xdeadbeef at {PROJECT} pid=12345"
        with patch.object(engine.base, "run_screen_row", side_effect=ValueError(message)):
            row, performance = engine.safe_run_row(spec, 64, "test-64")
        self.assertEqual(row["status"], "FAILED")
        self.assertEqual(row["failure"]["code"], "UNEXPECTED_EXCEPTION_VALUEERROR")
        sanitized = row["failure"]["detail"]["sanitized_message"]
        self.assertNotIn(str(PROJECT), sanitized)
        self.assertNotIn("deadbeef", sanitized)
        self.assertNotIn("12345", sanitized)
        self.assertIn("<PROJECT>", sanitized)
        self.assertGreaterEqual(performance["cpu_seconds"], 0)

    def test_keyboard_interrupt_and_system_exit_propagate(self) -> None:
        spec = engine.base.canonical_screen_specs()[1]
        with patch.object(engine.base, "run_screen_row", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                engine.safe_run_row(spec, 64, "test-64")
        with patch.object(engine.base, "run_screen_row", side_effect=SystemExit(3)):
            with self.assertRaises(SystemExit):
                engine.safe_run_row(spec, 64, "test-64")

    def test_validation_score_loss_has_distinct_literal_status(self) -> None:
        screen = {"retention": {"score": "-0.1000000000000000000000000000001"}}
        validation = {"status": "COMPLETED", "retention": {"score": "-0.1000000000000000000000000000002", "eligible": False}}
        comparison = engine.validation_comparison(validation, screen)
        self.assertEqual(comparison["status"], "SCORE_LOSS_FALSIFIER")
        validation["retention"]["score"] = screen["retention"]["score"]
        self.assertEqual(engine.validation_comparison(validation, screen)["status"], "NO_SCORE_LOSS")
        validation["status"] = "FAILED"
        self.assertEqual(engine.validation_comparison(validation, screen)["status"], "VALIDATION_EXECUTION_FAILURE")

    def test_atomic_checkpoint_roundtrip_and_tamper_failure(self) -> None:
        runtime = engine.check_runtime()
        checkpoint = engine.new_checkpoint(runtime)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            engine.atomic_replace(path, checkpoint)
            loaded = engine.load_checkpoint(path, runtime)
            self.assertEqual(loaded, checkpoint)
            loaded["engine"]["v1_sha256"] = "0" * 64
            engine.atomic_replace(path, loaded)
            with self.assertRaisesRegex(RuntimeError, "v1 engine hash mismatch"):
                engine.load_checkpoint(path, runtime)

    def test_screen_summary_exposes_zero_feasible_low_rows(self) -> None:
        spec = engine.base.canonical_screen_specs()[0]
        failed = engine.base.failed_screen_row(spec, engine.base.SCREEN_SCALE, "INFEASIBLE_CARDINALITY", {}, scale_label="2^12")
        checkpoint = {"screen_rows": [failed], "selected_screen_row_ids": [], "validation_rows": []}
        summary = engine.screen_outcome_summary(checkpoint)
        self.assertEqual(summary["low_regime_status"], "NO_FEASIBLE_LOW_REGIME_ROWS")
        self.assertEqual(summary["retention_status"], "NO_RETAINED")
        self.assertTrue(summary["no_retuning"])


if __name__ == "__main__":
    unittest.main()
