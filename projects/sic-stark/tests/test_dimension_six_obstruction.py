import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixObstructionTests(unittest.TestCase):
    def test_exact_ray_group_and_character_obstruction(self) -> None:
        result = subprocess.run(
            [
                "gp",
                "-q",
                str(
                    ROOT
                    / "scripts/dimension_six_conductor_obstruction.gp"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("BNF_CERTIFIED=1", result.stdout)
        self.assertIn(
            "ONE_PLACE_RAY_STRUCTURES="
            "mod1:trivial,mod2:trivial,mod3:C2,mod6:C6",
            result.stdout,
        )
        self.assertIn("REDUCTION_KERNEL=C3=<g^2>", result.stdout)
        self.assertIn(
            "DESCENDING_CHARACTERS_AMONG_ODD_INDICES=[chi_3]",
            result.stdout,
        )
        self.assertIn(
            "PRIMITIVE_CHARACTERS_KILLED_BY_CONDUCTOR_LOWERING="
            "[chi_1,chi_5]",
            result.stdout,
        )

    def test_duplication_relation_does_not_select_a_lift(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/dimension_six_lift_relation.py"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        certificate = json.loads(result.stdout)
        self.assertEqual(certificate["distribution_matrix_rank"], 1)
        self.assertEqual(
            certificate["augmented_with_selected_coordinate_rank"], 2
        )
        self.assertEqual(certificate["nullspace_dimension"], 3)
        self.assertFalse(certificate["selected_lift_determined"])
        self.assertEqual(len(certificate["lift_orbits"]), 4)

    def test_no_imaginary_quadratic_induction_shortcut(self) -> None:
        result = subprocess.run(
            [
                "gp",
                "-q",
                str(
                    ROOT
                    / "scripts/dimension_six_quadratic_induction_audit.gp"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("user error", result.stderr)
        self.assertIn("NORMAL_CLOSURE_GROUP_ID=[24, 8]", result.stdout)
        self.assertIn("FAITHFUL_QUOTIENT_GROUP_ID=[12, 4]", result.stdout)
        self.assertIn(
            "QUADRATIC_BASE_DISCRIMINANTS=[21,-3,-7]",
            result.stdout,
        )
        self.assertIn(
            "UNIQUE_ABELIAN_QUADRATIC_BASE_DISCRIMINANT=21",
            result.stdout,
        )
        self.assertIn(
            "IMAGINARY_QUADRATIC_ELLIPTIC_UNIT_TRANSFER_AVAILABLE=0",
            result.stdout,
        )

    def test_rational_induction_cannot_see_orientation(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts/dimension_six_rational_induction_gate.py"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn(
            "PRIMITIVE_EVEN_PACKET_IN_RATIONAL_SPAN=1",
            result.stdout,
        )
        self.assertIn(
            "PRIMITIVE_ODD_PACKET_IN_RATIONAL_SPAN=0",
            result.stdout,
        )
        self.assertIn(
            "RATIONAL_ARTIN_INDUCTION_CAN_ORIENT_CHI_1=0",
            result.stdout,
        )

    def test_exact_weight_one_modular_identification(self) -> None:
        result = subprocess.run(
            [
                "gp",
                "-q",
                str(
                    ROOT
                    / "scripts/dimension_six_weight_one_modularity.gp"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("user error", result.stderr)
        self.assertIn("ABSOLUTE_ARTIN_CONDUCTOR=756", result.stdout)
        self.assertIn("STURM_BOUND=144", result.stdout)
        self.assertIn("MATCHING_WEIGHT_ONE_NEWFORMS=1", result.stdout)
        self.assertIn("MATCHING_NEBENTYPUS=-7", result.stdout)
        self.assertIn(
            "MATCHING_PROJECTIVE_GALOIS_TYPE=12",
            result.stdout,
        )

    def test_qgamma_regularizes_the_full_rational_boundary(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts/dimension_six_qgamma_boundary.py"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("RADEMACHER_INVARIANT=6", result.stdout)
        self.assertIn(
            "ALL_SINGULAR_QGAMMA_PARAMETERS_MATCH=1",
            result.stdout,
        )
        self.assertIn(
            "ALL_NONZERO_BOUNDARY_ORDERS_ZERO=1",
            result.stdout,
        )
        self.assertIn(
            "QGAMMA_PATTERN_ZAUNER_COVARIANT=1",
            result.stdout,
        )
        self.assertIn(
            "DIRECT_PRODUCT_ERRORS_DECREASE=1",
            result.stdout,
        )
        self.assertIn(
            "RADIAL_HALF_POWER_CORRECTION_VERIFIED=1",
            result.stdout,
        )
        self.assertIn(
            "BOUNDARY_IDEMPOTENCY_RESIDUALS_DECREASE=1",
            result.stdout,
        )
        self.assertIn(
            "BOUNDARY_MINOR_RESIDUALS_DECREASE=1",
            result.stdout,
        )
        self.assertIn(
            "REGULARIZED_BOUNDARY_APPROACHES_ALGEBRAIC_PACKET=1",
            result.stdout,
        )
        self.assertIn("FINITE_LEVEL_TCC_IDENTITY_PROVED=0", result.stdout)

    def test_signed_defect_has_quadratic_geodesic_scale(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/dimension_six_defect_limit.py"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn(
            "EVEN_DIMENSION_WRAP_SIGN_VERIFIED=1",
            result.stdout,
        )
        self.assertIn(
            "NONZERO_DEFECT_REPRESENTATIVE_COUNT=13",
            result.stdout,
        )
        self.assertIn(
            "NUMERICAL_DEFECT_SCALE=O(1/denominator^2)",
            result.stdout,
        )
        self.assertIn(
            "CONVERGENT_NORM_IDENTITY=-21",
            result.stdout,
        )
        self.assertIn(
            "CONVERGENT_FIRST_DERIVATIVE_PACKET=1",
            result.stdout,
        )
        self.assertIn(
            "ASYMPTOTIC_DEFECT_BOUND_PROVED=0",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
