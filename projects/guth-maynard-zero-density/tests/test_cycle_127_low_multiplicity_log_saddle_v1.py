import unittest
from fractions import Fraction

from conventions.low_multiplicity_log_saddle_v1 import exponent_ledger, theorem_record


class LowMultiplicityLogSaddleTests(unittest.TestCase):
    def test_lower_endpoint_zero_multiplicity(self) -> None:
        row = exponent_ledger(Fraction(16, 25), Fraction(0))
        self.assertEqual(row["hs_derivative_weighted"], Fraction(3, 5))
        self.assertEqual(row["hs_tube_weighted"], Fraction(122, 225))
        self.assertEqual(row["hs_ratio_weighted"], Fraction(77, 225))
        self.assertEqual(row["two_dimensional_volume_weighted"], Fraction(22, 75))
        self.assertEqual(row["volume_margin"], Fraction(1, 25))

    def test_high_threshold_still_has_derivative_gap(self) -> None:
        xi = Fraction(16, 25)
        mu = (1 - xi) / 4
        row = exponent_ledger(xi, mu)
        self.assertGreater(row["derivative_gap"], 0)

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("3/5-mu/2", row["hs_sum"])
        self.assertIn(">=1/25", row["volume"])
        self.assertIn("H=1/delta=KQ/D", row["mellin_identity"])
        self.assertIn("sum_h|P(hD)|^2<<HL", row["mellin_target"])
        self.assertIn("no sampled-Mellin", row["boundary"])


if __name__ == "__main__":
    unittest.main()
