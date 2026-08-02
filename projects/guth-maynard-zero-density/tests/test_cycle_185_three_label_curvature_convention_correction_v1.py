from fractions import Fraction as Q
import unittest

from conventions.three_label_curvature_convention_correction_v1 import (
    original_unshifted_identity_failure,
    shifted_curvature_identity,
    verify_all,
)


class Cycle185ThreeLabelCurvatureConventionCorrectionTest(unittest.TestCase):
    def test_pinned_shift_invalidates_original_identity(self) -> None:
        record = original_unshifted_identity_failure(z=Q(2))
        self.assertEqual(record["unshifted_difference"], -2)

    def test_shifted_numerator_restores_exact_product_and_syzygy(self) -> None:
        record = shifted_curvature_identity(
            v=3, u_minus=2, u_zero=5, u_plus=7,
            A_minus=6, A_zero=45, A_plus=147,
            z_minus=Q(2), z_zero=Q(4), z_plus=Q(8),
        )
        self.assertEqual(record["K_plus"], 0)
        self.assertEqual(record["K_plus_prime"], 0)
        self.assertEqual(record["B"]["zero"], 60)

    def test_shifted_expansion_accepts_nonzero_errors(self) -> None:
        record = shifted_curvature_identity(
            v=2, u_minus=1, u_zero=3, u_plus=5,
            A_minus=-1, A_zero=1, A_plus=11,
            z_minus=Q(1, 2), z_zero=Q(1), z_plus=Q(2),
        )
        self.assertEqual(record["expanded_value"], Q(record["K_plus"], 2 * 1 * 2 * 5 * (2 * 3) ** 2))

    def test_replay_names_withheld_claim(self) -> None:
        record = verify_all()
        self.assertIn("WITHHELD", record["original_claim_disposition"])


if __name__ == "__main__":
    unittest.main()
