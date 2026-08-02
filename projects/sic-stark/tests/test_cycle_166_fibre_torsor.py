"""Regression coverage for the Cycle-166 fibre-resolved torsor."""
from __future__ import annotations

import json
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_166_fibre_torsor import build_payload  # noqa: E402


class FibreTorsorTests(unittest.TestCase):
    def test_exact_transport_and_anchor_invariants(self) -> None:
        payload = build_payload()
        summary = payload["summary"]
        self.assertEqual(summary["base_rows_checked"], 36)
        self.assertEqual(summary["torsor_states_checked"], 216)
        self.assertEqual(summary["orbit_count"], 14)
        self.assertTrue(summary["phase_differences_all_divisible_by_8"])
        self.assertTrue(summary["all_multiplier_square_identities_match"])
        self.assertTrue(summary["all_t_orbit_holonomies_zero"])
        self.assertTrue(summary["lifted_third_return_identity"])
        self.assertTrue(summary["graph_intertwining"])
        self.assertEqual(summary["orientation_anchors"], {"3,5": 1, "3,4": 2})

    def test_discovery_payload_is_deterministic(self) -> None:
        recorded = json.loads(
            (ROOT / "discovery/cycle-166-fibre-torsor-prototype-v1.json").read_text()
        )
        self.assertEqual(recorded, build_payload())

    def test_preregistration_has_one_freeze_manifest(self) -> None:
        preregistration = (ROOT / "docs/cycle-166-fibre-torsor-preregistration-v1.md").read_text()
        self.assertEqual(preregistration.count("research-freeze-v1"), 1)


if __name__ == "__main__":
    unittest.main()
