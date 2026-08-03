"""Regression checks for Cycle 223's explicit signed-product family."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_223_explicit_signed_product import run  # noqa: E402


class ExplicitSignedProductTests(unittest.TestCase):
    def test_first_shift_passes_and_second_shift_has_universal_residual(self) -> None:
        result = run()
        self.assertEqual(result["candidate_state_audit"]["candidate_count"], 4)
        self.assertTrue(result["candidate_state_audit"]["formal_reflection_label_condition"])
        self.assertTrue(result["first_shift_audit"]["all_match"])
        second = result["second_shift_audit"]
        self.assertFalse(second["all_match"])
        self.assertEqual(
            {row["residual"] for row in second["rows"]},
            {"exp(pi*i*tilde-tau)"},
        )
        self.assertEqual(result["downstream_identity_audit"]["factorization_16_17"], "not_reached_after_failed_second_shift")


if __name__ == "__main__":
    unittest.main()
