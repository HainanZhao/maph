"""Regression tests for the first ten research cycles."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Cycles001010Test(unittest.TestCase):
    def test_research_has_no_administrative_gate(self) -> None:
        record = json.loads(
            (ROOT / "data" / "research-activation-v3.json").read_text()
        )
        self.assertTrue(record["activated"])
        self.assertEqual(
            record["verdict"],
            "RESEARCH_ACTIVE_NO_EXTERNAL_SEQUENCING_GATE",
        )

    def test_all_seven_anchors_reproduced(self) -> None:
        result = json.loads(
            (ROOT / "artifacts" / "anchor-reproduction-v1.json").read_text()
        )
        self.assertEqual(result["expected_anchor_count"], 7)
        self.assertEqual(result["completed_anchor_count"], 7)
        self.assertTrue(all(row["passed"] for row in result["records"]))
        for row in result["records"]:
            transcript = ROOT / row["transcript"]
            self.assertTrue(transcript.is_file())
            self.assertEqual(
                hashlib.sha256(transcript.read_bytes()).hexdigest(),
                row["transcript_sha256"],
            )

    def test_anchor_structural_regression(self) -> None:
        result = json.loads(
            (ROOT / "artifacts" / "w1-anchor-regression-v1.json").read_text()
        )
        self.assertEqual(result["anchor_count"], 7)
        self.assertEqual(result["passed_count"], 7)
        self.assertEqual(result["failed"], [])

    def test_full_ideal_backbone(self) -> None:
        census = json.loads(
            (ROOT / "artifacts" / "frozen-ideal-census-v1.json").read_text()
        )
        self.assertEqual(census["field_count"], 121)
        self.assertEqual(census["raw_ideal_count"], 13939)
        self.assertEqual(census["deduplicated_case_count"], 8200)
        self.assertTrue(census["all_bnfcertify"])
        self.assertEqual(len(census["cases"]), 8200)
        identities = {
            (row["D"], tuple(map(tuple, row["finite_ideal_hnf"])))
            for row in census["cases"]
        }
        self.assertEqual(len(identities), 8200)

    def test_pilot_partition_and_tags(self) -> None:
        pilot = json.loads(
            (ROOT / "artifacts" / "w1-pilot-v1.json").read_text()
        )
        self.assertEqual(pilot["scope"]["case_count"], 66)
        self.assertEqual(
            pilot["verdict_counts"],
            {"FRONTIER": 1, "ROUTE_CANDIDATE": 65},
        )
        self.assertEqual(
            pilot["engine_counts"], {"A": 59, "B": 1, "C": 5}
        )
        for row in pilot["records"]:
            if row["verdict"] == "ROUTE_CANDIDATE":
                self.assertIn(row["engine"], {"A", "B", "C"})
                self.assertEqual(row["obstruction"], "NONE")
            else:
                self.assertEqual(row["engine"], "NONE")
                self.assertNotEqual(row["obstruction"], "NONE")
            self.assertEqual(row["bnfcertify"], 1)

    def test_new_b_candidate_and_frontier_control(self) -> None:
        pilot = json.loads(
            (ROOT / "artifacts" / "w1-pilot-v1.json").read_text()
        )
        records = {row["case_id"]: row for row in pilot["records"]}
        b_case = records["RQ-000190"]
        self.assertEqual(b_case["d"], 7)
        self.assertEqual(b_case["finite_norm"], 7)
        self.assertEqual(b_case["support_orders"], [2, 6])
        self.assertEqual(b_case["shintani_index"], 2)
        self.assertEqual(b_case["engine"], "B")
        frontier = records["RQ-000324"]
        self.assertEqual(frontier["d"], 11)
        self.assertEqual(frontier["support_orders"], [8])
        self.assertEqual(frontier["shintani_index"], 4)
        self.assertEqual(frontier["obstruction"], "INDEX_GT_2")


if __name__ == "__main__":
    unittest.main()
