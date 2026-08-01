from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "discovery/run_g1_exact_structural_atlas_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-3-g1-exact-structural-atlas-v2.json"
V1 = PROJECT / "artifacts/cycle-3-g1-exact-structural-atlas-v1.json"


class G1ExactStructuralAtlasV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text())
        cls.v1 = json.loads(V1.read_text())

    def test_corrected_authority_retains_exact_rows_and_direct_pins(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "PROVED")
        self.assertEqual(self.data["scope"], {"finite_complex_probes_evaluated": 0, "screen_rows_evaluated": 0, "local_rows": 7744, "transfer_rows": 560})
        self.assertEqual(self.data["local_rows"], self.v1["local_rows"])
        self.assertEqual(self.data["transfer_rows"], self.v1["transfer_rows"])
        inputs = self.data["frozen_inputs"]
        self.assertEqual(inputs["runtime"], {"implementation": "CPython", "python": "3.12.3", "mpmath": "1.2.1", "optimization": 0})
        self.assertEqual(inputs["convention_derivation"]["status"], "DIRECT_IMPORT_AND_PREREGISTRATION_CROSSCHECK")
        correction = inputs["convention_runtime_correction"]
        self.assertEqual(correction["epistemic_status"], "PROVED")
        self.assertEqual((correction["old_sha256"], correction["new_sha256"]), ("3d3cef60c32dff2a2e4cbd3c10b229464d74aadbbaef53ba1fccc7158b78d726", inputs["hashes"]["frozen_conventions"]))
        self.assertEqual(correction["checked"]["primary_spine_rows"], 42)
        self.assertEqual(inputs["hashes"]["preregistration_document"], hashlib.sha256((PROJECT / "docs/cycle-3-g1-atlas-preregistration-v1.md").read_bytes()).hexdigest())

    def test_replay_fails_closed_under_optimized_python(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        optimized = subprocess.run([sys.executable, "-O", str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(optimized.returncode, 0)
        self.assertIn("forbids -O/-OO", optimized.stderr)

    def test_separate_observed_performance_points_to_v2(self) -> None:
        performance = json.loads((PROJECT / "artifacts/cycle-3-g1-exact-structural-atlas-v2-performance.json").read_text())
        self.assertEqual(performance["epistemic_status"], "OBSERVED")
        self.assertEqual(performance["atlas_artifact"]["sha256"], hashlib.sha256(ARTIFACT.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
