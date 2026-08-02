import unittest
from fractions import Fraction as Q

from conventions.affine_eligibility_grid_v1 import full_ledger, residue_class, verify_all


class Cycle175AffineEligibilityGridTests(unittest.TestCase):
    def test_complete_range_residue_and_common_capacity_state(self) -> None:
        ledger = full_ledger(parameters=(0, 1, 2, 3, 4), h0=25, slope=1, a=5, q=4, H=20, K=5)
        self.assertEqual(ledger["range_parameters"], (0, 1, 2, 3, 4))
        self.assertEqual(ledger["residue"], (0, 5))
        self.assertEqual(ledger["eligible"], (0,))
        self.assertEqual(ledger["capacity_class"], "saturated")

    def test_large_parent_parameter_set_can_miss_residue(self) -> None:
        ledger = full_ledger(parameters=(1, 2, 3, 4, 6, 7, 8, 9), h0=25, slope=1, a=5, q=4, H=20, K=5)
        self.assertEqual(ledger["eligible"], ())
        self.assertEqual(ledger["breadth"], 0)
        self.assertEqual(ledger["discrepancy"], Q(-8, 5))

    def test_insoluble_residue_and_zero_slope(self) -> None:
        self.assertIsNone(residue_class(1, 2, 4))
        self.assertEqual(residue_class(12, 0, 3), (0, 1))
        ledger = full_ledger(parameters=(0, 1), h0=1, slope=2, a=4, q=3, H=3, K=1)
        self.assertEqual(ledger["reason"], "insoluble_residue")

    def test_boundary(self) -> None:
        self.assertIn("no actual breadth lower bound", verify_all()["boundary"])
