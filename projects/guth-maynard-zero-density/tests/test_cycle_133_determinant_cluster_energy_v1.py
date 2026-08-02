import unittest
from fractions import Fraction

from conventions.determinant_cluster_energy_v1 import (
    determinant,
    energy_ledger,
    matmul,
    theorem_record,
    transition,
)


class DeterminantClusterEnergyTests(unittest.TestCase):
    def test_minimum_extension(self) -> None:
        row = energy_ledger(Fraction(16, 25), Fraction(0))
        self.assertEqual(row["exact_ceiling"], Fraction(73, 300))
        self.assertEqual(row["extension_beyond_hs"], Fraction(79, 900))
        self.assertEqual(row["nonexact_width"], Fraction(9, 100))

    def test_maximal_multiplicity_closes_exponent_width(self) -> None:
        xi = Fraction(7, 10)
        mu = (1 - xi) / 4
        row = energy_ledger(xi, mu)
        self.assertEqual(row["nonexact_width"], 0)

    def test_integral_transition_cocycle(self) -> None:
        ua = ((3, 1), (2, 1))
        ub = ((7, 3), (5, 2))
        uc = ((10, 7), (7, 5))
        self.assertEqual(determinant(ua), 1)
        self.assertEqual(determinant(ub), -1)
        self.assertEqual(determinant(uc), 1)
        tab = transition(ua, ub)
        tbc = transition(ub, uc)
        tac = transition(ua, uc)
        self.assertEqual(matmul(tbc, tab), tac)
        self.assertEqual(determinant(tab), -1)

    def test_record_keeps_missing_invariant_visible(self) -> None:
        row = theorem_record()
        self.assertIn("S>>N^3", row["integer_forcing"])
        self.assertIn("79/900", row["forced_region"])
        self.assertIn("do not force", row["missing_invariant"])


if __name__ == "__main__":
    unittest.main()
