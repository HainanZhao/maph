import unittest
from fractions import Fraction

from conventions.high_cell_refinement_v1 import (
    disjoint_pair_mass_lower_bound,
    effective_multiplicity,
    hub_effective_neighbor_lower_bound,
    refined_class_witness,
    theorem_record,
)


class HighCellRefinementTests(unittest.TestCase):
    def test_fixed_refinement_retains_multiplicity_over_class_count(self) -> None:
        row = refined_class_witness(((Fraction(1), Fraction(1)), (Fraction(1), Fraction(1))))
        self.assertEqual(row["global_effective_multiplicity"], Fraction(4))
        self.assertEqual(row["best_refined_effective_multiplicity"], Fraction(2))
        self.assertEqual(row["retained_lower_bound"], Fraction(2))

    def test_disjoint_pair_mass_ledger(self) -> None:
        self.assertEqual(disjoint_pair_mass_lower_bound(Fraction(5), Fraction(1)), Fraction(15))
        self.assertEqual(disjoint_pair_mass_lower_bound(Fraction(5), Fraction(3)), Fraction())

    def test_hub_effective_neighbor_ledger(self) -> None:
        self.assertEqual(hub_effective_neighbor_lower_bound(hub_incidence=Fraction(3), total_square_mass=Fraction(8)), Fraction(9, 8))
        self.assertEqual(effective_multiplicity((Fraction(2), Fraction(1))), Fraction(9, 5))

    def test_boundary(self) -> None:
        self.assertIn("does not", theorem_record()["boundary"])


if __name__ == "__main__":
    unittest.main()
