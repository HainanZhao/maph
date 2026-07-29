from fractions import Fraction
import math
import unittest

from flint import arb, ctx

from src.producer_error import (
    certify_p2_cbc_branches,
    direct_product_p2_bound,
    independent_p2_merit,
)


class ProducerErrorTests(unittest.TestCase):
    def test_one_dimension_matches_closed_kernel_average(self):
        report = direct_product_p2_bound(8, [1], [Fraction(1, 1)])
        self.assertTrue(report["contains_independent_arb_target"])
        self.assertTrue(math.isfinite(report["float_value"]))
        self.assertGreater(report["operation_counts"]["mul"], 0)

    def test_multidimensional_adversarial_weights_are_contained(self):
        cases = [
            (8, [1, 3], [Fraction(1), Fraction(1, 4)]),
            (16, [1, 7, 5], [Fraction(1), Fraction(1, 1000), Fraction(7, 9)]),
            (32, [1, 15, 7, 13], [Fraction(1, j * j) for j in range(1, 5)]),
        ]
        for modulus, generator, weights in cases:
            with self.subTest(modulus=modulus):
                report = direct_product_p2_bound(modulus, generator, weights)
                self.assertTrue(report["contains_independent_arb_target"])

    def test_independent_merit_is_sign_symmetric(self):
        old_precision = ctx.prec
        ctx.prec = 192
        try:
            left = independent_p2_merit(
                16, [1, 3, 5], [Fraction(1), Fraction(1, 4), Fraction(1, 9)]
            )
            right = independent_p2_merit(
                16, [15, 13, 11], [Fraction(1), Fraction(1, 4), Fraction(1, 9)]
            )
            self.assertTrue((left - right).contains(0))
        finally:
            ctx.prec = old_precision

    def test_certifies_known_small_cbc_vector(self):
        report = certify_p2_cbc_branches(
            16,
            [1, 7, 5],
            [Fraction(1), Fraction(1, 4), Fraction(1, 9)],
        )
        self.assertTrue(report["all_branches_certified"])
        self.assertEqual(len(report["stages"]), 2)
        self.assertTrue(
            all(
                stage["all_competitors_nonnegative_or_exact_ties"]
                for stage in report["stages"]
            )
        )


if __name__ == "__main__":
    unittest.main()
