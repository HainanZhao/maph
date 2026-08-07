"""Regression tests for the width-three cochain gauge quotient."""

from __future__ import annotations

import unittest

from proof.verify_lane_b_cochain_gauge import verify


class LaneBCochainGaugeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify()

    def test_rank_bounds(self) -> None:
        theorem = self.result["rank_theorem"]
        self.assertEqual(theorem["F_pair_upper"], 256)
        self.assertEqual(theorem["F_internal_upper"], 256)

    def test_boundaries_and_normalization(self) -> None:
        self.assertIn("antiperiodic", self.result["boundary_audit"])
        self.assertIn("powers of two", self.result["normalization_audit"])


if __name__ == "__main__":
    unittest.main()
