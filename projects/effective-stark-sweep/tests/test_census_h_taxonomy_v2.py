from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/census-h-taxonomy-v2.json"


class CensusHTaxonomyV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(ARTIFACT.read_text())

    def test_rq0005298_uses_genuine_index(self):
        record = next(
            row for row in self.payload["records"]
            if row["case_id"] == "RQ-005298"
        )
        self.assertEqual(record["legacy_w1_shintani_index"], 2)
        self.assertEqual(record["genuine_derived_subgroup_order"], 4)
        self.assertEqual(record["shintani_index"], 4)
        self.assertFalse(record["engine_b_route_eligible"])

    def test_correction_did_not_change_route_counts(self):
        self.assertEqual(self.payload["counts"]["H_rows"], 2704)
        self.assertEqual(self.payload["counts"]["engine_b_route_eligible"], 232)
        self.assertEqual(self.payload["counts"]["engine_c_route_eligible"], 881)
        self.assertEqual(self.payload["counts"]["mechanism_status_incomplete"], 5)


if __name__ == "__main__":
    unittest.main()
