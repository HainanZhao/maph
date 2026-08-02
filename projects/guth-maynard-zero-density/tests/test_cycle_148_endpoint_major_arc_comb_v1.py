import unittest
from fractions import Fraction

from conventions.endpoint_major_arc_comb_v1 import (
    anchored_reduced_denominator,
    exponent_ledger,
    major_arc_multiples,
    theorem_record,
)


class EndpointMajorArcCombTests(unittest.TestCase):
    def test_bounded_anchor_denominator(self) -> None:
        h = anchored_reduced_denominator(
            numerator=7,
            denominator=13,
            anchor_numerator=3,
            anchor_denominator=2,
        )
        self.assertEqual(h, 26)
        self.assertGreaterEqual(h, Fraction(13, 3))
        self.assertLessEqual(h, 26)

    def test_comb_count(self) -> None:
        self.assertEqual(
            major_arc_multiples(frequency_floor=100, frequency_ceiling=200, modulus=13),
            8,
        )

    def test_excess_is_q_over_n(self) -> None:
        row = exponent_ledger(
            xi=Fraction(7, 10),
            rho=Fraction(1, 5),
            mode_mass=Fraction(1, 4),
        )
        self.assertEqual(row["excess"], Fraction(2, 15))
        self.assertEqual(row["comb_count"], Fraction(1, 2))

    def test_record_keeps_cross_cell_boundary(self) -> None:
        row = theorem_record()
        self.assertIn("Q/N", row["diagonal_comparison"])
        self.assertIn("cannot reach", row["structural_implication"])
        self.assertIn("does not", row["mass_boundary"])
        self.assertIn("no full second moment", row["boundary"])


if __name__ == "__main__":
    unittest.main()
