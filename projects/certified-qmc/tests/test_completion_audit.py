from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

from src.certificate import canonical_sha256


ROOT = Path(__file__).resolve().parents[1]


class CompletionAuditTests(unittest.TestCase):
    def test_completion_audit_is_self_hashed_and_requirement_complete(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "audit_production_phase_completion.py"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout)
        supplied = payload.pop("audit_sha256")
        self.assertEqual(supplied, canonical_sha256(payload))
        self.assertEqual(len(payload["checks"]), 14)
        names = {
            row["requirement"] for row in payload["checks"]
        }
        for cycle in ("Cycle 013", "Cycle 014", "Cycle 015",
                      "Cycles 016-017", "Cycle 018", "Cycle 019"):
            self.assertTrue(
                any(name.startswith(cycle) for name in names),
                cycle,
            )
        counted = sum(payload["counts"].values())
        self.assertEqual(counted, len(payload["checks"]))
        self.assertIn(
            payload["overall"], ("IN_PROGRESS", "COMPLETE", "FAILED")
        )

    def test_post_release_register_retains_all_promotion_controls(self):
        text = (
            ROOT / "docs" / "post-release-optimization-register.md"
        ).read_text()
        for required in (
            "Montgomery",
            "SIMD",
            "dual-shadow",
            "bit-identical",
            "published DOI",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
