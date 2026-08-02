import unittest
from fractions import Fraction

from conventions.coefficient_selector_information_loss_v1 import (
    multiplier_loss_witness,
    ray_atoms,
    theorem_record,
)


class CoefficientSelectorInformationLossTests(unittest.TestCase):
    def test_ray_multiplier_recovers_ordered_atoms(self) -> None:
        self.assertEqual(ray_atoms(numerator=3, denominator=2, multiplier=4), (8, 12))

    def test_same_ray_different_products_force_missing_multiplier(self) -> None:
        row = multiplier_loss_witness(
            numerator=3,
            denominator=2,
            first_multiplier=3,
            second_multiplier=4,
            first_oriented_product=Fraction(1),
            second_oriented_product=Fraction(2),
        )
        self.assertEqual(row["retained_ray_metadata"], (3, 2))
        self.assertIn("multiplier", row["minimal_repair"])

    def test_rejects_nonwitness(self) -> None:
        with self.assertRaises(ValueError):
            multiplier_loss_witness(
                numerator=3,
                denominator=2,
                first_multiplier=3,
                second_multiplier=3,
                first_oriented_product=Fraction(1),
                second_oriented_product=Fraction(2),
            )

    def test_boundary(self) -> None:
        self.assertIn("does not", theorem_record()["boundary"])


if __name__ == "__main__":
    unittest.main()
