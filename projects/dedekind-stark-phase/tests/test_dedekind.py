from fractions import Fraction
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dedekind import dedekind_sum, rademacher_phi, sawtooth
from cocycle import (
    kopp_theta_exponent,
    kopp_total_multiplier_exponent,
    sic_rademacher_invariant,
)


class DedekindTest(unittest.TestCase):
    def test_sawtooth(self):
        self.assertEqual(sawtooth(Fraction(0)), 0)
        self.assertEqual(sawtooth(Fraction(1)), 0)
        self.assertEqual(sawtooth(Fraction(1, 3)), Fraction(-1, 6))
        self.assertEqual(sawtooth(Fraction(-1, 3)), Fraction(1, 6))

    def test_s_one_k_closed_form(self):
        for k in range(2, 40):
            self.assertEqual(
                dedekind_sum(1, k),
                Fraction((k - 1) * (k - 2), 12 * k),
            )

    def test_reciprocity(self):
        for h, k in ((2, 3), (3, 5), (5, 7), (7, 11), (11, 13)):
            lhs = dedekind_sum(h, k) + dedekind_sum(k, h)
            rhs = (
                Fraction(h, k)
                + Fraction(k, h)
                + Fraction(1, h * k)
                - 3
            ) / 12
            self.assertEqual(lhs, rhs)

    def test_inversion_symmetry(self):
        for h, k in ((2, 5), (3, 7), (5, 12), (7, 17)):
            inverse = pow(h, -1, k)
            self.assertEqual(dedekind_sum(h, k), dedekind_sum(inverse, k))

    def test_rademacher_generators(self):
        self.assertEqual(rademacher_phi(1, 1, 0, 1), 1)  # T
        self.assertEqual(rademacher_phi(0, -1, 1, 0), 0)  # S
        self.assertEqual(rademacher_phi(1, 0, 1, 1), 2)

    def test_sic_rademacher_anchor_values(self):
        self.assertEqual(
            sic_rademacher_invariant(((21, -8), (8, -3))), 0
        )
        self.assertEqual(
            sic_rademacher_invariant(((56, -15), (15, -4))), 3
        )
        self.assertEqual(
            sic_rademacher_invariant(((204, -35), (35, -6))), 9
        )

    def test_dimension_four_kopp_multiplier(self):
        matrix = ((21, -8), (8, -3))
        self.assertEqual(
            kopp_theta_exponent(
                matrix, Fraction(0), Fraction(1, 4)
            ),
            Fraction(1, 4),
        )
        self.assertEqual(
            kopp_total_multiplier_exponent(
                matrix, Fraction(0), Fraction(1, 4)
            ),
            Fraction(3, 4),
        )
        inverse = ((-3, 8), (-8, 21))
        self.assertEqual(
            kopp_total_multiplier_exponent(
                inverse, Fraction(0), Fraction(1, 4)
            ),
            Fraction(1, 4),
        )


if __name__ == "__main__":
    unittest.main()
