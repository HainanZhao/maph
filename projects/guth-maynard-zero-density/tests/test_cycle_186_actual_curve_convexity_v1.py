from fractions import Fraction as Q
import unittest

from conventions.actual_curve_convexity_v1 import consecutive_deep_triple_regime, convexity_bounds, forbidden_rational_sandwich, verify_all


class Cycle186ActualCurveConvexityTest(unittest.TestCase):
    def test_weighted_convexity_envelope(self) -> None:
        bounds = convexity_bounds(p=2, q=3, t_lower=Q(1, 10), t_upper=Q(1, 5), exp_upper=Q(4))
        self.assertEqual(bounds["r"], 5)
        self.assertLess(bounds["lower"], bounds["upper"])

    def test_forbidden_grid_sandwich(self) -> None:
        record = forbidden_rational_sandwich(denominator_product=1000, curve_lower=Q(1, 5000), curve_upper=Q(1, 2000), error_upper=Q(1, 10000))
        self.assertEqual(record["status"], "FORBIDDEN_DEEP_TRIPLE")

    def test_consecutive_scale_fixture(self) -> None:
        record = consecutive_deep_triple_regime(T=100, C=1, chart_exp_upper=1000)
        self.assertEqual(record["certificate"]["status"], "FORBIDDEN_DEEP_TRIPLE")
        self.assertEqual(record["parameters"]["denominator_interval"][0], 100**9)

    def test_replay_boundary(self) -> None:
        self.assertIn("local three-point exclusion", verify_all()["boundary"])


if __name__ == "__main__":
    unittest.main()
