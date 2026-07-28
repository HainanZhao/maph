from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/dimension_six_checkpoint_gates.py"


class DimensionSixCheckpointGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        cls.data = json.loads(completed.stdout)

    def test_no_finite_pinch_but_endpoint_decay_fails(self) -> None:
        gate = self.data["pinch_gate"]
        self.assertFalse(gate["finite_pinch_at_g_equals_Q"])
        self.assertEqual(
            gate["verdict"],
            "UNPINCHED_BUT_NOT_ABSOLUTELY_CONVERGENT",
        )

    def test_d4_prediction_is_minus_q(self) -> None:
        gate = self.data["dimension_four_even_wrap_gate"]
        self.assertEqual(gate["bilateral_argument"], "-q")
        self.assertTrue(gate["prediction_confirmed"])

    def test_d5_level_bit_is_read(self) -> None:
        gate = self.data["dimension_five_level_bit_gate"]
        self.assertEqual(gate["bilateral_argument"], "+q")
        self.assertEqual(gate["fusion_sign_bit"], 0)

    def test_residue_gate_is_a_zero_mode_calibration(self) -> None:
        gate = self.data["residue_vs_rm_aux_gate"]
        self.assertEqual(
            gate["comparison_status"],
            "VERIFIED_CALIBRATION",
        )
        self.assertEqual(gate["inverse_helical_trace"], "-4*sqrt(7)")
        self.assertIn("normalization calibration", gate["logical_role"])
        self.assertEqual(self.data["silent_gate_count"], 0)


if __name__ == "__main__":
    unittest.main()
