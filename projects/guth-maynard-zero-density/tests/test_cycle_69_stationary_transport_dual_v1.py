from fractions import Fraction as Q
import unittest

from conventions.stationary_transport_dual_v1 import dual_ledger, verify_all


class Cycle69StationaryTransportDualTests(unittest.TestCase):
    def test_hessian_degeneracy(self) -> None:
        self.assertEqual(dual_ledger(Q(36, 25))["hessian_determinant"], Q(0))

    def test_top_index(self) -> None:
        row = dual_ledger(Q(36, 25))
        self.assertEqual(row["stationary_index_exponent"], Q(21, 25))

    def test_stationary_threshold(self) -> None:
        row = dual_ledger(Q(3, 5))
        self.assertTrue(row["stationary_regime_nonempty_at_power_scale"])
        self.assertEqual(row["stationary_index_exponent"], Q(0))

    def test_below_threshold(self) -> None:
        self.assertFalse(dual_ledger(Q(1, 2))["stationary_regime_nonempty_at_power_scale"])

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertEqual(rows["dual_index_ceiling"], rows["skeleton_target"])
        self.assertIn("projective", rows["gate"])


if __name__ == "__main__":
    unittest.main()
