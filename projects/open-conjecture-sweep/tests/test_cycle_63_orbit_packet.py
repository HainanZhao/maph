import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Cycle63OrbitPacketTest(unittest.TestCase):
    def test_packet_audit(self):
        subprocess.run(
            [sys.executable, str(ROOT / "proof" / "check_cycle_63_orbit_packet.py")],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        payload = json.loads(
            (ROOT / "discovery" / "out" / "cycle63-orbit-minimizer" / "packet-audit.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["exact"]["epistemic_status"], "PROVED")
        self.assertEqual(payload["schur_probe"]["epistemic_status"], "OBSERVED")
        self.assertIn("no positivity", payload["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
