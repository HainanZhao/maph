import unittest

from src.sic_stark import (
    IDENTITY_2,
    canonical_family_record,
    canonical_form,
    canonical_quadratic_identity,
    canonical_level_stabilizer,
    canonical_stabilizer,
    canonical_twist_kernel,
    canonical_twist_multiplier,
    canonical_zauner_action,
    canonical_zauner_orbits,
    determinant,
    extended_displacement_modulus,
    form_discriminant,
    matrix_mod,
    matrix_power,
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

    def test_twist_kernel_has_dimension_independent_representative(self) -> None:
        for dimension in range(4, 501):
            self.assertEqual(
                canonical_twist_kernel(dimension),
                ((0, dimension - 1), (1, 1)),
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

    def test_canonical_zauner_orbits_have_length_one_or_three(self) -> None:
        for dimension in range(4, 101):
            orbits = canonical_zauner_orbits(dimension)
            self.assertTrue(all(len(orbit) in (1, 3) for orbit in orbits))
            self.assertEqual(
                sum(len(orbit) for orbit in orbits), dimension * dimension
            )
            fixed_count = sum(len(orbit) == 1 for orbit in orbits)
            self.assertEqual(fixed_count, 3 if dimension % 3 == 0 else 1)

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

    def test_family_record_is_internally_consistent(self) -> None:
        record = canonical_family_record(4)
        self.assertEqual(record["form"], (1, -3, 1))
        self.assertEqual(record["discriminant"], 5)
        self.assertEqual(record["cube_mod_dimension"], IDENTITY_2)

    def test_invalid_dimensions_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            canonical_form(3)
        with self.assertRaises(ValueError):
            canonical_stabilizer(0)
        with self.assertRaises(ValueError):
            extended_displacement_modulus(0)


if __name__ == "__main__":
    unittest.main()
