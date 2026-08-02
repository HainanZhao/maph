from fractions import Fraction as Q
import unittest

from conventions.seeded_packet_recurrence_v1 import recurrence_ledger, verify_all


class Cycle67SeededPacketRecurrenceTests(unittest.TestCase):
    def test_critical_interface(self) -> None:
        row = recurrence_ledger(Q(1, 5), Q(6, 25))
        self.assertTrue(row["admissible"])
        self.assertTrue(row["critical_or_deeper"])
        self.assertEqual(row["one_sided_progression_count_exponent"], Q(6, 25))

    def test_shallow_packet(self) -> None:
        self.assertFalse(recurrence_ledger(Q(1, 10), Q(1, 10))["critical_or_deeper"])

    def test_propagated_error(self) -> None:
        row = recurrence_ledger(Q(1, 5), Q(6, 25))
        self.assertIn("C0+C1", row["propagated_error"])
        self.assertIn("floor(K/2)", row["boundary_guarantee"])

    def test_scope_correction(self) -> None:
        self.assertIn("genuine transport seed", verify_all()["scope_correction"])

    def test_verification(self) -> None:
        self.assertIn("E7/E9/E10", verify_all()["gate"])


if __name__ == "__main__":
    unittest.main()
