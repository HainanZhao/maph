"""Regression tests for theorem-first cycles 011--020."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Cycles011020Test(unittest.TestCase):
    def test_q7_two_route_and_divisor_certificates(self) -> None:
        two_route = (
            ROOT / "artifacts" / "q7-p7-w2-two-route-v1.txt"
        ).read_text()
        self.assertIn("TWO_ROUTE_FULL_RAY_MATCH_COUNT=2", two_route)
        self.assertIn("HALT_TWO_ROUTE_MISMATCH=0", two_route)
        self.assertIn("Q7_P7_W2_TWO_ROUTE_CERTIFIED=1", two_route)
        divisor = (
            ROOT / "artifacts" / "q7-p7-w2-divisor-table-v1.txt"
        ).read_text()
        self.assertIn("SHINTANI_DIVISOR_COUNT=2", divisor)
        self.assertIn("SHINTANI_SAFE_EXPONENT=4032", divisor)
        self.assertIn(
            "REAL_DISTRIBUTION_DENOMINATORS_CLEARED=1", divisor
        )

    def test_failed_uniqueness_assumptions_preserved(self) -> None:
        first = (
            ROOT / "artifacts" / "q7-w2-failed-unique-base-v1.txt"
        ).read_text()
        second = (
            ROOT / "artifacts" / "q7-w2-failed-single-full-ray-v2.txt"
        ).read_text()
        self.assertIn(
            "ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT: expected 1, got 2",
            first,
        )
        self.assertIn(
            "TWO_ROUTE_FULL_RAY_MATCH_COUNT: expected 1, got 2", second
        )

    def test_q7_w3_exact_candidate_and_arb_closure(self) -> None:
        exact = (
            ROOT / "artifacts" / "q7-p7-w3-exact-candidate-v1.txt"
        ).read_text()
        self.assertIn("PACKET_ABSOLUTE_IRREDUCIBLE=1", exact)
        self.assertIn("K_COMPATIBLE_RAY_ISOMORPHISM_COUNT=6", exact)
        self.assertIn("Q7_P7_W3_ANALYTIC_ARB_GATE=PENDING", exact)
        # This line is preserved in the historical algebraic-half
        # transcript. Promotion occurs only in the later Arb artifact.
        enclosed = (
            ROOT / "artifacts" / "q7-p7-w3-arb-certificate-v1.txt"
        ).read_text()
        self.assertIn("Q7_P7_ANALYTIC_ARB_CERTIFIED=1", enclosed)
        self.assertIn("Q7_P7_PACKET_IDENTITY_VERIFIED=1", enclosed)
        self.assertIn("VOUTIER_MARGIN=", enclosed)
        numerical = (
            ROOT / "artifacts" / "q7-p7-w3-recognition-v1.txt"
        ).read_text()
        self.assertIn("CLAIM_TAG=NUMERICAL_NOT_ENCLOSED", numerical)
        case = json.loads(
            (ROOT / "data" / "q7-p7-case-v1.json").read_text()
        )
        self.assertEqual(case["w2"]["safe_exponent"], 4032)
        self.assertEqual(
            case["w3"]["packet_identity_verdict"], "VERIFIED"
        )
        self.assertFalse(
            case["w3"]["analytic_arb_enclosure"][
                "pari_l_value_in_proof_chain"
            ]
        )

    def test_full_census_histograms(self) -> None:
        census = json.loads(
            (ROOT / "artifacts" / "w1-full-census-v1.json").read_text()
        )
        self.assertEqual(census["scope"]["case_count"], 8200)
        self.assertEqual(
            census["engine_counts"], {"A": 5459, "B": 655, "C": 817}
        )
        self.assertEqual(
            census["obstruction_counts"],
            {
                "EXPONENT_CAP": 156,
                "INDEX_GT_2": 1080,
                "UNIT_CONGRUENCE_FAIL": 33,
            },
        )

    def test_spotchecks_and_yield(self) -> None:
        spots = json.loads(
            (ROOT / "artifacts" / "w1-spotchecks-v1.json").read_text()
        )
        self.assertEqual(spots["case_count"], 10)
        self.assertEqual(spots["passed_count"], 10)
        analysis = json.loads(
            (ROOT / "artifacts" / "w1-census-analysis-v1.json").read_text()
        )
        self.assertEqual(
            analysis["yield_checkpoint"]["verdict"],
            "PASS_CENSUS_PAPER_FRAMING",
        )
        self.assertEqual(
            analysis["yield_checkpoint"][
                "structural_route_candidates_beyond_anchors"
            ],
            6928,
        )
        self.assertTrue(
            analysis[
                "frontier_share_strictly_increases_by_norm_quartile"
            ]
        )

    def test_identification_batch_order(self) -> None:
        batches = json.loads(
            (ROOT / "artifacts" / "identification-batches-v1.json").read_text()
        )
        self.assertEqual(batches["ordering"], ["C", "B", "A"])
        self.assertEqual(
            [(row["engine"], row["case_count"]) for row in batches["batches"]],
            [("C", 817), ("B", 655), ("A", 5459)],
        )
        self.assertEqual(batches["pre_bulk_spotchecks"], "10/10 PASSED")


if __name__ == "__main__":
    unittest.main()
