import unittest
from fractions import Fraction

from conventions.order_three_denominator_bridge_v1 import block_ledger, range_ledger, theorem_record


class OrderThreeDenominatorBridgeTests(unittest.TestCase):
    def test_lower_endpoint(self) -> None:
        row = range_ledger(Fraction(16, 25), Fraction(0))
        self.assertEqual(row["hs_ceiling"], Fraction(7, 45))
        self.assertEqual(row["extension_beyond_broad"], Fraction(2, 225))
        self.assertEqual(row["remaining_endpoint_width"], Fraction(8, 45))
        terms = block_ledger(Fraction(16, 25), Fraction(0), row["hs_ceiling"])
        self.assertEqual(terms["derivative"], Fraction(1, 3))

    def test_worst_endpoint_width(self) -> None:
        xi = Fraction(16, 25)
        mu = (1 - xi) / 4
        row = range_ledger(xi, mu)
        self.assertEqual(row["remaining_endpoint_width"], Fraction(133, 900))
        self.assertTrue(all(row[key] > 0 for key in ("tube_margin", "ratio_margin", "constant_margin")))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("rho_HS=7/45-2mu/3", row["closure_ceiling"])
        self.assertIn(">=2/225", row["broad_extension"])
        self.assertIn(">=133/900", row["remaining_width"])
        self.assertIn("no endpoint-denominator", row["boundary"])


if __name__ == "__main__":
    unittest.main()
