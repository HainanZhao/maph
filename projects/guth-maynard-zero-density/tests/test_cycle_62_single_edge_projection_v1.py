from fractions import Fraction as Q
import unittest

from conventions.single_edge_projection_v1 import single_edge_ledger, verify_all


class Cycle62SingleEdgeProjectionTests(unittest.TestCase):
    def test_exact_fraction(self) -> None:
        data = single_edge_ledger(4, Q(1, 25), Q(1, 49))
        self.assertEqual(data["retained_fraction"], Q(48, 49) * Q(24, 25) ** 4)

    def test_union_bound(self) -> None:
        for s in (3, 4):
            data = single_edge_ledger(s, Q(1, 25), Q(1, 49))
            self.assertTrue(data["union_bound_verified"])
            self.assertLessEqual(data["lost_fraction"], data["lost_fraction_union_upper"])

    def test_zero_kernel_endpoint(self) -> None:
        data = single_edge_ledger(4, 0, 0)
        self.assertEqual(data["retained_fraction"], 1)
        self.assertEqual(data["lost_fraction"], 0)

    def test_genuine_vector(self) -> None:
        data = single_edge_ledger(4, 0, 0)
        self.assertTrue(data["genuine_edge_nonnegative"])
        self.assertIn("|sum_t", data["genuine_edge_vector"])

    def test_verification(self) -> None:
        self.assertIn("nonnegative_multi_edge", verify_all()["analytic_gate"])


if __name__ == "__main__":
    unittest.main()
