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


if __name__ == "__main__":
    unittest.main()
