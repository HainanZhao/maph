import unittest
from fractions import Fraction

from conventions.triple_b_jacobian_v1 import (
    residual_envelope_bound,
    summability_record,
    symbolic_jacobian_record,
    theorem_record,
)


class TripleBJacobianTests(unittest.TestCase):
    def test_symbolic_scale_law_and_points(self) -> None:
        record = symbolic_jacobian_record()
        self.assertEqual(record["scale"], "J_ell=ell^(-3/2)*J0")
        self.assertTrue(record["points_invariant"])

    def test_summability_and_bv(self) -> None:
        for length in (1, 2, 3, 10, 100):
            record = summability_record(length)
            self.assertEqual(record["bv_norm"], 1)
            self.assertLess(record["integral_upper"], 3)

    def test_residual_envelope(self) -> None:
        self.assertEqual(
            residual_envelope_bound(Fraction(2, 7), Fraction(5, 3)),
            Fraction(10, 7),
        )

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("ell^(-3/2)", record["jacobian"])
        self.assertIn("subpower", record["implication"])
        self.assertIn("remainders", record["boundary"])


if __name__ == "__main__":
    unittest.main()
