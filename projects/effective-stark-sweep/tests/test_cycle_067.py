import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Cycle067Test(unittest.TestCase):
    def test_engine_d_corrected_population_is_empty(self):
        audit = load(
            "artifacts/engine-d-modulus-stability-audit-v1.json"
        )
        counts = audit["counts"]
        self.assertEqual(
            counts["former_index_one_abelian_proxy_occurrences"], 3521
        )
        self.assertEqual(
            counts["galois_stable_modulus_occurrences"], 1042
        )
        self.assertEqual(
            counts["corrected_substantive_engine_d_occurrences"], 0
        )
        self.assertEqual(
            counts["invalidated_unstable_substantive_occurrences"], 276
        )
        self.assertEqual(
            audit["former_3521_overlap_partition"],
            {
                "engine_a_substantive": 693,
                "invalidated_unstable_modulus_substantive": 276,
                "proved_trivial_empty_support": 2552,
            },
        )

    def test_all_three_former_anchors_are_exact_negative_controls(self):
        anchors = load("artifacts/engine-d-anchor-rejections-v1.json")
        self.assertEqual(anchors["claim_tag"], "VERIFIED_NEGATIVE_ANCHOR_BUNDLES")
        expected = {
            "RQ-000018": [8, 4],
            "RQ-000032": [6, 3],
            "RQ-000274": [4, 2],
        }
        self.assertEqual(len(anchors["records"]), 3)
        for record in anchors["records"]:
            exact = record["exact"]
            self.assertEqual(
                exact["finite_modulus_galois_stable"], 0
            )
            self.assertEqual(exact["mixed_signature"], 1)
            self.assertEqual(
                exact["one_place_absolute_signature"],
                expected[record["case_id"]],
            )
            transcript = ROOT / record["transcript"]
            self.assertEqual(sha(transcript), record["transcript_sha256"])

    def test_census_containment_quarantines_exactly_64_b_rows(self):
        audit = load(
            "artifacts/conjugation-dependent-census-audit-v1.json"
        )
        self.assertEqual(
            audit["formal_split_exposure"]["ENGINE_B_ELIGIBLE"],
            {
                "total": 195,
                "galois_stable_finite_modulus": 131,
                "galois_unstable_finite_modulus": 64,
            },
        )
        self.assertEqual(
            len(
                audit["engine_b_containment"][
                    "quarantined_unstable_case_ids"
                ]
            ),
            64,
        )
        self.assertTrue(all(audit["banked_headline_controls"].values()))

    def test_odd_index_law_is_retracted_and_five_exceptions_are_banked(self):
        correction = load(
            "artifacts/frontier-odd-index-stability-correction-v1.json"
        )
        self.assertEqual(
            correction["population"],
            {
                "rows": 88,
                "galois_stable_finite_moduli": 0,
                "galois_unstable_finite_moduli": 88,
            },
        )
        files = correction["exception_files"]
        self.assertEqual(len(files), 5)
        self.assertEqual(
            sum(row["exception_type"] == "INDEX_3_COMMUTATOR_6" for row in files),
            3,
        )
        self.assertEqual(
            sum(
                row["exception_type"] == "SUPPORT_NO_COMMON_ODD_PRIME"
                for row in files
            ),
            2,
        )
        for record in files:
            path = ROOT / record["path"]
            self.assertEqual(sha(path), record["sha256"])
            self.assertFalse(
                load(record["path"])["finite_modulus_galois_stable"]
            )

    def test_requested_v3_promotion_is_preserved_as_rejected(self):
        split = load(
            "artifacts/census-split-v3-engine-d-proposal-rejected-v1.json"
        )
        self.assertEqual(split["claim_tag"], "REJECTED_PROPOSED_PROMOTION")
        self.assertEqual(split["corrected_engine_d_substantive_occurrences"], 0)
        self.assertEqual(
            split["proposed_but_rejected_split"],
            {
                "frontier_after": 1542,
                "frontier_before": 1818,
                "substantive_eligible_after": 2759,
                "substantive_eligible_before": 2483,
            },
        )

    def test_new_artifact_source_hashes_replay(self):
        paths = [
            "artifacts/engine-d-modulus-stability-audit-v1.json",
            "artifacts/engine-d-anchor-rejections-v1.json",
            "artifacts/conjugation-dependent-census-audit-v1.json",
            "artifacts/frontier-odd-index-stability-correction-v1.json",
        ]
        for artifact_path in paths:
            artifact = load(artifact_path)
            for relative, expected in artifact["source_hashes"].items():
                self.assertEqual(
                    sha(ROOT / relative),
                    expected,
                    f"{artifact_path}: {relative}",
                )


if __name__ == "__main__":
    unittest.main()
