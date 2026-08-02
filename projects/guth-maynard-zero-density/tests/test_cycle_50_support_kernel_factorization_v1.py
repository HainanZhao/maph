from fractions import Fraction as Q
import unittest

from conventions.support_kernel_factorization_v1 import (
    coefficient_norm_bounds,
    complete_homogeneous_direct,
    h3_power_sum,
    h4_power_sum,
    support_size,
    verify_all,
)


class Cycle50SupportKernelFactorizationTests(unittest.TestCase):
    def test_h3_identity(self) -> None:
        values = (Q(-2), Q(1, 3), Q(5))
        self.assertEqual(complete_homogeneous_direct(values, 3), h3_power_sum(values))

    def test_h4_identity(self) -> None:
        values = (Q(-2), Q(1, 3), Q(5), Q(7))
        self.assertEqual(complete_homogeneous_direct(values, 4), h4_power_sum(values))

    def test_support_size(self) -> None:
        self.assertEqual(support_size(2, 4), 10)
        self.assertEqual(support_size(4, 3), 80)

    def test_norm_bounds(self) -> None:
        row = coefficient_norm_bounds(4, 4)
        self.assertEqual(row["coefficient_mass"], 4**5)
        self.assertEqual(row["coefficient_square_lower"], 4**5)
        self.assertGreaterEqual(row["coefficient_square_upper"], row["coefficient_square_lower"])

    def test_registered_checks(self) -> None:
        data = verify_all()
        self.assertEqual(data["injective_range"], "m>s")
        self.assertEqual(data["exceptional_harmonics"]["s4"], [2, 3, 4])


if __name__ == "__main__":
    unittest.main()
