import unittest
from fractions import Fraction

from conventions.selection_mask_negative_spectral_v1 import (
    negative_energy_localization,
    spectral_ledger,
    theorem_record,
)


class SelectionMaskNegativeSpectralTests(unittest.TestCase):
    def test_negative_correlation_is_carried_by_negative_spectrum(self) -> None:
        row = spectral_ledger(
            eigenvalues=(Fraction(3), Fraction(-2)),
            coefficient_projection_squares=(Fraction(1, 2), Fraction(1)),
            external_weight=Fraction(1),
        )
        self.assertEqual(row["real_hermitian_correlation"], Fraction(-1, 2))
        self.assertEqual(row["negative_spectral_energy"], Fraction(2))
        aggregate = negative_energy_localization((row,), Fraction(1, 2))
        self.assertEqual(aggregate["negative_spectral_energy"], Fraction(2))

    def test_requires_nonnegative_external_weight(self) -> None:
        with self.assertRaises(ValueError):
            spectral_ledger(
                eigenvalues=(Fraction(-1),),
                coefficient_projection_squares=(Fraction(1),),
                external_weight=Fraction(-1),
            )

    def test_boundary(self) -> None:
        self.assertIn("does not", theorem_record()["boundary"])


if __name__ == "__main__":
    unittest.main()
