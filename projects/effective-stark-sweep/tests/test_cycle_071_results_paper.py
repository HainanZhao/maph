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
        freeze = load("artifacts/results-paper-full-freeze-v1.json")
        self.assertEqual(
            freeze["status"],
            "COMPLETE_MAJOR_REVISION_REFEREE_READY_NOT_SUBMISSION_READY",
        )
        self.assertEqual(
            freeze["supersedes"], "artifacts/results-paper-ab-freeze-v1.json"
        )
        manuscript = freeze["primary_manuscript"]
        self.assertEqual(sha(manuscript["tex"]), manuscript["tex_sha256"])
        self.assertEqual(sha(manuscript["pdf"]), manuscript["pdf_sha256"])
        audit = freeze["referee_audit"]
        self.assertEqual(sha(audit["script"]), audit["script_sha256"])
        self.assertEqual(sha(audit["artifact"]), audit["artifact_sha256"])
        correction = freeze["engine_c_correction"]
        self.assertEqual(sha(correction["script"]), correction["script_sha256"])
        self.assertEqual(
            sha(correction["artifact"]), correction["artifact_sha256"]
        )
        scope = freeze["engine_c_scope_correction"]
        self.assertEqual(sha(scope["artifact"]), scope["artifact_sha256"])
        watch = freeze["literature_watch"]
        self.assertEqual(sha(watch["artifact"]), watch["artifact_sha256"])
        self.assertFalse(freeze["publication_gate"]["publish_action_allowed"])

    def test_cm_theorem_and_nonclaim_boundaries(self):
        paper = (ROOT / "paper/effective-stark-results.tex").read_text()
        self.assertIn("Cyclic-quartic CM norm bridge", paper)
        self.assertIn(r"\varepsilon=u^{e/2}", paper)
        self.assertIn("not used in the theorem", paper)
        self.assertIn("rests solely on Engine B", paper)
        self.assertNotIn("General-\\(e\\) CM normalization and orientation", paper)

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
