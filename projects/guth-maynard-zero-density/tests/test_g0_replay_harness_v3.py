"""Regression tests for the hardened, read-only G0 replay harness v3."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/run_g0_replay_v3.py"


def module():
    spec = importlib.util.spec_from_file_location("g0_replay_harness_v3", SCRIPT)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class G0ReplayHarnessV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.m = module()

    def test_explicit_runtime_and_corrected_v2_inventory(self) -> None:
        preflight = self.m.runtime_preflight()
        self.assertEqual((preflight["implementation"], preflight["version"], preflight["optimization"]), ("CPython", "3.12.3", 0))
        identifiers = [identifier for identifier, _ in self.m.CHECKS]
        self.assertEqual(len(identifiers), 22)
        self.assertEqual(identifiers[-1], "g0-authoritative-full-reconstruction-v2")
        for expected in ("cycle1-route-a-readonly-v1", "cycle1-route-b-readonly-v1", "stream-c-published-formula-source-v5", "g0-six-route-resource-configuration-v2", "g0-v2-bounded-hostile-audit-v1"):
            self.assertIn(expected, identifiers)
        self.m.validate_static_configuration()

    def test_optimized_invocation_fails_before_legacy_v2(self) -> None:
        result = subprocess.run([sys.executable, "-O", str(SCRIPT)], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sys.flags.optimize must equal 0", result.stderr)

    def test_one_command_is_read_only_for_registered_timing_records(self) -> None:
        before = {path: hashlib.sha256((PROJECT / path).read_bytes()).hexdigest() for path in self.m.TIMING_MUTABLE_RAW_ARTIFACTS}
        result = subprocess.run([sys.executable, str(SCRIPT)], cwd=PROJECT, check=True, capture_output=True, text=True)
        after = {path: hashlib.sha256((PROJECT / path).read_bytes()).hexdigest() for path in self.m.TIMING_MUTABLE_RAW_ARTIFACTS}
        self.assertEqual(after, before)
        replay = json.loads(result.stdout)
        self.assertEqual((replay["epistemic_status"], replay["status"]), ("OBSERVED", "PASS"))
        self.assertEqual(replay["runtime_preflight"]["version"], "3.12.3")
        self.assertIn("bypass", replay["bounded_v2_containment"])


if __name__ == "__main__":
    unittest.main()
