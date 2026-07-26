import unittest

from src.sic_stark import (
    IDENTITY_2,
    canonical_characteristic_correction_index,
    canonical_family_record,
    canonical_form,
    canonical_jacobi_scale_exponents,
    canonical_jacobi_word,
    canonical_kernel_identity,
    canonical_level_quotient,
    canonical_quadratic_identity,
    canonical_level_stabilizer,
    canonical_shift_partner,
    canonical_stabilizer,
    canonical_tcc_orbit_bound,
    canonical_twist_exponent,
    canonical_twist_kernel,
    canonical_twist_multiplier,
    canonical_zauner_action,
    canonical_zauner_orbit_sum,
    canonical_zauner_orbits,
    determinant,
    extended_displacement_modulus,
    form_discriminant,
    matrix_multiply,
    matrix_mod,
    matrix_power,
    matrix_vector_multiply,
)


class CanonicalSicStarkTests(unittest.TestCase):
    def test_canonical_discriminant_identity(self) -> None:
        for dimension in range(4, 501):
            discriminant = form_discriminant(canonical_form(dimension))
            self.assertEqual(
                discriminant, (dimension + 1) * (dimension - 3)
            )

    def test_canonical_stabilizer_quadratic_identity(self) -> None:
        for dimension in range(4, 501):
            self.assertEqual(
                canonical_quadratic_identity(dimension),
                ((0, 0), (0, 0)),
            )

    def test_canonical_stabilizer_is_unimodular(self) -> None:
        for dimension in range(4, 501):
            self.assertEqual(determinant(canonical_stabilizer(dimension)), 1)

    def test_canonical_stabilizer_cube_is_identity_mod_d(self) -> None:
        for dimension in range(4, 501):
            cube = canonical_level_stabilizer(dimension)
            self.assertEqual(matrix_mod(cube, dimension), IDENTITY_2)

    def test_exact_level_stabilizer_lift(self) -> None:
        for dimension in range(4, 501):
            quotient = canonical_level_quotient(dimension)
            reconstructed = tuple(
                tuple(
                    IDENTITY_2[row][column]
                    + dimension * quotient[row][column]
                    for column in range(2)
                )
                for row in range(2)
            )
            self.assertEqual(
                reconstructed, canonical_level_stabilizer(dimension)
            )

    def test_twist_kernel_has_dimension_independent_representative(self) -> None:
        for dimension in range(4, 501):
            self.assertEqual(
                canonical_twist_kernel(dimension),
                ((0, dimension - 1), (1, 1)),
            )
            self.assertEqual(
                canonical_kernel_identity(dimension), ((0, 0), (0, 0))
            )

    def test_shift_one_is_compatible_with_identity_twist(self) -> None:
        for dimension in range(4, 501):
            modulus = extended_displacement_modulus(dimension)
            self.assertEqual(
                canonical_twist_multiplier(dimension, 1),
                1 % modulus,
            )
            self.assertEqual(
                canonical_twist_multiplier(dimension, 0),
                -1 % modulus,
            )

    def test_shift_conjugation_pairs_zero_and_one(self) -> None:
        for dimension in range(4, 501):
            modulus = extended_displacement_modulus(dimension)
            self.assertEqual(canonical_shift_partner(dimension, 0), 1)
            self.assertEqual(canonical_shift_partner(dimension, 1), 0)
            for shift in range(dimension):
                partner = canonical_shift_partner(dimension, shift)
                self.assertEqual(
                    canonical_shift_partner(dimension, partner), shift
                )
                self.assertEqual(
                    canonical_twist_multiplier(dimension, partner),
                    -canonical_twist_multiplier(dimension, shift)
                    % modulus,
                )

    def test_characteristic_correction_index(self) -> None:
        for dimension in range(4, 101):
            level = canonical_level_stabilizer(dimension)
            for vector in (
                (0, 0),
                (1, 0),
                (0, 1),
                (dimension - 1, dimension - 2),
            ):
                transformed = matrix_vector_multiply(level, vector)
                difference = (
                    vector[0] - transformed[0],
                    vector[1] - transformed[1],
                )
                self.assertEqual(difference[0] % dimension, 0)
                self.assertEqual(difference[1] % dimension, 0)
                self.assertEqual(
                    difference[1] // dimension,
                    canonical_characteristic_correction_index(
                        dimension, vector
                    ),
                )

    def test_canonical_zauner_orbits_have_length_one_or_three(self) -> None:
        for dimension in range(4, 101):
            orbits = canonical_zauner_orbits(dimension)
            self.assertTrue(all(len(orbit) in (1, 3) for orbit in orbits))
            self.assertEqual(
                sum(len(orbit) for orbit in orbits), dimension * dimension
            )
            fixed_count = sum(len(orbit) == 1 for orbit in orbits)
            self.assertEqual(fixed_count, 3 if dimension % 3 == 0 else 1)
            self.assertEqual(
                len(orbits), canonical_tcc_orbit_bound(dimension)
            )

    def test_nonzero_fixed_vectors_when_three_divides_dimension(self) -> None:
        for dimension in (6, 9, 12, 15):
            step = dimension // 3
            expected = {(0, 0), (step, step), (2 * step, 2 * step)}
            fixed = {
                vector
                for vector in expected
                if canonical_zauner_action(dimension, vector) == vector
            }
            self.assertEqual(fixed, expected)

    def test_each_zauner_orbit_sums_to_zero(self) -> None:
        for dimension in range(4, 101):
            for first in range(dimension):
                for second in range(dimension):
                    self.assertEqual(
                        canonical_zauner_orbit_sum(
                            dimension, (first, second)
                        ),
                        (0, 0),
                    )

    def test_twist_phase_is_zauner_invariant(self) -> None:
        for dimension in range(4, 13):
            for p_1 in range(dimension):
                for p_2 in range(dimension):
                    left = (p_1, p_2)
                    acted_left = canonical_zauner_action(
                        dimension, left
                    )
                    for q_1 in range(dimension):
                        for q_2 in range(dimension):
                            right = (q_1, q_2)
                            acted_right = canonical_zauner_action(
                                dimension, right
                            )
                            self.assertEqual(
                                canonical_twist_exponent(
                                    dimension, acted_left, acted_right
                                ),
                                canonical_twist_exponent(
                                    dimension, left, right
                                ),
                            )

    def test_uniform_jacobi_word_and_scales(self) -> None:
        self.assertEqual(
            canonical_jacobi_scale_exponents(), (-2, -1, 0)
        )
        for dimension in range(4, 501):
            self.assertEqual(
                canonical_jacobi_word(dimension),
                (dimension - 1, dimension - 1, dimension - 1),
            )
            stabilizer = canonical_stabilizer(dimension)
            self.assertEqual(
                matrix_power(stabilizer, 3),
                matrix_multiply(
                    matrix_multiply(stabilizer, stabilizer), stabilizer
                ),
            )

    def test_family_record_is_internally_consistent(self) -> None:
        record = canonical_family_record(4)
        self.assertEqual(record["form"], (1, -3, 1))
        self.assertEqual(record["discriminant"], 5)
        self.assertEqual(record["cube_mod_dimension"], IDENTITY_2)
        self.assertEqual(record["shift_zero_partner"], 1)
        self.assertEqual(record["jacobi_scale_exponents"], (-2, -1, 0))

    def test_invalid_dimensions_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            canonical_form(3)
        with self.assertRaises(ValueError):
            canonical_stabilizer(0)
        with self.assertRaises(ValueError):
            extended_displacement_modulus(0)


if __name__ == "__main__":
    unittest.main()
