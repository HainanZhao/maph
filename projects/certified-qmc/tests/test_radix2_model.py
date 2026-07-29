from fractions import Fraction
import unittest

from src.radix2_model import (
    DEFAULT_TWIDDLE_ERROR,
    UNIT_ROUNDOFF,
    certify_reference_fft,
    gamma_k,
    reference_fft,
    transform_error_factor,
)


class RadixTwoModelTests(unittest.TestCase):
    def test_gamma_and_transform_factor_are_exact_rationals(self):
        self.assertEqual(gamma_k(0), 0)
        self.assertEqual(gamma_k(1), UNIT_ROUNDOFF / (1 - UNIT_ROUNDOFF))
        factor = transform_error_factor(16)
        self.assertIsInstance(factor, Fraction)
        self.assertGreater(factor, 0)
        self.assertLess(factor, Fraction(1, 10**12))

    def test_reference_round_trip(self):
        values = [complex((index - 3) / 7, (2 * index + 1) / 11) for index in range(8)]
        transformed = reference_fft(values)
        recovered = reference_fft(
            transformed, inverse=True, normalize_inverse=True
        )
        for expected, observed in zip(values, recovered):
            self.assertAlmostEqual(expected.real, observed.real, places=13)
            self.assertAlmostEqual(expected.imag, observed.imag, places=13)

    def test_analytic_envelope_contains_arb_dft(self):
        for length in (2, 4, 8, 16, 32):
            values = [
                complex((index - length / 3) / 17, (3 * index - 2) / 19)
                for index in range(length)
            ]
            for inverse, normalized in ((False, False), (True, True)):
                with self.subTest(
                    length=length, inverse=inverse, normalized=normalized
                ):
                    report = certify_reference_fft(
                        values,
                        inverse=inverse,
                        normalize_inverse=normalized,
                    )
                    self.assertTrue(report["twiddles_contained"])
                    self.assertTrue(report["transform_contained"])

    def test_sensitivity_variants_are_monotone(self):
        baseline = transform_error_factor(1024)
        doubled_twiddle = transform_error_factor(
            1024, twiddle_error=2 * DEFAULT_TWIDDLE_ERROR
        )
        doubled_depth = transform_error_factor(
            1024, radix2_equivalent_depth=20
        )
        self.assertGreater(doubled_twiddle, baseline)
        self.assertGreater(doubled_depth, baseline)


if __name__ == "__main__":
    unittest.main()
