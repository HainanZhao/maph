"""Regression checks for Cycle 227's augmented transport normal forms."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_227_augmented_transport_normal_forms import run  # noqa: E402


class AugmentedTransportNormalFormTests(unittest.TestCase):
    def test_normal_form_and_scaling_boundary(self) -> None:
        result = run()
        normal = result["normal_form_audit"]
        quotient = result["quotient_audit"]
        self.assertEqual(normal["rows_checked"], 32764)
        self.assertTrue(normal["all_rows_match_closed_form"])
        self.assertEqual(quotient["generic_full_label_scaling_quotient_count"], 0)
        self.assertGreater(quotient["zero_label_candidate_count"], 0)
        self.assertTrue(all(row["ordinary_gamma_factors_retained"] > 0 for row in quotient["zero_label_product_node_scaling_candidates"]))


if __name__ == "__main__":
    unittest.main()
