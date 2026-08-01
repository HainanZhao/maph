from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-ray-orthogonality-v1.json"
BUILDER = ROOT / "proof/build_p7_ray_orthogonality_v1.py"


class P7RayOrthogonalityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_input_hashes(self) -> None:
        result = subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        for row in self.data["artifact_identity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])
        for row in self.data["source_integrity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])

    def test_projector_has_conductor_and_coprimality_conditions(self) -> None:
        projector = self.data["exact_projectors"]
        self.assertIn("sum_{d|f}P_d", projector["conductor_partition"])
        self.assertIn("1_{(ab,f)=1}", projector["primitive_identity"])
        self.assertIn("makes the primitive formula false", projector["coprimality_warning"])
        for row in projector["finite_convolution_checks"]:
            self.assertEqual(row["sum_{d|f}mu(f/d)"], row["expected"])

    def test_large_sieve_specialization_and_scope(self) -> None:
        sieve = self.data["large_sieve"]
        self.assertIn("R=2Q", sieve["checked_specialization"])
        self.assertIn("m=0", sieve["checked_specialization"])
        self.assertIn("4Q^2T^2", sieve["shell_conclusion"])
        self.assertIn("single function", sieve["common_coefficient_requirement"])
        self.assertIn("arbitrary independently chosen", sieve["character_dependent_boundary"])

    def test_gate_and_nonpromotion_boundary(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "PROVED")
        self.assertEqual(self.data["gate_outcome"], "PASS_EXACT_PROJECTOR_AND_SCOPED_L2_LARGE_SIEVE")
        self.assertIn("no hostile audit", self.data["review_policy"])
        self.assertIn("remains open", self.data["large_sieve"]["unresolved_for_p7_3"])


if __name__ == "__main__":
    unittest.main()
