from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_bailey_product.py"


class DimensionSixBaileyProductTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.payload = json.loads(completed.stdout)

    def test_fixed_point_orientation_is_exact(self) -> None:
        identities = self.payload["fixed_point_identities"]
        self.assertEqual(
            identities["D_times_omega1_inverse_minus_one"],
            "-18",
        )
        self.assertEqual(identities["orientation_root"], "i^(19*N-s)=-1")

    def test_bailey_identity_holds_in_interior(self) -> None:
        self.assertLess(
            self.payload["numerical_interior_check"]["relative_error"],
            1e-12,
        )

    def test_boundary_gate_is_not_overclaimed(self) -> None:
        self.assertTrue(
            self.payload["conditional_Bailey_comparison_proved"]
        )
        self.assertFalse(
            self.payload["required_extra_dual_alias_weight_present"]
        )
        self.assertFalse(self.payload["modular_boundary_evaluation_proved"])


if __name__ == "__main__":
    unittest.main()
