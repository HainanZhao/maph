import math
import unittest

from src.fourier_suppression import (
    canonical_dark_pair,
    is_dark_prime_power,
    occupation_vectors,
    phase_histogram,
    prime_power_base,
    simple_cyclic_rule_predicts_dark,
)


class FourierSuppressionTests(unittest.TestCase):
    def test_occupation_vectors(self):
        vectors = list(occupation_vectors(4, 4))
        self.assertEqual(len(vectors), math.comb(7, 3))
        self.assertTrue(all(sum(vector) == 4 for vector in vectors))

    def test_prime_power_base(self):
        self.assertEqual(prime_power_base(2), 2)
        self.assertEqual(prime_power_base(8), 2)
        self.assertEqual(prime_power_base(9), 3)
        self.assertIsNone(prime_power_base(6))

    def test_hong_ou_mandel_event(self):
        occupation = (1, 1)
        self.assertEqual(phase_histogram(occupation, occupation), (1, 1))
        self.assertTrue(is_dark_prime_power(occupation, occupation))
        self.assertTrue(
            simple_cyclic_rule_predicts_dark(occupation, occupation)
        )

    def test_manifestly_nonzero_event(self):
        input_occupation = (4, 0, 0, 0)
        output_occupation = (4, 0, 0, 0)
        self.assertEqual(
            phase_histogram(input_occupation, output_occupation),
            (24, 0, 0, 0),
        )
        self.assertFalse(
            is_dark_prime_power(input_occupation, output_occupation)
        )

    def test_residual_four_mode_event(self):
        input_occupation = (0, 1, 2, 1)
        output_occupation = (0, 1, 2, 1)
        self.assertEqual(
            phase_histogram(input_occupation, output_occupation),
            (4, 8, 4, 8),
        )
        self.assertTrue(
            is_dark_prime_power(input_occupation, output_occupation)
        )
        self.assertFalse(
            simple_cyclic_rule_predicts_dark(
                input_occupation, output_occupation
            )
        )

    def test_canonicalization(self):
        pair = canonical_dark_pair((1, 2, 1, 0), (1, 0, 3, 0))
        rotated = canonical_dark_pair((0, 1, 2, 1), (0, 3, 0, 1))
        self.assertEqual(pair, rotated)

    def test_complete_four_photon_pilot_scan(self):
        occupations = list(occupation_vectors(4, 4))
        dark_count = 0
        cyclic_count = 0
        residual_families = set()
        for input_occupation in occupations:
            for output_occupation in occupations:
                if not is_dark_prime_power(
                    input_occupation, output_occupation
                ):
                    continue
                dark_count += 1
                if simple_cyclic_rule_predicts_dark(
                    input_occupation, output_occupation
                ):
                    cyclic_count += 1
                else:
                    residual_families.add(
                        canonical_dark_pair(
                            input_occupation, output_occupation
                        )
                    )
        self.assertEqual(dark_count, 193)
        self.assertEqual(cyclic_count, 113)
        self.assertEqual(len(residual_families), 3)


if __name__ == "__main__":
    unittest.main()
