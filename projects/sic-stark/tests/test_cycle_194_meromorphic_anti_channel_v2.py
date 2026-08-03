from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof" / "verify_cycle_194_meromorphic_anti_channel_v2.py"


class Cycle194MeromorphicAntiChannelCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)], check=True, capture_output=True, text=True
        )
        cls.result = json.loads(completed.stdout)

    def test_local_source_forced_anti_channel_is_retained(self) -> None:
        forced = self.result["retained_v1_results"]["forced_anti_fibre"]
        self.assertTrue(forced["all_six_anti_coordinates_source_forced"])
        self.assertTrue(forced["F24_preserves_A"])

    def test_true_pole_orbits_are_finite_and_exact(self) -> None:
        census = self.result["corrected_true_pole_census"]
        self.assertEqual(census["orbit_cardinalities"], [2, 4, 6, 8, 10, 12])
        self.assertEqual(census["total_true_pole_summands"], 42)
        for record in census["records"]:
            self.assertFalse(record["infinite_true_pole_tail_exists"])
            self.assertEqual(
                record["first_rejected_inequality"], -1
            )
            self.assertTrue(
                all(member["individual_simple_residue_nonzero"] for member in record["members"])
            )

    def test_tail_claims_are_explicitly_withdrawn(self) -> None:
        withdrawn = self.result["withdrawn_v1_claims"]
        self.assertEqual(len(withdrawn), 3)
        self.assertIn("OPEN", self.result["corrected_true_pole_census"]["combined_residue_status"])


if __name__ == "__main__":
    unittest.main()
