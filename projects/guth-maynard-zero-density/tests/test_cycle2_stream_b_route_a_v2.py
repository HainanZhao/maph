"""Tests for the versioned Stream B Route A v2 closure."""
import ast
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_cycle2_stream_b_route_a_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-2-stream-b-route-a-v2.json"

def module():
    spec = importlib.util.spec_from_file_location("stream_b_a_v2", SCRIPT)
    assert spec and spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

class StreamBRouteAV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.m = module()
    def test_all_v1_blockers_closed(self):
        report = self.m.build_report()
        self.assertEqual(report["open_blockers"], [])
        self.assertTrue(all(row["status"] == "PROVED" for row in report["rows"]))
        self.assertIn("PASS", report["pass_state"])
    def test_exact_bounded_k_and_budget(self):
        book = self.m.exact_bookkeeping()
        self.assertIn("k=ceil", book["bounded_power"]["small_branch"])
        self.assertIn("epsilon/20", book["epsilon_budget"])
        self.assertIn("delta>=1", book["mean_value"])
    def test_no_float_literals(self):
        tree = ast.parse(SCRIPT.read_text())
        self.assertEqual([n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, float)], [])
    def test_replay_hash(self):
        subprocess.run([sys.executable, str(SCRIPT)], check=True, cwd=PROJECT)
        artifact = json.loads(ARTIFACT.read_text())
        body = {k:v for k,v in artifact.items() if k not in {"mathematical_and_source_audit_sha256", "replay"}}
        self.assertEqual(artifact["mathematical_and_source_audit_sha256"], self.m.canonical_sha256(body))
        self.assertEqual(artifact["replay"]["script_sha256"], self.m.sha256(SCRIPT))

if __name__ == "__main__": unittest.main()
