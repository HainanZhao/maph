"""Regression gates for the Cycle-059/060 bulk-execution block."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class Cycle060BulkExecutionTest(unittest.TestCase):
    def test_q7_headline_is_present_and_verified(self) -> None:
        case = load("data/q7-p7-case-v1.json")
        self.assertEqual(case["case_id"], "RQ-000190")
        self.assertEqual(case["fourier_support_orders"], [2, 6])
        self.assertEqual(case["w3"]["packet_identity_verdict"], "VERIFIED")
        self.assertEqual(case["w2"]["safe_exponent"], 4032)

    def test_rq000458_is_dual_routed_not_overpromoted(self) -> None:
        case = load("data/rq000458-dual-case-v1.json")
        seal = load("artifacts/rq000458-seal-resolution-v1.json")
        self.assertEqual(case["verdict"], "DUAL_ROUTED")
        self.assertEqual(seal["outcome"], "DUAL_ROUTED")
        self.assertEqual(seal["field"], "Q(sqrt(14))")
        self.assertEqual(seal["modulus"]["finite_norm"], 72)
        self.assertEqual(seal["ray_group"], [4, 2])
        self.assertEqual(seal["support_orders"], [4])

    def test_general_e_theorem_opens_e6(self) -> None:
        theory = load("data/engine-c-general-e-theory-v1.json")
        self.assertEqual(theory["claim_tag"], "VERIFIED_THEOREM")
        self.assertEqual(
            theory["specializations"]["6"]["analytic_to_unit_scale"], 3
        )
        self.assertEqual(
            theory["specializations"]["8"]["analytic_to_unit_scale"], 4
        )
        self.assertEqual(
            theory["specializations"]["12"]["analytic_to_unit_scale"], 6
        )
        self.assertEqual(
            theory["e_gt_6_decision"]["choice"], "GENERAL_E"
        )

    def test_no_aligned_e6_candidate_exists(self) -> None:
        screen = load("artifacts/aligned-e6-screen-v1.json")
        self.assertEqual(screen["candidate_count"], 10)
        self.assertEqual(screen["e6_candidate_count"], 0)
        self.assertEqual(
            screen["task_8_disposition"], "SKIP_NO_E6_CANDIDATE"
        )
        self.assertTrue(
            (ROOT / "artifacts/aligned-e6-screen-failed-v0.transcript")
            .exists()
        )

    def test_frontier_ledger_separates_index_and_splitting(self) -> None:
        ledger = load("artifacts/frontier-index-inventory-v1.json")
        audit = ledger["index_obstruction_audit"]
        self.assertEqual(ledger["record_count"], 1818)
        self.assertEqual(sum(ledger["taxonomy"].values()), 1818)
        self.assertEqual(audit["row_count"], 1100)
        self.assertEqual(audit["odd_index_above_two_count"], 88)
        self.assertEqual(
            audit["odd_index_above_two_distribution"],
            {"3": 75, "5": 6, "9": 7},
        )
        self.assertEqual(
            audit["predicate_combinations"],
            {
                "INDEX_EQ_2__SPLIT_FAIL": 13,
                "INDEX_NE_2__SPLIT_FAIL": 102,
                "INDEX_NE_2__SPLIT_PASS": 985,
            },
        )

    def test_final_frontier_norm_trend_uses_final_population(self) -> None:
        declaration = load(
            "artifacts/full-census-yield-declaration-v3.json"
        )
        trend = declaration["conductor_norm_trend"]
        self.assertEqual(
            [row["frontier"] for row in trend["quartiles"]],
            [223, 447, 509, 639],
        )
        self.assertTrue(trend["strictly_increasing"])
        self.assertEqual(
            declaration["proved_eligible_row_occurrences"], 6382
        )

    def test_b_w2_bulk_is_complete_without_w3_overclaim(self) -> None:
        coverage = load(
            "artifacts/engine-b-closure-w2-coverage-v1.json"
        )
        closure = coverage["closure_coverage"]
        occurrence = coverage["occurrence_identity_coverage"]
        self.assertEqual(closure["required"], 51)
        self.assertEqual(closure["verified_w2"], 51)
        self.assertEqual(closure["two_route_disagreements"], 0)
        self.assertEqual(closure["w3_promotions_in_campaign"], 0)
        self.assertEqual(occurrence["occurrence_transport_pending_total"], 187)


if __name__ == "__main__":
    unittest.main()
