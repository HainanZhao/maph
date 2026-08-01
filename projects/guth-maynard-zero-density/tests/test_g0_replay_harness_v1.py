"""Regression tests for the read-only global G0 replay harness."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "run_g0_replay_v1.py"


def module():
    spec = importlib.util.spec_from_file_location("g0_replay_harness_v1", SCRIPT)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class G0ReplayHarnessV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.m = module()

    def test_exact_fixed_check_inventory(self) -> None:
        self.assertEqual(
            [identifier for identifier, _ in self.m.CHECKS],
            [
                "source-manifest-v3",
                "stream-a-frozen-source-ledger",
                "cycle-1-exact-two-route-reconciliation-v3",
                "stream-b-route-a-v3",
                "stream-b-route-b-v1",
                "stream-b-two-route-reconciliation-v2",
                "stream-c-official-formula-source-closure-v4",
                "stream-c-independent-official-sword-audit-v1",
                "stream-c-route-a-v5",
                "stream-c-route-b-v5",
                "stream-c-two-route-reconciliation-v2",
                "cycle-2-per-route-resource-configuration-v1",
                "g0-dependency-evidence-correction-v3",
            ],
        )
        self.m.validate_static_configuration()

    def test_harness_is_read_only_and_excludes_timing_records(self) -> None:
        arguments = [argument for _, command in self.m.CHECKS for argument in command]
        self.assertFalse(any(argument == "--write" or argument.startswith("--write-") for argument in arguments))
        for path in self.m.TIMING_MUTABLE_RAW_ARTIFACTS:
            self.assertNotIn(path, arguments)
        self.assertIn("--check-config", arguments)
        self.assertIn("--check", arguments)

    def test_one_command_replays_all_registered_checks(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=PROJECT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["epistemic_status"], "OBSERVED")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checks"], [
            {"id": identifier, "command": list(command), "epistemic_status": "OBSERVED"}
            for identifier, command in self.m.CHECKS
        ])
        self.assertIn("not G0 PASS", result["non_promotion"])


if __name__ == "__main__":
    unittest.main()
