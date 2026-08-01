"""Independent regression tests for the Stream-B Route-B application audit."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_cycle2_stream_b_route_b.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-b-route-b-v1.json"


class StreamBRouteBTests(unittest.TestCase):
    def replay(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *args], check=True, capture_output=True, text=True)

    def test_certificate_is_byte_stable(self) -> None:
        self.replay("--check", str(ARTIFACT))

    def test_all_preregistered_nodes_are_labeled(self) -> None:
        data = json.loads(self.replay().stdout)
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertEqual(data["label_coverage"]["required_nodes"], 10)
        self.assertEqual(data["label_coverage"]["labeled_rows"], 10)
        self.assertEqual(data["label_coverage"]["unlabeled_nodes"], [])
        self.assertTrue(all(row["status"] == "PROVED" for row in data["rows"]))

    def test_complement_and_multiplicity_conventions_are_explicit(self) -> None:
        data = json.loads(self.replay().stdout)
        rows = {row["id"]: row for row in data["rows"]}
        self.assertIn("not MP Type I", rows["SB-B1-complement-to-mp-type-ii"]["transfer"])
        conversion = rows["SB-B2-multiplicity-and-two-sided-conversion"]["transfer"]
        self.assertIn("multiplicity", conversion)
        self.assertIn("conjugation", conversion)

    def test_both_k_regimes_and_mvt_residual_are_exactly_retained(self) -> None:
        data = json.loads(self.replay().stdout)
        exact = data["exact_rational_checks"]
        self.assertEqual(exact["ell_max"], "10/13")
        self.assertEqual(exact["upper_min"], "15/14")
        self.assertEqual(exact["large_regime_gap"], "1/14")
        self.assertIn("250(s-3/4)^2", exact["mvt_residual"])
        rows = {row["id"]: row for row in data["rows"]}
        self.assertIn("Montgomery", rows["SB-B8-montgomery-discrete-mvt-and-polarity"]["locator"])
        self.assertIn("strictly below", rows["SB-B9-mvt-branch-and-strict-residual"]["transfer"])

    def test_narrow_pass_does_not_promote_stream_c_or_g0(self) -> None:
        data = json.loads(self.replay().stdout)
        self.assertIn("Stream C", data["pass_state"])
        self.assertIn("No new zero-density theorem", data["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
