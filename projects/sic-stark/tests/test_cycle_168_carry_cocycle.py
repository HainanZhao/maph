from __future__ import annotations

import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_168_carry_cocycle import build_payload  # noqa: E402


class CarryCocycleTests(unittest.TestCase):
    def test_exact_falsifier(self) -> None:
        summary = build_payload()["summary"]
        self.assertEqual(summary["cocycle_candidates_checked"], 46656)
        self.assertEqual(summary["probe_survivor_count"], 1)
        self.assertEqual(summary["graph_passing_parameter_count"], 0)
        self.assertEqual(summary["transport_passing_parameter_count"], 0)
        self.assertFalse(summary["carry_cocycle_completion_exists"])

    def test_recorded_payload_is_deterministic(self) -> None:
        recorded = json.loads((ROOT / "discovery/cycle-168-carry-cocycle-prototype-v1.json").read_text())
        self.assertEqual(recorded, build_payload())
