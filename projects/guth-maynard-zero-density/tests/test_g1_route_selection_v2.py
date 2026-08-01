from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/adjudicate_g1_route_selection_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-3-g1-route-decision-v2.json"


def load_module():
    spec = importlib.util.spec_from_file_location("g1_route_v2_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class G1RouteSelectionV2Tests(unittest.TestCase):
    def test_sealed_decision_and_executable_identity(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["decision"], "NO_SELECTION")
        self.assertEqual(data["gate_status"], "G1_CLOSED_NO_SELECTION")
        self.assertEqual(data["adjudicator"]["path"], "proof/adjudicate_g1_route_selection_v2.py")
        self.assertEqual(data["adjudicator"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertEqual(data["evidence_summary"]["retained_rows"], 0)
        self.assertEqual(data["evidence_summary"]["validation_rows"], 0)
        self.assertTrue(all(not row["selected"] for row in data["routes"].values()))

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)

    def test_optimized_modes_fail_closed(self) -> None:
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check", str(ARTIFACT)], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)

    def test_frozen_input_hash_tamper_fails_closed(self) -> None:
        module = load_module()
        original = module.INPUTS["exact_atlas_v2"]
        module.INPUTS["exact_atlas_v2"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: exact_atlas_v2"):
            module.adjudicate()

    def test_retained_row_counterfactual_requires_positive_adjudicator(self) -> None:
        module = load_module()
        empirical_path = module.INPUTS["empirical_reconciliation_v1"][0]
        original_load = module.load_json
        empirical = original_load(empirical_path)
        counterfactual = copy.deepcopy(empirical)
        counterfactual["agreement"]["retained_rows"] = 1
        counterfactual["agreement"]["validation_rows"] = 1
        counterfactual["screen_outcome_summary"]["retained_row_ids"] = []

        def load_with_counterfactual(path):
            if path == empirical_path:
                return counterfactual
            return original_load(path)

        with mock.patch.object(module, "load_json", side_effect=load_with_counterfactual):
            with self.assertRaisesRegex(RuntimeError, "positive feature adjudication required"):
                module.adjudicate()


if __name__ == "__main__":
    unittest.main()
