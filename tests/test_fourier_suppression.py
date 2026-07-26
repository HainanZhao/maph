import math
import unittest

from src.fourier_suppression import (
    canonical_dark_pair,
    four_mode_self_family_closed_form,
    four_mode_self_family_coefficient,
    four_mode_reflection_self_coefficient,
    fourier_support_type_counts,
    has_at_most_two_fourier_support_types,
    is_dark_prime_power,
    lift_fourier_occupations,
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

    def test_infinite_self_family_initial_cases(self):
        for a in (1, 3, 5, 7):
            self.assertEqual(four_mode_self_family_coefficient(a), 0)
            occupation = (0, a, 2 * a, a)
            self.assertTrue(is_dark_prime_power(occupation, occupation))
            self.assertFalse(
                simple_cyclic_rule_predicts_dark(occupation, occupation)
            )
        for a in (2, 4, 6):
            self.assertNotEqual(four_mode_self_family_coefficient(a), 0)
            occupation = (0, a, 2 * a, a)
            self.assertFalse(is_dark_prime_power(occupation, occupation))

    def test_self_family_closed_form(self):
        for a in range(51):
            self.assertEqual(
                four_mode_self_family_coefficient(a),
                four_mode_self_family_closed_form(a),
            )

    def test_support_type_filter_separates_pilot_families(self):
        reducible_pairs = (
            ((0, 0, 2, 2), (0, 1, 0, 3)),
            ((0, 1, 0, 3), (0, 1, 2, 1)),
        )
        for pair in reducible_pairs:
            self.assertEqual(fourier_support_type_counts(*pair), (2, 2))
            self.assertTrue(has_at_most_two_fourier_support_types(*pair))

        multitype_pair = ((0, 1, 2, 1), (0, 1, 2, 1))
        self.assertEqual(
            fourier_support_type_counts(*multitype_pair), (3, 3)
        )
        self.assertFalse(
            has_at_most_two_fourier_support_types(*multitype_pair)
        )

    def test_reflection_family_specializes_to_closed_family(self):
        for a in range(11):
            self.assertEqual(
                four_mode_reflection_self_coefficient(a, 2 * a),
                four_mode_self_family_closed_form(a),
            )

    def test_reflection_family_matches_permanent_for_small_parameters(self):
        for a in range(1, 4):
            for b in range(5):
                occupation = (0, a, b, a)
                histogram = phase_histogram(occupation, occupation)
                permanent = histogram[0] - histogram[2]
                input_factorials = (
                    math.factorial(a) ** 2 * math.factorial(b)
                )
                self.assertEqual(
                    permanent,
                    input_factorials
                    * four_mode_reflection_self_coefficient(a, b),
                )

    def test_four_mode_dark_family_lifts_to_larger_power_of_two(self):
        source = (0, 3, 6, 3)
        for target_modes in (8, 16):
            lifted_input, lifted_output = lift_fourier_occupations(
                source, source, target_modes
            )
            self.assertTrue(
                is_dark_prime_power(lifted_input, lifted_output)
            )

    def test_lift_requires_divisibility(self):
        with self.assertRaises(ValueError):
            lift_fourier_occupations((1, 1), (1, 1), 3)


if __name__ == "__main__":
    unittest.main()
