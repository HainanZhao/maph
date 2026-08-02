import unittest
from fractions import Fraction

from conventions.colored_four_cycle_condenser_v1 import condenser_ledger, effective_codegree, theorem_record


class ColoredFourCycleCondenserTests(unittest.TestCase):
    def test_effective_weighted_codegree(self) -> None:
        self.assertEqual(effective_codegree((Fraction(1), Fraction(1))), Fraction(2))
        self.assertEqual(effective_codegree(()), Fraction())

    def test_diagonal_split_ledger(self) -> None:
        row = condenser_ledger(
            atom_l2_mass=Fraction(3),
            off_pair_l2_mass=Fraction(8),
            maximum_effective_codegree=Fraction(2),
            cutoff_mass_over_k=Fraction(1),
            kernel_schur_constant=Fraction(1),
        )
        self.assertEqual(row["diagonal_baseline_over_k"], Fraction(9))
        self.assertEqual(row["off_diagonal_bound_over_k"], Fraction(16))
        self.assertEqual(row["fourth_moment_bound_over_k"], Fraction(50))

    def test_boundary(self) -> None:
        self.assertIn("does not", theorem_record()["boundary"])


if __name__ == "__main__":
    unittest.main()
