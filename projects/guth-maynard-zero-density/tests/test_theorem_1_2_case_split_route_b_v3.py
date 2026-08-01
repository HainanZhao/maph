"""Tests for the independent Route-B v3 Theorem 1.2 case audit."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_theorem_1_2_case_split_route_b_v3.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-1-route-b-v3-theorem-1-2-case-split.json"
V1_SCRIPT = PROJECT / "proof" / "replay_baseline_route_b.py"
V1_ARTIFACT = PROJECT / "artifacts" / "cycle-1-route-b-baseline.json"
V2_SCRIPT = PROJECT / "proof" / "replay_bottleneck_cell_route_b_v2.py"
V2_ARTIFACT = PROJECT / "artifacts" / "cycle-1-route-b-v2-bottleneck-cell.json"


class Theorem12CaseSplitRouteBV3Tests(unittest.TestCase):
    def replay(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_artifact_replays_byte_for_byte(self) -> None:
        self.replay("--check", str(ARTIFACT))

    def test_prior_route_b_artifacts_are_preserved(self) -> None:
        subprocess.run([sys.executable, str(V1_SCRIPT), "--check", str(V1_ARTIFACT)], check=True)
        subprocess.run([sys.executable, str(V2_SCRIPT), "--check", str(V2_ARTIFACT)], check=True)

    def test_type_ii_and_integer_choice_labels_are_present(self) -> None:
        data = json.loads(self.replay().stdout)
        self.assertEqual(data["type_ii"]["conclusion"], "2*(1-s) <= B(s)")
        choices = data["integer_choice_regimes"]
        self.assertIn("ceil", choices["small_n"]["choice"])
        self.assertIn("k=2", choices["large_n"]["choice"])
        self.assertIn("not asserted", choices["large_n"]["endpoint_containment"])

    def test_guth_maynard_terms_have_all_three_labeled_residuals(self) -> None:
        data = json.loads(self.replay().stdout)
        branch = data["guth_maynard_branch_q_le_alpha"]
        self.assertEqual(branch["term_1"]["conclusion"], "2*q*(1-s)<=B(s)")
        self.assertIn("alpha(s)<=u(s)", branch["term_1"]["sign_source"])
        self.assertEqual(branch["term_2"]["conclusion"], "d(s)*q<=B(s)")
        self.assertEqual(branch["term_3"]["conclusion"], "1+(12/5-4*s)*q<=B(s)")

    def test_mean_value_margin_is_strict_and_factored_and_expanded(self) -> None:
        data = json.loads(self.replay().stdout)
        strict = data["mean_value_branch_q_gt_alpha"]["term_2_strict"]
        self.assertIn("250*(s-3/4)^2+3/8", strict["M_factored"])
        self.assertEqual(strict["M_expanded_numerator"], "250*s^2-375*s+141")
        self.assertEqual(strict["conclusion"], "1+(1-2*s)*q<B(s)")

    def test_no_finite_t_upgrade_of_logarithmic_endpoint(self) -> None:
        data = json.loads(self.replay().stdout)
        policy = data["endpoint_slack_policy"]
        self.assertTrue(policy["no_silent_upgrade"])
        self.assertIn("o(1)", policy["logarithmic_upper_endpoint"])


if __name__ == "__main__":
    unittest.main()
