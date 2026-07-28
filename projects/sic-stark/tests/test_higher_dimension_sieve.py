import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HigherDimensionSieveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts/screen_higher_dimension_theorem_coverage.py"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        cls.coverage = json.loads(process.stdout)
        cls.records = {
            record["dimension"]: record
            for record in cls.coverage["records"]
        }

    def test_closed_dimensions_and_next_targets(self) -> None:
        self.assertEqual(self.coverage["closed_dimensions"], [4, 5, 7])
        self.assertEqual(self.coverage["next_exact_tcc_target"], 8)
        self.assertEqual(
            self.coverage["next_analytic_theorem_target"], 6
        )
        self.assertEqual(
            self.records[7]["classification"], "proved-control"
        )

    def test_known_dimensions_calibrate_shintani_index(self) -> None:
        self.assertEqual(self.records[4]["shintani_index"], 2)
        self.assertEqual(self.records[5]["shintani_index"], 2)
        self.assertEqual(self.records[6]["shintani_index"], 6)

    def test_dimension_seven_order_and_field_tests(self) -> None:
        record = self.records[7]
        self.assertEqual(record["order_conductor"], 2)
        self.assertEqual(record["order_ray_order"], 12)
        self.assertEqual(record["maximal_one_ray_order"], 12)
        self.assertTrue(record["order_to_maximal_ray_isomorphism"])
        self.assertEqual(record["shintani_index"], 2)
        self.assertEqual(
            record["maximal_one_ray_structure"], [6, 2]
        )

    def test_dimension_eight_retains_quartic_obstruction(self) -> None:
        record = self.records[8]
        self.assertEqual(record["shintani_index"], 4)
        self.assertEqual(
            record["local_one_place_ray_kernel_exponent"], 4
        )
        self.assertEqual(
            record["classification"], "finite-closure-target"
        )

    def test_dimension_eight_tcc_selects_one_discrete_orientation(self) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts/analyze_dimension_eight_orientation_sieve.py"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("ORIENTATION_COUNT=64", process.stdout)
        self.assertIn("PASSING_ORIENTATION_COUNT=1", process.stdout)
        self.assertIn("RANK_1_ORIENTATION=0,0", process.stdout)

    def test_dimension_eight_primitive_overlap_field_collapse(self) -> None:
        process = subprocess.run(
            [
                "gp",
                "-q",
                str(
                    ROOT
                    / "scripts/dimension_eight_overlap_polynomial.gp"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("CANDIDATE_ABSOLUTE_IRREDUCIBLE=1", process.stdout)
        self.assertIn("CANDIDATE_ABSOLUTE_DEGREE=32", process.stdout)
        self.assertIn(
            "CANDIDATE_FIELD_MATCHES_RAY_24=1", process.stdout
        )

        isolation = subprocess.run(
            [
                "gp",
                "-q",
                str(
                    ROOT
                    / "scripts/dimension_eight_root_isolation.gp"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("TOTAL_REAL_ROOT_COUNT=16", isolation.stdout)
        self.assertIn(
            "ISOLATED_PRIMITIVE_ROOT_COUNT=16", isolation.stdout
        )

    def test_dimension_eight_artin_labels(self) -> None:
        process = subprocess.run(
            [
                "gp",
                "-q",
                str(
                    ROOT
                    / "scripts/dimension_eight_artin_labels.gp"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("user error", process.stderr)
        self.assertIn("RAY_GROUP=[4, 2, 2]", process.stdout)
        self.assertIn("PRIME_31_RAY_LOG=[1, 0, 0]", process.stdout)
        self.assertIn("PRIME_59_RAY_LOG=[0, 1, 0]", process.stdout)
        self.assertIn("PRIME_71_RAY_LOG=[0, 0, 1]", process.stdout)
        self.assertIn("MATCHED_ROOT_COUNT=16", process.stdout)
        self.assertIn(
            "ALL_DIMENSION_EIGHT_ARTIN_LABELS_CERTIFIED=1",
            process.stdout,
        )

    def test_dimension_eight_signed_field_and_exact_finite_tcc(self) -> None:
        lift = subprocess.run(
            [
                "gp",
                "-q",
                str(
                    ROOT
                    / "scripts/dimension_eight_square_root_lift.gp"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("user error", lift.stderr)
        self.assertIn(
            "SIGNED_OVERLAP_ABSOLUTE_DEGREE=64", lift.stdout
        )
        self.assertIn(
            "ALL_CONJUGATE_RATIO_ROOTS_VERIFIED=16", lift.stdout
        )
        self.assertIn(
            "LOWER_CONDUCTOR_FIELD_LIES_IN_SIGNED_FIELD=1",
            lift.stdout,
        )

        finite = subprocess.run(
            [
                "gp",
                "-q",
                str(ROOT / "scripts/dimension_eight_exact_tcc.gp"),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("user error", finite.stderr)
        self.assertIn("INSTALLED_OVERLAP_COUNT=64", finite.stdout)
        self.assertIn("COMMON_EXACT_FIELD_DEGREE=128", finite.stdout)
        self.assertIn("SHIFT_1_IDEMPOTENCY_CERTIFIED=1", finite.stdout)
        self.assertIn("SHIFT_1_RANK_ONE_CERTIFIED=1", finite.stdout)
        self.assertIn("SHIFT_0_IDEMPOTENCY_CERTIFIED=1", finite.stdout)
        self.assertIn("SHIFT_0_RANK_ONE_CERTIFIED=1", finite.stdout)
        self.assertIn(
            "DIMENSION_EIGHT_EXACT_FINITE_TCC_CERTIFIED=1",
            finite.stdout,
        )

    def test_dimension_eight_lower_stratum_is_shintani_index_two(self) -> None:
        process = subprocess.run(
            [
                "gp",
                "-q",
                str(
                    ROOT
                    / "scripts/dimension_eight_lower_shintani_audit.gp"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("user error", process.stderr)
        self.assertIn(
            "LOWER_POLYNOMIAL_MATCHES_RAY_12=1", process.stdout
        )
        self.assertIn("SHINTANI_INDEX=2", process.stdout)
        self.assertIn("SHINTANI_SAFE_EXPONENT=576", process.stdout)
        self.assertIn(
            "LOWER_DIMENSION_EIGHT_SHINTANI_"
            "ALGEBRAICITY_CERTIFIED=1",
            process.stdout,
        )

    def test_dedicated_dimension_seven_certificate(self) -> None:
        process = subprocess.run(
            [
                "gp",
                "-q",
                str(ROOT / "scripts/dimension_seven_candidate_audit.gp"),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("user error", process.stderr)
        self.assertIn("ORDER_TO_MAXIMAL_RAY_14_ISOMORPHISM=1", process.stdout)
        self.assertIn("RAY_14_SHINTANI_INDEX=2", process.stdout)
        self.assertIn("RAY_7_SHINTANI_INDEX=2", process.stdout)
        self.assertIn("CONDUCTOR_LIFT_COUNT=96", process.stdout)
        self.assertIn(
            "ALL_NONQUADRATIC_LOWERED_FIELDS_PASS_"
            "SHINTANI_INDEX_TWO=1",
            process.stdout,
        )
        self.assertIn(
            "DIMENSION_SEVEN_NEXT_UNCONDITIONAL_CANDIDATE=1",
            process.stdout,
        )

    def test_dimension_seven_direct_ghost_is_numerically_rank_one(self) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/explore_dimension_seven.py"),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        residuals = {}
        for line in process.stdout.splitlines():
            if " residual = " not in line:
                continue
            label, value = line.split(" = ", 1)
            residuals[label] = float(value)
        self.assertLess(residuals["trace residual"], 1e-12)
        self.assertLess(residuals["maximum idempotency residual"], 1e-8)
        self.assertLess(residuals["maximum 2-minor residual"], 1e-8)

    def test_dimension_seven_conductor_lowering_bridge(self) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts/verify_dimension_seven_conductor_lowering.py"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn(
            "nonzero characteristics checked = 48", process.stdout
        )
        residual_line = next(
            line
            for line in process.stdout.splitlines()
            if line.startswith("maximum log-square residual = ")
        )
        residual = float(residual_line.split(" = ", 1)[1])
        self.assertLess(residual, 1e-7)


if __name__ == "__main__":
    unittest.main()
