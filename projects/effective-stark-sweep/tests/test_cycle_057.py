"""Regression tests for the post-Q(sqrt(7)) verification block."""

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


class Cycle057Test(unittest.TestCase):
    def test_ranked_w3_closures_are_verified(self) -> None:
        paths = [
            "data/rq000108-case-v1.json",
            "data/rq000021-case-v1.json",
            "data/rq002955-case-v1.json",
            "data/q33-p11-order10-case-v1.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(load(path)["verdict"], "VERIFIED")

    def test_order_ten_frozen_height_gate(self) -> None:
        case = load("data/q33-p11-order10-case-v1.json")
        identification = case["identification"]
        self.assertEqual(
            identification["maximum_packet_comparison_degree"], 40
        )
        self.assertEqual(identification["certified_degree_cap"], 80)
        self.assertLess(
            float(identification["raw_log_error_upper"]),
            float(identification["raw_log_error_target"]),
        )
        self.assertGreaterEqual(
            int(identification["voutier_margin_lower"]), 100
        )
        self.assertEqual(
            identification["certificate_hashes"][
                "arb_certificate_sha256"
            ],
            digest("artifacts/rq001107-w3-arb-certificate-v1.transcript"),
        )

    def test_full_census_declaration_closes_yield_gate(self) -> None:
        declaration = load(
            "artifacts/full-census-yield-declaration-v1.json"
        )
        self.assertEqual(
            declaration["corrected_engine_histogram"]["FRONTIER"][
                "row_occurrences"
            ],
            1818,
        )
        self.assertEqual(
            sum(declaration["frontier_taxonomy"].values()), 1818
        )
        self.assertGreaterEqual(
            declaration["proved_eligible_beyond_seven_anchors"],
            declaration["pre_registered_threshold"],
        )
        self.assertTrue(
            declaration["conductor_norm_trend"]["strictly_increasing"]
        )

    def test_dimension_16_has_final_named_failure(self) -> None:
        result = load("artifacts/d16-corrected-battery-v1.json")
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["frontier_taxonomy"], "INDEX_GT_2")
        self.assertEqual(result["observed_shintani_index"], 16)
        self.assertEqual(result["record"]["maximal_one_ray_structure"],
                         [16, 4, 2])

    def test_dual_case_is_exactly_dual_proved(self) -> None:
        case = load("data/rq000458-dual-case-v1.json")
        self.assertEqual(case["verdict"], "DUAL_PROVED")
        self.assertTrue(case["packet"]["same_modulus"])
        self.assertTrue(case["packet"]["identical_packet_polynomial"])
        self.assertEqual(
            {
                case["engine_b"]["theorem_base"].split()[0],
                case["engine_c"]["theorem_base"].split()[0],
            },
            {"Shintani", "Stark"},
        )

    def test_q6_remains_blocked_before_arb(self) -> None:
        case = load("data/q6-norm8-case-v1.json")
        identification = case["identification"]
        self.assertTrue(
            identification["state"].startswith("BLOCKED_BEFORE_ARB")
        )
        self.assertEqual(
            len(identification["required_promotion_gates"]), 3
        )


if __name__ == "__main__":
    unittest.main()
