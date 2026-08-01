import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]


class G1AtlasPreregistrationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((PROJECT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json").read_text())

    def test_frozen_counts_and_reduced_critical_anchors(self) -> None:
        self.assertTrue(self.data["frozen_before_discovery"])
        self.assertEqual(self.data["local_grid"]["expected_rows"], 7744)
        self.assertEqual(self.data["screen"]["expected_rows"], 588)
        self.assertEqual(len(self.data["screen"]["spine"]), 42)
        self.assertEqual(len(self.data["screen"]["pairs"]), 14)
        self.assertEqual(self.data["mandatory_anchors"]["transfer"], {"s": "7/10", "n0": "5/13", "k": 2, "q": "10/13"})
        self.assertEqual(self.data["mandatory_anchors"]["local"]["energy_terms"], ["5/3"] * 3)

    def test_source_range_and_energy_firewalls(self) -> None:
        self.assertEqual(self.data["formulas"]["energy_diagonal_only"]["eligibility"], "v=s")
        self.assertNotIn("1/100", {row["n0"] for row in self.data["transfer_rows"]})
        endpoint = [row for row in self.data["transfer_rows"] if row["n0"] == "1/2"]
        self.assertTrue(endpoint and all(row["provenance"] == "ASYMPTOTIC_ENDPOINT_ONLY" for row in endpoint))
        self.assertEqual(self.data["resources"]["maximum_finite_rows"] * self.data["resources"]["seconds_per_finite_row"] // 3600, 33)
        self.assertLessEqual(self.data["resources"]["worst_case_hours_at_row_cap"], self.data["resources"]["aggregate_cpu_hours"])

    def test_deterministic_artifact_replays(self) -> None:
        subprocess.run([sys.executable, str(PROJECT / "discovery/build_g1_atlas_preregistration_v1.py"), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
