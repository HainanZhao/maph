import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


class ResultsPaperMajorRevisionTests(unittest.TestCase):
    def test_parity_lemma_is_genuine_normal_closure_theorem(self):
        record = load("artifacts/results-paper-index-parity-lemma-v1.json")
        self.assertEqual(record["claim_tag"], "VERIFIED_THEOREM")
        self.assertIn("actual normal closure", record["scope_boundary"])

    def test_historical_freeze_is_superseded_by_major_revision_hold(self):
        hold = load("artifacts/results-paper-major-revision-hold-v1.json")
        self.assertEqual(hold["status"], "MAJOR_REVISION_NOT_SUBMISSION_READY")
        self.assertFalse(hold["publication_actions_allowed"])
        self.assertEqual(
            hold["supersedes_submission_readiness_of"],
            "artifacts/results-paper-freeze-v5.json",
        )

    def test_full_referee_audit_replays(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_results_paper_full.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("RESULTS_PAPER_FULL_AUDIT=PASS", completed.stdout)

    def test_full_freeze_hashes(self):
        freeze = load("artifacts/results-paper-full-freeze-v7.json")
        self.assertEqual(
            freeze["status"],
            "PUBLISHED_ZENODO_VERIFIED",
        )
        self.assertEqual(
            freeze["supersedes"], "artifacts/results-paper-full-freeze-v6.json"
        )
        manuscript = freeze["primary_manuscript"]
        self.assertEqual(sha(manuscript["tex"]), manuscript["tex_sha256"])
        self.assertEqual(sha(manuscript["pdf"]), manuscript["pdf_sha256"])
        supplement = freeze["supplement"]
        self.assertEqual(sha(supplement["tex"]), supplement["tex_sha256"])
        self.assertEqual(sha(supplement["pdf"]), supplement["pdf_sha256"])
        audit = freeze["referee_audit"]
        self.assertEqual(sha(audit["script"]), audit["script_sha256"])
        self.assertEqual(sha(audit["artifact"]), audit["artifact_sha256"])
        source_map = freeze["shintani_source_map"]
        self.assertEqual(
            sha(source_map["artifact"]), source_map["artifact_sha256"]
        )
        companion = freeze["companion_archive"]
        self.assertEqual(sha(companion["builder"]), companion["builder_sha256"])
        self.assertEqual(sha(companion["verifier"]), companion["verifier_sha256"])
        self.assertEqual(
            sha(companion["local_freeze"]), companion["local_freeze_sha256"]
        )
        publication = freeze["publication"]
        self.assertEqual(publication["doi"], "10.5281/zenodo.21703306")
        self.assertTrue(publication["top_level_pdf_and_tex"])
        self.assertEqual(
            sha(publication["metadata"]), publication["metadata_sha256"]
        )
        self.assertEqual(sha(publication["record"]), publication["record_sha256"])

    def test_cm_theorem_and_nonclaim_boundaries(self):
        paper = (ROOT / "paper/effective-stark-results.tex").read_text()
        self.assertIn("Cyclic-quartic CM norm bridge", paper)
        self.assertIn(r"\varepsilon=u^{e/2}", paper)
        self.assertIn(r"j(E)=E,\qquad j|_k\ne1", paper)
        self.assertIn(r"Put \(E^+=E^{\langle j\rangle}\)", paper)
        self.assertIn(r"=-\frac4e(\ell_1+i\ell_\sigma)", paper)
        self.assertIn(r"N_{E/E^+}(\sigma^ru)^{-1}", paper)
        self.assertNotIn(r"\ell_1-i\ell_\sigma", paper)
        self.assertNotIn(r"\sigma^{-r}u", paper)
        self.assertIn("not used in the theorem", paper)
        self.assertIn("rests solely on Engine B", paper)
        self.assertNotIn("General-\\(e\\) CM normalization and orientation", paper)

    def test_referee_must_fixes_are_regression_guarded(self):
        paper = (ROOT / "paper/effective-stark-results.tex").read_text()
        prose = " ".join(paper.split())
        self.assertNotIn(r"\tag{", paper)
        self.assertNotIn(r"\begin{center}\scriptsize", paper)
        self.assertGreaterEqual(
            paper.count(r"\begin{center}\footnotesize"), 2
        )
        self.assertIn("examples comprise five order-six packets", paper)
        self.assertIn(r"\(e=|\mu(E)|=2,6,8\)", paper)
        self.assertNotIn(r"\(e=|\mu(E)|=2,4,6,8\)", paper)
        self.assertIn(r"\phantomsection\label{par:conventions}", paper)
        self.assertIn(r"\theta(\bar s)=i", paper)
        self.assertIn(r"\psi(\sigma)=i", paper)
        self.assertIn(r"\label{eq:index-parity}", paper)
        self.assertIn(r"\label{sec:rq458}", paper)
        self.assertIn("complete the proof of Theorem", prose)

    def test_audit_tables_and_queue_counts_moved_to_supplement(self):
        paper = (ROOT / "paper/effective-stark-results.tex").read_text()
        prose = " ".join(paper.split())
        supplement = (
            ROOT / "paper/effective-stark-results-supplement.tex"
        ).read_text()
        self.assertIn(r"\section{Exact finite moduli}\label{app:moduli}", paper)
        self.assertIn("Supplementary Table~S1", prose)
        self.assertIn("Supplementary Table~S2", prose)
        self.assertNotIn(r"\path{data/q7-p7-case-v1.json}", paper)
        self.assertNotIn("672 such characters among 2,232", paper)
        self.assertIn("Supplementary Table S1: certificate record map", supplement)
        self.assertIn(
            "Supplementary Table S2: complete Artin-label interval replay",
            supplement,
        )
        self.assertIn("672 zero Euler products", supplement)
        self.assertIn("In 346 rows every supported derivative vanishes", supplement)

    def test_engine_a_euler_degeneracy_audit(self):
        record = load("artifacts/engine-a-euler-degeneracy-v1.json")
        self.assertEqual(
            record["claim_tag"], "VERIFIED_EXACT_EULER_DEGENERACY_AUDIT"
        )
        self.assertEqual(record["case_count"], 1560)
        self.assertEqual(record["supported_quadratic_character_count"], 2232)
        self.assertEqual(record["characters_with_zero_euler_product"], 672)
        self.assertEqual(record["cases_with_zero_euler_product"], 603)
        self.assertEqual(
            record["cases_with_all_supported_euler_products_zero"], 346
        )

    def test_engine_c_fourier_convention_correction(self):
        theory = load("data/engine-c-general-e-theory-v4.json")
        correction = load(
            "artifacts/engine-c-fourier-convention-correction-v1.json"
        )
        self.assertEqual(
            theory["claim_tag"], "VERIFIED_THEOREM_CONVENTION_CORRECTION"
        )
        self.assertEqual(
            theory["formulas"]["direct_lprime_forward"],
            "L'_S(0,psi)=-(4/e)*(ell_1+i*ell_sigma)",
        )
        self.assertEqual(
            theory["formulas"]["primitive_packet"],
            "Y_(sbar^r)=N_(E/E+)(sigma^r*u)^-1",
        )
        self.assertEqual(correction["verdict"], "PASS")
        self.assertEqual(
            correction["packet_log_coefficients_m0_m1"],
            [[-2, 0], [0, -2], [2, 0], [0, 2]],
        )

    def test_height_lemma_uses_only_powered_algebraic_elements(self):
        paper = (ROOT / "paper/effective-stark-results.tex").read_text()
        self.assertIn(r"\frac1m\log|\sigma_v(X_A^m)|", paper)
        self.assertNotIn(
            r"\left|\log|X_A|_v-\log|\alpha_A|_v\right|", paper
        )

    def test_shintani_source_map_and_priority_boundary(self):
        paper = (ROOT / "paper/effective-stark-results.tex").read_text()
        prose = " ".join(paper.split())
        self.assertIn("Shintani's Proposition~4 on pp.~154--156", prose)
        self.assertIn(
            "Shintani's Proposition~5(i)--(iii) on pp.~156--158", prose
        )
        self.assertIn(
            "We are not aware of previous unconditional one-place Stark packet",
            prose,
        )
        self.assertIn("support order ten", prose)
        self.assertNotIn("support orders six or ten", prose)
        self.assertIn(r"\cite{Zhao45}", paper)
        self.assertIn(r"\cite{Zhao78}", paper)
        self.assertIn(
            "That order-eight packet is not repeated in the selected tables",
            prose,
        )
        self.assertNotIn("so these are apparently the first examples", prose)

    def test_superseded_cm_gap_draft_is_removed(self):
        self.assertFalse(
            (ROOT / "paper/effective-stark-cm-major-revision.tex").exists()
        )
        self.assertFalse(
            (ROOT / "paper/effective-stark-cm-major-revision.pdf").exists()
        )

    def test_e6_primitive_correction_divides_coordinates_exactly(self):
        correction = load(
            "artifacts/engine-c-e6-primitive-packet-correction-v1.json"
        )
        self.assertEqual(
            correction["claim_tag"],
            "VERIFIED_EXACT_PRIMITIVE_PACKET_CORRECTION",
        )
        self.assertEqual(len(correction["records"]), 6)
        for row in correction["records"]:
            self.assertEqual(
                row["powered_stark_coordinates"],
                [3 * value for value in row["primitive_coordinates"]],
            )

    def test_superseded_engine_c_scopes_are_explicit(self):
        correction = load("artifacts/engine-c-claim-scope-correction-v1.json")
        tags = correction["current_theorem_tags"]
        self.assertEqual(tags["e6_primitive_packets"], "VERIFIED_AFTER_CORRECTION")
        self.assertEqual(tags["q6_e12_route"], "CROSS_CHECK_NOT_IN_PROOF")
        self.assertEqual(tags["rq000458_engine_c"], "DIAGNOSTIC_NOT_IN_PROOF")


if __name__ == "__main__":
    unittest.main()
