"""Regression tests for the source-sealed Stream-C Route-A v4 correction."""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/replay_cycle2_stream_c_route_a_v4.py"
ARTIFACT = PROJECT / "artifacts/cycle-2-stream-c-route-a-v4.json"


def module():
    spec = importlib.util.spec_from_file_location("stream_c_a_v4", SCRIPT)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class StreamCARouteAV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = module()

    def test_artifact_is_deterministic_and_timing_is_separate(self):
        before = ARTIFACT.read_bytes()
        subprocess.run([sys.executable, str(SCRIPT), "--check", str(ARTIFACT)], check=True, cwd=PROJECT)
        with tempfile.TemporaryDirectory() as temporary:
            timing = Path(temporary) / "performance.json"
            subprocess.run([sys.executable, str(SCRIPT), "--write-performance", str(timing)], check=True, cwd=PROJECT)
            performance = json.loads(timing.read_text())
        self.assertEqual(performance["epistemic_status"], "OBSERVED")
        self.assertIn("wall_time_ns", performance)
        self.assertEqual(before, ARTIFACT.read_bytes())
        self.assertNotIn("wall_time_ns", json.loads(before)["replay"])

    def test_both_kedlaya_units_and_v2_ledgers_are_sealed(self):
        data = json.loads(ARTIFACT.read_text())
        inputs = data["source_inputs"]
        self.assertIn("docs/cycle-2-stream-c-explicit-formula-access-ledger-v2-correction.md", inputs)
        self.assertIn("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v2.json", inputs)
        self.assertIn("artifacts/sources/kedlaya-2007-errorbounds-author.pdf", inputs)
        self.assertIn("artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf", inputs)

    def test_universal_huxley_factorization_uses_coefficient_identity(self):
        arithmetic = self.m.exact_route_a_arithmetic()
        near_one = arithmetic["near_one"]
        self.assertIn("coefficient equality", near_one["coefficient_certificate"])
        self.assertIn("3(30s-23)", near_one["universal_factorization"])
        self.assertEqual(arithmetic["uniform"]["theta"], "17/30")
        self.assertEqual(arithmetic["almost_all"]["theta"], "2/15")

    def test_v3_containment_is_precise(self):
        data = json.loads(ARTIFACT.read_text())
        row = {item["id"]: item for item in data["rows"]}["SC-A41-v3-source-authority-and-byte-provenance-containment"]
        self.assertEqual(row["epistemic_status"], "PROVED")
        self.assertIn("not a claim that v3 output bytes were nondeterministic", row["statement"])
        self.assertIn("wall_time_ns", data["preserved_route_a_v1_v3_identities"]["v1_v2_byte_note"])

    def test_no_float_literals(self):
        tree = ast.parse(SCRIPT.read_text())
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
