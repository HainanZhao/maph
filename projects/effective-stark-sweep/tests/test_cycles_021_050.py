"""Regression tests for the geometry/W2/dedup cycles 021--050."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Cycles021050Test(unittest.TestCase):
    def test_complete_engine_c_geometry(self) -> None:
        result = json.loads(
            (
                ROOT / "artifacts" / "engine-c-geometry-analysis-v1.json"
            ).read_text()
        )
        self.assertEqual(result["packet_count"], 1350)
        self.assertEqual(
            result["packet_taxonomy"],
            {
                "GEOMETRY_PASS": 1255,
                "LINEAR_REINDUCTION_BASE_COUNT_FAIL": 77,
                "NORMAL_CLOSURE_GROUP_NOT_16_13": 1,
                "NORMAL_CLOSURE_ORDER_NE_16": 13,
                "TOOL_BLOCKED": 4,
            },
        )
        self.assertEqual(
            result["case_routing_after_complete_c_gate"],
            {
                "C_ELIGIBLE": 728,
                "FRONTIER": 22,
                "REROUTE_B": 63,
                "TOOL_BLOCKED": 4,
            },
        )
        self.assertEqual(result["distinct_cm_base_pairs"], 217)

    def test_engine_c_failures_are_preserved_and_quarantined(self) -> None:
        quarantine = json.loads(
            (
                ROOT / "data" / "engine-c-tool-quarantine-v1.json"
            ).read_text()
        )
        self.assertEqual(len(quarantine["entries"]), 4)
        for name in [
            "engine-c-geometry-failed-v0.txt",
            "engine-c-geometry-failed-v1.json",
            "engine-c-geometry-failed-v2.json",
            "engine-c-geometry-failed-v3.json",
            "engine-c-geometry-failed-v4.json",
            "engine-c-geometry-failed-v8.json",
        ]:
            self.assertTrue((ROOT / "artifacts" / name).is_file())

    def test_engine_b_two_route_census(self) -> None:
        result = json.loads(
            (
                ROOT / "artifacts" / "engine-b-two-route-analysis-v1.json"
            ).read_text()
        )
        self.assertEqual(result["case_count"], 372)
        self.assertEqual(
            result["classification_counts"],
            {
                "NO_ABELIAN_IMAGINARY_BASE": 177,
                "TWO_ROUTE_PASS": 195,
            },
        )
        self.assertEqual(
            result["two_route_pass_distinct_normal_closures"], 59
        )
        self.assertEqual(result["two_route_pass_distinct_cm_base_sets"], 56)
        self.assertNotIn(
            "TWO_ROUTE_MISMATCH", result["classification_counts"]
        )

    def test_q14_and_q111_exponent_tables(self) -> None:
        q14 = (
            ROOT / "artifacts" / "q14-p7-w2-divisor-table-v1.transcript"
        ).read_text()
        self.assertIn("SHINTANI_CLEARING_EXPONENTS=[576, 84]", q14)
        self.assertIn("SHINTANI_SAFE_EXPONENT=4032", q14)
        self.assertIn("Q14_P7_W2_DIVISOR_TABLE_CERTIFIED=1", q14)
        q111 = (
            ROOT / "artifacts"
            / "q111-norm3-w2-divisor-table-v1.transcript"
        ).read_text()
        self.assertIn("SHINTANI_DIVISOR_COUNT=8", q111)
        self.assertIn("SHINTANI_SAFE_EXPONENT=13810176", q111)
        self.assertIn("Q111_NORM3_W2_DIVISOR_TABLE_CERTIFIED=1", q111)

    def test_q6_engine_c_algebraic_half_and_boundary(self) -> None:
        reinduction = (
            ROOT / "artifacts" / "q6-norm8-c-reinduction-v1.transcript"
        ).read_text()
        self.assertIn("CM_BASE_COUNT=2", reinduction)
        self.assertIn(
            "Q6_NORM8_LINEAR_REINDUCTION_VERIFIED=1", reinduction
        )
        conditions = (
            ROOT / "artifacts"
            / "q6-norm8-c-stark-conditions-v1.transcript"
        ).read_text()
        self.assertIn("CHARACTER_FIELD_ROOTS_OF_UNITY=8", conditions)
        self.assertIn("STARK_S_SIZE=3", conditions)
        self.assertIn(
            "Q6_NORM8_STARK_1980_CONDITIONS_VERIFIED=1", conditions
        )
        lattice = (
            ROOT / "artifacts" / "q6-norm8-c-unit-lattice-v2.transcript"
        ).read_text()
        self.assertIn(
            "Q6_NORM8_EXACT_UNIT_LATTICE_VERIFIED=1", lattice
        )
        self.assertIn(
            "Q6_NORM8_ANALYTIC_ARB_ORIENTATION_GATE=PENDING", lattice
        )
        case = json.loads(
            (ROOT / "data" / "q6-norm8-case-v1.json").read_text()
        )
        self.assertEqual(
            case["verdict"], "THEOREM_CANDIDATE_NOT_YET_VERIFIED"
        )
        self.assertEqual(
            case["identification"]["claim_tag"], "NUMERICAL"
        )

    def test_engine_a_exact_split_and_field_deduplication(self) -> None:
        queue = json.loads(
            (
                ROOT / "artifacts" / "engine-a-queue-analysis-v1.json"
            ).read_text()
        )
        self.assertEqual(queue["case_count"], 5459)
        self.assertEqual(queue["trivial_packet_count"], 3899)
        self.assertEqual(queue["quadratic_packet_count"], 1560)
        fields = json.loads(
            (
                ROOT / "artifacts" / "engine-a-field-census-v1.json"
            ).read_text()
        )
        self.assertEqual(fields["case_count"], 1560)
        self.assertEqual(fields["quadratic_packet_occurrence_count"], 2232)
        self.assertEqual(fields["distinct_absolute_quartic_field_count"], 912)
        self.assertEqual(
            fields["claim_tag"], "VERIFIED_EXACT_FIELD_EXTRACTION"
        )

    def test_refined_queue_counts_and_order(self) -> None:
        queues = json.loads(
            (
                ROOT / "artifacts" / "identification-queues-v2.json"
            ).read_text()
        )
        self.assertEqual(queues["ordering"], ["C", "B", "A"])
        self.assertEqual(
            queues["engine_c"]["geometry_eligible_case_count"], 728
        )
        self.assertEqual(queues["engine_b"]["two_route_pass_count"], 195)
        self.assertEqual(
            queues["engine_b"]["degree_above_40_pending_count"], 346
        )
        self.assertEqual(
            queues["engine_a"]["verified_trivial_x_equals_one_count"],
            3899,
        )


if __name__ == "__main__":
    unittest.main()
