import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/reconcile_g0_full_v3.py"


class G0FullReconstructionV3Tests(unittest.TestCase):
    def test_normal_replay_and_authority(self) -> None:
        completed = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(completed.stdout)["status"], "PASS")
        data = json.loads((PROJECT / "artifacts/g0-full-reconstruction-v3.json").read_text())
        self.assertEqual(data["decision"]["status"], "PASS")
        self.assertEqual(data["runtime"]["optimize"], 0)
        self.assertIn("replay-hardening", data["supersedes"])

    def test_optimized_replay_fails_closed(self) -> None:
        completed = subprocess.run([sys.executable, "-O", str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("forbids -O/-OO", completed.stderr)


if __name__ == "__main__":
    unittest.main()
