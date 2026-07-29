from __future__ import annotations

from fractions import Fraction
import itertools
import unittest

from src.exact_error import exact_squared_error
from src.scaled_integer import (
    b2_numerator,
    b2_numerator_span,
    balanced_crt_bits,
    candidate_difference_bound,
    candidate_difference_integer,
    scaled_squared_error,
)


class ScaledIntegerTests(unittest.TestCase):
    def test_scaled_form_matches_fraction_oracle(self):
        cases = [
            (5, [1, 2], [1, Fraction(1, 3)]),
            (8, [1, 3, 5], [1, Fraction(1, 2), Fraction(2, 7)]),
            (9, [1, 2], [Fraction(2, 5), Fraction(3, 11)]),
        ]
        for modulus, generator, weights in cases:
            scaled = scaled_squared_error(modulus, generator, weights)
            self.assertEqual(
                scaled.value,
                exact_squared_error(modulus, generator, weights),
            )
            self.assertLessEqual(abs(scaled.numerator), scaled.numerator_bound)

    def test_b2_span_is_exact_exhaustively(self):
        for modulus in range(2, 18):
            values = [b2_numerator(r, modulus) for r in range(modulus)]
            self.assertEqual(max(values) - min(values), b2_numerator_span(modulus))

    def test_candidate_difference_matches_scaled_scores(self):
        for modulus in (5, 8, 9):
            weights = [Fraction(2, 3), Fraction(3, 5)]
            prefix = [1]
            for u, v in itertools.product(range(1, modulus), repeat=2):
                difference = candidate_difference_integer(
                    modulus, prefix, weights, u, v
                )
                score_u = scaled_squared_error(
                    modulus, [*prefix, u], weights
                )
                score_v = scaled_squared_error(
                    modulus, [*prefix, v], weights
                )
                self.assertEqual(difference, score_u.numerator - score_v.numerator)
                bound = candidate_difference_bound(
                    modulus, weights[:-1], weights[-1]
                )
                self.assertLessEqual(abs(difference), bound)

    def test_zero_new_weight_forces_exact_tie(self):
        self.assertEqual(
            candidate_difference_integer(7, [1], [1, 0], 2, 3),
            0,
        )

    def test_balanced_crt_bit_requirement(self):
        self.assertEqual(balanced_crt_bits(0), 1)
        self.assertGreaterEqual(2 ** balanced_crt_bits(100), 201)


if __name__ == "__main__":
    unittest.main()
