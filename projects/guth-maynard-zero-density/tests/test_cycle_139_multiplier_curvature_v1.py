import unittest
from fractions import Fraction

from conventions.multiplier_curvature_v1 import curvature_ledger, range_ledger, theorem_record


class MultiplierCurvatureTests(unittest.TestCase):
    def test_minimum_extension_is_positive(self) -> None:
        row = range_ledger(Fraction(16, 25), Fraction(9, 100))
        self.assertEqual(row["extension"], Fraction(13, 1800))
        self.assertGreater(row["tube_margin_at_new_ceiling"], 0)
        self.assertGreater(row["ratio_margin_at_new_ceiling"], 0)
        self.assertGreater(row["constant_margin_at_new_ceiling"], 0)

    def test_derivative_ties_at_new_ceiling(self) -> None:
        xi, mu = Fraction(16, 25), Fraction(0)
        rho = Fraction(17, 90)
        tau = xi + Fraction(1, 3) - rho
        row = curvature_ledger(xi, mu, rho, tau, Fraction(0))
        self.assertEqual(row["derivative_margin"], 0)
        self.assertEqual(row["edge_ceiling_derivative"], 0)

    def test_positive_low_edge_cell(self) -> None:
        row = curvature_ledger(
            Fraction(16, 25), Fraction(0), Fraction(11, 60), Fraction(4, 5), Fraction(1, 100)
        )
        self.assertTrue(all(row[key] > 0 for key in (
            "derivative_margin", "tube_margin", "ratio_margin", "constant_margin"
        )))

    def test_record_keeps_high_edges_open(self) -> None:
        row = theorem_record()
        self.assertIn("j/2", row["high_edge_limit"])
        self.assertIn("no high-edge", row["boundary"])


if __name__ == "__main__":
    unittest.main()
