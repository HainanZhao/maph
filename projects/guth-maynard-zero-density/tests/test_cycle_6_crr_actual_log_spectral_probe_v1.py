from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
V1_BUILDER = PROJECT / "discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v1.py"
V2_BUILDER = PROJECT / "discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v2.py"
RUNNER = PROJECT / "discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_actual_log_spectral_probe_v1.py"
V1_ARTIFACT = PROJECT / "artifacts/cycle-6-crr-actual-log-spectral-probe-preregistration-v1.json"
V2_ARTIFACT = PROJECT / "artifacts/cycle-6-crr-actual-log-spectral-probe-preregistration-v2.json"
RESULT = PROJECT / "discovery/cycle-6-crr-actual-log-spectral-probe-v1.json"


def load_module(path: Path, label: str):
    spec = importlib.util.spec_from_file_location(label, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {label}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRActualLogSpectralProbeV1Tests(unittest.TestCase):
    def test_v2_preserves_v1_schedule_and_pins_runner(self) -> None:
        v1 = json.loads(V1_ARTIFACT.read_text(encoding="utf-8"))
        v2 = json.loads(V2_ARTIFACT.read_text(encoding="utf-8"))
        self.assertTrue(v2["correction"]["preserves_v1"])
        self.assertFalse(v2["correction"]["scientific_parameters_changed"])
        self.assertEqual(v2["row_schedule"], v1["row_schedule"])
        self.assertEqual(v2["actual_labels"], v1["actual_labels"])
        self.assertEqual(v2["iteration"], v1["iteration"])
        self.assertEqual(v2["retention"], v1["retention"])
        self.assertEqual(v2["resources"], v1["resources"])
        self.assertEqual(v2["frozen_hashes"]["runner"]["sha256"], hashlib.sha256(RUNNER.read_bytes()).hexdigest())
        self.assertEqual(v2["runner_control"]["sha256"], hashlib.sha256(RUNNER.read_bytes()).hexdigest())

    def test_literal_scales_labels_and_exact_energy(self) -> None:
        conventions = load_module(CONVENTIONS, "crr_actual_log_spectral_probe_conventions_under_test")
        rows = conventions.exact_rows()
        self.assertEqual((rows["v"], rows["H"], rows["L"], rows["R"], rows["Q"]), (2, 4096, 1024, 256, 16))
        self.assertEqual(rows["farey_pair_count"], 95)
        self.assertEqual(rows["smooth_support_count"], 1023)
        self.assertEqual(rows["energy_center_R4_over_H"], 1048576)
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        for row in result["rows"]:
            if row["status"] in {"RESOURCE_CAP", "GLOBAL_CAP_UNREACHED"}:
                continue
            times = __import__("numpy").array(row["common_pair"]["W"], dtype=__import__("numpy").int64)
            self.assertEqual(conventions.tolerance_one_energy(times), row["energy"]["exact_value"])
            self.assertEqual(row["common_pair"]["W_cardinality"], 256)
            self.assertGreaterEqual(row["common_pair"]["W_minimum_spacing"], 2)
            self.assertIn("actual-log", row["claim_boundary"])

    def test_outcomes_are_scoped_and_semantically_replayable(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        self.assertEqual(result["outcome_counts"], {"NO_RETAINED_HIT": 3})
        self.assertIn("not a universal negative", result["claim_boundary"])
        self.assertIn("three theta nodes", result["literal_structure"]["not_rationalmass"])
        for row in result["rows"]:
            self.assertEqual(row["epistemic_status"], "OBSERVED")
            self.assertIn("no continuous", row["claim_boundary"])
            self.assertTrue(row["retention_gates"]["coefficient_cap"])
            for record in row["minimum_value_iteration"]["records"]:
                self.assertGreaterEqual(record["fixed_p_linear_after_recognized"] + 1e-8, record["fixed_p_weighted_abs_before_recognized"])
                self.assertGreaterEqual(record["fixed_p_weighted_abs_after_recognized"] + 1e-8, record["fixed_p_linear_after_recognized"])
        subprocess.run([sys.executable, str(V1_BUILDER), "--check"], cwd=PROJECT, check=True)
        subprocess.run([sys.executable, str(V2_BUILDER), "--check"], cwd=PROJECT, check=True)
        subprocess.run([sys.executable, str(RUNNER), "--check"], cwd=PROJECT, check=True)

    def test_tamper_rejection_and_no_asserts(self) -> None:
        for path in (V1_BUILDER, V2_BUILDER, RUNNER, CONVENTIONS):
            self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))))
        builder = load_module(V2_BUILDER, "crr_actual_log_spectral_prereg_v2_under_test")
        original = builder.RUNNER_HASH
        builder.RUNNER_HASH = "0" * 64
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: runner"):
            builder.seal()
        builder.RUNNER_HASH = original
        runner = load_module(RUNNER, "crr_actual_log_spectral_runner_under_test")
        original_self = runner.SELF
        runner.SELF = V1_BUILDER
        try:
            with self.assertRaisesRegex(RuntimeError, "runner hash mismatch"):
                runner.load_prereg()
        finally:
            runner.SELF = original_self


if __name__ == "__main__":
    unittest.main()
