import cmath
import math
import unittest

from scripts.certify_general_fourier_cat_tomography import (
    amplitude_gradient,
    basis_entry,
    certificate_matrix,
    coordinates,
    f4_spam_matrix,
    imaginary_probe_entry,
    modular_charge,
    probe_amplitude,
    rational_rank,
    selected_events,
    verify,
)


def defining_polynomial_derivative(
    occupation, coordinate
):
    """Differentiate the defining cat polynomial, independently of Eq. (1)."""
    modes = len(occupation)
    photons = sum(occupation)
    omega = cmath.exp(2j * math.pi / modes)
    fourier = [
        [
            omega ** (row * column) / math.sqrt(modes)
            for column in range(modes)
        ]
        for row in range(modes)
    ]
    direction = [[0j] * modes for _ in range(modes)]
    for row in range(modes):
        for column in range(modes):
            direction[row][column] = 1j * sum(
                complex(*basis_entry(coordinate, row, middle))
                * fourier[middle][column]
                for middle in range(modes)
            )
    prefactor = math.sqrt(
        math.factorial(photons)
        / math.prod(math.factorial(count) for count in occupation)
    ) / math.sqrt(modes)
    total = 0j
    for column in range(modes):
        for differentiated_row, count in enumerate(occupation):
            if not count:
                continue
            term = count * direction[differentiated_row][column]
            for row, exponent in enumerate(occupation):
                if row == differentiated_row:
                    exponent -= 1
                term *= fourier[row][column] ** exponent
            total += term
    return prefactor * total


class GeneralFourierCatTomographyTests(unittest.TestCase):
    def test_minimal_rank_certificates_at_n_equals_m(self):
        for modes in range(3, 9):
            with self.subTest(modes=modes):
                result = verify(modes, modes)
                dimension = modes * (modes - 1)
                self.assertEqual(result["events"], dimension // 2)
                self.assertEqual(result["rows"], dimension)
                self.assertEqual(result["rank"], dimension)

    def test_rank_certificates_for_second_photon_multiple(self):
        for modes in range(2, 9):
            with self.subTest(modes=modes):
                photons = 2 * modes
                matrix = certificate_matrix(modes, photons)
                self.assertEqual(
                    rational_rank(matrix), modes * (modes - 1)
                )

    def test_selected_events_are_in_claimed_dark_sectors(self):
        for modes in range(2, 9):
            photons = 4 if modes == 2 else modes
            events = selected_events(modes, photons)
            occupations = [occupation for _, _, occupation in events]
            self.assertEqual(len(occupations), modes * (modes - 1) // 2)
            self.assertEqual(len(set(occupations)), len(occupations))
            for charge, _, occupation in events:
                with self.subTest(
                    modes=modes, charge=charge, occupation=occupation
                ):
                    self.assertEqual(sum(occupation), photons)
                    self.assertEqual(modular_charge(occupation), charge)
                    self.assertNotEqual(charge, 0)

    def test_imaginary_probe_is_hermitian(self):
        for modes in range(2, 21):
            for row in range(modes):
                for column in range(modes):
                    value = imaginary_probe_entry(
                        modes, row, column
                    )
                    reverse = imaginary_probe_entry(
                        modes, column, row
                    )
                    self.assertEqual(value, (reverse[0], -reverse[1]))

    def test_fixed_probe_reference_factors(self):
        for modes in range(2, 9):
            photons = 4 if modes == 2 else modes
            for charge, _, occupation in selected_events(modes, photons):
                with self.subTest(
                    modes=modes, charge=charge, occupation=occupation
                ):
                    self.assertEqual(
                        probe_amplitude(
                            occupation, charge, imaginary=False
                        ),
                        (photons, 0),
                    )
                    antipodal = (
                        modes % 2 == 0 and charge == modes // 2
                    )
                    imaginary_factor = (
                        photons - 2 if antipodal else photons
                    )
                    self.assertEqual(
                        probe_amplitude(
                            occupation, charge, imaginary=True
                        ),
                        (0, imaginary_factor),
                    )

    def test_gradient_sign_and_normalization_against_cat_polynomial(self):
        cases = ((2, 4),) + tuple((modes, modes) for modes in range(3, 7))
        for modes, photons in cases:
            alpha = math.sqrt(photons) * modes ** ((1 - photons) / 2)
            basis = coordinates(modes)
            for charge, _, occupation in selected_events(modes, photons):
                gradient = amplitude_gradient(occupation, charge)
                for coordinate, gaussian in zip(basis, gradient):
                    with self.subTest(
                        modes=modes,
                        charge=charge,
                        occupation=occupation,
                        coordinate=coordinate,
                    ):
                        expected = 1j * alpha * complex(*gaussian)
                        actual = defining_polynomial_derivative(
                            occupation, coordinate
                        )
                        self.assertAlmostEqual(actual.real, expected.real, 10)
                        self.assertAlmostEqual(actual.imag, expected.imag, 10)

    def test_f4_amplitude_and_phase_spam_ranks(self):
        amplitude = f4_spam_matrix(include_phases=False)
        phase = f4_spam_matrix(include_amplitudes=False)
        combined = f4_spam_matrix()
        self.assertEqual(rational_rank(amplitude), 3)
        self.assertEqual(rational_rank(phase), 3)
        # The two three-dimensional images overlap in two directions.
        self.assertEqual(rational_rank(combined), 4)


if __name__ == "__main__":
    unittest.main()
