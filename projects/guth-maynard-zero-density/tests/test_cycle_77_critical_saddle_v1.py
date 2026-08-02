from fractions import Fraction as Q
import unittest

from conventions.critical_saddle_v1 import critical_ledger, det2, saddle_hessian, verify_all


class Cycle77CriticalSaddleTests(unittest.TestCase):
    def test_saddle_determinant(self) -> None:
        beta, c0, y, exponential = Q(2), Q(5, 4), Q(3, 2), Q(7, 5)
        matrix = saddle_hessian(beta, c0, y, exponential)
        self.assertEqual(det2(matrix), -(beta * c0 * exponential) ** 2)

    def test_anchored_scales(self) -> None:
        row = critical_ledger()
        self.assertEqual(row["packet_count_target_exponent_open"], Q(2, 15))
        self.assertEqual(row["normalized_tube_exponent"], -Q(36, 25))
        self.assertEqual(row["anchored_volume_exponent"], -Q(13, 75))

    def test_ratio_anchor_loss(self) -> None:
        row = critical_ledger()
        self.assertEqual(row["ratio_census_volume_exponent"], Q(37, 75))
        self.assertEqual(row["ratio_pair_target_exponent_open"], Q(4, 15))
        self.assertEqual(row["ratio_anchor_loss_exponent"], Q(17, 75))

    def test_common_denominator_loss(self) -> None:
        row = critical_ledger()
        self.assertEqual(row["common_denominator_height_exponent"], Q(14, 15))
        self.assertEqual(row["common_embedding_gap_to_target"], Q(4, 5))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("2/15", rows["anchored_target"])
        self.assertIn("seed-aware", rows["gate"])


if __name__ == "__main__":
    unittest.main()
