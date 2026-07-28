from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_wrap_holonomy.py"


class DimensionSixWrapHolonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.payload = json.loads(completed.stdout)

    def test_primitive_quotient_is_antiperiodic(self) -> None:
        self.assertEqual(
            self.payload["primitive_quotient_wrap"],
            "R(a,b+6)=-R(a,b)",
        )
        self.assertEqual(
            self.payload["primal_helical_periodization_weight"],
            "(-1)^k",
        )

    def test_all_primitive_directions_transport(self) -> None:
        self.assertEqual(self.payload["primitive_direction_count"], 24)
        self.assertTrue(
            self.payload["all_primitive_directions_are_SL2_transports"]
        )

    def test_bailey_sign_gate_is_not_overclaimed(self) -> None:
        self.assertFalse(self.payload["Bailey_alias_sign_gate_closed"])
        self.assertIn("Z+1/2", self.payload["dual_effect"])


if __name__ == "__main__":
    unittest.main()
