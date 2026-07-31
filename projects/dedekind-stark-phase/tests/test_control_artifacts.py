import json
import hashlib
from pathlib import Path
import subprocess
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
        cls.bridge_verdict = json.loads(
            (
                ROOT
                / "artifacts"
                / "cycle-055-bridge-verdict-v1.json"
            ).read_text()
        )
        cls.final_no_go = json.loads(
            (
                ROOT
                / "artifacts"
                / "class-descent-fourier-no-go-v1.json"
            ).read_text()
        )
        cls.email_readiness = json.loads(
            (
                ROOT
                / "artifacts"
                / "roblot-email-send-readiness-v1.json"
            ).read_text()
        )
        cls.email_handoff = json.loads(
            (
                ROOT
                / "artifacts"
                / "roblot-email-human-handoff-v2.json"
            ).read_text()
        )
        cls.b1_action_audit = json.loads(
            (
                ROOT
                / "artifacts"
                / "b1-action-convention-audit-v1.json"
            ).read_text()
        )
        cls.b1_note_audit = json.loads(
            (
                ROOT
                / "artifacts"
                / "b1-note-audit-v1.json"
            ).read_text()
        )
        cls.b2_transport = json.loads(
            (
                ROOT / "artifacts" / "b2-artin-transport-v1.json"
            ).read_text()
        )
        cls.b2_oriented_replay = json.loads(
            (
                ROOT / "artifacts" / "b2-oriented-phase-replay-v1.json"
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

    def test_phase_clarification_containment_and_census_gate(self):
        circularity = json.loads(
            (
                ROOT / "artifacts" / "circularity-audit-v1.json"
            ).read_text()
        )
        self.assertEqual(
            circularity["claim_tag"],
            "CONTAINED_ORIENTATION_CIRCULARITY",
        )
        self.assertEqual(
            circularity["gates"]["dominant_gauge_data_independent"],
            "PASS",
        )
        self.assertEqual(
            circularity["gates"][
                "character_orientation_data_independent"
            ],
            "FAIL",
        )

        readiness = json.loads(
            (
                ROOT
                / "artifacts"
                / "quartic-census-readiness-audit-v1.json"
            ).read_text()
        )
        self.assertEqual(
            readiness["verdict"], "BLOCKED_BEFORE_TARGET_OPENING"
        )
        self.assertFalse(readiness["phase_targets_opened"])
        self.assertEqual(
            readiness["population_gate"]["higher_order_row_count"],
            2704,
        )
        self.assertEqual(
            readiness["rigorous_evaluator_gate"]["weak_unit_side"],
            "NUMERICAL_FROM_EXACT_UNIT",
        )

        lemma = (
            ROOT / "docs" / "roblot-phase-clarification-lemma-v1.md"
        ).read_text()
        self.assertIn(r"\chi(h)^{-1}\in\mu_4", lemma)
        self.assertIn("are equivalent", lemma)
        self.assertFalse(self.field_only_no_go["fit_executed"])

    def test_holdout_stays_closed_at_theory_pivot(self):
        self.assertFalse(self.cocycle_audit["generic_extractor_present"])
        self.assertFalse(self.cocycle_audit["holdout_authorized"])
        self.assertEqual(
            self.cocycle_audit["fit_track_status"], "STOPPED"
        )

    def test_restricted_bridge_verdict_preserves_fit_gate(self):
        self.assertEqual(
            self.bridge_verdict["verdict"], "RESTRICTED_SIC_BRIDGE"
        )
        self.assertEqual(
            self.bridge_verdict["supplied_tuple_layer"]["status"],
            "VERIFIED",
        )
        self.assertFalse(
            self.bridge_verdict["five_control_feature_test"]["authorized"]
        )
        self.assertFalse(
            self.bridge_verdict["coefficient_fit_authorized"]
        )
        self.assertFalse(self.bridge_verdict["holdout_authorized"])

    def test_final_fourier_no_go_is_exact(self):
        self.assertEqual(self.final_no_go["class_descent"], "PASS")
        exponents = self.final_no_go["multiplier_exponents"]
        for index in range(4):
            self.assertEqual(
                exponents[str(index)], exponents[str(index + 4)]
            )
        self.assertEqual(
            set(self.final_no_go["differenced_support_characters"]),
            {1, 3, 5, 7},
        )
        self.assertEqual(
            set(self.final_no_go["relevant_fourier_resolvents"].values()),
            {"0"},
        )
        self.assertEqual(
            self.final_no_go["verdict"],
            "SQUARED_MULTIPLIER_PHASE_MECHANISM_REJECTED",
        )

    def test_roblot_email_is_ready_but_not_claimed_sent(self):
        readiness = self.email_readiness
        self.assertEqual(
            readiness["status"],
            "READY_AWAITING_AUTHORIZED_MAIL_CHANNEL",
        )
        self.assertEqual(readiness["message"]["question_count"], 3)
        self.assertTrue(readiness["message"]["ai_assistance_disclosed"])
        self.assertTrue(
            readiness["message"]["withdrawn_raw_orientation_labels_omitted"]
        )
        self.assertEqual(
            readiness["message"]["public_doi"],
            "10.5281/zenodo.21712478",
        )
        self.assertEqual(
            readiness["attachment"]["sha256"],
            "e2a945edaddcec32e3aad10e67f8b960af0bc304b07ba5503ab7be62384b9506",
        )
        self.assertFalse(readiness["delivery"]["sent"])

    def test_current_outbound_handoff_is_human_only_and_unsent(self):
        handoff = self.email_handoff
        self.assertEqual(handoff["status"], "HUMAN_ONLY_READY_NOT_SENT")
        self.assertTrue(handoff["delivery"]["handoff_complete"])
        self.assertFalse(handoff["delivery"]["sent_by_agent"])
        self.assertFalse(handoff["delivery"]["sent_by_human"])
        self.assertTrue(
            handoff["research_scheduling"]["local_track_b_work_authorized"]
        )
        self.assertTrue(
            handoff["research_scheduling"][
                "no_submission_or_circulation_before_b3"
            ]
        )

    def test_b1_action_conventions_are_explicitly_separated(self):
        audit = self.b1_action_audit
        self.assertEqual(audit["status"], "CONTAINED_NOTATIONAL_CORRECTION")
        self.assertEqual(
            audit["right_exponent_action"]["covariance"],
            "c_chi(u^a) = chi(a)^(-1) c_chi(u)",
        )
        self.assertEqual(
            audit["left_group_ring_action"]["covariance"],
            "c_chi(a dot u) = chi(a) c_chi(u)",
        )

    def test_b1_note_audit_and_frozen_hashes(self):
        audit = self.b1_note_audit
        self.assertEqual(audit["status"], "PASS_LOCAL_ONLY_NOT_FOR_CIRCULATION")
        self.assertTrue(all(audit["exact_checks"].values()))
        self.assertFalse(audit["circulation"]["authorized"])
        self.assertFalse(audit["circulation"]["outbound_actions_by_agent"])
        for relative_path, expected_hash in audit["source_hashes"].items():
            digest = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(digest, expected_hash, relative_path)

    def test_b1_exact_replay(self):
        replay = subprocess.run(
            ["python3", "proof/audit_b1_note.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertIn("B1_NOTE_AUDIT=PASS", replay.stderr)

    def test_b2_exact_transport_and_preserved_correction(self):
        transport = self.b2_transport
        self.assertEqual(
            transport["status"],
            "PASS_EXACT_TRANSPORT_WITH_CONTAINED_EXPOSURE",
        )
        self.assertEqual(transport["claim_tag"], "PROVED_EXACT_TRANSPORT")
        self.assertTrue(
            transport["exact_gates"]["frobenius_checked_on_full_integral_basis"]
        )
        self.assertEqual(
            {
                row["case_id"]: row["dedekind_to_analytic_orientation"]
                for row in transport["cases"]
            },
            {
                "RQ-000129": "inverse",
                "RQ-001280": "inverse",
                "RQ-001569": "direct",
                "RQ-001894": "direct",
                "RQ-007519": "inverse",
            },
        )
        self.assertEqual(
            transport["preserved_failure"]["case_id"], "RQ-007519"
        )
        self.assertEqual(
            transport["contained_input_exposure"]["status"],
            "PREREGISTRATION_INPUT_VIOLATION_CONTAINED",
        )
        self.assertFalse(transport["outbound_actions_by_agent"])
        for relative_path, expected_hash in transport["source_hashes"].items():
            digest = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(digest, expected_hash, relative_path)

    def test_b2_one_orientation_replay_is_observed_not_proof(self):
        replay = self.b2_oriented_replay
        self.assertEqual(replay["status"], "PASS_FIVE_EXACT_ORIENTATIONS")
        self.assertEqual(
            replay["claim_tag"], "OBSERVED_FIVE_CASE_ORIENTED_MATCH"
        )
        self.assertFalse(replay["alternative_orientation_searched"])
        self.assertFalse(replay["proof_route"])
        self.assertEqual(len(replay["cases"]), 5)
        for relative_path, expected_hash in replay["source_hashes"].items():
            digest = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(digest, expected_hash, relative_path)

    def test_b2_exact_and_oriented_replays(self):
        for command, marker in (
            (
                ["python3", "proof/audit_b2_artin_transport.py"],
                "B2_ARTIN_TRANSPORT_AUDIT=PASS",
            ),
            (
                ["python3", "proof/replay_b2_oriented_phase.py"],
                "B2_ORIENTED_PHASE_REPLAY=PASS",
            ),
        ):
            replay = subprocess.run(
                command,
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(replay.returncode, 0, replay.stderr)
            self.assertIn(marker, replay.stderr)


if __name__ == "__main__":
    unittest.main()
