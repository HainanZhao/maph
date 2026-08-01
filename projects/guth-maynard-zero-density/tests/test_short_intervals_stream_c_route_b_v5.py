"""Regression checks for the independent Stream-C Route-B v5 narrow pass."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_short_intervals_stream_c_route_b_v5.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-route-b-v5.json"


class StreamCRouteBV5Tests(unittest.TestCase):
    def execute(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *args], check=True, capture_output=True, text=True)

    def test_certificate_replays_and_has_no_timing(self) -> None:
        self.execute("--check")
        data = json.loads(ARTIFACT.read_text())
        self.assertNotIn("wall_time_ns", json.dumps(data))
        self.assertIn("--write-performance", data["replay"]["timing_policy"])

    def test_official_v4_source_chain_replaces_v2_premise(self) -> None:
        data = json.loads(self.execute().stdout)
        source = data["official_formula_source_chain"]
        self.assertEqual(source["source_closure"], "v4, not v2")
        self.assertIn("CC BY-NC-SA 3.0", source["provenance_correction"])
        self.assertIn("official_sword_zip", data["frozen_dependencies"])
        self.assertIn("source_closure_v4", data["frozen_dependencies"])

    def test_narrow_route_boundary_and_exact_thresholds(self) -> None:
        data = json.loads(self.execute().stdout)
        values = data["exact_transfer_invariants"]
        self.assertEqual((values["b"], values["uniform_theta"], values["almost_all_theta"]), ("30/13", "17/30", "2/15"))
        conclusion = data["route_conclusion"]
        self.assertIn("narrow", conclusion["status"])
        self.assertIn("no G0 PASS", conclusion["not_promoted"])
        self.assertNotIn("route_a", SCRIPT.read_text().lower())


if __name__ == "__main__":
    unittest.main()
