from fractions import Fraction as Q
import unittest

from conventions.fibre_line_rigidity_v1 import certify_common_intercept_fibre, verify_all


PACKET_STATE = {
    "labels": {"left": 1, "right": 2},
    "slope_determinant": 2,
    "product_shell": "stable",
    "individual_residuals_retained": True,
}


class Cycle182FibreLineRigidityTest(unittest.TestCase):
    def test_replay(self) -> None:
        self.assertIn("one reduced rational slope", verify_all()["slope_rigidity"])

    def test_nonzero_beta_primitive_line(self) -> None:
        row = certify_common_intercept_fibre(
            [(22, 5), (26, 6), (30, 7)],
            label=2, alpha=Q(1, 4), beta=Q(1, 2), rho=Q(-1, 2),
            x=100000, height=20, strip_constant=1, packet_state=PACKET_STATE,
        )
        self.assertEqual(row["primitive_slope"]["value"], Q(1, 4))
        self.assertEqual(row["common_intercept"]["denominator"], 2)
        self.assertEqual(row["base_height_residue_modulo_slope_denominator"], 2)
        self.assertEqual(row["fibre_count"], 3)

    def test_missing_lattice_row_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing lattice point"):
            certify_common_intercept_fibre(
                [(22, 5), (30, 7)],
                label=2, alpha=Q(1, 4), beta=Q(1, 2), rho=Q(-1, 2),
                x=100000, height=20, strip_constant=1, packet_state=PACKET_STATE,
            )

    def test_slope_cutoff_is_enforced(self) -> None:
        with self.assertRaisesRegex(ValueError, "slope rigidity cutoff"):
            certify_common_intercept_fibre(
                [(22, 5), (26, 6)],
                label=2, alpha=Q(1, 4), beta=Q(1, 2), rho=Q(-1, 2),
                x=1000, height=20, strip_constant=1, packet_state=PACKET_STATE,
            )


if __name__ == "__main__":
    unittest.main()
