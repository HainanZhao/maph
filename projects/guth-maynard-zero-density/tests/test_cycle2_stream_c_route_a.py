"""Tests for the independent Cycle 2 Stream C Route A replay."""

import ast
import importlib.util
import json
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/replay_cycle2_stream_c_route_a.py"
ARTIFACT = PROJECT / "artifacts/cycle-2-stream-c-route-a-v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("cycle2_stream_c_route_a", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CycleTwoStreamCRouteATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_exact_endpoints_and_secondary_epsilon_bookkeeping(self):
        book = self.module.exact_bookkeeping()
        self.assertEqual(book["density_coefficient"], "30/13")
        self.assertEqual(book["uniform"]["theta"], "17/30")
        self.assertEqual(book["almost_all"]["theta"], "2/15")
        self.assertEqual(book["almost_all"]["delta_times_X_power"], "2/15")
        self.assertIn("13/15-epsilon/3", book["almost_all"]["epsilon_bookkeeping"])
        self.assertIn("dominates", book["vk_absorption"]["decay_comparison"])

    def test_blockers_and_pair_input_are_retained(self):
        report = self.module.build_report()
        rows = {row["id"]: row for row in report["rows"]}
        self.assertEqual(rows["SC-A3-vinogradov-korobov-zero-free"]["status"], "PROVED")
        for name in ("SC-A1-GM-explicit-formula", "SC-A2-near-one-density", "SC-A5-local-zero-and-pair-kernel-bound"):
            self.assertEqual(rows[name]["status"], "OBSERVED")
        self.assertIn("NOT PASS", report["pass_state"])
        self.assertIn("SC-A2-near-one-density", report["blockers"])

    def test_no_float_literals(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        self.assertEqual(
            [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)],
            [],
        )

    def test_legacy_timed_artifact_has_read_only_semantic_identity(self):
        # The v1 writer embeds wall_time_ns.  A regression test must therefore
        # not invoke it: raw bytes are intentionally mutable and v1's stable
        # identity is exact_replay_sha256 over the mathematical report body.
        artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(artifact["exact_replay_sha256"], self.module.canonical_sha256(self.module.build_report()))
        self.assertEqual(artifact["replay"]["script_sha256"], self.module.sha256(SCRIPT))


if __name__ == "__main__":
    unittest.main()
