from fractions import Fraction as Q
import unittest

from conventions.positive_forward_balance_v1 import forward_bounds, positive_forward_infeasible, verify_all


class Cycle173PositiveForwardBalanceTests(unittest.TestCase):
    def test_positive_branch_is_strictly_infeasible(self) -> None:
        result = positive_forward_infeasible(y_bound=Q(101, 100), slack=Q(1))
        self.assertGreater(result["strict_lower"], 2)

    def test_only_formal_endpoint_survives_without_positivity(self) -> None:
        result = forward_bounds(H=Q(10), h=Q(20), h_plus=Q(10), a=2, q=1, K=Q(10), y_bound=Q(1), slack=Q(1))
        self.assertEqual(result["a_over_q"], 2)

    def test_scope_is_visible(self) -> None:
        theorem = verify_all()
        self.assertIn("reverse orientation", theorem["scope"])
