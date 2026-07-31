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
        cls.constructor_v2 = json.loads(
            (
                ROOT
                / "artifacts"
                / "roblot-rq000129-constructor-sealed-v2.json"
            ).read_text()
        )
        cls.phase_gate = json.loads(
            (
                ROOT / "artifacts" / "rq000129-phase-gate-v1.json"
            ).read_text()
        )
        cls.all_phase_gates = json.loads(
            (
                ROOT / "artifacts" / "all-five-phase-gates-v1.json"
            ).read_text()
        )
        cls.frozen_feature_audit = json.loads(
            (
                ROOT / "artifacts" / "frozen-feature-family-audit-v1.json"
            ).read_text()
        )
        cls.dominant_gauge = json.loads(
            (
                ROOT / "artifacts" / "dominant-gauge-controls-v1.json"
            ).read_text()
        )
        cls.field_only_no_go = json.loads(
            (
                ROOT
                / "artifacts"
                / "field-only-dedekind-family-no-go-v1.json"
            ).read_text()
        )
        cls.cocycle_audit = json.loads(
            (
                ROOT
                / "artifacts"
                / "ray-cocycle-availability-audit-v1.json"
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

    def test_corrected_constructor_uses_genuine_plus_lattice(self):
        exact = self.constructor_v2["exact_data"]
        self.assertEqual(exact["norm_index"], 2)
        self.assertEqual(exact["e_exponent"], 1)
        self.assertEqual(exact["anti_unit_norm"], 1)
        self.assertEqual(
            self.constructor_v2["correction"]["v1_proxy"],
            "fixed sublattice of U_K modulo torsion",
        )

    def test_first_independent_phase_gate_passes_without_fit(self):
        self.assertEqual(self.phase_gate["verdict"], "PASS")
        self.assertEqual(self.phase_gate["phase_defect_mod_pi_over_2"], 0)
        checks = self.phase_gate["component_checks"]
        self.assertTrue(checks["real_contained"])
        self.assertTrue(checks["imag_contained"])
        authorization = self.phase_gate["fit_authorization"]
        self.assertEqual(
            authorization["independent_defect_values_available"], 1
        )
        self.assertFalse(authorization["coefficient_fit_authorized"])

    def test_all_five_independent_phase_gates_quantize(self):
        self.assertEqual(self.all_phase_gates["case_count"], 5)
        self.assertEqual(self.all_phase_gates["quantized_count"], 5)
        self.assertTrue(
            self.all_phase_gates["all_unique_orientation_matches"]
        )
        self.assertEqual(
            {
                row["case_id"]: row["defect_quarter_turn"]
                for row in self.all_phase_gates["cases"]
            },
            {
                "RQ-000129": 3,
                "RQ-001280": 0,
                "RQ-001569": 3,
                "RQ-001894": 3,
                "RQ-007519": 0,
            },
        )

    def test_frozen_feature_family_rejected_before_fit(self):
        self.assertEqual(
            self.frozen_feature_audit["status"], "REJECTED_BEFORE_FIT"
        )
        nonintegral = [
            row
            for row in self.frozen_feature_audit["cases"]
            if "/" in row["twelve_dedekind_sum"]
        ]
        self.assertEqual(
            {row["case_id"] for row in nonintegral},
            {"RQ-001894", "RQ-007519"},
        )

    def test_dominant_gauge_and_exact_field_only_no_go(self):
        self.assertEqual(
            {
                row["case_id"]: row["dominant_q"]
                for row in self.dominant_gauge["cases"]
            },
            {
                "RQ-000129": 0,
                "RQ-001280": 1,
                "RQ-001569": 1,
                "RQ-001894": 3,
                "RQ-007519": 3,
            },
        )
        self.assertEqual(
            self.field_only_no_go["claim_tag"],
            "VERIFIED_EXACT_NO_SOLUTION",
        )
        left, right = self.field_only_no_go["witness_pair"]
        self.assertEqual(
            left["feature_vector_mod_4"],
            right["feature_vector_mod_4"],
        )
        self.assertNotEqual(left["dominant_q"], right["dominant_q"])
        self.assertFalse(self.field_only_no_go["fit_executed"])

    def test_holdout_stays_closed_at_theory_pivot(self):
        self.assertFalse(self.cocycle_audit["generic_extractor_present"])
        self.assertFalse(self.cocycle_audit["holdout_authorized"])
        self.assertEqual(
            self.cocycle_audit["fit_track_status"], "STOPPED"
        )


if __name__ == "__main__":
    unittest.main()
