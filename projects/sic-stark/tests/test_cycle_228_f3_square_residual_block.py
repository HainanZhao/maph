"""Regression checks for Cycle 228's F3-square residual block."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_228_f3_square_residual_block import audit  # noqa: E402


class F3SquareResidualBlockTests(unittest.TestCase):
    def test_all_frozen_factors_remain_unreduced(self) -> None:
        result = audit()
        self.assertEqual(set(result["blocks"]), {"A", "C"})
        self.assertTrue(all(len(block) == 4 for block in result["blocks"].values()))
        self.assertTrue(all(not row["reflection_match_available"] for row in result["reflection_audit"]))
        self.assertFalse(result["multiplication_audit"]["equation_15_operand_available"])


if __name__ == "__main__":
    unittest.main()
