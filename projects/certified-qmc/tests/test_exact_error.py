from __future__ import annotations

from fractions import Fraction
import random
import unittest

from src.exact_error import (
    RuleSpec,
    bernoulli_b2,
    exact_squared_error,
    exact_squared_error_double_sum,
    float_squared_error,
    master_denominator,
)


class ExactErrorTests(unittest.TestCase):
    def test_bernoulli_values_are_exact(self):
        self.assertEqual(bernoulli_b2(0, 8), Fraction(1, 6))
        self.assertEqual(bernoulli_b2(4, 8), Fraction(-1, 12))
        self.assertEqual(bernoulli_b2(1, 2), Fraction(-1, 12))
        self.assertEqual(bernoulli_b2(-1, 8), bernoulli_b2(7, 8))

    def test_single_sum_matches_independent_double_sum(self):
        for modulus, generator, weights in [
            (5, [1, 2], [1, Fraction(1, 3)]),
            (8, [1, 3, 5], [1, Fraction(1, 2), Fraction(1, 7)]),
            (9, [1, 2], [Fraction(2, 5), Fraction(3, 11)]),
        ]:
            self.assertEqual(
                exact_squared_error(modulus, generator, weights),
                exact_squared_error_double_sum(
                    modulus,
                    generator,
                    weights,
                ),
            )

    def test_denominator_proof_includes_weight_denominators(self):
        spec = RuleSpec.create(
            5,
            [1, 2],
            [Fraction(1, 2), Fraction(1, 3)],
        )
        result = exact_squared_error(
            spec.modulus,
            spec.generator,
            spec.weights,
        )
        bound = master_denominator(spec)
        self.assertEqual(bound, 675000)
        self.assertEqual(bound % result.denominator, 0)

    def test_sign_symmetry_is_exact(self):
        modulus = 31
        weights = [1, Fraction(1, 2), Fraction(1, 3)]
        first = exact_squared_error(modulus, [1, 7, 11], weights)
        mirrored = exact_squared_error(modulus, [1, 7, 20], weights)
        self.assertEqual(first, mirrored)

    def test_float_reference_on_100_frozen_random_cases(self):
        random_source = random.Random(20260729)
        for _ in range(100):
            modulus = random_source.randint(3, 40)
            dimension = random_source.randint(1, 6)
            generator = [
                random_source.randrange(1, modulus)
                for _ in range(dimension)
            ]
            weights = [
                Fraction(
                    random_source.randint(0, 5),
                    random_source.randint(1, 9),
                )
                for _ in range(dimension)
            ]
            exact = exact_squared_error(modulus, generator, weights)
            floating = float_squared_error(modulus, generator, weights)
            self.assertAlmostEqual(float(exact), floating, delta=2e-14)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            RuleSpec.create(1, [1], [1])
        with self.assertRaises(ValueError):
            RuleSpec.create(8, [1, 3], [1])
        with self.assertRaises(ValueError):
            RuleSpec.create(8, [1], [-1])


if __name__ == "__main__":
    unittest.main()
