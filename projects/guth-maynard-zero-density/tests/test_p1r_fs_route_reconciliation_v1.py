from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/reconcile_p1r_fs_routes_v1.py"
ARTIFACT = PROJECT / "artifacts/p1r-fs-route-reconciliation-v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("p1r_fs_reconciliation_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class P1RFSReconciliationV1Tests(unittest.TestCase):
    def test_reconciled_scope_and_independence(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertEqual(data["status"], "TWO_ROUTE_RECONCILED_PENDING_HOSTILE_AUDIT")
        self.assertEqual(data["agreement"]["strict_left_supremum"], "30/13")
        self.assertEqual(data["independence_audit"]["status"], "PASS")
        self.assertEqual(data["independence_audit"]["cross_route_file_references"], [])
        self.assertIn("not saturation", data["claim_boundary"])

    def test_replay_runtime_overwrite_self_and_input_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["reconciler"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)
        module = load_module()
        original = module.INPUTS["route_b_artifact"]
        module.INPUTS["route_b_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: route_b_artifact"):
            module.reconcile()
        module.INPUTS["route_b_artifact"] = original
        with tempfile.NamedTemporaryFile(dir=PROJECT / "proof", suffix=".py") as handle:
            handle.write(SCRIPT.read_bytes() + b"\n# self mutation\n")
            handle.flush()
            original_self = module.SELF
            module.SELF = Path(handle.name)
            try:
                self.assertNotEqual(module.reconcile()["reconciler"]["sha256"], data["reconciler"]["sha256"])
            finally:
                module.SELF = original_self


if __name__ == "__main__":
    unittest.main()
