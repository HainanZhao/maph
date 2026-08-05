import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Cycle66PivotAuditTest(unittest.TestCase):
    def test_packet(self):
        subprocess.run(
            [sys.executable, str(ROOT / "proof" / "check_cycle_66_pivot_audit.py")],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        payload = json.loads(
            (ROOT / "discovery/out/cycle66-pivot-audit/packet-audit.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(payload["status"], "PASS")
        self.assertFalse(payload["logical_interface"]["fixed_s3_implies_sidorenko"])
        self.assertEqual(payload["banked_reduction"]["resultant_u_degree"], 26)
        self.assertEqual(payload["novelty"]["epistemic_status"], "CONJECTURED")


if __name__ == "__main__":
    unittest.main()
