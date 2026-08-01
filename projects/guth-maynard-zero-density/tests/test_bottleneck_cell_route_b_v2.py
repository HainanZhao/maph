"""Regression checks for the Route-B v2 bottleneck-cell certificate."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_bottleneck_cell_route_b_v2.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-1-route-b-v2-bottleneck-cell.json"
PRIOR_SCRIPT = PROJECT / "proof" / "replay_baseline_route_b.py"
PRIOR_ARTIFACT = PROJECT / "artifacts" / "cycle-1-route-b-baseline.json"


class BottleneckCellRouteBV2Tests(unittest.TestCase):
    def replay(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_v2_artifact_replays_byte_for_byte(self) -> None:
        self.replay("--check", str(ARTIFACT))

    def test_prior_route_b_artifact_is_preserved_and_still_valid(self) -> None:
        subprocess.run([sys.executable, str(PRIOR_SCRIPT), "--check", str(PRIOR_ARTIFACT)], check=True)

    def test_all_theorem_terms_and_tie_are_exact(self) -> None:
        data = json.loads(self.replay().stdout)
        rows = data["theorem_1_1_term_table"]["rows"]
        self.assertEqual([row["U_exponent"] for row in rows], ["1/2", "2/3", "2/3"])
        self.assertEqual(data["theorem_1_1_term_table"]["max_U_exponent"], "2/3")
        self.assertIn("tie", data["theorem_1_1_term_table"]["cleared_comparisons"][1])

    def test_all_energy_terms_tie_at_the_remark_scale(self) -> None:
        data = json.loads(self.replay().stdout)
        rows = data["proposition_11_1_energy_table"]["rows"]
        self.assertEqual([row["U_exponent"] for row in rows], ["5/3", "5/3", "5/3"])
        self.assertEqual([row["cleared_twelfths"] for row in rows], ["20", "20", "20"])
        self.assertTrue(data["proposition_11_1_energy_table"]["matches_final_remark_energy"])

    def test_local_to_global_count_matches_the_density_target(self) -> None:
        data = json.loads(self.replay().stdout)
        count = data["local_to_global_count"]
        self.assertEqual(count["local_W_in_T_exponent"], "8/13")
        self.assertEqual(count["number_of_U_subintervals_in_T_exponent"], "1/13")
        self.assertEqual(count["combined_T_exponent"], "9/13")
        self.assertEqual(count["theorem_1_2_density_exponent_at_sigma"], "9/13")
        self.assertTrue(count["exact_match"])


if __name__ == "__main__":
    unittest.main()
