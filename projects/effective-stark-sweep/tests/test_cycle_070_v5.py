import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class Cycle070V5Test(unittest.TestCase):
    def test_b_recovery_is_complete_and_has_no_mismatch(self):
        summary = load("artifacts/genuine-b-recovery-summary-v1.json")
        self.assertEqual(summary["recovered_population"], 241)
        self.assertEqual(summary["former_proxy_passes"]["genuine_repasses"], 64)
        self.assertEqual(
            summary["former_proxy_negatives"]["new_genuine_b_passes"],
            26,
        )
        self.assertEqual(summary["mismatches"], 0)
        self.assertEqual(summary["tool_failures"], 0)

    def test_c_catchup_is_complete(self):
        summary = load("artifacts/engine-c-catchup-summary-v1.json")
        self.assertEqual(summary["catchup_case_count"], 252)
        self.assertEqual(
            summary["updated_c_accounting"]["total_certified_c_eligible"],
            881,
        )
        self.assertEqual(
            summary["case_taxonomy"],
            {
                "C_ELIGIBLE": 153,
                "HAS_TOOL_BLOCK": 1,
                "MIXED_PASS_FAIL": 3,
                "NO_PACKET_PASSES": 95,
            },
        )

    def test_full_index_ledger_is_genuine_and_complete(self):
        ledger = load("artifacts/genuine-index-ledger-8200-v3.json")
        self.assertEqual(ledger["status"], "COMPLETE")
        self.assertEqual(ledger["completed_representative_count"], 8200)
        self.assertTrue(
            all(
                row["predicate_provenance"] == "GENUINE"
                for row in ledger["records"]
            )
        )
        odd = [
            row for row in ledger["records"]
            if row["derived_subgroup_order"] > 2
            and row["derived_subgroup_order"] % 2
        ]
        self.assertEqual(len(odd), 446)
        self.assertTrue(all(row["odd_index_non_substantive"] for row in odd))

    def test_v5_accounting_and_taxonomy(self):
        v5 = load("artifacts/full-census-yield-declaration-v5.json")
        self.assertEqual(v5["predicate_provenance"], "GENUINE")
        self.assertEqual(sum(v5["histogram"].values()), 8200)
        self.assertEqual(
            v5["histogram"],
            {
                "ENGINE_A_NONTRIVIAL_ELIGIBLE": 1560,
                "ENGINE_B_ELIGIBLE": 232,
                "ENGINE_C_ELIGIBLE": 881,
                "FRONTIER": 1628,
                "PROVED_TRIVIAL": 3899,
            },
        )
        self.assertEqual(
            v5["frontier_taxonomy"],
            {
                "EXPONENT_CAP": 502,
                "INDEX_GT_2": 1088,
                "REAL_PLACE_SPLITTING_FAIL": 2,
                "TOOL_BLOCKED": 5,
                "UNIT_CONGRUENCE_FAIL": 31,
            },
        )
        self.assertEqual(len(v5["classification_records"]), 8200)
        self.assertEqual(len(v5["frontier_records"]), 1628)

    def test_v5_distinct_counts_and_trend(self):
        v5 = load("artifacts/full-census-yield-declaration-v5.json")
        self.assertEqual(
            v5["distinct_objects"]["ENGINE_B_NORMAL_CLOSURES"], 88
        )
        self.assertEqual(
            v5["distinct_objects"]["ENGINE_C_PACKET_FIELDS"], 447
        )
        self.assertTrue(
            v5["frontier_share_strictly_increases_by_norm_quartile"]
        )
        self.assertEqual(
            [
                (row["frontier"], row["total"])
                for row in v5["frontier_norm_quartiles"]
            ],
            [(189, 2245), (404, 2069), (459, 1867), (576, 2019)],
        )

    def test_v5_source_hashes_replay(self):
        v5 = load("artifacts/full-census-yield-declaration-v5.json")
        for relative, expected in v5["source_hashes"].items():
            self.assertEqual(
                hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(),
                expected,
                relative,
            )


if __name__ == "__main__":
    unittest.main()
