"""Tests for the deterministic Cycle-2 per-route resource-gate harness."""

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
SCRIPT = PROJECT / "proof/run_cycle2_g0_resource_gate_v1.py"
CONFIG = PROJECT / "artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json"
PERFORMANCE = PROJECT / "artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json"


def module():
    spec = importlib.util.spec_from_file_location("g0_resource_gate", SCRIPT)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class G0ResourceGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = module()

    def test_config_is_deterministic_and_lists_exactly_four_routes(self):
        subprocess.run([sys.executable, str(SCRIPT), "--check-config", str(CONFIG)], check=True, cwd=PROJECT)
        data = json.loads(CONFIG.read_text())
        self.assertEqual(data["limits"]["wall_seconds_strictly_less_than"], 60)
        self.assertEqual(data["limits"]["max_rss_kib_strictly_less_than"], 256 * 1024)
        self.assertEqual([route["id"] for route in data["routes"]], ["stream-b-route-a-v3", "stream-b-route-b-v1", "stream-c-route-a-v5", "stream-c-route-b-v5"])
        self.assertIn("does not claim G0 PASS", data["non_promotion"])

    def test_performance_is_observed_and_all_routes_pass_limits(self):
        data = json.loads(PERFORMANCE.read_text())
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["resource_gate"]["gate_status"], "PASS")
        for result in data["route_results"]:
            self.assertEqual(result["epistemic_status"], "OBSERVED")
            self.assertEqual(result["gate_status"], "PASS")
            self.assertLess(float(result["wall_seconds"]), 60)
            self.assertLess(result["max_rss_kib"], 256 * 1024)
            self.assertIn("sealed_source_check", result)

    def test_runner_can_write_a_temporary_observation(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "performance.json"
            subprocess.run([sys.executable, str(SCRIPT), "--write-performance", str(target)], check=True, cwd=PROJECT)
            data = json.loads(target.read_text())
        self.assertEqual(data["resource_gate"]["gate_status"], "PASS")
        self.assertIn("time_version", data["environment"])

    def test_strict_threshold_parser_and_no_float_literals(self):
        self.assertEqual(self.m.elapsed_seconds("1:00.00"), 60)
        _, rss, status = self.m.parse_time_report("Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.01\nMaximum resident set size (kbytes): 1\nExit status: 0\n")
        self.assertEqual((rss, status), (1, 0))
        tree = ast.parse(SCRIPT.read_text())
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
