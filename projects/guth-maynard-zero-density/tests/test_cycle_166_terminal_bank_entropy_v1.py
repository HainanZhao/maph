import unittest
from itertools import combinations, permutations
from fractions import Fraction
from math import gcd

from conventions.anchored_fibre_product_determinant_v1 import Anchor
from conventions.terminal_bank_entropy_v1 import (
    ETA,
    canonical_packet_state,
    canonical_rank_one_witness,
    plane_shift_state,
    select_packet_coordinate,
    state_ledger,
    theorem_record,
    unique_integer_candidates,
    verify_all,
)


class Cycle166TerminalBankEntropyTests(unittest.TestCase):
    def test_exact_margins(self):
        ledger = state_ledger()
        self.assertEqual(ledger["rank_or_plane_forced_fibre_exponent"], Fraction(1, 25))
        self.assertEqual(ledger["packet_forced_fibre_exponent"], Fraction(2, 25))
        self.assertEqual(ledger["subcritical_rank_or_plane_bound"], Fraction(149, 100))
        self.assertEqual(ledger["registered_target"], Fraction(151, 100))
        self.assertEqual(2 * ETA, Fraction(1, 50))

    def test_complete_ledger(self):
        checked = verify_all()
        self.assertIn("at most one ell", checked["transverse"])
        self.assertIn("does not bound", theorem_record()["boundary"])

    def test_rank_one_normalization_is_permutation_and_rescaling_invariant(self):
        """Exhaust all small four-subsets and every input ordering.

        The expected direction absorbs the common gcd of the affine parameter
        set.  This is the exact anti-alias rule used by the entropy count.
        """
        r0, s0, t0 = 2, 3, -1
        for values in combinations(range(-3, 4), 4):
            minimum = min(values)
            shifted = tuple(value - minimum for value in values)
            parameter_gcd = 0
            for value in shifted:
                parameter_gcd = gcd(parameter_gcd, value)
            anchors = tuple(
                Anchor(50 + r0 * n, 80 + s0 * n, 100 + t0 * n, 120)
                for n in values
            )
            expected = {
                "base": Anchor(50 + r0 * minimum, 80 + s0 * minimum, 100 + t0 * minimum, 120),
                "r": r0 * parameter_gcd,
                "s": s0 * parameter_gcd,
                "t": t0 * parameter_gcd,
                "parameters": tuple(value // parameter_gcd for value in shifted),
            }
            for ordering in permutations(anchors):
                self.assertEqual(canonical_rank_one_witness(ordering), expected)

    def test_rank_one_normalization_rejects_rank_two_input(self):
        anchors = (
            Anchor(1, 1, 1, 0),
            Anchor(2, 1, 1, 0),
            Anchor(1, 2, 1, 0),
            Anchor(3, 3, 2, 0),
        )
        with self.assertRaises(ValueError):
            canonical_rank_one_witness(anchors)

    def test_plane_state_preserves_signs_and_unique_integer_rule(self):
        self.assertEqual(plane_shift_state(2, -6, -3, -9), (2, -9, -15))
        self.assertEqual(plane_shift_state(1, 6, 3, 9), (1, 9, 15))
        with self.assertRaises(ValueError):
            plane_shift_state(0, 6, 3, 9)
        with self.assertRaises(ValueError):
            plane_shift_state(1, 6, -6, 9)
        with self.assertRaises(ValueError):
            plane_shift_state(1, 6, 3, -6)
        self.assertEqual(unique_integer_candidates(Fraction(151, 10), Fraction(2, 5)), (15,))
        self.assertEqual(unique_integer_candidates(Fraction(1, 2), Fraction(49, 100)), ())
        self.assertEqual(unique_integer_candidates(Fraction(1, 2), Fraction(1, 2)), (0, 1))

    def test_packet_routing_and_base_are_deterministic(self):
        seeds = ((9, 4), (5, 2), (7, 9))
        expected = (3, 2, 5, 7, 5, 2)
        for ordering in permutations(seeds):
            self.assertEqual(canonical_packet_state(ell=3, a=2, q=5, k_max=7, seeds=ordering), expected)
        self.assertEqual(select_packet_coordinate(True, True), "first")
        self.assertEqual(select_packet_coordinate(False, True), "second")
        with self.assertRaises(ValueError):
            select_packet_coordinate(False, False)


if __name__ == "__main__":
    unittest.main()
