from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_slater_reduction.py"


class DimensionSixSlaterReductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.payload = json.loads(completed.stdout)

    def test_slater_cores_lose_characteristic_parameter(self) -> None:
        self.assertTrue(
            self.payload["unilateral_cores_are_independent_of_x"]
        )
        self.assertEqual(
            len(self.payload["Slater_unilateral_cores"]),
            2,
        )

    def test_q_kummer_parameter_relation_holds(self) -> None:
        self.assertTrue(
            self.payload["Bailey_Daum_parameter_relation_holds"]
        )

    def test_last_sign_gap_is_explicit(self) -> None:
        self.assertEqual(self.payload["actual_argument"], "-q")
        self.assertEqual(
            self.payload["Bailey_Daum_closed_argument"],
            "+q",
        )
        self.assertTrue(self.payload["remaining_sign_gap"])


if __name__ == "__main__":
    unittest.main()
