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
        freeze = load("artifacts/results-paper-full-freeze-v2.json")
        self.assertEqual(
            freeze["status"],
            "MATHEMATICAL_REPAIRS_PASS_LOCAL_ARCHIVE_FROZEN_PENDING_PUBLIC_DEPOSIT_AND_HUMAN_REFEREE",
        )
        self.assertEqual(
            freeze["supersedes"], "artifacts/results-paper-full-freeze-v1.json"
        )
        manuscript = freeze["primary_manuscript"]
        self.assertEqual(sha(manuscript["tex"]), manuscript["tex_sha256"])
        self.assertEqual(sha(manuscript["pdf"]), manuscript["pdf_sha256"])
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
        self.assertIsNone(companion["public_identifier"])
        self.assertFalse(freeze["publication_gate"]["publish_action_allowed"])

    def test_cm_theorem_and_nonclaim_boundaries(self):
        paper = (ROOT / "paper/effective-stark-results.tex").read_text()
        self.assertIn("Cyclic-quartic CM norm bridge", paper)
        self.assertIn(r"\varepsilon=u^{e/2}", paper)
        self.assertIn(r"j(E)=E,\qquad j|_k\ne1", paper)
        self.assertIn(r"Put \(E^+=E^{\langle j\rangle}\)", paper)
        self.assertIn("not used in the theorem", paper)
        self.assertIn("rests solely on Engine B", paper)
        self.assertNotIn("General-\\(e\\) CM normalization and orientation", paper)

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
        self.assertIn("We are unaware of earlier unconditional oriented", prose)
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
