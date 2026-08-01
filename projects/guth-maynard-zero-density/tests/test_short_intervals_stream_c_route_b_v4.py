"""Regression tests for the v4 Stream-C Route-B closure."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_short_intervals_stream_c_route_b_v4.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-route-b-v4.json"


class StreamCRouteBV4Tests(unittest.TestCase):
    def replay(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *arguments], check=True, capture_output=True, text=True)

    def test_artifact_replays_byte_for_byte(self) -> None:
        self.replay("--check", str(ARTIFACT))

    def test_formula_node_and_convention_bridge_are_closed(self) -> None:
        data = json.loads(self.replay().stdout)
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertEqual(data["external_truncated_explicit_formula"]["status"], "PROVED")
        self.assertEqual(data["convention_bridge"]["status"], "PROVED")
        self.assertIn("multiplicity", data["convention_bridge"]["multiplicity"])

    def test_exact_short_interval_exponents_are_preserved(self) -> None:
        data = json.loads(self.replay().stdout)
        values = data["exact_transfer_invariants"]
        self.assertEqual(values["b"], "30/13")
        self.assertEqual(values["uniform_theta"], "17/30")
        self.assertEqual(values["almost_all_theta"], "2/15")


if __name__ == "__main__":
    unittest.main()
