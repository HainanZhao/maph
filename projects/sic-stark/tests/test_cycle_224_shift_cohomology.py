"""Regression checks for Cycle 224's joint shift cohomology."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_224_shift_cohomology import run  # noqa: E402


class ShiftCohomologyTests(unittest.TestCase):
    def test_unique_integrable_minimal_cochain(self) -> None:
        result = run()
        shifts = result["shift_action_audit"]
        self.assertTrue(shifts["commute"])
        solution = result["minimal_exponential_solution_audit"]
        self.assertEqual(solution["solution"], "a=1")
        self.assertEqual(solution["cochain"], "D(u)=exp(pi*i*tilde-u_-)")
        self.assertTrue(result["commutator_audit"]["integrable"])
        reflection = result["combined_reflection_audit"]
        self.assertEqual(reflection["candidate_count"], 4)
        self.assertFalse(reflection["all_match"])
        self.assertEqual(
            {row["combined_reflection_product"] for row in reflection["rows"]},
            {-1},
        )
        self.assertEqual(
            result["combined_boundary_audit"]["factorization_16_17"],
            "not_reached_after_failed_reflection",
        )


if __name__ == "__main__":
    unittest.main()
