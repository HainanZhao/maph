"""Regression coverage for the bounded G0 v2 hostile audit."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_g0_v2_hostile_v1.py"


class G0V2HostileAuditV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((PROJECT / "artifacts/g0-v2-hostile-audit-v1.json").read_text())

    def test_normal_source_and_six_route_scope(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "OBSERVED")
        self.assertEqual(self.data["normal_frozen_command"]["status"], "PASS")
        self.assertEqual(self.data["published_source_classification"]["epistemic_status"], "PROVED")
        resource = self.data["six_route_resource_semantics"]
        self.assertEqual(resource["status"], "PASS")
        self.assertEqual(len(resource["route_ids"]), 6)
        self.assertEqual(resource["strict_limits"]["wall_seconds_strictly_less_than"], 60)

    def test_optimized_bypass_is_preserved_as_containment(self) -> None:
        probe = self.data["optimization_mode_probe"]
        self.assertEqual(probe["status"], "CONTAINED_OPTIMIZATION_BYPASS_OBSERVED")
        self.assertEqual(probe["result"], "exit status 0")
        self.assertFalse(self.data["recommendation"]["standalone_optimization_robustness"])

    def test_byte_replay(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
