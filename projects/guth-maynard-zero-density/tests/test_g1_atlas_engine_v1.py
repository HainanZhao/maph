"""Regression tests for the quarantined Cycle-3 G1 discovery engine."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from discovery import run_g1_atlas_v1 as engine  # noqa: E402


class G1AtlasEngineV1Tests(unittest.TestCase):
    def test_exact_rational_power_and_reference_splitmix64(self) -> None:
        self.assertEqual(engine.floor_rational_power(4096, Fraction(4, 5)), 776)
        self.assertEqual(engine.floor_rational_power(4096, Fraction(2, 3)), 256)
        stream = engine.SplitMix64(0)
        self.assertEqual(stream.next_u64(), 0xE220A8397B1DCDAF)
        self.assertEqual(stream.next_u64(), 0x6E789E6AA1B965F4)

    def test_exact_energy_matches_independent_direct_quadruple_count(self) -> None:
        points = [0, 2, 5]
        budget = engine.RowBudget(U=64, v=Fraction(7, 10), started=0.0, cpu_started=0.0, seconds_cap=10**9)
        observed = engine.exact_energy(points, budget)
        direct = sum(1 for a in points for b in points for c in points for d in points if abs(a + b - c - d) <= 1)
        self.assertEqual(observed, direct)

    def test_frozen_structural_anchor_and_optimization_safe_integrity(self) -> None:
        report = engine.integrity_report()
        self.assertEqual(report["structural_local_rows"], 7744)
        self.assertEqual(report["screen_rows"], 588)
        self.assertEqual(report["mandatory_energy_anchor"], {"E1": "5/3", "E2": "5/3", "E3": "5/3"})
        command = [sys.executable, "-O", str(PROJECT / "discovery/run_g1_atlas_v1.py"), "--check-integrity"]
        result = subprocess.run(command, cwd=PROJECT, check=True, capture_output=True, text=True)
        self.assertIn('"screen_rows": 588', result.stdout)

    def test_small_frozen_row_is_deterministic_at_both_precisions(self) -> None:
        spec = engine.canonical_screen_specs()[1]  # frozen C0/W1 coordinate
        first, _ = engine.run_screen_row(spec, U=64, scale_label="test-64")
        second, _ = engine.run_screen_row(spec, U=64, scale_label="test-64")
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "COMPLETED")
        self.assertEqual(len(first["recognized_observables"]["evaluations"]), 2)
        self.assertTrue(first["validity"]["one_separated"])

    def test_infeasible_registered_set_is_retained_not_dropped(self) -> None:
        # This is the first w=2/3 screen coordinate paired with W0-sidon.
        row, _ = engine.run_screen_row(engine.canonical_screen_specs()[14], U=64, scale_label="test-64")
        self.assertEqual(row["status"], "FAILED")
        self.assertEqual(row["failure"]["code"], "INFEASIBLE_CARDINALITY")
        self.assertFalse(row["retention"]["eligible"])

    def test_decimal_quota_ranking_preserves_near_tie_order(self) -> None:
        def row(row_id: str, score: str) -> dict:
            return {
                "row_id": row_id, "status": "COMPLETED",
                "family": {"declared_energy_regime": "intermediate", "coefficient": "C0-flat"},
                "retention": {"eligible": True, "score": score, "reason": "PENDING_GLOBAL_QUOTA"},
            }
        scores = [
            row("G1-S002", "1.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"),
            row("G1-S001", "1.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002"),
            row("G1-S000", "1.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003"),
        ]
        self.assertEqual(engine.retention_selection(scores), ["G1-S000", "G1-S001"])
        self.assertEqual(scores[0]["retention"]["reason"], "QUOTA_PER_REGIME_COEFFICIENT")


if __name__ == "__main__":
    unittest.main()
