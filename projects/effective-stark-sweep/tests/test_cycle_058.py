"""Regression tests for theorem and bulk-gate cycle 058."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Cycle058Test(unittest.TestCase):
    def test_yield_has_trivial_substantive_and_c_scope_split(self):
        data = load("artifacts/full-census-yield-declaration-v2.json")
        histogram = data["corrected_engine_histogram"]
        self.assertEqual(histogram["PROVED_TRIVIAL"]["row_occurrences"],
                         3899)
        substantive = sum(
            histogram[key]["row_occurrences"]
            for key in (
                "ENGINE_A_NONTRIVIAL_ELIGIBLE",
                "ENGINE_B_ELIGIBLE",
                "ENGINE_C_ELIGIBLE",
            )
        )
        self.assertEqual(substantive, 2483)
        self.assertEqual(
            histogram["ENGINE_C_ELIGIBLE"]["packet_occurrences"], 1163
        )
        self.assertEqual(
            data["engine_c_all_geometry_passes"]["packet_occurrences"],
            1255,
        )

    def test_uniform_engine_a_theorem_opens_bulk(self):
        theorem = load("data/engine-a-uniform-theorem-v1.json")
        self.assertEqual(theorem["claim_tag"], "VERIFIED_THEOREM")
        self.assertEqual(
            theorem["relative_index_definition"].split()[0], "I_chi"
        )
        self.assertEqual(
            theorem["bulk_gate"], "OPEN_FOR_FINITE_VERIFICATION"
        )
        for anchor in theorem["anchor_transcripts"]:
            self.assertEqual(
                anchor["sha256"], digest(ROOT / anchor["path"])
            )

    def test_engine_c_e_inventory_is_complete(self):
        data = load("artifacts/engine-c-e-inventory-v1.json")
        self.assertEqual(data["scope"]["eligible_case_count"], 728)
        self.assertEqual(
            data["scope"]["eligible_packet_occurrence_count"], 1163
        )
        self.assertEqual(data["scope"]["distinct_packet_field_count"],
                         393)
        self.assertEqual(
            data["field_minimum_e_histogram"],
            {"2": 227, "4": 90, "6": 75, "8": 1},
        )
        self.assertEqual(
            data["occurrence_minimum_e_histogram"],
            {"2": 404, "4": 292, "6": 457, "8": 10},
        )
        self.assertTrue(data["banked_e_2_4_dominates_fields"])
        self.assertTrue(data["banked_e_2_4_dominates_occurrences"])
        self.assertEqual(
            sum(
                item["case_count"]
                for item in data["case_staging"].values()
            ),
            728,
        )

    def test_bulk_plan_has_exact_remaining_counts(self):
        data = load("artifacts/post-theorem-bulk-plan-v1.json")
        self.assertEqual(data["engine_b"]["remaining_closure_count"], 51)
        self.assertEqual(
            data["engine_b"]["remaining_closure_occurrence_count"], 159
        )
        self.assertEqual(
            data["engine_b"]["unverified_members_of_banked_closures"],
            28,
        )
        self.assertEqual(
            data["engine_b"]["remaining_occurrence_identities"], 187
        )
        self.assertEqual(
            data["remaining_overlap_alignment_queue"]["candidate_count"],
            10,
        )

    def test_remaining_overlaps_are_alignment_only(self):
        data = load("artifacts/remaining-dual-alignments-v1.json")
        self.assertEqual(data["candidate_count"], 10)
        self.assertEqual(data["aligned_count"], 10)
        self.assertTrue(
            all(
                record["state"] == "ALIGNED_NOT_DUAL_PROVED"
                for record in data["records"]
            )
        )

    def test_dual_case_and_paper_iii_seals(self):
        case = load("data/rq000458-dual-case-v1.json")
        self.assertEqual(case["sealed_at_utc"], "2026-07-30T05:15:41Z")
        self.assertEqual(case["modulus"]["finite_norm"], 72)
        seal = load("artifacts/paper-iii-sweep-citation-seal-v1.json")
        paper = REPO / (
            "projects/sic-stark/paper/"
            "sic-stark-dimension-six-boundary-fusion.tex"
        )
        pdf = paper.with_suffix(".pdf")
        self.assertEqual(seal["paper_iii_source_sha256"], digest(paper))
        self.assertEqual(seal["paper_iii_pdf_sha256"], digest(pdf))
        self.assertEqual(
            seal["dimension_16_resolution"]["observed_shintani_index"],
            16,
        )


if __name__ == "__main__":
    unittest.main()
