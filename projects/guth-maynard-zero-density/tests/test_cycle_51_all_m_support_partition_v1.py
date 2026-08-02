from fractions import Fraction as Q
import unittest

from conventions.all_m_support_partition_v1 import (
    complete_homogeneous_power_polynomial,
    evaluate_power_polynomial,
    evaluate_support_direct,
    multiply_by_power,
    support_partitions,
    support_power_polynomial,
    verify_all,
)


class Cycle51AllMSupportPartitionTests(unittest.TestCase):
    def test_support_criterion_examples(self) -> None:
        self.assertIn((2, 1, 1, 1, 1), support_partitions(4, 2))
        self.assertNotIn((1, 1, 1, 1, 1, 1), support_partitions(4, 2))
        self.assertIn((4, 4), support_partitions(4, 4))

    def test_small_m_direct_evaluation(self) -> None:
        values = (Q(-1), Q(2), Q(3), Q(5))
        for s, m in ((3, 2), (3, 3), (4, 2), (4, 3), (4, 4)):
            poly = support_power_polynomial(s, m)
            self.assertEqual(evaluate_power_polynomial(poly, values), evaluate_support_direct(s, m, values))

    def test_injective_reconciliation(self) -> None:
        for s, m in ((3, 4), (4, 5), (4, 9)):
            self.assertEqual(
                support_power_polynomial(s, m),
                multiply_by_power(complete_homogeneous_power_polynomial(s), m),
            )

    def test_registered_rows(self) -> None:
        rows = verify_all()["registered_small_m"]
        self.assertEqual(set(rows), {"s3_m2", "s3_m3", "s4_m2", "s4_m3", "s4_m4"})


if __name__ == "__main__":
    unittest.main()
