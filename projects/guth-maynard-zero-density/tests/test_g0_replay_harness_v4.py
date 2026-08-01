"""Regression tests for the minimal runtime-v2/G0-v3 replay successor."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/run_g0_replay_v4.py"


def module():
    spec = importlib.util.spec_from_file_location("g0_replay_harness_v4", SCRIPT)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class G0ReplayHarnessV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.m = module()

    def test_v4_is_minimal_and_pins_runtime_v2_and_g0_v3(self) -> None:
        self.assertEqual([identifier for identifier, _ in self.m.CHECKS], ["g0-read-only-replay-harness-v3", "g0-authoritative-full-reconstruction-v3"])
        self.assertIn("runtime_v2", self.m.FROZEN)
        self.assertIn("v3_reconciliation", self.m.FROZEN)
        self.assertEqual(self.m.runtime_preflight()["version"], "3.12.3")
        self.m.validate_static_configuration()

    def test_optimized_invocation_fails(self) -> None:
        result = subprocess.run([sys.executable, "-O", str(SCRIPT)], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("forbids -O/-OO", result.stderr)

    def test_one_command_is_read_only_and_finishes_at_g0_v3(self) -> None:
        before = {path: hashlib.sha256((PROJECT / path).read_bytes()).hexdigest() for path in self.m.TIMING_MUTABLE_RAW_ARTIFACTS}
        result = subprocess.run([sys.executable, str(SCRIPT)], cwd=PROJECT, check=True, capture_output=True, text=True)
        after = {path: hashlib.sha256((PROJECT / path).read_bytes()).hexdigest() for path in self.m.TIMING_MUTABLE_RAW_ARTIFACTS}
        self.assertEqual(after, before)
        replay = json.loads(result.stdout)
        self.assertEqual((replay["epistemic_status"], replay["status"]), ("OBSERVED", "PASS"))
        self.assertEqual(replay["checks"][-1]["id"], "g0-authoritative-full-reconstruction-v3")
        self.assertEqual(replay["runtime_preflight"]["optimize"], 0)


if __name__ == "__main__":
    unittest.main()
