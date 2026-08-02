import unittest
from fractions import Fraction

from conventions.coefficient_escape_localization_v1 import localized_escape, theorem_record


class CoefficientEscapeLocalizationTests(unittest.TestCase):
    def test_extracts_fixed_fraction_of_finite_partition(self) -> None:
        row = localized_escape(
            total_negative_projection=Fraction(1),
            class_real_projections=(Fraction(-1, 10), Fraction(2, 5), Fraction(-9, 10)),
            witness_norm_squared_over_scale=Fraction(2),
        )
        self.assertEqual(row["class_count"], 3)
        self.assertGreaterEqual(row["chosen_class_negative_projection"], row["per_class_lower_bound"])
        self.assertEqual(row["one_ray_l2_squared_over_scale_lower_bound"], Fraction(1, 18))

    def test_rejects_insufficient_partition(self) -> None:
        with self.assertRaises(ValueError):
            localized_escape(
                total_negative_projection=Fraction(1),
                class_real_projections=(Fraction(-1, 2),),
                witness_norm_squared_over_scale=Fraction(1),
            )

    def test_boundary(self) -> None:
        self.assertIn("does not", theorem_record()["boundary"])


if __name__ == "__main__":
    unittest.main()
