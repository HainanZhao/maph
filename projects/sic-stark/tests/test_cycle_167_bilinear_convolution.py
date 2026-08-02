"""Regression coverage for the Cycle-167 bilinear convolution census."""
from __future__ import annotations

import json
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_167_bilinear_convolution import build_payload  # noqa: E402


class BilinearConvolutionTests(unittest.TestCase):
    def test_complete_falsifier(self) -> None:
        summary = build_payload()["summary"]
        self.assertEqual(summary["matrices_checked"], 1296)
        self.assertEqual(summary["basis_pairs_per_matrix"], 1296)
        self.assertEqual(summary["graph_identity_checks"], 1679616)
        self.assertEqual(summary["transport_identity_checks"], 1679616)
        self.assertEqual(summary["graph_passing_matrix_count"], 0)
        self.assertEqual(summary["transport_passing_matrix_count"], 0)
        self.assertEqual(summary["compatible_matrix_count"], 0)
        self.assertFalse(summary["bilinear_convolution_exists"])

    def test_recorded_payload_is_deterministic(self) -> None:
        recorded = json.loads((ROOT / "discovery/cycle-167-bilinear-convolution-prototype-v1.json").read_text())
        self.assertEqual(recorded, build_payload())


if __name__ == "__main__":
    unittest.main()
