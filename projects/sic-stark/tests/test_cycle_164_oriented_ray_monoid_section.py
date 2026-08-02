"""Regression coverage for the Cycle-164 exact ray-monoid section."""
from __future__ import annotations

import json
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_164_oriented_ray_monoid_section import build_payload  # noqa: E402


class OrientedRayMonoidSectionTests(unittest.TestCase):
    def test_total_section_full_recovery_and_anchors(self) -> None:
        payload = build_payload()
        self.assertEqual(payload["source"], {"ray_cyc": [6], "generator_log": [1]})
        summary = payload["summary"]
        self.assertEqual(summary["rows_checked"], 36)
        self.assertEqual(summary["full_modulus_rows"], 18)
        self.assertEqual(summary["lowered_modulus_rows"], 18)
        self.assertTrue(summary["all_rows_in_projected_source_image"])
        self.assertTrue(summary["full_modulus_recovery"])
        self.assertEqual(summary["orientation_anchors"], {"3,5": 1, "3,4": 2})

    def test_discovery_payload_is_the_deterministic_prototype(self) -> None:
        expected = build_payload()
        recorded = json.loads(
            (ROOT / "discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json").read_text()
        )
        self.assertEqual(recorded, expected)

    def test_preregistration_has_one_freeze_manifest(self) -> None:
        preregistration = (
            ROOT / "docs/cycle-164-oriented-ray-monoid-preregistration-v1.md"
        ).read_text()
        self.assertEqual(preregistration.count("research-freeze-v1"), 1)


if __name__ == "__main__":
    unittest.main()
