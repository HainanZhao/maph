import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ControlArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controls = json.loads(
            (ROOT / "artifacts" / "certified-controls-v1.json").read_text()
        )
        cls.audit = json.loads(
            (ROOT / "artifacts" / "control-phase-audit-v1.json").read_text()
        )
        cls.screen = json.loads(
            (
                ROOT
                / "data"
                / "roblot-original-quartic-screen-v1.json"
            ).read_text()
        )

    def test_control_population(self):
        self.assertEqual(self.controls["case_count"], 5)
        self.assertEqual(self.controls["route_count"], 10)
        self.assertEqual(
            {row["case_id"] for row in self.controls["cases"]},
            {
                "RQ-000129",
                "RQ-001280",
                "RQ-001569",
                "RQ-001894",
                "RQ-007519",
            },
        )

    def test_every_case_has_two_routes(self):
        counts = {}
        for row in self.controls["routes"]:
            counts[row["case_id"]] = counts.get(row["case_id"], 0) + 1
        self.assertEqual(set(counts.values()), {2})

    def test_route_invariance_and_raw_nonquantization(self):
        findings = self.audit["findings"]
        self.assertEqual(findings["route_pairs_checked"], 5)
        self.assertEqual(findings["route_pairs_identical"], 5)
        self.assertEqual(
            findings["raw_lprime_phases_certifiably_nonquantized_count"],
            10,
        )
        self.assertEqual(findings["raw_lprime_phases_total"], 10)
        self.assertEqual(
            findings["raw_phase_quantization_verdict"], "REJECTED"
        )

    def test_no_circular_fit(self):
        identifiability = self.audit["identifiability"]
        self.assertEqual(
            identifiability["independent_canonical_defect_values_available"],
            0,
        )
        self.assertFalse(identifiability["fit_authorized"])
        self.assertFalse(identifiability["holdout_authorized"])
        self.assertTrue(identifiability["circular_fit_rejected"])

    def test_recovery_queue_is_frozen_and_unopened(self):
        self.assertEqual(self.screen["status"], "FROZEN_INPUT_QUEUE")
        self.assertEqual(len(self.screen["cases"]), 5)
        self.assertEqual(
            {row["case_id"] for row in self.screen["cases"]},
            {row["case_id"] for row in self.controls["cases"]},
        )
        for row in self.screen["cases"]:
            self.assertEqual(row["A1"], "PENDING_GENUINE_CHECK")
            self.assertEqual(row["A2"], "PENDING_GENUINE_CHECK")
            self.assertEqual(row["A3"], "PENDING_GENUINE_CHECK")


if __name__ == "__main__":
    unittest.main()
