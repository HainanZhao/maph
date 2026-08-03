"""Regression checks for Cycle 222's source-normalization cocycle audit."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_222_z_label_cocycle import run  # noqa: E402


class ZLabelCocycleTests(unittest.TestCase):
    def test_complete_shift_torsor_and_source_boundary(self) -> None:
        result = run()
        cocycle = result["first_shift_coboundary_audit"]
        self.assertEqual(cocycle["orbit_size"], 24)
        self.assertEqual(cocycle["normalized_solution"]["0"], 1)
        self.assertEqual(cocycle["normalized_solution"]["5"], -1)
        self.assertTrue(result["formal_reflection_constraint_audit"]["compatibility"])
        source = result["source_z_phase_audit"]
        self.assertEqual(source["z_quadratic_phase_coefficient"], "((1-s)k-p)/(2k)=-547/48")
        self.assertFalse(source["cross_sign_relation_supplied"])
        self.assertFalse(result["source_bridge_audit"]["source_defined_Z_minus"])
        self.assertFalse(result["source_bridge_audit"]["factorization_lambda_pullback_available"])


if __name__ == "__main__":
    unittest.main()
