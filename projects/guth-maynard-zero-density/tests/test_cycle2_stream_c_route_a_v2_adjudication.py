"""Regression test for the independent Route-A v2 containment audit."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "check_cycle_2_stream_c_route_a_v2_adjudication.py"


class RouteAV2AdjudicationTests(unittest.TestCase):
    def test_negative_audit_replays(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, text=True)
        self.assertIn("CONTAINMENT", result.stdout)
        self.assertIn("almost-all", result.stdout)
        self.assertIn("archival published-primary subgate remains open", result.stdout)


if __name__ == "__main__":
    unittest.main()
