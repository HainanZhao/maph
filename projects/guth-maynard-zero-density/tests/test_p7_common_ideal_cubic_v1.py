from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-common-ideal-cubic-v1.json"
BUILDER = ROOT / "proof/build_p7_common_ideal_cubic_v1.py"


class P7CommonIdealCubicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_pins(self) -> None:
        result = subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        for row in self.data["artifact_identity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])
        for row in self.data["source_integrity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])

    def test_exact_labelled_gram_and_repeated_norm_check(self) -> None:
        bridge = self.data["exact_ideal_gram_bridge"]
        check = bridge["finite_exact_check"]
        self.assertEqual(check["ideal_norms"][:2], [5, 5])
        self.assertEqual(check["direct_trace_K_cubed"], check["expanded_labelled_ideal_trace"])
        self.assertIn("B_xy", bridge["norm_fibre_formula"])
        self.assertIn("Distinct ideals", bridge["repeated_norm_statement"])
        self.assertIn("Cauchy", bridge["single_character_l2_fibre_bound"])
        self.assertIn("N^(o(1))", bridge["single_character_l2_fibre_bound"])

    def test_coloured_energy_uses_complete_ambient_group(self) -> None:
        energy = self.data["fixed_modulus_coloured_energy"]
        check = energy["finite_exact_check"]
        self.assertEqual(check["coloured_energy"], check["orthogonality_parseval_count"])
        self.assertLessEqual(check["coloured_energy"], check["uncoloured_time_energy_with_multiplicity"])
        self.assertIn("not be closed", energy["primitive_not_group"])
        self.assertIn("multiset", energy["comparison"])

    def test_scoped_non_import_boundary(self) -> None:
        boundary = self.data["scoped_verbatim_import_failure"]
        self.assertIn("pair", boundary["failure_1_pair_coefficients"])
        self.assertIn("same height", boundary["failure_2_colour_collisions"])
        self.assertIn("common multiple", boundary["failure_3_varying_moduli"])
        self.assertIn("does not rule out", boundary["scope"])
        self.assertEqual(self.data["epistemic_status"], "PROVED")


if __name__ == "__main__":
    unittest.main()
