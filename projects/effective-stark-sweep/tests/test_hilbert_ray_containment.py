#!/usr/bin/env python3
"""Regression checks for the exact Cohen--Roblot object controls."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HilbertRayContainmentTest(unittest.TestCase):
    def test_four_frozen_controls(self) -> None:
        first = json.loads((ROOT / "artifacts/b5079-hilbert-ray-containment-v1.json").read_text())
        tranche = json.loads((ROOT / "artifacts/hilbert-ray-containment-tranche-v1.json").read_text())
        self.assertEqual(first["claim_tag"], "PROVED_EXACT_SUBFIELD_TEST")
        self.assertEqual((first["degree4_subfield_count"],
                          first["hilbert_field_match_count"],
                          first["hilbert_field_contained"]), (11, 1, True))
        self.assertEqual(tranche["claim_tag"], "PROVED_EXACT_SUBFIELD_TEST")
        observed = {
            row["base_radicand"]: (row["case_id"],
                                    row["normal_closure_degree"],
                                    row["degree4_subfield_count"],
                                    row["hilbert_field_match_count"],
                                    row["hilbert_field_contained"])
            for row in tranche["records"]
        }
        self.assertEqual(observed, {
            42: ("RQ-001569", 16, 7, 1, True),
            51: ("RQ-001894", 16, 7, 0, False),
            186: ("RQ-007519", 16, 7, 1, True),
        })


if __name__ == "__main__":
    unittest.main()
