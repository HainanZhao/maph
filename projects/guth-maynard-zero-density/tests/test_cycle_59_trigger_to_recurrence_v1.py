from fractions import Fraction as Q
import unittest

from conventions.trigger_to_recurrence_v1 import recurrence_ledger, verify_all


class Cycle59TriggerToRecurrenceTests(unittest.TestCase):
    def test_target_rows(self) -> None:
        data = recurrence_ledger(Q(21, 25), Q(0), Q(7, 50))
        self.assertEqual(data["required_surplus_open_endpoint"], Q(7, 10))

    def test_uniform_rows(self) -> None:
        data = recurrence_ledger(Q(1), Q(0), Q(7, 50))
        self.assertEqual(data["required_surplus_open_endpoint"], Q(43, 50))

    def test_full_contraction(self) -> None:
        data = recurrence_ledger(Q(1), Q(47, 50), Q(7, 50))
        self.assertTrue(data["desired_deficit_forced"])
        self.assertEqual(data["minimum_deficit_open_endpoint"], Q(3, 50))

    def test_target_direct_contradiction(self) -> None:
        data = recurrence_ledger(Q(21, 25), Q(47, 50), Q(7, 50))
        self.assertTrue(data["all_edges_insufficient"])

    def test_totals(self) -> None:
        data = verify_all()
        self.assertEqual(data["hybrid_total_saving_for_target_7_50_open"], Q(19, 25))
        self.assertEqual(data["hybrid_total_saving_for_uniform_7_50_open"], Q(23, 25))


if __name__ == "__main__":
    unittest.main()
