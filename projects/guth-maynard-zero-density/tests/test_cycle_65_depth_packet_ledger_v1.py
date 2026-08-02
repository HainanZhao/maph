from fractions import Fraction as Q
import unittest

from conventions.depth_packet_ledger_v1 import (
    DENOMINATOR_THRESHOLD,
    RECURRENCE_DEPTH,
    scale_ledger,
    verify_all,
)


class Cycle65DepthPacketLedgerTests(unittest.TestCase):
    def test_thresholds(self) -> None:
        self.assertEqual(RECURRENCE_DEPTH, Q(6, 25))
        self.assertEqual(DENOMINATOR_THRESHOLD, Q(1, 5))

    def test_target_tie(self) -> None:
        row = scale_ledger(Q(1, 5), Q(6, 25))
        self.assertTrue(row["admissible"])
        self.assertTrue(row["single_packet_reaches_pair_target"])
        self.assertEqual(row["packet_weight_exponent"], Q(17, 25))

    def test_shallow_low_denominator_is_not_automatically_dangerous(self) -> None:
        row = scale_ledger(Q(1, 10), Q(1, 10))
        self.assertTrue(row["admissible"])
        self.assertFalse(row["single_packet_reaches_pair_target"])

    def test_count_and_random_margin(self) -> None:
        row = scale_ledger(Q(3, 25), Q(1, 5))
        self.assertEqual(row["packet_count_target_exponent_open"], Q(1, 25))
        self.assertEqual(row["random_packet_count_exponent"], -Q(12, 25))
        self.assertEqual(row["random_margin_to_target"], Q(13, 25))

    def test_verification(self) -> None:
        data = verify_all()
        self.assertEqual(data["constants"]["dangerous_depth_threshold"], Q(6, 25))
        self.assertIn("AP recurrence", data["gate"])


if __name__ == "__main__":
    unittest.main()
