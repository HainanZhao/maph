from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_stage1_baseline import build_report  # noqa: E402
from src.conventions import cubic_box, orientable_genus_lower_bound_for_free_box  # noqa: E402


class StageOneBaselineTests(unittest.TestCase):
    def test_exact_report(self) -> None:
        report = build_report()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(report["cases"]), 6)

    def test_wrapped_length_two_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            cubic_box((2, 2, 2), periodic=(0,))

    def test_cubic_genus_bound_formula(self) -> None:
        self.assertEqual(orientable_genus_lower_bound_for_free_box((3, 3, 3)), 1)
        self.assertEqual(orientable_genus_lower_bound_for_free_box((4, 4, 4)), 5)


if __name__ == "__main__":
    unittest.main()
