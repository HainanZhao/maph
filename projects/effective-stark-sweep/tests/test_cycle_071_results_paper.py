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

    def test_ab_referee_audit_replays(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_results_paper_ab.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("RESULTS_PAPER_AB_AUDIT=PASS", completed.stdout)

    def test_ab_freeze_hashes(self):
        freeze = load("artifacts/results-paper-ab-freeze-v1.json")
        self.assertEqual(freeze["status"], "REFEREE_ROUND_READY_NOT_SUBMISSION_READY")
        manuscript = freeze["primary_manuscript"]
        self.assertEqual(sha(manuscript["tex"]), manuscript["tex_sha256"])
        self.assertEqual(sha(manuscript["pdf"]), manuscript["pdf_sha256"])
        cm_draft = freeze["cm_quarantine_draft"]
        self.assertEqual(sha(cm_draft["tex"]), cm_draft["tex_sha256"])
        self.assertEqual(sha(cm_draft["pdf"]), cm_draft["pdf_sha256"])
        audit = freeze["referee_audit"]
        self.assertEqual(sha(audit["script"]), audit["script_sha256"])
        self.assertEqual(sha(audit["artifact"]), audit["artifact_sha256"])
        watch = freeze["literature_watch"]
        self.assertEqual(sha(watch["artifact"]), watch["artifact_sha256"])
        self.assertFalse(freeze["publication_gate"]["publish_action_allowed"])

    def test_cm_claims_are_quarantined(self):
        ab_paper = (ROOT / "paper/effective-stark-results.tex").read_text()
        main_body = ab_paper.split(r"\appendix", 1)[0]
        for forbidden in ("Engine C", "RQ-000458", r"\Q(\sqrt6)", "DUAL_ROUTED"):
            self.assertNotIn(forbidden, main_body)

        cm_paper = (ROOT / "paper/effective-stark-cm-major-revision.tex").read_text()
        self.assertIn("not a submission manuscript", cm_paper)
        self.assertIn("Required bridge; not yet proved", cm_paper)
        self.assertIn("finite valuations", cm_paper)


if __name__ == "__main__":
    unittest.main()
