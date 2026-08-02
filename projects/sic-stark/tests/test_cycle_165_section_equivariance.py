"""Regression coverage for the Cycle-165 section-equivariance falsifier."""
from __future__ import annotations

import json
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_165_section_equivariance import build_payload  # noqa: E402


class SectionEquivarianceTests(unittest.TestCase):
    def test_exhaustive_pointwise_class_falsifier(self) -> None:
        payload = build_payload()
        summary = payload["summary"]
        self.assertEqual(summary["rows_checked"], 36)
        self.assertEqual(summary["target_actions_checked"], 46656)
        self.assertEqual(summary["compatible_target_actions"], 0)
        self.assertFalse(summary["section_equivariant_descent_exists"])
        self.assertEqual(
            summary["first_fibre_instability_witness"],
            {
                "source_label": 0,
                "first_point": [0, 0],
                "first_successor_label": 0,
                "second_point": [0, 1],
                "second_successor_label": 3,
                "successor_labels": [0, 1, 2, 3, 4],
            },
        )
        self.assertEqual(
            payload["gate_outcome"]["pointwise_section_equivariant_operation"],
            "FALSIFIED_BY_FIBRE_INSTABILITY",
        )

    def test_discovery_payload_is_deterministic(self) -> None:
        recorded = json.loads(
            (ROOT / "discovery/cycle-165-section-equivariance-prototype-v1.json").read_text()
        )
        self.assertEqual(recorded, build_payload())

    def test_preregistration_has_one_freeze_manifest(self) -> None:
        preregistration = (
            ROOT / "docs/cycle-165-section-equivariance-preregistration-v1.md"
        ).read_text()
        self.assertEqual(preregistration.count("research-freeze-v1"), 1)


if __name__ == "__main__":
    unittest.main()
