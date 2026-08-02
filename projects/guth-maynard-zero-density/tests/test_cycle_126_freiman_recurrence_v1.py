import unittest
from fractions import Fraction

from conventions.freiman_recurrence_v1 import (
    error_margin,
    longest_chain_edges,
    popular_difference_edges,
    sufficient_edges_for_depth,
    theorem_record,
)


class FreimanRecurrenceTests(unittest.TestCase):
    def test_combinatorial_ledgers(self) -> None:
        self.assertEqual(popular_difference_edges(20, 100), 2)
        self.assertEqual(longest_chain_edges(20, 15), 3)
        self.assertEqual(sufficient_edges_for_depth(20, 3), 15)

    def test_error_margin(self) -> None:
        self.assertEqual(error_margin(Fraction(16, 25)), Fraction(28, 75))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("independent of a", row["difference_multiplier"])
        self.assertIn("ceil(L_d/(R-L_d))", row["chain_bound"])
        self.assertIn("J/(KQ)", row["approximation"])
        self.assertIn("still tie", row["anchor_gate"])
        self.assertIn("no long chain", row["boundary"])


if __name__ == "__main__":
    unittest.main()
