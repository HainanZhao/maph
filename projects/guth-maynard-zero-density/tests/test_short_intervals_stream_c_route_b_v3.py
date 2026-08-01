"""Regression tests for the v3 Route-B correction and containment record."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_short_intervals_stream_c_route_b_v3.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-route-b-v3.json"
LEDGER = PROJECT / "artifacts" / "cycle-2-stream-c-source-ledger-v3.json"


class StreamCRouteBV3Tests(unittest.TestCase):
    def replay(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *arguments], check=True, capture_output=True, text=True)

    def test_artifact_replays_byte_for_byte(self) -> None:
        self.replay("--check", str(ARTIFACT))

    def test_huxley_citation_is_corrected_without_changing_math(self) -> None:
        data = json.loads(self.replay().stdout)
        correction = data["correction_1_huxley_bibliography"]
        self.assertEqual(correction["status"], "PROVED")
        self.assertIn("On the difference between consecutive primes", correction["correct_citation"])
        huxley = data["unchanged_huxley_math"]
        self.assertEqual(huxley["near_one_coefficient"]["h(4/5)"], "15/7")
        self.assertEqual(huxley["near_one_coefficient"]["b_minus_h(4/5)"], "15/91")
        self.assertIn("(log T)^44", huxley["statement"])

    def test_external_formula_blocks_route_and_g0_promotion(self) -> None:
        data = json.loads(self.replay().stdout)
        formula = data["correction_2_explicit_formula_status"]
        self.assertEqual(formula["external_dependency_status"], "OBSERVED")
        self.assertIn("No full Stream-C", formula["consequence"])
        self.assertEqual(data["epistemic_status"], "OBSERVED")

    def test_ledger_records_both_corrections_and_exact_statuses(self) -> None:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(ledger["epistemic_status"], "OBSERVED")
        self.assertEqual(len(ledger["corrections"]), 2)
        self.assertIn("On the difference", ledger["corrections"][0]["correct_identity"])
        statuses = ledger["status_by_node"]
        self.assertEqual(statuses["external_truncated_explicit_formula"], "OBSERVED")
        self.assertEqual(statuses["full_stream_c_route_b"], "OBSERVED")
        self.assertEqual(statuses["g0"], "OBSERVED")


if __name__ == "__main__":
    unittest.main()
