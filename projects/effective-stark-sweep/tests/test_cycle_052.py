"""Regression tests for the corrected-battery repair and protocol changes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


class Cycle052Test(unittest.TestCase):
    def test_q7_headline_case_remains_verified(self) -> None:
        case = load("data/q7-p7-case-v1.json")
        self.assertEqual(case["theorem_claim"]["claim_tag"], "VERIFIED")
        self.assertEqual(case["w2"]["safe_exponent"], 4032)
        self.assertGreaterEqual(
            int(
                case["w3"]["analytic_arb_enclosure"][
                    "certified_margin_lower"
                ]
            ),
            5688,
        )

    def test_corrected_anchor_battery_is_complete(self) -> None:
        end_to_end = load(
            "artifacts/corrected-battery-anchor-reproduction-v1.json"
        )
        w1 = load("artifacts/corrected-battery-w1-anchor-screen-v1.json")
        routed_b = load("artifacts/corrected-battery-anchor-b-v1.json")
        self.assertEqual(end_to_end["verdict"], "ANCHOR_GATE_PASSED")
        self.assertEqual(end_to_end["completed_anchor_count"], 7)
        self.assertEqual(w1["passed_count"], 7)
        self.assertEqual(
            routed_b["verdict"], "CORRECTED_B_ROUTED_ANCHORS_PASSED"
        )
        self.assertEqual(routed_b["passed_anchor_count"], 3)

    def test_all_195_prior_b_passes_were_freshly_rescreened(self) -> None:
        data = load("artifacts/corrected-battery-b195-v1.json")
        self.assertEqual(
            data["verdict"], "CORRECTED_BATTERY_195_OF_195_PASSED"
        )
        self.assertEqual(data["completed_case_count"], 195)
        self.assertEqual(data["passed_case_count"], 195)
        self.assertEqual(
            len({record["case_id"] for record in data["records"]}), 195
        )
        for record in data["records"]:
            self.assertTrue(record["passed"])
            self.assertTrue(all(record["checks"].values()))
            self.assertGreater(
                record["actual"][
                    "route1_abelian_imaginary_base_count"
                ],
                0,
            )
            self.assertGreater(
                record["actual"]["two_route_ray_subfield_match_count"],
                0,
            )

    def test_corrected_battery_summary_hashes_its_inputs(self) -> None:
        summary = load("artifacts/corrected-battery-summary-v1.json")
        self.assertEqual(
            summary["verdict"], "CORRECTED_BATTERY_GATE_CLOSED"
        )
        anchor = summary["anchor_gate"]
        self.assertEqual(
            anchor["end_to_end_reproduction"]["sha256"],
            digest(
                "artifacts/corrected-battery-anchor-reproduction-v1.json"
            ),
        )
        self.assertEqual(
            anchor["w1_structural_screen"]["sha256"],
            digest(
                "artifacts/corrected-battery-w1-anchor-screen-v1.json"
            ),
        )
        self.assertEqual(
            anchor[
                "currently_b_routed_corrected_two_route_screen"
            ]["sha256"],
            digest("artifacts/corrected-battery-anchor-b-v1.json"),
        )
        population = summary["population_gate"]
        self.assertEqual(
            population["sha256"],
            digest("artifacts/corrected-battery-b195-v1.json"),
        )
        self.assertEqual(
            population["transcript_sha256"],
            digest("artifacts/corrected-battery-b195-v1.transcript"),
        )

    def test_q6_arb_gate_has_all_three_inherited_obligations(self) -> None:
        case = load("data/q6-norm8-case-v1.json")
        identification = case["identification"]
        self.assertTrue(
            identification["state"].startswith("BLOCKED_BEFORE_ARB")
        )
        self.assertEqual(
            len(identification["required_promotion_gates"]), 3
        )
        joined = " ".join(identification["required_promotion_gates"])
        self.assertIn("e=8", joined)
        self.assertIn("eight", joined)
        self.assertIn("Q(sqrt(-3))", joined)

    def test_dimension_six_analogue_is_promoted(self) -> None:
        case = load("data/q57-norm27-case-v1.json")
        self.assertEqual(case["case_id"], "RQ-002057")
        self.assertEqual(
            case["local_shape"]["ramified_rational_prime"], 3
        )
        self.assertEqual(
            case["local_shape"]["fourier_support_orders"], [2, 6]
        )
        self.assertEqual(case["exponent"]["safe_exponent"], 2592)
        self.assertEqual(
            [
                row["clearing_exponent"]
                for row in case["exponent"]["divisor_rows"]
            ],
            [864, 324, 108],
        )
        self.assertEqual(
            case["engine_b"]["two_route_transcript_sha256"],
            digest("artifacts/rq57-norm27-w2-two-route-v1.transcript"),
        )
        self.assertEqual(
            case["exponent"]["divisor_table_transcript_sha256"],
            digest(
                "artifacts/rq57-norm27-w2-divisor-table-v1.transcript"
            ),
        )
        self.assertEqual(
            case["significance"]["priority"],
            "PROMOTED_ABOVE_RQ-000021",
        )

    def test_order_ten_height_window_is_explicit(self) -> None:
        case = load("data/q33-p11-order10-case-v1.json")
        window = case["height_window"]
        self.assertEqual(
            window["maximum_packet_comparison_degree_cap"], 80
        )
        self.assertEqual(window["minimum_occurs_at_degree"], 3)
        self.assertGreater(
            float(window["minimum_voutier_lower_bound"]), 5.22e-5
        )
        self.assertGreater(
            float(window["degree_80_voutier_bound"]), 1.19e-4
        )
        self.assertLess(
            float(window["raw_log_error_ceiling_for_100x_margin"]),
            3.31e-11,
        )

    def test_packet_level_dual_engine_queue_is_not_overclaimed(self) -> None:
        data = load("artifacts/dual-engine-alignment-queue-v1.json")
        self.assertEqual(data["candidate_count"], 11)
        self.assertEqual(len(data["records"]), 11)
        for record in data["records"]:
            self.assertEqual(
                record["state"],
                "ELEVATED_SAME_PACKET_ALIGNMENT_REQUIRED",
            )
            self.assertIn(
                "not yet two proofs", record["claim_boundary"]
            )
        self.assertIn(
            "same exact packet", data["protocol"]["promotion_gate"]
        )

    def test_amended_execution_order(self) -> None:
        order = load("data/closure-execution-order-v2.json")
        self.assertEqual(
            order["gates_now_closed"],
            {
                "seven_anchor_corrected_battery": True,
                "all_195_b_passes_corrected_battery": True,
            },
        )
        self.assertEqual(
            order["execution_order"][1]["case_id"], "RQ-002057"
        )
        self.assertEqual(order["blocked"][0]["case_id"], "RQ-000129")
        self.assertEqual(order["deferred"][0]["safe_exponent"], 13810176)


if __name__ == "__main__":
    unittest.main()
