from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
BUILDER = PROJECT / "discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v3.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v3.json"
CONVENTIONS = PROJECT / "conventions/crr_finite_analogue_probe_v3.py"
RUNNER = PROJECT / "discovery/run_cycle_4_p1r_crr_finite_probe_v3.py"
RESULT = PROJECT / "discovery/cycle-4-p1r-crr-finite-probe-v3.json"
SEMANTIC_REPLAY = PROJECT / "discovery/replay_cycle_4_p1r_crr_finite_probe_v3_semantic_v1.py"
METADATA_CORRECTION_BUILDER = PROJECT / "discovery/build_cycle_4_p1r_crr_finite_probe_v3_replay_metadata_correction_v1.py"
METADATA_CORRECTION = PROJECT / "artifacts/cycle-4-p1r-crr-finite-probe-v3-replay-metadata-correction-v1.json"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRFiniteProbeV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        cls.conventions = load(CONVENTIONS, "crr_probe_v3_conventions_test")
        cls.runner = load(RUNNER, "crr_probe_v3_runner_test")

    def test_schedule_and_thresholds_are_exactly_v2(self) -> None:
        v2 = json.loads((PROJECT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v2.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["schedule"], v2["schedule"])
        self.assertEqual(self.data["exact_scale_rows"], v2["exact_scale_rows"])
        self.assertEqual(self.data["thresholds"], v2["thresholds"])
        self.assertEqual(len(self.data["schedule"]["rows"]), 160)
        self.assertEqual(self.data["schedule"]["rows"][0]["row_seed"], "0xBDA8E4574E64BA87")
        self.assertIn("Never use tr((diag(w)G-M I_(2M))^3).", self.conventions.CUBIC_DIMENSIONAL_IDENTITY)

    def test_ambient_dimensional_cubic_compression(self) -> None:
        w = np.array([0, 2, 5, 8], dtype=np.int64)
        n, h, mode = 11, 13, 3
        compressed = self.runner.base.cubic_binary(w, n, h, mode)
        differences = (w[:, None] - w[None, :]) % h
        matrix = np.zeros((len(w), len(w)), dtype=np.float64)
        for m in range(1, mode + 1):
            matrix += 2 * (1 - m / (mode + 1)) * np.cos(2 * np.pi * m * differences / h)
        np.fill_diagonal(matrix, 0.0)
        direct = float((n**3 * np.trace(matrix @ matrix @ matrix)).real)
        self.assertAlmostEqual(compressed, direct, places=7)
        modes = np.concatenate((np.arange(-mode, 0), np.arange(1, mode + 1)))
        u = np.exp(2j * np.pi * np.outer(w, modes) / h)
        gram = u.conj().T @ u
        weights = 1 - np.abs(modes) / (mode + 1)
        shifted = weights[:, None] * gram - mode * np.eye(2 * mode)
        wrong = float((n**3 * np.trace(shifted @ shifted @ shifted)).real)
        self.assertGreater(abs(compressed - wrong), 1.0)

    def test_initializers_are_deterministic_and_cardinality_preserving(self) -> None:
        for row in self.data["schedule"]["rows"][::17]:
            values_a, words_a = self.runner.base.initialize_w(row, self.conventions)
            values_b, words_b = self.runner.base.initialize_w(row, self.conventions)
            self.assertEqual(values_a, values_b)
            self.assertEqual(words_a, words_b)
            self.assertIsNotNone(values_a)
            scale = self.conventions.scales(row["N"])
            self.assertEqual(len(values_a), scale["R"])
            self.assertTrue(all(0 <= point < scale["H"] for point in values_a))

    def test_seal_replay_and_no_asserts(self) -> None:
        self.assertEqual(self.data["sealer"]["sha256"], hashlib.sha256(BUILDER.read_bytes()).hexdigest())
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(BUILDER.read_text(encoding="utf-8")))))
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(RUNNER.read_text(encoding="utf-8")))))
        subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=PROJECT, check=True)

    def test_v3_runner_uses_v3_frozen_convention_key(self) -> None:
        artifact, conventions = self.runner.base.validate_prereg()
        self.assertEqual(artifact["artifact_id"], "cycle-4-p1r-crr-finite-probe-preregistration-v3")
        self.assertEqual(artifact["frozen_hashes"]["v3_conventions"]["sha256"], hashlib.sha256(CONVENTIONS.read_bytes()).hexdigest())
        self.assertEqual(conventions.CUBIC_DIMENSIONAL_IDENTITY, self.conventions.CUBIC_DIMENSIONAL_IDENTITY)

    def test_completed_table_is_complete_and_only_observational(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        self.assertEqual(result["epistemic_status"], "OBSERVED")
        self.assertEqual(result["status_counts"], {"NO_RETAINED_HIT": 160})
        self.assertEqual(len(result["rows"]), 160)
        self.assertEqual([row["id"] for row in result["rows"]], [row["id"] for row in self.data["schedule"]["rows"]])
        self.assertLess(result["resources"]["wall_seconds"], result["resources"]["cap_seconds"])
        self.assertLess(result["resources"]["peak_rss_bytes"], result["resources"]["cap_rss_bytes"])
        for row in result["rows"]:
            self.assertEqual(row["outcome_diagnostic"], "cubic")
            self.assertTrue(row["recognized_cubic"]["dual_precision"]["256"]["fails"])
            self.assertTrue(row["recognized_cubic"]["dual_precision"]["384"]["fails"])
            final = row["recognized_cubic"]["dual_precision"]["384"]
            c8, c12 = float(final["C8"]), float(final["C12"])
            threshold = 1.05 / 20 * row["N"] ** 3.6
            disagreement = abs(c8 - c12) / max(abs(c12), 1 / 20 * row["N"] ** 3.6)
            self.assertGreater(c8, 0.0)
            self.assertGreaterEqual(c12, threshold)
            self.assertGreater(disagreement, 0.05)

    def test_semantic_replay_projection_keeps_caps_and_drops_only_variable_resources(self) -> None:
        replay = load(SEMANTIC_REPLAY, "crr_probe_v3_semantic_replay_test")
        original = json.loads(RESULT.read_text(encoding="utf-8"))
        projection = replay.deterministic_projection(original)
        self.assertEqual(projection["resources"], {"cap_rss_bytes": 1073741824, "cap_seconds": 3300})
        self.assertIsNone(replay.first_difference(projection, replay.deterministic_projection(original)))
        changed = json.loads(json.dumps(original))
        changed["resources"]["cap_seconds"] = 1
        self.assertEqual(replay.first_difference(projection, replay.deterministic_projection(changed))["path"], "$.resources.cap_seconds")

    def test_metadata_correction_preserves_result_and_reports_full_census(self) -> None:
        correction = json.loads(METADATA_CORRECTION.read_text(encoding="utf-8"))
        self.assertEqual(correction["status"], "SEALED_METADATA_CORRECTION")
        self.assertEqual(correction["immutable_inputs"]["immutable_v3_result"]["sha256"], hashlib.sha256(RESULT.read_bytes()).hexdigest())
        self.assertEqual(correction["correction"]["corrected_values"]["check_command"], "python3 discovery/run_cycle_4_p1r_crr_finite_probe_v3.py --check")
        self.assertEqual(correction["semantic_replay"]["status"], "SEMANTIC_REPLAY_MATCH")
        self.assertIsNone(correction["semantic_replay"]["comparison"]["first_difference"])
        self.assertEqual(correction["post_result_screen_census"]["pass_counts"], {
            "large_value": 0, "energy_lower": 160, "energy_upper": 147,
            "rational_measure": 13, "quadrature_agreement": 10,
            "cubic_positive_and_size": 160, "cubic_agreement": 0,
        })
        subprocess.run([sys.executable, str(METADATA_CORRECTION_BUILDER), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
