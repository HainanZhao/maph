#!/usr/bin/env python3
"""Regression gate for exhaustion of reusable direct-source batches."""
from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DirectSourceCompletionTest(unittest.TestCase):
    def test_all_remaining_direct_source_batches_are_exact_no_go(self) -> None:
        b5086 = json.loads((ROOT / "artifacts/b5086-transport-geometry-v1.json").read_text())
        final = json.loads((ROOT / "artifacts/final-direct-source-coprime-screen-v1.json").read_text())
        self.assertEqual((b5086["claim_tag"], b5086["eligible_count"], len(b5086["records"])),
                         ("PROVED_EXACT_TRANSPORT_GEOMETRY", 0, 7))
        self.assertEqual({row["closure_id"]: row["eligible_count"] for row in final["closures"]},
                         {"B5-021": 0, "B5-033": 0})


if __name__ == "__main__":
    unittest.main()
