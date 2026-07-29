from fractions import Fraction
import unittest

from src.format_bound import (
    exact_decimal,
    formatting_bound,
    lexical_grid_exponent,
    observed_significant_digits,
)


class FormattingBoundTests(unittest.TestCase):
    def test_decimal_lexemes_are_exact(self):
        self.assertEqual(exact_decimal("1.25"), Fraction(5, 4))
        self.assertEqual(exact_decimal("-1.25e-3"), Fraction(-1, 800))
        self.assertEqual(exact_decimal(".000"), 0)

    def test_lexical_grid_includes_exponent_and_trailing_zeroes(self):
        self.assertEqual(lexical_grid_exponent("1.2300e-4"), -8)
        self.assertEqual(observed_significant_digits("1.2300e-4"), 5)
        bound = formatting_bound("1.2300e-4")
        self.assertEqual(bound.grid_spacing, Fraction(1, 10**8))
        self.assertEqual(bound.half_cell, Fraction(1, 2 * 10**8))

    def test_table_precision_resolves_integer_trailing_zero_ambiguity(self):
        bound = formatting_bound("1200", significant_digits=2)
        self.assertEqual(bound.grid_spacing, 100)
        self.assertEqual(bound.half_cell, 50)

    def test_typical_precision_scale(self):
        self.assertEqual(
            formatting_bound("1.2345", significant_digits=5).half_cell,
            Fraction(1, 20000),
        )
        self.assertEqual(
            formatting_bound("0.0001234", significant_digits=4).half_cell,
            Fraction(1, 2 * 10**7),
        )

    def test_zero_uses_observed_lexical_grid(self):
        bound = formatting_bound("0.0000")
        self.assertEqual(bound.grid_exponent, -4)
        self.assertEqual(bound.half_cell, Fraction(1, 20000))

    def test_rejects_nonfinite_or_nondecimal_input(self):
        for text in ("nan", "inf", "1/3", ""):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    formatting_bound(text)


if __name__ == "__main__":
    unittest.main()
