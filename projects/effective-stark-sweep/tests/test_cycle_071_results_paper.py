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


class ResultsPaperFreezeTests(unittest.TestCase):
    def test_parity_lemma_is_genuine_normal_closure_theorem(self):
        record = load("artifacts/results-paper-index-parity-lemma-v1.json")
        self.assertEqual(record["claim_tag"], "VERIFIED_THEOREM")
        self.assertIn("actual normal closure", record["scope_boundary"])

    def test_general_e_v3_has_signed_specializations(self):
        theory = load("data/engine-c-general-e-theory-v3.json")
        self.assertEqual(theory["specializations"]["6"]["class_log_forward"], "-1/3")
        self.assertEqual(theory["specializations"]["8"]["direct_lprime_forward"], "-1/2")
        self.assertEqual(theory["specializations"]["12"]["direct_lprime_forward"], "-1/3")

    def test_freeze_hashes(self):
        freeze = load("artifacts/results-paper-freeze-v2.json")
        manuscript = freeze["primary_manuscript"]
        self.assertEqual(sha(manuscript["tex"]), manuscript["tex_sha256"])
        self.assertEqual(sha(manuscript["pdf"]), manuscript["pdf_sha256"])
        audit = freeze["referee_audit"]
        self.assertEqual(sha(audit["artifact"]), audit["sha256"])

    def test_referee_audit_replays(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_results_paper.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("RESULTS_PAPER_AUDIT=PASS", completed.stdout)


if __name__ == "__main__":
    unittest.main()
