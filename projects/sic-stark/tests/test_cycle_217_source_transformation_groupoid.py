"""Regression checks for the Cycle 217 raw source-groupoid audit."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_217_source_transformation_groupoid import run  # noqa: E402


class SourceTransformationGroupoidTests(unittest.TestCase):
    def test_frozen_raw_groupoid(self) -> None:
        result = run()
        raw = result["raw_orbit_audit"]
        canonical = result["candidate_canonical_orbit_audit"]
        affine = result["affine_period_argument_audit"]
        packet = result["packet_boundary_audit"]
        self.assertEqual(raw["raw_orbit_size"], 4)
        self.assertTrue(raw["two_step_matrix_is_minus_M_E"])
        self.assertEqual(canonical["epistemic_status"], "OBSERVED")
        self.assertFalse(affine["raw_two_step_periods_match_E_target"])
        self.assertFalse(packet["source_arrow_to_packet_t_a_b_map_available"])


if __name__ == "__main__":
    unittest.main()
