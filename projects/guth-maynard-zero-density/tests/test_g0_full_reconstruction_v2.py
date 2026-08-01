import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]


class G0FullReconstructionV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((PROJECT / "artifacts/g0-full-reconstruction-v2.json").read_text())

    def test_correction_and_authoritative_pass(self) -> None:
        self.assertEqual(self.data["decision"]["status"], "PASS")
        self.assertEqual(self.data["decision"]["open_blockers"], [])
        self.assertEqual(self.data["counts"]["resource_routes"], 6)
        self.assertEqual(len(self.data["correction"]["v1_defects"]), 3)
        self.assertIn("premature", self.data["supersedes"])

    def test_published_source_runtime_and_six_routes(self) -> None:
        rows = {row["id"]: row for row in self.data["gate_rows"]}
        self.assertEqual(rows["G0-SOURCE-CONVENTIONS"]["epistemic_status"], "PROVED")
        self.assertEqual(len(rows["G0-RESOURCES"]["evidence"]), 6)
        self.assertEqual(self.data["runtime"]["version"], "3.12.3")
        self.assertEqual(rows["G0-RUNTIME-PIN"]["status"], "PASS")

    def test_byte_replay(self) -> None:
        subprocess.run([sys.executable, str(PROJECT / "proof/reconcile_g0_full_v2.py"), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
