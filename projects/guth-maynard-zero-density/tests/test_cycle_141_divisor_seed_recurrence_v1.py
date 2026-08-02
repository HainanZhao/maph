import unittest
from fractions import Fraction

from conventions.divisor_seed_recurrence_v1 import (
    continuation_ledger,
    forced_transition,
    repeated_transition_possible,
    theorem_record,
)


class DivisorSeedRecurrenceTests(unittest.TestCase):
    def test_forced_diagonal(self) -> None:
        self.assertEqual(forced_transition(15, 14, 3, 7), (Fraction(5, 7), Fraction(2, 3)))
        self.assertFalse(repeated_transition_possible(15, 14, 3, 7))
        self.assertTrue(repeated_transition_possible(1, 1, 1, 1))

    def test_continuation_counts(self) -> None:
        row = continuation_ledger(100, 75, 3)
        self.assertEqual(row["longest_chain_edges"], 3)
        self.assertEqual(row["length_two_starts"], 50)
        self.assertEqual(row["depth_starts"], 25)
        self.assertEqual(row["edges_sufficient_for_depth"], 75)

    def test_sparse_edges_give_no_continuation(self) -> None:
        row = continuation_ledger(100, 40, 2)
        self.assertEqual(row["length_two_starts"], 0)
        self.assertEqual(row["longest_chain_edges"], 1)

    def test_record_replaces_wrong_invariant(self) -> None:
        row = theorem_record()
        self.assertIn("at most one edge", row["unimodular_no_go"])
        self.assertIn("neither", row["independence"])
        self.assertIn("must not be used", row["replacement_invariant"])


if __name__ == "__main__":
    unittest.main()
