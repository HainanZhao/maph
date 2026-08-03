"""Regression checks for Cycle 220's normalized-reflection reduction."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_220_normalized_reflection import run  # noqa: E402


class NormalizedReflectionTests(unittest.TestCase):
    def test_reflection_reduces_to_the_diagonal_family(self) -> None:
        result = run()
        reduction = result["reflection_reduction_audit"]
        census = result["reflected_coordinate_census"]
        self.assertEqual(
            reduction["candidate_after_reduction"],
            "H_abcd=Gamma_M(a*mu,b*m;c*omega1,d*omega2)",
        )
        self.assertEqual(census["candidate_count"], 16)
        self.assertEqual(census["survivor_count"], 0)
        self.assertTrue(result["downstream_axiom_audit"]["reflection_tested"])
        self.assertFalse(result["downstream_axiom_audit"]["involutivity_tested"])


if __name__ == "__main__":
    unittest.main()
