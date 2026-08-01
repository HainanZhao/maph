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
SCRIPT = PROJECT / "discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("crr_finite_probe_preregistration_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load finite-probe preregistration builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRFiniteProbePreregistrationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_exact_160_row_schedule_and_seeds(self) -> None:
        schedule = self.data["schedule"]
        rows = schedule["rows"]
        self.assertEqual(schedule["factorization"], "4 N values * 5 families * 4 variants * 2 replicates = 160")
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({row["id"] for row in rows}), 160)
        self.assertEqual(rows[0]["id"], "N256-F1-phase-rounded-frame-V1-R0")
        self.assertEqual(rows[0]["row_seed"], "0xBDA8E4574E64BA87")
        self.assertEqual(rows[-1]["id"], "N2048-F5-symmetric-positive-trace-spectral-V4-R1")
        self.assertEqual(rows[-1]["row_seed"], "0xE1E13DA13EC0A55F")
        self.assertEqual({row["N"] for row in rows}, {256, 512, 1024, 2048})
        self.assertEqual({row["family"] for row in rows}, set(self.data["family_registry"]))
        self.assertEqual({row["replicate"] for row in rows}, {0, 1})

    def test_frozen_scales_search_rules_and_resources(self) -> None:
        self.assertEqual(self.data["exact_scale_rows"]["1024"], {"H": 4096, "Q": 16, "R": 256, "V": 128, "cubic": 68719476736, "rational_height": 64})
        self.assertEqual(self.data["mutation"]["proposals_per_row"], 128)
        quadrature = self.data["quadrature_and_cubic"]
        self.assertEqual((quadrature["proxy_nodes"], quadrature["final_nodes"]), (16, 32))
        self.assertEqual((quadrature["proxy_cubic_mode"], quadrature["final_cubic_mode"]), (8, 12))
        self.assertEqual(quadrature["quadrature_relative_disagreement"], "1/100")
        self.assertEqual(quadrature["cubic_relative_disagreement"], "1/20")
        self.assertEqual(self.data["retention"]["retained_hit_margin"], "1/20")
        self.assertEqual(self.data["resources"], {"aggregate_wall_minutes": 55, "aggregate_wall_seconds": 3300, "max_rss_bytes": 1073741824, "max_rss_gib": 1})
        self.assertIn("GLOBAL_CAP_UNREACHED", self.data["retention"]["failure_codes"])

    def test_claim_boundary_and_research_stage_policy(self) -> None:
        self.assertEqual(self.data["status"], "SEALED_DISCOVERY_PREREGISTRATION_UNEXECUTED")
        self.assertTrue(self.data["execution"]["authorized_after_seal"])
        self.assertFalse(self.data["execution"]["executed_by_this_builder"])
        self.assertIn("no_miss_table_implies_universal_negative", self.data["execution"]["result_classification"])
        self.assertEqual(self.data["research_stage_review_policy"]["hostile_audit"], "NOT_INITIATED; DEFERRED_TO_PAPER_STAGE")
        self.assertTrue(self.data["retention"]["no_universal_negative_from_misses"])
        self.assertIn("not a rigorous enclosure", self.data["retention"]["recognition_ball"])

    def test_byte_replay_tamper_rejection_and_no_asserts(self) -> None:
        self.assertEqual(self.data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(SCRIPT.read_text(encoding="utf-8")))))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        optimized = subprocess.run([sys.executable, "-O", str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(optimized.returncode, 0)
        self.assertIn("non-optimized CPython 3.12.3", optimized.stderr)
        module = load_module()
        original = module.INPUTS["conventions"]
        module.INPUTS["conventions"] = (original[0], "0" * 64)
        try:
            with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: conventions"):
                module.seal()
        finally:
            module.INPUTS["conventions"] = original


if __name__ == "__main__":
    unittest.main()
