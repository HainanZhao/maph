import unittest
from fractions import Fraction

from conventions.tail_coupled_transition_v1 import (
    frequency_ledger,
    paired_edge_residual,
    shell_memberships,
    theorem_record,
    tiled_interval,
)


class TailCoupledTransitionTests(unittest.TestCase):
    def test_complete_shells_tile(self) -> None:
        self.assertEqual(tiled_interval(1, 3, 2, 6), (Fraction(7), Fraction(19)))
        for y in (Fraction(15, 2), Fraction(21, 2), Fraction(35, 2)):
            self.assertEqual(len(shell_memberships(y, 1, 3, 2, 6)), 1)

    def test_exact_paired_edge_identity(self) -> None:
        # alpha_left=7/5 and alpha_right=21/11, so g^d=15/11.
        left = (4, 3, 4, 1, Fraction(1, 3))
        right = (11, 6, 1, 1, Fraction(1, 5))
        self.assertEqual(paired_edge_residual(Fraction(15, 11), left, right), Fraction(1, 66))

    def test_full_endpoint_frequency_floor(self) -> None:
        row = frequency_ledger(Fraction(16, 25), Fraction(0), Fraction(1, 3), Fraction(16, 25))
        self.assertEqual(row["tail_frequency"], Fraction(23, 75))
        self.assertEqual(row["raw_residual_frequency"], Fraction(32, 25))

    def test_record_keeps_paired_norm_open(self) -> None:
        row = theorem_record()
        self.assertIn("reproduces the Cycle-132", row["marginal_no_gain"])
        self.assertIn("Omega_d", row["paired_norm"])
        self.assertIn("not proved", row["boundary"])


if __name__ == "__main__":
    unittest.main()
