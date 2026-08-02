import unittest
from fractions import Fraction

from conventions.sparse_path_fourier_v1 import (
    layered_large_sieve_factor,
    scalar_threshold,
    signed_moments,
    theorem_record,
)


class SparsePathFourierTests(unittest.TestCase):
    def test_layer_cauchy_factor(self) -> None:
        self.assertEqual(layered_large_sieve_factor(17), 17)

    def test_scalar_threshold_is_unchanged(self) -> None:
        row = scalar_threshold(Fraction(1, 5), Fraction(7, 10))
        self.assertEqual(row["frequency"], Fraction(1, 2))
        self.assertEqual(row["kappa_threshold"], Fraction(-1, 10))
        self.assertEqual(row["kappa_threshold_simplified"], Fraction(-1, 10))
        self.assertEqual(row["rational_error_threshold"], Fraction(-1))

    def test_signed_moment_hierarchy(self) -> None:
        moments = signed_moments(
            (Fraction(1), Fraction(-1)),
            (Fraction(2, 3), Fraction(3, 4)),
            2,
        )
        self.assertEqual(moments[0], 0)
        self.assertEqual(moments[1], Fraction(-1, 12))

    def test_record_keeps_actual_weights_open(self) -> None:
        row = theorem_record()
        self.assertIn("unchanged", row["self_duality"])
        self.assertIn("M_0", row["moment_expansion"])
        self.assertIn("not bounded", row["boundary"])


if __name__ == "__main__":
    unittest.main()
