"""Regression checks for Cycle 219's diagonal signed-k census."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_219_signed_k_extension import run  # noqa: E402


class SignedKExtensionTests(unittest.TestCase):
    def test_all_diagonal_lifts_fail_all_three_coordinates(self) -> None:
        result = run()
        census = result["coordinate_sign_census"]
        self.assertEqual(census["candidate_count"], 16)
        self.assertEqual(census["survivor_count"], 0)
        self.assertEqual(len(census["tau_and_u_candidates"]), 2)
        self.assertTrue(all(not row["tilde_u"] for row in census["tau_and_u_candidates"]))
        self.assertFalse(result["extension_axiom_audit"]["agreement_with_positive_product"])


if __name__ == "__main__":
    unittest.main()
