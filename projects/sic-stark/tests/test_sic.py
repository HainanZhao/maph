import math
import unittest

from src.sic import (
    dimension_four_fiducial,
    displacement_overlap,
    frame_operator,
    hesse_fiducial,
    max_frame_residual,
    max_sic_residual,
    max_twisted_idempotency_residual,
    normalize,
    projector_displacement_coefficients,
    qubit_tetrahedral_fiducial,
    sic_residuals,
    twisted_idempotency_residuals,
)


class SicDiagnosticsTests(unittest.TestCase):
    def test_normalize_rejects_empty_and_zero_vectors(self) -> None:
        with self.assertRaises(ValueError):
            normalize(())
        with self.assertRaises(ValueError):
            normalize((0, 0))

    def test_qubit_tetrahedral_fiducial(self) -> None:
        fiducial = qubit_tetrahedral_fiducial()
        self.assertLess(max_sic_residual(fiducial), 1e-14)
        self.assertLess(max_frame_residual(fiducial), 1e-14)
        self.assertEqual(len(sic_residuals(fiducial)), 3)

    def test_hesse_fiducial(self) -> None:
        fiducial = hesse_fiducial()
        self.assertLess(max_sic_residual(fiducial), 1e-14)
        self.assertLess(max_frame_residual(fiducial), 1e-14)
        self.assertEqual(len(sic_residuals(fiducial)), 8)

    def test_dimension_four_fiducial(self) -> None:
        fiducial = dimension_four_fiducial()
        self.assertLess(max_sic_residual(fiducial), 1e-14)
        self.assertLess(max_frame_residual(fiducial), 1e-14)
        self.assertEqual(len(sic_residuals(fiducial)), 15)

    def test_identity_displacement_overlap_is_one(self) -> None:
        overlap = displacement_overlap(hesse_fiducial(), 0, 0)
        self.assertAlmostEqual(overlap.real, 1.0)
        self.assertAlmostEqual(overlap.imag, 0.0)

    def test_generic_vector_is_not_a_sic(self) -> None:
        self.assertGreater(max_sic_residual((1, 0, 0)), 0.5)

    def test_frame_operator_is_d_times_identity(self) -> None:
        operator = frame_operator(normalize((1, 2j, -3, 4 - 1j)))
        dimension = len(operator)
        for row in range(dimension):
            for column in range(dimension):
                expected = dimension if row == column else 0.0
                self.assertTrue(
                    math.isclose(
                        abs(operator[row][column] - expected),
                        0.0,
                        abs_tol=1e-13,
                    )
                )

    def test_twisted_convolution_encodes_projector_idempotency(self) -> None:
        for fiducial in (
            qubit_tetrahedral_fiducial(),
            hesse_fiducial(),
            dimension_four_fiducial(),
            normalize((1, 2j, -3, 4 - 1j)),
        ):
            dimension = len(fiducial)
            coefficients = projector_displacement_coefficients(fiducial)
            self.assertLess(
                max_twisted_idempotency_residual(
                    coefficients, dimension
                ),
                1e-12,
            )

    def test_twisted_convolution_rejects_nonprojector_coefficients(self) -> None:
        coefficients = {
            (p, q): complex(p + 2 * q)
            for p in range(3)
            for q in range(3)
        }
        residuals = twisted_idempotency_residuals(coefficients, 3)
        self.assertGreater(max(abs(value) for value in residuals.values()), 1)

    def test_twisted_convolution_requires_complete_grid(self) -> None:
        with self.assertRaises(ValueError):
            twisted_idempotency_residuals({(0, 0): 1}, 2)


if __name__ == "__main__":
    unittest.main()
