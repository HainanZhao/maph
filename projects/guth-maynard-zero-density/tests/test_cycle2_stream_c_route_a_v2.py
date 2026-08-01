"""Tests for the versioned Stream C Route A v2 closure audit."""

import ast
import importlib.util
import json
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/replay_cycle2_stream_c_route_a_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-2-stream-c-route-a-v2.json"


def load_module():
    spec = importlib.util.spec_from_file_location("stream_c_route_a_v2", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StreamCRouteAV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_exact_huxley_margin(self):
        closures = self.module.exact_closures()
        near_one = closures["huxley_near_one"]
        self.assertEqual(near_one["h_4_5"], "15/7")
        self.assertEqual(near_one["B_minus_h_4_5"], "15/91")
        self.assertEqual(near_one["h_over_B_max"], "13/14")

    def test_closes_v1_blockers_but_keeps_chj_ii_scope_finding(self):
        report = self.module.build_report()
        rows = {row["id"]: row for row in report["rows"]}
        for row_id in ("SC-A1-explicit-formula-CHJ-I", "SC-A2-near-one-density-Huxley", "SC-A3-VK-and-low-height", "SC-A5-local-zero-and-pair-kernel"):
            self.assertEqual(rows[row_id]["status"], "PROVED")
        self.assertEqual(rows["SC-A5b-CHJ-II-scope"]["status"], "OBSERVED")
        self.assertEqual(report["open_blockers"], [])
        self.assertIn("PASS", report["pass_state"])

    def test_no_float_literals(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        values = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(values, [])

    def test_legacy_timed_artifact_has_read_only_semantic_identity(self):
        # v2 also embeds wall_time_ns.  Keep the historical artifact read-only
        # and validate its semantic certificate instead of rerunning its writer.
        artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(artifact["exact_replay_sha256"], self.module.canonical_sha256(self.module.build_report()))
        self.assertEqual(artifact["replay"]["script_sha256"], self.module.sha256(SCRIPT))


if __name__ == "__main__":
    unittest.main()
