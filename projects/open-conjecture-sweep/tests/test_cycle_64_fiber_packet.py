import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Cycle64FiberPacketTest(unittest.TestCase):
    def test_packet(self):
        subprocess.run(
            [sys.executable, str(ROOT / "proof" / "check_cycle_64_fiber_packet.py")],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        payload = json.loads(
            (ROOT / "discovery" / "out" / "cycle64-fiber-minimization" / "packet-audit.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["exact_reduction"]["resultant_u_degree"], 26)
        self.assertTrue(payload["exact_reduction"]["top_coefficient_nonzero_constant"])
        self.assertIn("no sign", payload["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
