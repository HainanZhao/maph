"""Regression checks for Cycle 218's product-domain cover audit."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_218_signed_period_cover import run  # noqa: E402


class SignedPeriodCoverTests(unittest.TestCase):
    def test_frozen_product_domain(self) -> None:
        result = run()
        self.assertEqual(result["positive_scaling_audit"]["scale"], 576)
        self.assertTrue(result["swap_reindexing_audit"]["all_delta_sets_reindexed"])
        self.assertFalse(result["signed_representative_domain_audit"]["raw_k_in_source_product_domain"])
        self.assertFalse(result["legal_lift_audit"]["complete_raw_to_E_lift_available"])


if __name__ == "__main__":
    unittest.main()
