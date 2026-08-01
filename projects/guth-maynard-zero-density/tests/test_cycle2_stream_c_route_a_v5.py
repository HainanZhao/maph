"""Regression tests for the official-source Stream-C Route-A v5 replay."""

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
SCRIPT = PROJECT / "proof/replay_cycle2_stream_c_route_a_v5.py"
ARTIFACT = PROJECT / "artifacts/cycle-2-stream-c-route-a-v5.json"


def module():
    spec = importlib.util.spec_from_file_location("stream_c_a_v5", SCRIPT)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class StreamCARouteAV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = module()

    def test_deterministic_artifact_and_separate_observed_timing(self):
        original = ARTIFACT.read_bytes()
        subprocess.run([sys.executable, str(SCRIPT), "--check", str(ARTIFACT)], check=True, cwd=PROJECT)
        with tempfile.TemporaryDirectory() as directory:
            performance = Path(directory) / "performance.json"
            subprocess.run([sys.executable, str(SCRIPT), "--write-performance", str(performance)], check=True, cwd=PROJECT)
            data = json.loads(performance.read_text())
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertIn("wall_time_ns", data)
        self.assertEqual(original, ARTIFACT.read_bytes())
        self.assertNotIn("wall_time_ns", json.loads(original)["replay"])

    def test_official_sword_chain_is_sealed_and_author_identity_is_not_used(self):
        data = json.loads(ARTIFACT.read_text())
        inputs = data["official_source_inputs"]
        for path in (
            "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json",
            "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py",
            "artifacts/sources/mit-ocw-18-785-2007-sword-official.zip",
            "artifacts/sources/mit-ocw-18-785-2007-errorbounds-official.pdf",
            "artifacts/sources/mit-ocw-18-785-2007-von-mangoldt-official.pdf",
            "artifacts/sources/mit-dspace-1721.1-101679-metadata.json",
        ):
            self.assertIn(path, inputs)
        source = SCRIPT.read_text()
        self.assertNotIn("kedlaya-2007-errorbounds-author.pdf", source)
        self.assertNotIn("kedlaya-2007-von-mangoldt-author.pdf", source)
        row = {item["id"]: item for item in data["rows"]}["SC-A51-v2-v4-provenance-corrections"]
        self.assertIn("no author-copy identity claim", row["statement"])

    def test_exact_global_arithmetic(self):
        arithmetic = self.m.exact_route_a_arithmetic()
        self.assertEqual(arithmetic["uniform"]["theta"], "17/30")
        self.assertEqual(arithmetic["almost_all"]["theta"], "2/15")
        self.assertIn("coefficient equality", arithmetic["huxley"]["certificate"])
        self.assertIn("3(30s-23)", arithmetic["huxley"]["identity"])

    def test_only_allowed_epistemic_tags_and_narrow_scope(self):
        data = json.loads(ARTIFACT.read_text())
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertTrue(data["pass_state"].startswith("NARROW PASS:"))
        self.assertIn("G0 remains OBSERVED", data["pass_state"])
        allowed = {"PROVED", "CERTIFIED_NUMERICAL", "RECOGNIZED", "OBSERVED", "CONJECTURED"}
        self.assertTrue(all(row["epistemic_status"] in allowed for row in data["rows"]))

    def test_no_float_literals(self):
        tree = ast.parse(SCRIPT.read_text())
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
