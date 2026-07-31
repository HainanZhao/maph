import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CensusPaperLayer0Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(
            (
                ROOT
                / "artifacts"
                / "census-paper-layer0-reconciliation-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.preregistration = json.loads(
            (
                ROOT / "data" / "census-paper-preregistration-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.synthesis_preregistration = json.loads(
            (
                ROOT
                / "data"
                / "census-paper-preregistration-amendment-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.synthesis = json.loads(
            (
                ROOT
                / "artifacts"
                / "census-packet-polynomial-synthesis-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.artin_preregistration = json.loads(
            (
                ROOT
                / "data"
                / "census-paper-preregistration-amendment-v2.json"
            ).read_text(encoding="utf-8")
        )
        cls.corrected_anchor_preregistration = json.loads(
            (
                ROOT
                / "data"
                / "census-paper-preregistration-amendment-v3.json"
            ).read_text(encoding="utf-8")
        )
        cls.rq000245_synthesis = json.loads(
            (
                ROOT
                / "artifacts"
                / "rq000245-packet-synthesis-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.height_calibration = json.loads(
            (
                ROOT
                / "artifacts"
                / "census-packet-height-calibration-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.q_packet_corpus_audit = json.loads(
            (
                ROOT
                / "artifacts"
                / "census-q-packet-corpus-audit-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.q_arb_sample = json.loads(
            (
                ROOT / "data" / "census-paper-q-arb-sample-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.q_arb_audit = json.loads(
            (
                ROOT / "artifacts" / "census-q-arb-audit-v1.json"
            ).read_text(encoding="utf-8")
        )

    def test_frozen_range(self):
        universe = self.record["publication_universe"]
        self.assertEqual(universe["D_min"], 2)
        self.assertEqual(universe["D_max"], 200)
        self.assertEqual(universe["finite_ideal_norm_max"], 100)
        self.assertEqual(universe["field_count"], 121)
        self.assertEqual(universe["representative_count"], 8200)
        self.assertFalse(universe["nonmaximal_form_order_moduli_in_universe"])
        self.assertTrue(
            self.record["clean_enumeration_rerun"][
                "mathematical_payload_identical"
            ]
        )

    def test_support_first_trichotomy(self):
        split = self.record["structural_trichotomy"]
        self.assertEqual(
            [
                split["T_empty_support"],
                split["Q_nonempty_quadratic_support"],
                split["H_nonempty_higher_order_support"],
                split["sum"],
            ],
            [3936, 1560, 2704, 8200],
        )
        higher = self.record["higher_order_mechanism_cross_tab"]
        self.assertEqual(
            [
                higher["ENGINE_B_ELIGIBLE"],
                higher["ENGINE_C_ELIGIBLE"],
                higher["FRONTIER"],
                higher["sum"],
            ],
            [232, 881, 1591, 2704],
        )

    def test_v5_reconciliation_is_explicit(self):
        correction = self.record["v5_reconciliation"]
        self.assertEqual(correction["banked_routing_trivial_count"], 3899)
        self.assertEqual(correction["structural_empty_support_count"], 3936)
        self.assertEqual(
            correction["empty_support_rows_previously_routed_FRONTIER"], 37
        )
        self.assertEqual(len(correction["affected_case_ids"]), 37)

    def test_quadratic_counts_and_semantics(self):
        quadratic = self.record["quadratic_stratum_reconciliation"]
        self.assertEqual(quadratic["rows"], 1560)
        self.assertEqual(
            quadratic["supported_quadratic_character_occurrences"], 2232
        )
        self.assertEqual(quadratic["distinct_quartic_fields"], 912)
        self.assertEqual(quadratic["zero_Euler_character_occurrences"], 672)
        self.assertEqual(quadratic["rows_affected_by_zero_Euler_factors"], 603)
        self.assertEqual(
            quadratic["rows_with_all_supported_derivatives_zero"], 346
        )
        self.assertIn("remain in Q", quadratic["classification_rule"])

    def test_preregistered_gates(self):
        # The original cap remains historical evidence; the versioned
        # trace-descent amendment explicitly supersedes this field.
        self.assertEqual(
            self.preregistration["packet_polynomial_policy"][
                "maximum_absolute_compositum_degree"
            ],
            32,
        )
        spot = self.preregistration["independent_analytic_spotcheck"]
        self.assertEqual(spot["sample_size"], 50)
        self.assertEqual(spot["target_decimal_digits"], 38)
        self.assertIn("halt publication", spot["failure_rule"])
        amendment = self.synthesis_preregistration
        self.assertEqual(
            amendment["supersedes"]["historical_value"], 32
        )
        self.assertFalse(amendment["full_q_corpus_authorized"])
        self.assertIn(
            "coefficient-height",
            amendment["next_freeze_required"],
        )

    def test_trace_descent_anchor_and_denominator_correction(self):
        synthesis = self.synthesis
        self.assertEqual(
            synthesis["status"],
            "PASS_TRACE_DESCENT_AND_DENOMINATOR_TWO_ANCHOR",
        )
        self.assertEqual(
            synthesis["claim_tags"]["algebraic_recurrence"], "PROVED"
        )
        self.assertEqual(
            synthesis["correction_to_proposed_method"][
                "dimension_eight_common_denominator"
            ],
            2,
        )
        self.assertEqual(
            synthesis["correction_to_proposed_method"]["raw_result_is_for"],
            "X_A^2",
        )
        gates = synthesis["exact_gates"]
        self.assertEqual(gates["source_infinity_vector"], [1, 0])
        self.assertEqual(gates["selected_split_real_place"], 2)
        self.assertTrue(gates["powered_orbit_reciprocal"])
        self.assertTrue(gates["packet_factor_reciprocal"])
        self.assertTrue(gates["packet_factor_irreducible_over_K"])
        self.assertTrue(gates["absolute_packet_irreducible"])
        self.assertFalse(
            synthesis["quarantined_numerical_validation"][
                "used_for_selection"
            ]
        )
        self.assertFalse(
            synthesis["claim_boundary"]["linear_bit_complexity_claimed"]
        )

    def test_trace_descent_one_command_replay(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_packet_polynomial_synthesis.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        replay = json.loads(completed.stdout)
        self.assertEqual(
            replay["status"],
            "PASS_TRACE_DESCENT_AND_DENOMINATOR_TWO_ANCHOR",
        )

    def test_proper_artin_image_anchor(self):
        self.assertEqual(
            self.artin_preregistration["claim_boundary"][
                "ambient_trace_polynomial"
            ],
            "all formal sign patterns",
        )
        self.assertFalse(
            self.artin_preregistration["claim_boundary"][
                "q_equals_1_suffices_without_factor_gate"
            ]
        )
        self.assertEqual(
            self.corrected_anchor_preregistration["corrected_anchor"][
                "case_id"
            ],
            "RQ-000245",
        )
        synthesis = self.rq000245_synthesis
        self.assertEqual(
            synthesis["status"],
            "PASS_PROPER_ARTIN_IMAGE_AND_DENOMINATOR_LIFT",
        )
        gates = synthesis["exact_gates"]
        self.assertEqual(gates["formal_sign_orbit_size"], 16)
        self.assertEqual(gates["artin_sign_image_size"], 8)
        self.assertEqual(gates["common_denominator"], 2)
        self.assertEqual(gates["matching_packet_factor_count"], 1)
        self.assertEqual(gates["packet_factor_degree_over_K"], 8)
        self.assertTrue(gates["packet_factor_reciprocal"])
        self.assertTrue(gates["packet_factor_irreducible_over_K"])
        self.assertEqual(gates["packet_absolute_degree"], 16)
        self.assertFalse(
            synthesis["claim_boundary"][
                "analytic_lprime_or_packet_target_opened"
            ]
        )

    def test_proper_artin_image_one_command_replay(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_rq000245_packet_synthesis.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        replay = json.loads(completed.stdout)
        self.assertEqual(
            replay["status"],
            "PASS_PROPER_ARTIN_IMAGE_AND_DENOMINATOR_LIFT",
        )

    def test_height_calibration_and_exhaustive_q_corpus(self):
        calibration = self.height_calibration
        self.assertEqual(
            calibration["status"], "PASS_HEIGHT_CALIBRATION_CAP_RULE"
        )
        self.assertEqual(calibration["population"]["q_rows"], 1560)
        self.assertEqual(
            calibration["cap_rule_result"]["maximum_observed_B"], 89
        )
        self.assertEqual(
            calibration["cap_rule_result"][
                "frozen_rule_output_decimal_digits"
            ],
            256,
        )
        self.assertFalse(
            calibration["claim_boundary"]["packet_polynomials_constructed"]
        )
        audit = self.q_packet_corpus_audit
        self.assertEqual(
            audit["status"], "PASS_EXHAUSTIVE_Q_PACKET_CORPUS_AUDIT"
        )
        self.assertEqual(audit["population"]["rows"], 1560)
        self.assertEqual(
            audit["population"]["all_zero_X_minus_1_rows"], 346
        )
        self.assertEqual(
            audit["exact_distributions"]["packet_degree_over_K"],
            {"1": 346, "2": 930, "4": 242, "8": 42},
        )
        self.assertEqual(
            audit["exact_distributions"]["common_denominator"],
            {"1": 1491, "2": 69},
        )
        self.assertEqual(
            audit["exact_distributions"][
                "maximum_coefficient_coordinate_decimal_digits"
            ],
            62,
        )
        self.assertTrue(audit["chain"]["verified"])

    def test_q_packet_corpus_one_command_audit(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_census_q_packet_corpus.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        replay = json.loads(completed.stdout)
        self.assertEqual(
            replay["chain"]["final_sha256"],
            "7c04242b1d4c11293af96f83f4915dbed25f6125c60d82965e533df5c9d81855",
        )

    def test_independent_q_arb_audit(self):
        self.assertEqual(len(self.q_arb_sample["selected"]), 50)
        self.assertFalse(self.q_arb_sample["analytic_values_opened"])
        audit = self.q_arb_audit
        self.assertEqual(
            audit["status"], "PASS_50_ROW_INDEPENDENT_ARB_AUDIT"
        )
        self.assertEqual(audit["claim_tag"], "CERTIFIED_NUMERICAL")
        self.assertEqual(audit["population"]["sample_rows"], 50)
        self.assertEqual(
            audit["population"]["effective_character_occurrences"], 43
        )
        self.assertEqual(audit["population"]["checked_artin_sign_rows"], 101)
        self.assertEqual(audit["population"]["all_zero_rows"], 13)
        wall = audit["independence_wall"]
        self.assertFalse(wall["relative_unit_norm_kernel_opened"])
        self.assertFalse(wall["packet_factor_or_roots_opened"])
        self.assertTrue(
            wall["independent_balls_completed_before_corpus_traces_opened"]
        )
        self.assertEqual(audit["precision"]["initial_bits"], 192)
        self.assertEqual(audit["precision"]["bits"], 384)

    def test_independent_q_arb_one_command_replay(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_census_q_arb_sample.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        replay = json.loads(completed.stdout)
        self.assertEqual(
            replay["status"], "PASS_50_ROW_INDEPENDENT_ARB_AUDIT"
        )


if __name__ == "__main__":
    unittest.main()
