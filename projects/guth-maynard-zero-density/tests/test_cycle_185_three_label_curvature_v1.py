from fractions import Fraction as Q
import unittest

from conventions.three_label_curvature_v1 import (
    cantor_ap_free,
    critical_ap_free_occupancy,
    curvature_identity,
    deep_exactification_bound,
    verify_all,
)


class Cycle185ThreeLabelCurvatureTest(unittest.TestCase):
    def test_exact_curvature_and_v_square_factor(self) -> None:
        record = curvature_identity(
            v=3, u_minus=2, u_zero=5, u_plus=7,
            A_minus=6, A_zero=15, A_plus=30,
            alpha_minus=Q(1, 1), alpha_zero=Q(2, 1), alpha_plus=Q(4, 1),
        )
        self.assertEqual(record["K"] % 9, 0)
        self.assertEqual(record["expanded_value"], Q(record["K"], 3 * 2 * 3 * 7 * (3 * 5) ** 2))

    def test_deep_bound(self) -> None:
        bound = deep_exactification_bound(chart_cap=Q(3), C=2, H=100, X=10**12, v=5, S=100)
        self.assertLess(bound["total"], 1)

    def test_cantor_set_has_no_nontrivial_three_ap(self) -> None:
        values = cantor_ap_free(5)
        self.assertTrue(all(x + z != 2 * y for x in values for y in values for z in values if not (x == y == z)))

    def test_critical_ap_free_occupancy(self) -> None:
        ledger = critical_ap_free_occupancy(1)
        self.assertGreaterEqual(8 * ledger["mass"]["ordered_cross_mass"], ledger["mass"]["critical_target"])
        self.assertGreaterEqual(ledger["stable_shell"]["minimum_product"], ledger["stable_shell"]["cutoff_upper"])

    def test_replay_boundary(self) -> None:
        record = verify_all()
        self.assertIn("no actual-exponential distribution bound", record["boundary"])


if __name__ == "__main__":
    unittest.main()
