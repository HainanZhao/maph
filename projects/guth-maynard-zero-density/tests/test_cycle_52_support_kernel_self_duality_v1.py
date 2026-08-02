from fractions import Fraction as Q
import unittest

from conventions.support_kernel_self_duality_v1 import inverse_deficits, stable_support_counts, verify_all


class Cycle52SupportKernelSelfDualityTests(unittest.TestCase):
    def test_collision_counts(self) -> None:
        row = stable_support_counts(7, 4)
        self.assertEqual(row["full_support"], 7 * 210)
        self.assertEqual(row["all_distinct_support"], 105)
        self.assertGreater(row["collision_support"], 0)

    def test_narrow_inverse_deficits(self) -> None:
        row = inverse_deficits(4, Q(7, 50))
        self.assertEqual(row["K_h_max_deficit"], Q(7, 200))
        self.assertEqual(row["K_mh_max_deficit"], Q(7, 50))

    def test_full_inverse_deficits(self) -> None:
        row = inverse_deficits(4, Q(4, 25))
        self.assertEqual(row["K_h_max_deficit"], Q(1, 25))
        self.assertEqual(row["K_mh_max_deficit"], Q(4, 25))

    def test_registered_gap(self) -> None:
        data = verify_all()
        self.assertEqual(data["collision_gap"], Q(1))
        self.assertEqual(data["leading_term"], "K(mh) K(h)^s / s!")


if __name__ == "__main__":
    unittest.main()
