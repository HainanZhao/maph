from fractions import Fraction as Q
import unittest

from conventions.adaptive_slack_transport_v1 import (
    capacity_class,
    deficit_lower_bound,
    propagated_residual,
    saturated_transport,
    verify_all,
)


class Cycle174AdaptiveSlackTransportTests(unittest.TestCase):
    def test_saturated_fixed_slack(self) -> None:
        result = saturated_transport(h=20, h_plus=10, a=2, q=1, K=10, H=10, y=Q(6, 5), Y=Q(3, 2))
        self.assertEqual(result["rho"], Q(6, 5))
        self.assertEqual(result["slack"], 6)

    def test_dyadic_deficit_is_labelled(self) -> None:
        self.assertEqual(capacity_class(q=1, K=5, H=20), {"kind": "capacity_deficit", "index": 2})
        result = deficit_lower_bound(h=40, h_plus=20, a=2, q=1, K=5, H=20, y=Q(6, 5))
        self.assertEqual(result["lower"], Q(24, 5))

    def test_exact_residual_and_boundary(self) -> None:
        self.assertEqual(propagated_residual(source=Q(0), edge_error=Q(1, 100), rho=Q(6, 5)), Q(-3, 250))
        self.assertIn("no actual saturated population", verify_all()["boundary"])
