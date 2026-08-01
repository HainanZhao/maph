from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/reconstruct_p6_cgl_v2_route_a_v1.py"
ARTIFACT = ROOT / "artifacts/p6-cgl-v2-route-a-v1.json"


class P6CGLRouteATests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(ARTIFACT.read_text())

    def test_full_canonical_registry_and_subchecks(self) -> None:
        expected = [f"S{i:02d}" for i in range(1, 7)] + [f"L{i:02d}" for i in range(1, 13)] + [f"M{i:02d}" for i in range(1, 9)] + [f"Z{i:02d}" for i in range(1, 11)] + [f"F{i:02d}" for i in range(1, 11)]
        self.assertEqual([row["id"] for row in self.data["rows"]], expected)
        self.assertEqual(self.data["row_count"], 46)
        l12 = next(row for row in self.data["rows"] if row["id"] == "L12")
        self.assertEqual([x["id"] for x in l12["subchecks"]], ["odd_prime", "two_power"])
        self.assertEqual(self.data["l12_subcheck_count"], 2)

    def test_open_rows_and_no_silent_repairs(self) -> None:
        rows = {row["id"]: row for row in self.data["rows"]}
        for row_id in ("S06", "Z03", "Z05", "Z06", "F08"):
            self.assertTrue(rows[row_id]["disposition"].startswith("OPEN_ANALYTIC_INPUT"))
        self.assertIn("no q<=T^C restriction", self.data["claim_boundary"])
        self.assertEqual(self.data["status"], "OPEN_ANALYTIC_INPUT")

    def test_exact_q1_equals_q_algebra(self) -> None:
        self.assertEqual(self.data["exact_algebra"]["identities"]["7/3-9/4"], "1/12")
        self.assertEqual(self.data["exact_algebra"]["identities"]["7/3-30/13"], "1/39")
        self.assertEqual(self.data["exact_algebra"]["identities"]["B_at_beta_1"], "(10-sqrt(10))/3")

    def test_replay_and_identity(self) -> None:
        replay = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertEqual(self.data["replay"]["script_sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
