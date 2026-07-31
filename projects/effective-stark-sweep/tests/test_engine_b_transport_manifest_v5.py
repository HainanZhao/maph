from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/engine-b-transport-manifest-v5.json"
PREREGISTRATION = ROOT / "data/census-paper-preregistration-amendment-v12.json"


class EngineBTransportManifestV5Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(ARTIFACT.read_text())

    def test_v5_scope_reconciles_historical_population(self):
        counts = self.payload["counts"]
        self.assertEqual(counts["v5_engine_b_rows"], 232)
        self.assertEqual(counts["v5_distinct_normal_closures"], 88)
        self.assertEqual(counts["historical_v4_engine_b_rows_retained"], 195)
        self.assertEqual(counts["historical_pending_member_ids_retained"], 159)
        self.assertEqual(counts["new_v5_engine_b_rows"], 37)
        self.assertEqual(counts["v5_rows_outside_historical_pending_member_list"], 73)

    def test_no_member_is_promoted_by_the_manifest(self):
        boundary = self.payload["claim_boundary"]
        self.assertFalse(boundary["closure_membership_proves_member_packet"])
        self.assertFalse(boundary["banked_representative_promotes_other_members"])
        self.assertFalse(boundary["member_transport_completed"])
        self.assertEqual(self.payload["counts"]["member_transport_completed"], 0)
        self.assertTrue(all(
            member["transport_status"] == "UNSTARTED_NO_CASE_LEVEL_PACKET_CLAIM"
            for member in self.payload["members"]
        ))

    def test_grouping_is_a_partition(self):
        closure_members = {
            case_id
            for closure in self.payload["closures"]
            for case_id in closure["member_ids"]
        }
        member_ids = {member["case_id"] for member in self.payload["members"]}
        self.assertEqual(len(self.payload["closures"]), 88)
        self.assertEqual(closure_members, member_ids)
        self.assertEqual(len(member_ids), 232)

    def test_artifact_records_the_frozen_preregistration(self):
        self.assertEqual(
            self.payload["source_hashes"][
                "data/census-paper-preregistration-amendment-v12.json"
            ],
            hashlib.sha256(PREREGISTRATION.read_bytes()).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
