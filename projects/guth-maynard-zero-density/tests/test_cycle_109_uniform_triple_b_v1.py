import unittest
from fractions import Fraction

from conventions.uniform_triple_b_v1 import (
    one_dimensional_norm_constant,
    summable_kernel_bound,
    symbolic_log_phase_record,
    tensor_bound_squared,
    theorem_record,
)


class UniformTripleBTests(unittest.TestCase):
    def test_symbolic_log_phases(self) -> None:
        record = symbolic_log_phase_record()
        self.assertEqual(record["fixed_signs"], ("negative", "positive", "negative"))
        self.assertTrue(record["ell_independent"])

    def test_one_dimensional_exact_contract(self) -> None:
        squared = one_dimensional_norm_constant(
            curvature_lower=Fraction(9, 4),
            sup_norm=Fraction(2),
            derivative_l1=Fraction(1),
        )
        self.assertEqual(squared, 36)

    def test_tensor_contract(self) -> None:
        squared = tensor_bound_squared(
            curvature_lowers=(Fraction(1), Fraction(4), Fraction(9)),
            symbol_norm=Fraction(1, 8**3),
        )
        self.assertEqual(squared, Fraction(1, 36))

    def test_absolute_scale_sum(self) -> None:
        self.assertEqual(summable_kernel_bound(Fraction(7, 11)), Fraction(21, 11))

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("ell^(-3/2)", record["complete_kernel"])
        self.assertIn("fixed smooth", record["smooth_model"])
        self.assertIn("distinct core", record["boundary"])


if __name__ == "__main__":
    unittest.main()
