import unittest
from fractions import Fraction

from conventions.gaudron_direct_ledger_v1 import cost_ledger, support_ledger


class GaudronDirectLedgerTests(unittest.TestCase):
    def test_cost_sum(self) -> None:
        ledger = cost_ledger()
        costs = ledger["costs"]
        total = sum(Fraction(value) for value in costs.values())
        self.assertEqual(total, Fraction(12, 5))
        self.assertEqual(ledger["negative_log_exponent"], "12/5")

    def test_gaudron_specialization(self) -> None:
        ledger = cost_ledger()
        self.assertEqual((ledger["gaudron_n"], ledger["gaudron_t"]), (2, 1))
        self.assertIn("TOO_WEAK", ledger["comparison"])

    def test_support_chain(self) -> None:
        support = support_ledger()
        self.assertIn("<<D", support["mode_radius"])
        self.assertIn("<=4M", support["field_degree"])

    def test_scope_boundary(self) -> None:
        self.assertIn("no saturation claim", cost_ledger()["scope"])


if __name__ == "__main__":
    unittest.main()
