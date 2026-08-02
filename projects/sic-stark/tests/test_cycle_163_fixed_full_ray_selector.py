"""Regression coverage for the exact Cycle-163 finite selector prototype."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_163_fixed_full_ray_selector import build_payload  # noqa: E402


class FixedFullRaySelectorTests(unittest.TestCase):
    def test_exact_domain_falsifier_and_anchors(self) -> None:
        payload = build_payload()
        summary = payload["summary"]
        self.assertEqual(summary["rows_checked"], 36)
        self.assertEqual(summary["eligible_rows"], 18)
        self.assertEqual(summary["ineligible_rows"], 18)
        self.assertFalse(summary["fixed_full_ray_total"])
        self.assertTrue(summary["orientation_anchors"]["3,5"]["eligible"])
        self.assertTrue(summary["orientation_anchors"]["3,4"]["eligible"])
        self.assertEqual(
            payload["gate_outcome"]["fixed_full_ray_direct_selector"],
            "FALSIFIED_BY_NONCOPRIME_ROWS",
        )


if __name__ == "__main__":
    unittest.main()
