from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/p6_detector_qt_tail_v1.py"
ARTIFACT = ROOT / "artifacts/p6-detector-qt-tail-v1.json"
CGL_TAR = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar"


class P6DetectorQtTailV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_pinned_source(self) -> None:
        check = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"], cwd=ROOT,
            text=True, capture_output=True, timeout=60,
        )
        self.assertEqual(check.returncode, 0, check.stderr)
        source = self.data["source_checks"]["cgl_v2_tar"]
        self.assertEqual(source["sha256"], hashlib.sha256(CGL_TAR.read_bytes()).hexdigest())
        self.assertEqual(source["locators"]["old_tail_and_its_X_T_restriction"], "TeX 2140")
        self.assertEqual(source["locators"]["class_II_maximizer_and_fourth_moment"], "TeX 2163--2173")

    def test_cutoff_is_qt_dependent_not_a_forbidden_patch(self) -> None:
        lemma = self.data["lemma"]
        params = lemma["range_and_parameters"]
        self.assertIn("Q=qT", params["Q"])
        self.assertIn("U=C log(Q+3)", params["detector_lengths"])
        tail = lemma["self_contained_steps"]["Mellin_tail"]
        self.assertIn("No relation q<=T^c is used", tail[-1])
        effect = lemma["conclusion"]["Z03_effect"]
        self.assertIn("no q<=T^c condition", effect)
        self.assertIn("q1-sensitive", self.data["claim_boundary"])

    def test_shift_spacing_and_small_T_height_transport(self) -> None:
        steps = self.data["lemma"]["self_contained_steps"]
        self.assertIn("Q^eta-2U>=Q^eta/2", steps["shifted_spacing"][0])
        self.assertIn("T=1 and q=Q->infinity", steps["fourth_moment_height"][2])
        exact = self.data["exact_algebra"]
        self.assertIn("T=1", exact["height_test"])
        self.assertIn("2C log(Q+3)<=Q^eta/2", exact["spacing_test"])

    def test_principal_compact_and_multiplicity_boundaries_are_retained(self) -> None:
        lemma = self.data["lemma"]
        principal = lemma["self_contained_steps"]["principal_residue"]
        self.assertIn("z=0 residue", principal[-1])
        self.assertIn("LOW_HEIGHT_MULTIPLICITY_COUNT", principal[-2])
        self.assertIn("compact Q", lemma["self_contained_steps"]["compact_Q"][-1])
        self.assertIn("S03_MULTIPLICITY_NOT_STATED", lemma["self_contained_steps"]["multiplicity_boundary"][-1])
        remain = self.data["p6_effect"]["remaining_open_obligations"]
        self.assertIn("S06_EXTERNAL_INPUTS", remain)
        self.assertIn("F08_T_SMOOTH_UNDEFINED", remain)

    def test_conditional_boundary_and_no_paper_audit(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "PROVED_CONDITIONAL")
        inputs = self.data["lemma"]["conditional_inputs"]
        self.assertEqual(inputs["L_POLY_A"]["status"], "CONDITIONAL_EXTERNAL_INPUT")
        self.assertEqual(inputs["FOURTH_MOMENT_H"]["status"], "CONDITIONAL_EXTERNAL_INPUT_S06")
        self.assertIn("No hostile audit is initiated", self.data["claim_boundary"])
        self.assertFalse(self.data["p6_effect"]["upstream_reconciliation_edited"])


if __name__ == "__main__":
    unittest.main()
