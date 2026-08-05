from pathlib import Path
import subprocess
import sys
import unittest


class Cycle75ExactTemplateControls(unittest.TestCase):
    def test_replay(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "proof/verify_cycle75_kkt_boundary_reduction.py"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("OK: C75 template", result.stdout)


if __name__ == "__main__":
    unittest.main()
