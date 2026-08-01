from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/p1r_fs_route_a_v1.py"
ARTIFACT = PROJECT / "artifacts/p1r-fs-route-a-v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("p1r_fs_route_a_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class P1RFSRouteAV1Tests(unittest.TestCase):
    def test_sealed_theorem_and_boundaries(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertEqual(data["theorem_id"], "P1R-FS-A")
        self.assertEqual(data["exact_proof"]["supremum"], "sup_{1/2<=sigma<7/10} I(sigma)=30/13")
        self.assertIn("not saturation", data["claim_boundary"])
        self.assertIn("changing the left branch", data["out_of_scope"])

    def test_universal_witness_helper(self) -> None:
        module = load_module()
        for eta in (Fraction(1, 10**9), Fraction(7, 100), Fraction(1, 1), Fraction(29, 13)):
            row = module.epsilon_witness(eta)
            self.assertGreater(row["I_sigma"], module.TARGET - eta)
            self.assertGreaterEqual(row["sigma"], module.LEFT_MIN)
            self.assertLess(row["sigma"], module.SPLICE)
        for eta in (Fraction(0), Fraction(30, 13), Fraction(3, 1)):
            with self.assertRaises(RuntimeError):
                module.epsilon_witness(eta)

    def test_replay_runtime_overwrite_self_and_source_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["prover"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)
        module = load_module()
        original_input = module.INPUTS["huxley_pdf"]
        module.INPUTS["huxley_pdf"] = (original_input[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: huxley_pdf"):
            module.prove()
        module.INPUTS["huxley_pdf"] = original_input
        with tempfile.NamedTemporaryFile(dir=PROJECT / "proof", suffix=".py") as handle:
            handle.write(SCRIPT.read_bytes() + b"\n# self mutation\n")
            handle.flush()
            original_self = module.SELF
            module.SELF = Path(handle.name)
            try:
                self.assertNotEqual(module.prove()["prover"]["sha256"], data["prover"]["sha256"])
            finally:
                module.SELF = original_self


if __name__ == "__main__":
    unittest.main()
