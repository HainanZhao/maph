import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from exact_q_transform_v1 import (  # noqa: E402
    CURRENT_XI,
    MAX_XI,
    RAW_L1_TARGET,
    central_error_ledger,
    dual_support,
    transform_formula,
    verify_all,
)

Q = Fraction


class ExactQTransformTests(unittest.TestCase):
    def test_fourier_sign_and_leading_weight(self) -> None:
        row = transform_formula()
        self.assertIn("V(a)", row["leading"])
        self.assertNotIn("V(-a)", row["leading"])
        self.assertIn("hatV(-y)", row["exact_kernel"])

    def test_dual_support_matches_cycle_79(self) -> None:
        row = dual_support(MAX_XI)
        self.assertEqual(row["r"], Q(83, 75))
        self.assertEqual(row["h"], Q(21, 25))
        self.assertEqual(row["amplitude"], Q(-38, 75))

    def test_central_error_sums_to_constant_per_k(self) -> None:
        for xi in (CURRENT_XI, Q(2, 5), Q(3, 5), MAX_XI):
            row = central_error_ledger(xi)
            self.assertEqual(row["per_k_total"], 0)

    def test_full_range_error_has_strict_margin(self) -> None:
        self.assertEqual(RAW_L1_TARGET - MAX_XI, Q(2, 15))

    def test_verification(self) -> None:
        row = verify_all()
        self.assertEqual(row["strict_margin"], "2/15")
        self.assertEqual(row["per_k_error_exponent"], "0")
        self.assertIn("cancellation open", row["gate"])


if __name__ == "__main__":
    unittest.main()

