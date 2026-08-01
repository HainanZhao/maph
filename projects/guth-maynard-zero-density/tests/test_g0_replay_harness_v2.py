"""Regression tests for the expanded read-only global G0 replay harness."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "run_g0_replay_v2.py"


def module():
    spec = importlib.util.spec_from_file_location("g0_replay_harness_v2", SCRIPT)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class G0ReplayHarnessV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.m = module()

    def test_fixed_v2_inventory_appends_only_sealed_gate_inputs(self) -> None:
        identifiers = [identifier for identifier, _ in self.m.CHECKS]
        self.assertEqual(len(identifiers), 16)
        self.assertEqual(identifiers[-3:], [
            "g0-literature-source-gate-audit-v1",
            "g0-hostile-final-gate-audit-v1",
            "g0-authoritative-full-reconstruction-v1",
        ])
        self.m.validate_static_configuration()

    def test_harness_is_read_only_and_excludes_host_timing_records(self) -> None:
        arguments = [argument for _, command in self.m.CHECKS for argument in command]
        self.assertFalse(any(argument == "--write" or argument.startswith("--write-") for argument in arguments))
        self.assertIn("--check-config", arguments)
        self.assertIn("--check", arguments)
        for path in self.m.TIMING_MUTABLE_RAW_ARTIFACTS:
            self.assertNotIn(path, arguments)

    def test_one_command_replays_all_registered_checks_without_mutating_timing_records(self) -> None:
        before = {
            path: hashlib.sha256((PROJECT / path).read_bytes()).hexdigest()
            for path in self.m.TIMING_MUTABLE_RAW_ARTIFACTS
        }
        completed = subprocess.run([sys.executable, str(SCRIPT)], cwd=PROJECT, check=True, capture_output=True, text=True)
        after = {
            path: hashlib.sha256((PROJECT / path).read_bytes()).hexdigest()
            for path in self.m.TIMING_MUTABLE_RAW_ARTIFACTS
        }
        self.assertEqual(after, before)
        result = json.loads(completed.stdout)
        self.assertEqual((result["epistemic_status"], result["status"]), ("OBSERVED", "PASS"))
        self.assertEqual(result["checks"], [
            {"id": identifier, "command": list(command), "epistemic_status": "OBSERVED"}
            for identifier, command in self.m.CHECKS
        ])
        self.assertIn("adds no theorem", result["non_promotion"])


if __name__ == "__main__":
    unittest.main()
