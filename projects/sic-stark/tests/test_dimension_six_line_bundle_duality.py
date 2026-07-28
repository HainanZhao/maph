from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_line_bundle_duality.py"


class DimensionSixLineBundleDualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.payload = json.loads(completed.stdout)

    def test_tau_character_has_negative_holonomy(self) -> None:
        self.assertEqual(
            self.payload["tau6_character"]["value_on_T"],
            "-1",
        )

    def test_dual_lattice_is_half_shifted(self) -> None:
        self.assertIn("Z+1/2", self.payload["dual_descent_condition"])
        self.assertEqual(
            self.payload["dual_alias_coefficients"],
            "unweighted",
        )

    def test_wrap_is_not_misused_as_alias_sign(self) -> None:
        self.assertTrue(
            self.payload["wrap_sign_is_not_dual_alias_sign"]
        )


if __name__ == "__main__":
    unittest.main()
