from __future__ import annotations

from fractions import Fraction
import unittest

from src.cbc import exact_cbc
from src.crt import balanced_reconstruct, choose_moduli
from src.exact_error import exact_squared_error
from src.modular_error import (
    certified_crt_cbc,
    reconstruct_candidate_difference,
    reconstruct_error_numerator,
)
from src.ntt_prime import generate_ntt_prime_schedule
from src.scaled_integer import candidate_difference_integer


class CrtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schedule = generate_ntt_prime_schedule(4)

    def test_balanced_reconstruction_at_both_signs(self):
        moduli = [101, 103]
        for value in (-5000, -1, 0, 1, 5000):
            residues = [value % p for p in moduli]
            self.assertEqual(
                balanced_reconstruct(residues, moduli, bound=5000), value
            )

    def test_shortest_schedule_prefix_is_selected(self):
        self.assertEqual(choose_moduli([101, 103, 107], 40), [101])
        self.assertEqual(choose_moduli([101, 103, 107], 100), [101, 103])

    def test_modular_error_matches_fraction_oracle(self):
        reconstruction = reconstruct_error_numerator(
            31,
            [1, 7, 11, 13],
            [1, Fraction(1, 4), Fraction(1, 9), Fraction(1, 16)],
            self.schedule,
        )
        self.assertEqual(
            Fraction(
                int(reconstruction["reduced_numerator"]),
                int(reconstruction["reduced_denominator"]),
            ),
            exact_squared_error(
                31,
                [1, 7, 11, 13],
                [1, Fraction(1, 4), Fraction(1, 9), Fraction(1, 16)],
            ),
        )

    def test_candidate_difference_matches_integer_oracle(self):
        weights = [1, Fraction(1, 4), Fraction(1, 9)]
        proof = reconstruct_candidate_difference(
            31, [1, 7], weights, 5, 11, self.schedule
        )
        self.assertEqual(
            proof["difference"],
            candidate_difference_integer(31, [1, 7], weights, 5, 11),
        )

    def test_crt_cbc_matches_fraction_oracle(self):
        weights = [Fraction(1, j * j) for j in range(1, 6)]
        crt = certified_crt_cbc(31, weights, self.schedule)
        exact = exact_cbc(31, weights)
        self.assertEqual(crt["generator"], exact["generator"])
        self.assertEqual(crt["final_squared_error"], exact["final_squared_error"])
        self.assertTrue(
            all(
                int(comparison["candidate_minus_winner"]) >= 0
                for decision in crt["decisions"]
                for comparison in decision["comparisons"]
            )
        )


if __name__ == "__main__":
    unittest.main()
