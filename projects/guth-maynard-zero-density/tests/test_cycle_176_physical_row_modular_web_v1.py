import unittest

from conventions.physical_row_modular_web_v1 import row_ledger, split_codegree, verify_all


class Cycle176PhysicalRowModularWebTests(unittest.TestCase):
    def test_divisor_cap_and_exact_eligibility(self) -> None:
        ledger = row_ledger(((60, 1, 2, 1), (60, 2, 3, 1), (60, 3, 7, 1)))
        self.assertEqual(ledger[60]["eligible"], ((1, 2), (2, 3)))
        self.assertLessEqual(ledger[60]["eligible_distinct"], ledger[60]["divisor_cap"])

    def test_support_split(self) -> None:
        ledger = row_ledger(((12, 1, 2, 1), (12, 2, 5, 1), (13, 3, 2, 1)))
        self.assertEqual(split_codegree(ledger, 2), {"low_reuse": (13,), "high_reuse": (12,)})

    def test_boundary(self) -> None:
        self.assertIn("no actual row-reuse lower bound", verify_all()["boundary"])
