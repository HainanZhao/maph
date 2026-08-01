"""Regression tests for the conditional Cycle-2 Stream-C Route-B audit."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_short_intervals_stream_c_route_b_v1.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-route-b-v1.json"


class StreamCRouteBTests(unittest.TestCase):
    def replay(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *arguments], check=True, capture_output=True, text=True)

    def test_artifact_replays_byte_for_byte(self) -> None:
        self.replay("--check", str(ARTIFACT))

    def test_all_frozen_boundaries_and_epsilon_range_are_labeled(self) -> None:
        data = json.loads(self.replay().stdout)
        frozen = data["frozen_parameters"]
        self.assertEqual(frozen["b"], "30/13")
        self.assertEqual(frozen["uniform_theta"], "17/30")
        self.assertEqual(frozen["almost_all_theta"], "2/15")
        self.assertEqual(frozen["nonvacuous_epsilon_range"], "0 < epsilon < 127/300")

    def test_uniform_and_almost_all_include_all_secondary_transfers(self) -> None:
        data = json.loads(self.replay().stdout)
        uniform = data["uniform_replay"]
        self.assertIn("T=x/y", uniform["truncation"])
        self.assertIn("-epsilon/2", uniform["epsilon_absorption"]["power_after_subpower"])
        self.assertIn("2/7", uniform["zero_free_cutoff"]["supremum_decay"])
        almost = data["almost_all_replay"]
        self.assertIn("-epsilon/3", almost["epsilon_absorption"]["power_after_subpower"])
        self.assertIn("Chebyshev", almost["splitting_and_exceptional_conversion"]["chebyshev_threshold"])
        self.assertIn("O(X*E(X)^-1)", almost["splitting_and_exceptional_conversion"]["exceptional_measure"])

    def test_unread_external_nodes_remain_explicit_blockers(self) -> None:
        data = json.loads(self.replay().stdout)
        inputs = data["external_inputs_and_status"]
        self.assertEqual(inputs["near_one_density"]["status"], "OBSERVED")
        self.assertIn("blocker", inputs["near_one_density"])
        self.assertEqual(inputs["almost_all_local_zero_count"]["status"], "OBSERVED")
        self.assertIn("blocker", inputs["almost_all_local_zero_count"])
        self.assertEqual(data["epistemic_status"], "OBSERVED")

    def test_zero_free_input_has_a_scoped_not_global_claim(self) -> None:
        data = json.loads(self.replay().stdout)
        zero_free = data["external_inputs_and_status"]["vinogradov_korobov_zero_free"]
        self.assertEqual(zero_free["status"], "PROVED")
        self.assertIn("low-height", zero_free["scope_limit"])


if __name__ == "__main__":
    unittest.main()
