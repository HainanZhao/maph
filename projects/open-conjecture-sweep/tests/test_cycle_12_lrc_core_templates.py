"""Regression test for the sealed Cycle-12 exact-template no-go."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_12_lrc_core_templates as builder


class Cycle12CoreTemplatesTest(unittest.TestCase):
    def test_exact_mapping_family_boundary(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-12-b012-lrc-core-template-v1")
        self.assertEqual(payload["certified_cores"]["count"], 100)
        self.assertEqual(payload["whole_core_no_go"]["validation_nonmatches"], 1600)
        self.assertEqual(payload["shrunk_template_no_go"]["final_clauses"], 293)
        self.assertEqual(payload["shrunk_template_no_go"]["external_nonmatches"], 100)
        self.assertEqual(len(payload["core_certificate_manifest"]), 100)


if __name__ == "__main__":
    unittest.main()
