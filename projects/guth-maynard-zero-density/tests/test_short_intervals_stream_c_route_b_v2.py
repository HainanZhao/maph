"""Regression tests for the versioned Stream-C Route-B v2 closure."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_short_intervals_stream_c_route_b_v2.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-route-b-v2.json"
LEDGER = PROJECT / "artifacts" / "cycle-2-stream-c-source-ledger-v2.json"


class StreamCRouteBV2Tests(unittest.TestCase):
    def replay(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *arguments], check=True, capture_output=True, text=True)

    def test_artifact_replays_byte_for_byte(self) -> None:
        self.replay("--check", str(ARTIFACT))

    def test_huxley_correction_has_exact_coefficient_and_retains_log_factor(self) -> None:
        data = json.loads(self.replay().stdout)
        huxley = data["external_inputs"]["density_near_one_huxley"]
        self.assertEqual(huxley["status"], "PROVED")
        self.assertEqual(huxley["exact_coefficient_check"]["h(4/5)"], "15/7")
        self.assertEqual(huxley["exact_coefficient_check"]["b_minus_h_at_4/5"], "15/91")
        self.assertIn("(log T)^44", huxley["input"])
        self.assertIn("log^44", huxley["conclusion"])

    def test_local_pair_input_is_multiplicity_inclusive_and_pinned(self) -> None:
        data = json.loads(self.replay().stdout)
        local = data["external_inputs"]["local_zero_count_and_pair_sum"]
        self.assertEqual(local["status"], "PROVED")
        self.assertIn("multiplicity", local["multiplicity"])
        self.assertIn("O((log(T+2))^2)", local["derivation"])
        self.assertIn("sqrt", local["denominator_check"])

    def test_low_height_completion_and_narrow_boundary_are_explicit(self) -> None:
        data = json.loads(self.replay().stdout)
        cutoff = data["external_inputs"]["zero_free_cutoff"]
        self.assertEqual(cutoff["status"], "PROVED")
        self.assertIn("3,000,175,332,800", cutoff["low_height"])
        self.assertEqual(data["narrow_pass"]["status"], "PROVED")
        self.assertIn("not an independent proof", data["claim_boundary"])

    def test_source_ledger_is_a_versioned_correction(self) -> None:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(ledger["epistemic_status"], "PROVED")
        self.assertIn("v1", ledger["supersedes"])
        self.assertIn("Huxley", ledger["correction"]["corrected_v1_statement"])
        self.assertIn("multiplicity", ledger["closed_dependency_nodes"][-1])


if __name__ == "__main__":
    unittest.main()
