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

    def test_dimension_seven_is_unique_best_candidate(self) -> None:
        self.assertEqual(
            self.coverage["best_unconditional_candidate"], 7
        )
        best = [
            dimension
            for dimension, record in self.records.items()
            if dimension >= 7
            and record["classification"] == "best-candidate"
        ]
        self.assertEqual(best, [7])

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
        self.assertNotEqual(record["classification"], "best-candidate")

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
